# Exercise 3: Zero-shot Prompting

## Objective
Ask the model to complete a task without providing an example, and observe how it infers the required response structure purely from instructions.

## Prompt Used
```
Act as a Java code reviewer.

Review the following Spring Boot controller and identify:
- Functional defects
- REST design issues
- Validation problems
- Exception-handling issues
- Security concerns

For every issue, provide:
1. Issue
2. Why it is a problem
3. Recommended correction
4. Corrected code

Code:

@RestController
public class OrderController {

    @Autowired
    private OrderRepository repository;

    @PostMapping("/order")
    public Order save(@RequestBody Order order) {
        return repository.save(order);
    }
}
```

## Model's Response (Zero-shot Output)

### 1. Functional Defect — No HTTP status control on creation
**Issue:** The method returns the saved `Order` with the default `200 OK` status.
**Why it is a problem:** REST conventions require `201 Created` for a successful resource creation, so clients can't reliably distinguish "created" from "read."
**Recommended correction:** Wrap the response in `ResponseEntity` and return `201 Created` with a `Location` header.
**Corrected code:**
```java
@PostMapping("/order")
public ResponseEntity<Order> save(@RequestBody Order order) {
    Order saved = repository.save(order);
    URI location = ServletUriComponentsBuilder.fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(saved.getId())
            .toUri();
    return ResponseEntity.created(location).body(saved);
}
```

### 2. REST Design Issue — Non-plural, non-resource-oriented endpoint
**Issue:** The route is `/order` instead of `/orders`.
**Why it is a problem:** REST convention uses plural nouns for collections, keeping the API consistent with other services (Product, Inventory) in the system.
**Recommended correction:** Rename the mapping to `/orders`.
**Corrected code:**
```java
@RestController
@RequestMapping("/orders")
public class OrderController {
    @PostMapping
    public ResponseEntity<Order> save(@RequestBody Order order) { ... }
}
```

### 3. REST Design Issue — Entity exposed directly as request/response body
**Issue:** `Order` (the JPA entity) is bound directly to `@RequestBody` and returned directly as the response.
**Why it is a problem:** Couples the API contract to the persistence model. Any DB schema change breaks the API, and it enables **mass assignment / overposting** — a client can set fields like `id`, `status`, or `totalAmount` that should never be client-controlled.
**Recommended correction:** Introduce `OrderRequest` (input DTO) and `OrderResponse` (output DTO), and map between DTO and entity in the service layer.
**Corrected code:**
```java
public record OrderRequest(Long customerId, Long productId, int quantity) {}
public record OrderResponse(Long id, Long customerId, Long productId, int quantity, String status) {}
```

### 4. Validation Problem — No input validation
**Issue:** `customerId` and `productId` are never checked for presence or validity before saving.
**Why it is a problem:** Invalid or missing IDs will either cause a DB constraint failure (ugly 500 error) or silently create a corrupt order.
**Recommended correction:** Add Bean Validation annotations on the DTO and `@Valid` on the controller parameter.
**Corrected code:**
```java
public record OrderRequest(
    @NotNull Long customerId,
    @NotNull Long productId,
    @Min(1) int quantity
) {}

@PostMapping
public ResponseEntity<OrderResponse> save(@Valid @RequestBody OrderRequest request) { ... }
```

### 5. Exception-Handling Issue — No handling for save failures
**Issue:** Any exception thrown by `repository.save()` (e.g., constraint violation, DB down) propagates unhandled.
**Why it is a problem:** Results in a raw `500 Internal Server Error` with a stack trace potentially leaked to the client — poor UX and a security risk (information disclosure).
**Recommended correction:** Add a `@RestControllerAdvice` global exception handler mapping known exceptions to appropriate HTTP statuses and safe messages.
**Corrected code:**
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<String> handleDataIntegrity(DataIntegrityViolationException ex) {
        return ResponseEntity.status(HttpStatus.CONFLICT).body("Invalid order data.");
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<String> handleValidation(MethodArgumentNotValidException ex) {
        return ResponseEntity.badRequest().body("Validation failed: " + ex.getMessage());
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<String> handleGeneric(Exception ex) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Unexpected error occurred.");
    }
}
```

### 6. Security Concern — No authentication/authorization on a state-changing endpoint
**Issue:** Anyone who can reach the endpoint can create orders; there's no check on caller identity or permissions.
**Why it is a problem:** Order creation should be tied to an authenticated customer to prevent abuse (fake orders, spam, DoS on downstream Inventory/Payment services via Kafka).
**Recommended correction:** Secure the endpoint with Spring Security (e.g., `@PreAuthorize` or gateway-level auth) and derive `customerId` from the authenticated principal rather than trusting the request body.
**Corrected code:**
```java
@PreAuthorize("isAuthenticated()")
@PostMapping
public ResponseEntity<OrderResponse> save(@Valid @RequestBody OrderRequest request,
                                           @AuthenticationPrincipal UserDetails principal) {
    // resolve customerId from principal instead of trusting client input
}
```

### 7. Constructor Injection vs Field Injection
**Issue:** `@Autowired` is used for field injection on `repository`.
**Why it is a problem:** Field injection hides dependencies, makes unit testing harder (can't construct with mocks without reflection), and prevents the field from being `final`.
**Recommended correction:** Use constructor injection.
**Corrected code:**
```java
private final OrderRepository repository;

public OrderController(OrderRepository repository) {
    this.repository = repository;
}
```

## Fully Corrected Controller
```java
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderRepository repository;
    private final OrderMapper mapper;

    public OrderController(OrderRepository repository, OrderMapper mapper) {
        this.repository = repository;
        this.mapper = mapper;
    }

    @PreAuthorize("isAuthenticated()")
    @PostMapping
    public ResponseEntity<OrderResponse> save(@Valid @RequestBody OrderRequest request) {
        Order saved = repository.save(mapper.toEntity(request));
        URI location = ServletUriComponentsBuilder.fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(saved.getId())
                .toUri();
        return ResponseEntity.created(location).body(mapper.toResponse(saved));
    }
}
```

## Expected Learning — Reflection
No example output was provided in the prompt — only a bulleted instruction list (5 categories of issues, 4-part structure per issue). The model had to **infer**:
- How many issues to find (driven by actually scanning the code against each category, not a fixed count)
- The exact shape of "Issue / Why / Correction / Code" for every single finding
- That "corrected code" means a runnable snippet, not just prose description

This demonstrates the core zero-shot behavior: **clear task decomposition in the prompt (categories + required fields) is what makes an example unnecessary.** The structure came from the instructions, not from a demonstrated sample.
