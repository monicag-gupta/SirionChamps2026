# Exercise 7: Role-based Prompting

## Objective
Observe how changing the assigned role changes the response to a related question, even when the underlying subsystems (Order Service, Inventory Service) stay the same.

---

## Prompt A: Developer Role
**Prompt:** "Act as a senior Java developer. Explain how to implement communication between Order Service and Inventory Service using Spring Cloud OpenFeign. Include dependencies, configuration, interface and error handling."

**Response:**

*Dependencies (pom.xml):*
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

*Enable Feign clients:*
```java
@SpringBootApplication
@EnableFeignClients
public class OrderServiceApplication { }
```

*Feign interface:*
```java
@FeignClient(name = "inventory-service", url = "${inventory.service.url}")
public interface InventoryClient {

    @PostMapping("/inventory/reserve")
    ReservationResponse reserveStock(@RequestBody ReservationRequest request);
}
```

*Usage in Order Service:*
```java
@Service
public class OrderService {
    private final InventoryClient inventoryClient;

    public OrderService(InventoryClient inventoryClient) {
        this.inventoryClient = inventoryClient;
    }

    public void placeOrder(OrderRequest request) {
        ReservationResponse response = inventoryClient.reserveStock(
                new ReservationRequest(request.productId(), request.quantity()));
        if (!response.reserved()) {
            throw new InsufficientStockException(request.productId());
        }
        // proceed to save order
    }
}
```

*Error handling — custom Feign error decoder:*
```java
public class InventoryErrorDecoder implements ErrorDecoder {
    @Override
    public Exception decode(String methodKey, Response response) {
        return switch (response.status()) {
            case 404 -> new ProductNotFoundException();
            case 409 -> new InsufficientStockException();
            default -> new InventoryServiceUnavailableException();
        };
    }
}
```

*Config:* register `InventoryErrorDecoder` as a `@Bean`, add `feign.client.config.inventory-service.connectTimeout`/`readTimeout`, and pair with a circuit breaker (Resilience4j) for resilience against Inventory Service downtime.

---

## Prompt B: Architect Role
**Prompt:** "Act as a microservices solution architect. Evaluate whether Order Service and Inventory Service should communicate using OpenFeign or Kafka. Compare coupling, availability, consistency, performance, failure handling, operational complexity. Recommend an approach."

**Response:**

| Dimension | OpenFeign (Synchronous REST) | Kafka (Asynchronous Events) |
|---|---|---|
| **Coupling** | Tight — Order Service must know Inventory Service's address/contract and both must be up simultaneously. | Loose — Order Service publishes an event and doesn't need to know who consumes it or whether they're currently available. |
| **Availability** | Order placement fails/blocks if Inventory Service is down (unless a circuit breaker + fallback is added). | Order placement succeeds independent of Inventory Service's availability; the event is processed when Inventory comes back. |
| **Consistency** | Strong/immediate — the caller knows the reservation result before responding to the customer. | Eventual — order confirmation may need a follow-up state transition (e.g., "PENDING" → "CONFIRMED") once inventory is reserved. |
| **Performance** | Adds synchronous latency to the order-placement request path (Order waits on Inventory's response). | Order-placement request returns fast; inventory reservation happens asynchronously off the critical path. |
| **Failure Handling** | Requires explicit timeout/retry/circuit-breaker logic per call site. | Requires idempotent consumers and dead-letter-topic handling, but failures don't cascade synchronously. |
| **Operational Complexity** | Simpler to trace (a single request/response chain) but creates a distributed-call chain that's brittle under load. | Higher operational overhead (broker, topic/partition management, consumer lag monitoring) but scales and isolates failures better. |

**Recommendation:** For this e-commerce Order Management System, use **Kafka** for the Order → Inventory reservation flow, since order volume needs to survive Inventory Service slowness/outages without blocking checkout, and eventual consistency (order goes to "PENDING_INVENTORY" then "CONFIRMED"/"REJECTED") is acceptable for this business process. Reserve OpenFeign/REST for **synchronous, read-only lookups** where the caller needs an immediate answer (e.g., checking current stock availability to display on a product page), since that's a query, not a state-changing workflow step.

---

## Prompt C: Security Reviewer Role
**Prompt:** "Act as an application security reviewer. Review communication between Order Service and Inventory Service. Identify risks related to authentication, authorization, token propagation, data exposure, replay attacks, service-to-service trust. Provide recommended Spring Security controls."

**Response:**

| Risk Area | Concern | Recommended Control |
|---|---|---|
| **Authentication** | Inventory Service accepts calls from any caller on the network with no identity check. | Use mutual TLS (mTLS) between services, or OAuth2 client-credentials tokens issued per service. |
| **Authorization** | Even if authenticated, Inventory Service might not verify the caller is *allowed* to reserve/deduct stock. | Enforce scope/role checks (`SCOPE_inventory.write`) via Spring Security `@PreAuthorize`, not just "is authenticated." |
| **Token Propagation** | If a user's JWT is blindly forwarded from Order Service to Inventory Service, Inventory Service now trusts a token meant for a different audience. | Use a dedicated service-to-service token (client-credentials grant with `aud=inventory-service`), or re-issue a downstream token rather than forwarding the original user token unchanged. |
| **Data Exposure** | The reservation payload might carry more customer/order data than Inventory Service needs (e.g., customer PII). | Apply data minimization — only send productId/quantity/orderId, not full customer details. |
| **Replay Attacks** | A captured reservation request could be resent to reserve/deduct stock again. | Combine with the idempotency-key mechanism from Exercise 6, plus short-lived tokens and request timestamps/nonces validated server-side. |
| **Service-to-Service Trust** | Flat trust ("any internal IP is trusted") is risky in a compromised-pod/lateral-movement scenario. | Adopt zero-trust: every service call authenticated and authorized regardless of network location (service mesh with mTLS, e.g., Istio, or Spring Security Resource Server validating JWTs on every hop). |

**Recommended Spring Security controls:** `spring-boot-starter-oauth2-resource-server` on Inventory Service to validate incoming JWTs; `spring-security-oauth2-client` (client-credentials) on Order Service to obtain a service token; method-level `@PreAuthorize("hasAuthority('SCOPE_inventory.write')")` on the reservation endpoint; and short token TTLs to limit replay windows.

---

## Learner Activity — Comparison of How the Role Changed the Response

| Aspect | Developer Role | Architect Role | Security Reviewer Role |
|---|---|---|---|
| **Primary Concern** | "How do I make this code work?" | "Which communication style is right for the system, long-term?" | "What can go wrong, and how do we prevent it?" |
| **Level of Abstraction** | Code-level (annotations, classes, config files) | System-level (trade-off tables across quality attributes) | Threat-level (attack vectors and mitigations) |
| **Output Shape** | Runnable Java code + config snippets | Comparative table + a single recommendation with justification | Risk table mapped to concrete Security controls |
| **Assumed Decision Already Made** | Yes — assumes OpenFeign was already chosen and just wants implementation. | No — the role's job is precisely to make that choice. | No — assumes some protocol exists and audits it regardless of which one. |
| **Key Insight** | Same two services, same integration point, but each role surfaces a *completely different* set of concerns — implementation detail, architectural trade-off, or security risk — showing that the role assigned in a prompt acts as a lens that determines which aspects of a problem the model prioritizes. |
