# Exercise 6: Structured Reasoning Prompting

## Objective
Guide the model through a complex problem using clearly defined analysis stages, producing an auditable decision process rather than hidden reasoning.

## Scenario
The Order Service receives duplicate order requests when the client retries after a timeout.

## Model's Staged Response

### 1. Restate the Problem
When a client calls `POST /orders` and the response is delayed or lost (network blip, gateway timeout), the client's retry logic resends the same order request. The Order Service has no way of knowing the second request is a retry of the first rather than a genuinely new order, so it may create two separate `Order` records for what the customer intended as a single purchase.

### 2. Likely Technical Causes
- No idempotency key sent by the client or honored by the server.
- HTTP timeout is shorter than the actual processing time, so the client retries before the first request even finishes.
- Client-side retry logic (e.g., Feign/RestTemplate retry, browser resubmission) with no deduplication.
- Kafka consumer re-processing the same "OrderPlaced" event after a rebalance or a failed offset commit (at-least-once delivery).
- No unique constraint in the database to reject a logical duplicate at the persistence layer.

### 3. Risks
- **Data integrity:** Duplicate `Order` rows corrupt reporting and analytics.
- **Financial risk:** Downstream Payment Service may charge the customer twice.
- **Inventory risk:** Downstream Inventory Service may reserve/deduct stock twice for one real order.
- **Customer trust:** Duplicate confirmation notifications and duplicate charges damage trust and generate support load.
- **Cascading duplication:** Because the system is event-driven (Kafka), one duplicate order can fan out into duplicate events across every downstream consumer.

### 4. Comparison of Solutions

| Solution | How It Works | Pros | Cons |
|---|---|---|---|
| **Idempotency Key** | Client generates a unique key (e.g., UUID) per logical order attempt and sends it in a header; server stores it and returns the original result for repeated keys instead of creating a new order. | Client-driven, works across retries and network failures; industry-standard (Stripe-style); prevents duplication at the API entry point before any downstream effects occur. | Requires client cooperation (must reuse the same key on retry); server must persist keys with a TTL and handle key-store cleanup. |
| **Database Unique Constraint** | Add a unique constraint on a natural business key (e.g., `customerId + cartId` or `customerId + idempotencyKey`) so a second insert fails at the DB level. | Strong guarantee, works even if application logic has bugs; cheap to implement. | Only protects the database — a duplicate request can still trigger duplicate downstream calls before the DB rejects it, unless checked first; requires a meaningful natural key, which isn't always available for orders. |
| **Distributed Transaction (2PC/XA)** | Coordinate a single global transaction across Order, Inventory, and Payment services so the whole operation commits or rolls back atomically. | Strong consistency guarantee across services. | Heavyweight, blocks resources across services, poor fit for microservices/Kafka, doesn't actually solve the "client retried the same HTTP call" problem — it solves a different problem (cross-service atomicity). Not recommended here. |
| **Kafka Consumer Deduplication** | Consumers track processed event IDs (or use Kafka's exactly-once semantics/transactional producer) to ignore already-seen "OrderPlaced" events. | Solves duplication *within* the event pipeline (broker redelivery), complements the other solutions. | Doesn't solve the original client-retry problem at the REST entry point — only handles Kafka-level redelivery, so it's necessary but not sufficient alone. |

### 5. Recommended Solution
**Idempotency Key at the API layer, backed by a database unique constraint**, combined with Kafka consumer-side deduplication for event redelivery.

**Justification:** The idempotency key solves the root cause (the client not being able to tell the server "this is a retry of the same attempt"), stopping duplication before any downstream service is invoked — which is the cheapest point to fix it. The unique DB constraint is a low-cost safety net in case the idempotency check is bypassed (e.g., app restart mid-request). Kafka-side deduplication is added because Kafka's at-least-once delivery is an independent source of duplicates further down the pipeline, unrelated to the client retry — both problems exist in this architecture, so both are worth addressing, but the API-layer idempotency key is what solves *this specific* reported issue.

### 6. Implementation Steps
1. Client generates a UUID (`Idempotency-Key`) once per checkout attempt and sends it on every retry of the same request.
2. Order Service adds an `idempotency_key` column (unique index) on the `orders` table.
3. On `POST /orders`, the service first checks if a record with that key already exists.
4. If it exists, return the previously stored response (same status/body) instead of creating a new order.
5. If it doesn't exist, insert the new order with the key inside the same transaction (relying on the unique constraint to catch races).
6. Handle the `DataIntegrityViolationException` from a duplicate-key race by re-fetching and returning the existing order (treat it as a successful idempotent replay, not an error).
7. Add a Kafka consumer-side "processed event id" check (or use `enable.idempotence=true` with a transactional producer) so replayed "OrderPlaced" events don't cause Inventory/Payment to act twice.

### 7. Spring Boot Code Example
```java
@Entity
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String idempotencyKey;

    private Long customerId;
    private Long productId;
    private BigDecimal amount;
    private String status;
    // getters/setters
}

@Service
public class OrderService {

    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    @Transactional
    public Order placeOrder(OrderRequest request, String idempotencyKey) {
        return repository.findByIdempotencyKey(idempotencyKey)
                .orElseGet(() -> createNewOrder(request, idempotencyKey));
    }

    private Order createNewOrder(OrderRequest request, String idempotencyKey) {
        Order order = new Order();
        order.setIdempotencyKey(idempotencyKey);
        order.setCustomerId(request.customerId());
        order.setProductId(request.productId());
        order.setAmount(request.amount());
        order.setStatus("PLACED");
        try {
            return repository.save(order);
        } catch (DataIntegrityViolationException ex) {
            // Concurrent retry raced past the findBy check; treat as idempotent replay.
            return repository.findByIdempotencyKey(idempotencyKey)
                    .orElseThrow(() -> ex);
        }
    }
}

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<Order> placeOrder(
            @RequestHeader("Idempotency-Key") String idempotencyKey,
            @Valid @RequestBody OrderRequest request) {
        Order order = service.placeOrder(request, idempotencyKey);
        return ResponseEntity.status(HttpStatus.CREATED).body(order);
    }
}
```

### 8. Test Cases

| Test Case ID | Scenario | Input | Expected Result |
|---|---|---|---|
| TC-01 | New order with a fresh idempotency key | Unique `Idempotency-Key`, valid request body | New order created, HTTP 201 |
| TC-02 | Retry with the same idempotency key (sequential) | Same `Idempotency-Key` sent twice, one after the other | Second call returns the original order, no new row created, HTTP 201 |
| TC-03 | Concurrent retry with the same idempotency key (race) | Same `Idempotency-Key` sent in two parallel requests | Exactly one order persisted; the losing request catches `DataIntegrityViolationException` and returns the winner's order |
| TC-04 | Missing idempotency key header | Request without `Idempotency-Key` | HTTP 400 Bad Request |
| TC-05 | Same key, different request body | Same `Idempotency-Key`, but different `productId`/`amount` | Original order returned (key wins); optionally log a mismatch warning |
| TC-06 | Kafka "OrderPlaced" event redelivered | Same event ID consumed twice by Inventory Service | Stock reduced only once; second consumption is a no-op |

## Expected Outcome
This staged structure turns an ambiguous bug report into a transparent, auditable decision trail: problem → causes → risks → compared options → justified recommendation → concrete implementation → verifiable tests — with the reasoning visible and checkable at each stage, rather than hidden inside a single unexplained answer.
