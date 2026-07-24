# Exercise 9: Prompt Templates

## Objective
Create reusable prompts using placeholders, then instantiate the same template for four different services.

## Reusable Template
```
Act as a senior Java Spring Boot developer.

Create a {SERVICE_NAME} microservice for a {BUSINESS_DOMAIN} application.

Technology:
- Java: {JAVA_VERSION}
- Spring Boot: {SPRING_BOOT_VERSION}
- Database: {DATABASE}
- Build tool: {BUILD_TOOL}

Entity fields:
{ENTITY_FIELDS}

Required endpoints:
{ENDPOINTS}

Validation rules:
{VALIDATION_RULES}

Additional requirements:
- Use layered architecture
- Include global exception handling
- Use DTOs
- Include unit tests
- Include API documentation
- Follow REST conventions

Output:
1. Project structure
2. Dependencies
3. Configuration
4. Entity and DTOs
5. Repository
6. Service
7. Controller
8. Exception handling
9. Tests
```

---

## 1. Product Service
```
Act as a senior Java Spring Boot developer.

Create a Product Service microservice for an e-commerce Order Management System application.

Technology:
- Java: 21
- Spring Boot: 3.2
- Database: MySQL
- Build tool: Maven

Entity fields:
- Long id
- String name
- String description
- BigDecimal price
- String category
- boolean active

Required endpoints:
- POST /api/products (create a product)
- GET /api/products (list all products)
- GET /api/products/{id} (get product by id)
- PUT /api/products/{id} (update a product)
- DELETE /api/products/{id} (deactivate a product)

Validation rules:
- name must not be blank
- price must be greater than 0
- category must not be blank

Additional requirements:
- Use layered architecture
- Include global exception handling
- Use DTOs
- Include unit tests
- Include API documentation
- Follow REST conventions

Output:
1. Project structure
2. Dependencies
3. Configuration
4. Entity and DTOs
5. Repository
6. Service
7. Controller
8. Exception handling
9. Tests
```

---

## 2. Customer Service
```
Act as a senior Java Spring Boot developer.

Create a Customer Service microservice for an e-commerce Order Management System application.

Technology:
- Java: 21
- Spring Boot: 3.2
- Database: MySQL
- Build tool: Maven

Entity fields:
- Long id
- String fullName
- String email
- String phoneNumber
- BigDecimal approvedTransactionLimit
- LocalDateTime registeredAt

Required endpoints:
- POST /api/customers (register a customer)
- GET /api/customers/{id} (get customer by id)
- GET /api/customers/{id}/transaction-limit (get approved transaction limit)
- PUT /api/customers/{id} (update customer profile)

Validation rules:
- fullName must not be blank
- email must be a valid email format and unique
- phoneNumber must match a valid phone pattern
- approvedTransactionLimit must be greater than or equal to 0

Additional requirements:
- Use layered architecture
- Include global exception handling
- Use DTOs
- Include unit tests
- Include API documentation
- Follow REST conventions

Output:
1. Project structure
2. Dependencies
3. Configuration
4. Entity and DTOs
5. Repository
6. Service
7. Controller
8. Exception handling
9. Tests
```

---

## 3. Payment Service
```
Act as a senior Java Spring Boot developer.

Create a Payment Service microservice for an e-commerce Order Management System application.

Technology:
- Java: 21
- Spring Boot: 3.2
- Database: MySQL
- Build tool: Maven

Entity fields:
- Long id
- Long orderId
- Long customerId
- BigDecimal amount
- String status
- String cardToken
- LocalDateTime processedAt

Required endpoints:
- POST /api/payments (process a payment for an order)
- GET /api/payments/{id} (get payment details)
- GET /api/payments/order/{orderId} (get payment by order id)

Validation rules:
- orderId and customerId must not be null
- amount must be greater than 0
- amount must not exceed the customer's approved transaction limit
- cardToken must not be blank

Additional requirements:
- Use layered architecture
- Include global exception handling
- Use DTOs
- Include unit tests
- Include API documentation
- Follow REST conventions
- Publish PaymentSucceeded/PaymentFailed events to Kafka after processing

Output:
1. Project structure
2. Dependencies
3. Configuration
4. Entity and DTOs
5. Repository
6. Service
7. Controller
8. Exception handling
9. Tests
```

---

## 4. Inventory Service
```
Act as a senior Java Spring Boot developer.

Create an Inventory Service microservice for an e-commerce Order Management System application.

Technology:
- Java: 21
- Spring Boot: 3.2
- Database: MySQL
- Build tool: Maven

Entity fields:
- Long id
- Long productId
- int availableStock
- int reservedStock
- LocalDateTime lastUpdatedAt

Required endpoints:
- GET /api/inventory/{productId} (get current stock for a product)
- POST /api/inventory/reserve (reserve stock for an order)
- POST /api/inventory/release (release previously reserved stock, e.g., on order cancellation)

Validation rules:
- productId must not be null
- reservation quantity must be greater than 0
- reservation must fail if availableStock is less than requested quantity

Additional requirements:
- Use layered architecture
- Include global exception handling
- Use DTOs
- Include unit tests
- Include API documentation
- Follow REST conventions
- Consume OrderPlaced events from Kafka to trigger stock reservation

Output:
1. Project structure
2. Dependencies
3. Configuration
4. Entity and DTOs
5. Repository
6. Service
7. Controller
8. Exception handling
9. Tests
```

## Key Takeaway
The same skeleton produced four consistent, non-generic prompts just by substituting domain-specific values into the placeholders. This is the payoff of prompt templating: **consistency across a whole microservices suite** (same architecture, same quality bar) **without re-authoring the instructions each time** — only the domain-specific fields change per service.
