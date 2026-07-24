# Exercise 4: One-shot Prompting

## Objective
Provide one example to guide the model's response structure and level of detail.

## Prompt (with one example)
```
Convert a Java requirement into a user story with acceptance criteria.

Example:
Requirement: Customers should be able to retrieve an order using the order ID.
Output:
User Story: As a customer, I want to retrieve an order using its ID so that I can view its current status.
Acceptance Criteria:
- The endpoint must accept an order ID.
- The service must return HTTP 200 when the order exists.
- The service must return HTTP 404 when the order does not exist.
- The response must contain order ID, customer ID, amount and status.

Now convert the following requirement:
The Inventory Service should reduce the available stock after an order is successfully placed.
```

## Model's Output — Inventory Requirement

**User Story:**
As the system, I want to reduce the available stock of a product after an order is successfully placed, so that inventory levels stay accurate and prevent overselling.

**Acceptance Criteria:**
- The Inventory Service must consume the "OrderPlaced" event (or receive a stock-reduction request) containing productId and quantity.
- The available stock for the given productId must be decremented by the ordered quantity.
- If available stock is insufficient, the operation must fail and no partial deduction should occur.
- The service must return/publish HTTP 200 (or an "InventoryReserved" event) when the reduction succeeds.
- The service must return HTTP 409 Conflict (or publish an "InventoryReservationFailed" event) when stock is insufficient.
- The stock update must be atomic to prevent race conditions under concurrent orders for the same product.

---

## Learner Activity — Payment Requirement

**Requirement:**
The Payment Service should reject a transaction when the payment amount is greater than the customer's approved transaction limit.

**User Story:**
As the Payment Service, I want to reject a transaction whose amount exceeds the customer's approved transaction limit, so that customers cannot be charged beyond what they are authorized for and the business is protected from fraudulent or erroneous high-value charges.

**Acceptance Criteria:**
- The endpoint must accept customerId, orderId and paymentAmount.
- The service must retrieve the customer's approved transaction limit before processing payment.
- If paymentAmount > approved transaction limit, the transaction must be rejected.
- The service must return HTTP 422 Unprocessable Entity (or HTTP 400) with a clear reason code (e.g., "LIMIT_EXCEEDED") when rejected.
- The service must return HTTP 200/201 when paymentAmount is within the approved limit and the transaction succeeds.
- A rejected transaction must not be persisted as a successful payment and must not trigger downstream "PaymentSucceeded" events.
- The rejection must be logged/published (e.g., "PaymentRejected" event) so the Order Service can update the order status accordingly.

## Key Takeaway
The single example fixed the exact response shape (User Story sentence pattern + bulleted Acceptance Criteria covering happy path, failure path, and data/status expectations). Both new requirements — Inventory and Payment — followed that same shape automatically, without needing to be told the format again. This is the core benefit of one-shot prompting: **one demonstration anchors structure and tone for all subsequent conversions.**
