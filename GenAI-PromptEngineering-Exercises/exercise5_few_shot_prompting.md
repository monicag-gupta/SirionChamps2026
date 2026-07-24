# Exercise 5: Few-shot Prompting

## Objective
Use multiple examples to establish a consistent response pattern for REST API documentation.

## Prompt (3 examples establishing the pattern)
```
Generate REST API endpoint documentation using the pattern shown below.

Example 1: Retrieve all products -> GET /api/products, 200 OK, 500 Internal Server Error
Example 2: Retrieve a product by ID -> GET /api/products/{productId}, 200 OK, 404 Not Found
Example 3: Delete an order by ID -> DELETE /api/orders/{orderId}, 204 No Content, 404 Not Found

Now document: 1) Create a payment 2) Update an order status 3) Search orders by customer ID 4) Cancel an order
```

## Model's Output

### 1. Create a payment
```
Method: POST
Endpoint: /api/payments
Success Status: 201 Created
Error Status: 400 Bad Request, 422 Unprocessable Entity, 500 Internal Server Error
Purpose: Processes a new payment for an order.
```

### 2. Update an order status
```
Method: PATCH
Endpoint: /api/orders/{orderId}/status
Success Status: 200 OK
Error Status: 400 Bad Request, 404 Not Found
Purpose: Updates the status of an existing order.
```

### 3. Search orders by customer ID
```
Method: GET
Endpoint: /api/orders?customerId={customerId}
Success Status: 200 OK
Error Status: 400 Bad Request, 404 Not Found
Purpose: Returns all orders belonging to the specified customer.
```

### 4. Cancel an order
```
Method: DELETE
Endpoint: /api/orders/{orderId}/cancel
Success Status: 204 No Content
Error Status: 404 Not Found, 409 Conflict
Purpose: Cancels an existing order if it is still in a cancellable state.
```

## Consistency Observations (Expected Learning)
- **Terminology:** Every entry uses the same five field labels (Method, Endpoint, Success Status, Error Status, Purpose) exactly as demonstrated — no drift into alternate labels like "HTTP Verb" or "Description."
- **Structure:** Path conventions stay consistent — path parameters in braces (`{orderId}`), query parameters for search/filter operations (`?customerId=`), and sub-resource actions as path suffixes (`/status`, `/cancel`) matching the granularity level shown in the examples.
- **Status code judgment:** Examples showed that mutating/deleting operations without a body return `204 No Content` (Example 3), while returning a body uses `200`/`201`. The model applied this reasoning to new cases: POST (create) → `201 Created`; PATCH (partial update) → `200 OK`; DELETE (cancel) → `204 No Content`; plus contextually appropriate extra error codes (`409 Conflict` for cancelling an already-completed order, `422` for invalid payment data) inferred from domain logic, not just copied from the examples.
- **Why few-shot > one-shot here:** A single example might have fixed only the "read" case. Three varied examples (GET collection, GET by ID, DELETE) taught the model to vary Method/Endpoint/Status realistically per operation type, rather than mechanically repeating one pattern.
