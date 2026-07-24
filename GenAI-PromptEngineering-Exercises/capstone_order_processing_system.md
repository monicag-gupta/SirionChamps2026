# Capstone Exercise: AI-Assisted Microservice Design — Order Processing System

## Business Requirement
Customer places an order → Inventory is reserved → Payment is processed → Order status is updated → Confirmation notification is sent → Failed operations trigger compensation actions.

---

## 1. Microservice Boundaries

| Service | Responsibility | Owns Data |
|---|---|---|
| **API Gateway** | Single entry point; routing, auth token validation, rate limiting. | None (stateless) |
| **Order Service** | Owns the order lifecycle and orchestrating/choreographing the saga's outcome. | `orders`, `order_items` |
| **Product Service** | Product catalog, pricing. | `products` |
| **Inventory Service** | Stock levels, reservation, release. | `inventory` |
| **Payment Service** | Payment processing, transaction-limit enforcement. | `payments` |
| **Notification Service** | Sends confirmation/failure notifications to customers. | `notifications` (log/audit only) |

Each service owns its own MySQL schema — no cross-service joins; all cross-service data needs go through REST calls (queries) or Kafka events (state changes).

---

## 2. REST API Contracts (Key Endpoints)

| Service | Method & Path | Purpose |
|---|---|---|
| Order Service | `POST /api/orders` | Place a new order (requires `Idempotency-Key` header). |
| Order Service | `GET /api/orders/{orderId}` | Retrieve order status/details. |
| Product Service | `GET /api/products/{productId}` | Retrieve product details/price. |
| Inventory Service | `GET /api/inventory/{productId}` | Check current stock. |
| Payment Service | `GET /api/payments/order/{orderId}` | Retrieve payment status for an order. |
| Notification Service | `GET /api/notifications/order/{orderId}` | Retrieve notification history for an order. |

Inventory reservation and payment processing are **not** exposed as synchronous calls from Order Service in the happy path — they are driven by Kafka events (see Saga Workflow), keeping the checkout request fast and decoupled.

---

## 3. Kafka Event Definitions

| Topic | Producer | Consumer(s) | Payload (key fields) |
|---|---|---|---|
| `order.placed` | Order Service | Inventory Service | orderId, customerId, items[{productId, quantity}] |
| `inventory.reserved` | Inventory Service | Payment Service | orderId, reservationId |
| `inventory.reservation-failed` | Inventory Service | Order Service | orderId, reason |
| `payment.succeeded` | Payment Service | Order Service, Notification Service | orderId, paymentId, amount |
| `payment.failed` | Payment Service | Order Service, Inventory Service (compensation), Notification Service | orderId, reason |
| `order.confirmed` | Order Service | Notification Service | orderId, customerId |
| `order.cancelled` | Order Service | Inventory Service (compensation), Notification Service | orderId, reason |

All consumers are idempotent (dedupe by event ID / order ID + event type), and each topic has a matching dead-letter topic (e.g., `payment.failed.DLT`) for poison-pill handling.

---

## 4. Database Design (per service, simplified)

```
orders(id, customer_id, idempotency_key UNIQUE, status, total_amount, created_at)
order_items(id, order_id FK, product_id, quantity, unit_price)

products(id, name, description, price, category, active)

inventory(id, product_id UNIQUE, available_stock, reserved_stock, updated_at)

payments(id, order_id UNIQUE, customer_id, amount, status, card_token, processed_at)

notifications(id, order_id, customer_id, channel, message, status, sent_at)
```

---

## 5. Spring Boot Project Structure (per service, using the Exercise 9 template pattern)
```
order-service/
├── controller/
├── service/
├── repository/
├── entity/
├── dto/
├── event/            (Kafka producers/consumers)
├── exception/
├── config/
└── OrderServiceApplication.java
```
(Same layered shape repeated for Product, Inventory, Payment, and Notification Service — consistent with the reusable template from Exercise 9.)

---

## 6. DTOs and Validation Rules (example: Order)
```java
public record OrderRequest(
    @NotNull Long customerId,
    @NotEmpty List<@Valid OrderItemRequest> items
) {}

public record OrderItemRequest(
    @NotNull Long productId,
    @Min(1) int quantity
) {}
```
Validation is enforced at the API boundary (Bean Validation) and again at the business-rule level (e.g., Payment Service re-checks transaction limit server-side regardless of what the client sent).

---

## 7. Exception-Handling Strategy
Each service uses a `@RestControllerAdvice` mapping domain exceptions to HTTP statuses (`ProductNotFoundException` → 404, `InsufficientStockException` → 409, `TransactionLimitExceededException` → 422), with a catch-all handler returning a sanitized `500` that never leaks stack traces. Kafka consumer exceptions go to a retry topic, then a dead-letter topic after N attempts, rather than blocking the partition.

---

## 8. Saga Workflow (Choreography-based)

```
Customer -> API Gateway -> Order Service: POST /orders
Order Service: save order (status=PENDING), publish order.placed
Inventory Service: consume order.placed
  -> sufficient stock? publish inventory.reserved
  -> insufficient stock? publish inventory.reservation-failed
Payment Service: consume inventory.reserved
  -> within limit? charge, publish payment.succeeded
  -> over limit / declined? publish payment.failed
Order Service: consume payment.succeeded -> status=CONFIRMED, publish order.confirmed
Order Service: consume payment.failed OR inventory.reservation-failed -> status=CANCELLED, publish order.cancelled
Inventory Service: consume order.cancelled -> release any reserved stock (compensation)
Notification Service: consume order.confirmed / order.cancelled -> notify customer
```

**Compensating actions:** if payment fails after inventory was reserved, Order Service publishes `order.cancelled`, which Inventory Service consumes to release the reservation — this is the compensating transaction for the saga.

**Choreography vs. Orchestration — structured reasoning (Exercise 6 style) summary:** Choreography was chosen over a central orchestrator because the workflow is a linear chain with few branches, it avoids a single orchestrator becoming a bottleneck/SPOF, and it fits naturally with the Kafka-based architecture already in place. Trade-off accepted: harder end-to-end visibility, mitigated with distributed tracing (see Resilience Strategy).

---

## 9. Resilience Strategy
- **Idempotency keys** on `POST /orders` (Exercise 6) to prevent duplicate orders from client retries.
- **Circuit breakers (Resilience4j)** on any synchronous calls (e.g., Order Service querying Product Service for price display) to fail fast when a dependency is down.
- **Kafka consumer retries + dead-letter topics** for transient failures (DB momentarily unavailable) vs. poison messages.
- **Timeouts** on all synchronous REST calls, tuned below the caller's own SLA.
- **Distributed tracing** (e.g., Micrometer Tracing + Zipkin) to reconstruct the saga's path across services for debugging.
- **Consumer group scaling** on Inventory/Payment topics to handle load spikes without falling behind.

---

## 10. Security Controls
- API Gateway validates the customer's JWT (OAuth2 Resource Server) before routing.
- Service-to-service calls use client-credentials tokens or mTLS (zero-trust — no implicit network trust), per Exercise 7's security-reviewer analysis.
- Card data is tokenized before reaching Payment Service; raw PANs are never stored or logged.
- Secrets (DB credentials, Kafka credentials) live in a vault, never in application config committed to source control, per Exercise 12/13's secret-isolation principle.
- Any AI-assisted customer-facing text (e.g., a notification-content classifier) treats customer input as untrusted data, per Exercise 12's injection-safe prompt pattern.
- Least-privilege DB users per service; Notification Service, for example, has no write access to `payments` or `inventory`.

---

## 11. Unit and Integration Tests
- **Unit tests:** JUnit 5 + Mockito per service, covering service-layer business rules (e.g., transaction-limit rejection, insufficient-stock rejection) with repositories/Kafka producers mocked.
- **Integration tests:** Testcontainers spinning up real MySQL + Kafka per service to verify repository queries, Kafka publish/consume round-trips, and the idempotency-key unique-constraint race (Exercise 6, TC-03).
- **Saga-level test:** an end-to-end test harness that places an order, forces a simulated payment failure, and asserts the compensating `order.cancelled` event correctly triggers inventory release.

---

## 12. Docker Compose Configuration
```yaml
version: "3.8"
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on: [zookeeper]
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports: ["9092:9092"]

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: order_management
    ports: ["3306:3306"]
    volumes: ["mysql_data:/var/lib/mysql"]

  api-gateway:
    build: ./api-gateway
    ports: ["8080:8080"]
    depends_on: [order-service, product-service, inventory-service, payment-service]

  order-service:
    build: ./order-service
    depends_on: [mysql, kafka]
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/order_management
      SPRING_KAFKA_BOOTSTRAP_SERVERS: kafka:9092

  product-service:
    build: ./product-service
    depends_on: [mysql]

  inventory-service:
    build: ./inventory-service
    depends_on: [mysql, kafka]

  payment-service:
    build: ./payment-service
    depends_on: [mysql, kafka]

  notification-service:
    build: ./notification-service
    depends_on: [kafka]

volumes:
  mysql_data:
```
*(Secrets like `MYSQL_ROOT_PASSWORD` are supplied via an `.env` file excluded from version control, not hardcoded — consistent with Exercise 12/13's secret-isolation guidance.)*

---

## 13. API Documentation
Each service exposes OpenAPI docs via `springdoc-openapi-starter-webmvc-ui`, viewable at `/swagger-ui.html`; the API Gateway aggregates them at a single `/docs` route for consumers.

---

## Mandatory Prompting Techniques — Where Each Was Demonstrated

| Technique | Where Applied in This Capstone |
|---|---|
| **Zero-shot prompting** | Generating the exception-handling strategy (Section 7) directly from instructions, no example given — same style as Exercise 3. |
| **One-shot prompting** | Converting the "compensating action" requirement into a user story ("As the system, I want to release reserved inventory when payment fails, so that stock isn't incorrectly held") using the Exercise 4 pattern. |
| **Few-shot prompting** | Documenting the REST endpoints in Section 2 following the consistent Method/Endpoint/Status/Purpose pattern from Exercise 5. |
| **Role-based prompting** | The choreography-vs-orchestration decision in Section 8 was reasoned through an architect lens (Exercise 7, Prompt B style), weighing coupling/availability/complexity. |
| **Structured reasoning** | Section 8's saga design decision follows the Exercise 6 stage structure: problem → causes/options → risks → comparison → recommendation. |
| **Structured JSON output** | A service manifest for Notification Service (responsibilities, endpoints, eventsConsumed, securityControls) can be generated in the exact JSON shape from Exercise 8 for automated service-catalog ingestion. |
| **Reusable prompt templates** | Section 5's project structure and Section 6's DTO conventions reuse the Exercise 9 template, applied consistently across all five services. |
| **Prompt evaluation** | The capstone's own generation prompts (e.g., "design the saga workflow") were checked against the Exercise 10 rubric — role, context, requirements, constraints, and output format were all made explicit before generating each section above. |
| **Iterative prompt optimization** | The saga design went through the Exercise 11 pattern: start broad ("design order processing") → add context (microservices, Kafka) → add functional scope (reserve/pay/notify) → add technical/architecture requirements → add output constraints (tables, code, compose file). |
| **Prompt-injection protection** | Section 10 notes that any AI-assisted handling of customer-supplied text (e.g., order notes, notification content) must use the Exercise 12 pattern — treat customer text as untrusted data, never as instructions. |

---

## Final Reflection

**Which parts were decided by the learner before using AI?**
The business requirement itself (order → inventory → payment → notification → compensation), the service boundaries dictated by the given case study (API Gateway, Order/Product/Inventory/Payment/Notification, MySQL, Kafka, Docker), and the decision to use choreography-style Kafka events rather than a synchronous call chain, were fixed constraints going in — not something the AI chose.

**Which parts were suggested by AI?**
The specific event names and topic list, the DTO/validation structure, the exact resilience techniques (circuit breaker placement, idempotency-key mechanism), the Docker Compose layout, and the mapping of each business scenario onto a specific prompting technique.

**Which AI suggestions were rejected or corrected?**
A first-pass instinct would be to have Order Service synchronously call Inventory and Payment via REST for simplicity — this was rejected in favor of the event-driven choreography to match the case study's stated Kafka-based communication and to avoid tight coupling/blocking checkout on downstream availability (reasoned through in Section 8).

**How was the generated code/design validated?**
Against the Exercise 10 rubric (role/context/requirements/constraints/output/security/testability) for prompt quality, and structurally against the case study's stated technology list (Java Spring Boot, MySQL, Kafka, Docker) to ensure nothing invented a mismatched stack.

**What security risks were identified?**
Card data exposure, credential/secret leakage, service-to-service trust gaps, replay of payment/order requests, and injection risk in any AI-assisted handling of free-text customer input — each mapped to a specific control in Section 10.

**Did AI act as a thought partner, or did it make the architectural decisions?**
Thought partner: the choreography-vs-orchestration trade-off, the compensating-transaction design, and the resilience strategy were reasoned through with pros/cons and recommendations, but the final architectural commitments align with constraints the human/case-study already set (Kafka-based, microservices, layered Spring Boot), and would require human sign-off before being treated as final.

**What would need human approval before production deployment?**
Real credential provisioning and secret storage, the actual transaction-limit business rule values, security review of the auth/mTLS configuration, load/capacity testing of Kafka consumer groups, and sign-off on the compensation logic's correctness under concurrent failure scenarios — none of these should go live purely on AI-generated output without human verification.
