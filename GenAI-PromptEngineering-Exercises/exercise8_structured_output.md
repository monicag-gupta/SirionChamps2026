# Exercise 8: Structured Output Prompting

## Objective
Generate predictable output that can be parsed and reused by another system (no prose, exact format only).

---

## 1. JSON Output — Payment Service

**Prompt constraint:** Return only valid JSON, no markdown or explanatory text outside the JSON.

**Output:**
```json
{
  "serviceName": "PaymentService",
  "responsibilities": [
    "Process credit-card payments for orders",
    "Notify Order Service of payment success or failure"
  ],
  "endpoints": [
    {
      "method": "POST",
      "path": "/api/payments",
      "description": "Processes a credit-card payment for a given order",
      "successStatus": 201,
      "errorStatuses": [400, 402, 422, 500]
    },
    {
      "method": "GET",
      "path": "/api/payments/{paymentId}",
      "description": "Retrieves the status/details of a payment",
      "successStatus": 200,
      "errorStatuses": [404, 500]
    }
  ],
  "eventsPublished": [
    "PaymentSucceeded",
    "PaymentFailed"
  ],
  "eventsConsumed": [
    "OrderPlaced"
  ],
  "databaseTables": [
    "payments",
    "payment_transactions"
  ],
  "securityControls": [
    "PCI-DSS compliant card data handling (no raw PAN storage)",
    "OAuth2 client-credentials for service-to-service calls",
    "TLS in transit",
    "Idempotency key on payment creation"
  ],
  "validationRules": [
    "orderId must not be null",
    "amount must be greater than zero",
    "cardToken must be present and valid",
    "amount must not exceed customer's approved transaction limit"
  ]
}
```

---

## 2. Table Output — Order Service Test Cases

**Prompt constraint:** Columns = Test Case ID | Scenario | Input | Expected HTTP Status | Expected Result. Include positive, negative, validation and exception scenarios.

| Test Case ID | Scenario | Input | Expected HTTP Status | Expected Result |
|---|---|---|---|---|
| TC-01 | Positive: place a valid order | Valid customerId, productId, quantity | 201 | Order created and returned with status PLACED |
| TC-02 | Positive: retrieve an existing order | Valid orderId | 200 | Order details returned |
| TC-03 | Negative: retrieve a non-existent order | Invalid/unknown orderId | 404 | Error response indicating order not found |
| TC-04 | Validation: missing customerId | Request body without customerId | 400 | Validation error listing the missing field |
| TC-05 | Validation: quantity is zero or negative | quantity = 0 | 400 | Validation error: quantity must be greater than 0 |
| TC-06 | Negative: place order for out-of-stock product | Valid customerId, productId with 0 stock | 409 | Order rejected; error indicates insufficient stock |
| TC-07 | Exception: downstream Inventory Service unavailable | Valid order request, Inventory Service down | 503 | Order marked PENDING or rejected gracefully; no unhandled exception/stack trace exposed |
| TC-08 | Exception: database constraint violation (duplicate idempotency key race) | Duplicate concurrent request with same idempotency key | 201 (idempotent replay) | Original order returned; no duplicate row created |
| TC-09 | Negative: unauthorized access | Request without valid auth token | 401 | Access denied |
| TC-10 | Positive: cancel an order in a cancellable state | Valid orderId, status = PLACED | 204 | Order status updated to CANCELLED |

---

## 3. Java Output — OrderResponse Record

**Prompt constraint:** Return only a compilable Java record, no explanations or markdown.

```java
public record OrderResponse(
        Long orderId,
        Long customerId,
        BigDecimal totalAmount,
        String status,
        LocalDateTime createdAt
) {}
```

*(Note: `BigDecimal` and `LocalDateTime` require `import java.math.BigDecimal;` and `import java.time.LocalDateTime;` in the actual file.)*

## Key Takeaway
Structured output prompting works by pairing a **rigid target schema** (JSON shape, table columns, or a language grammar like a Java record) with an explicit **"nothing else" constraint**. This is what makes the output machine-parseable — safe to feed directly into another service, a test runner, or a code file, without a human stripping out conversational filler first.
