# Exercise 10: Prompt Evaluation

## Objective
Assess whether a prompt produces a useful, accurate and reusable result using the rubric, then iteratively improve it until it scores at least 17/20.

*Note: the rubric's individual row maximums (2+2+2+2+2+2+3+3+2+2) actually sum to 22, one point over the stated "Total: 20" — likely a minor drafting inconsistency in the source rubric. Scoring below still targets the stated 17–20 "Excellent" band; the extra headroom doesn't change the interpretation.*

## Step 1 — Score the Original Prompt
```
Create Java code for payment.
```

| Criterion | Score | Reasoning |
|---|---|---|
| Clear role | 0/2 | No role assigned at all. |
| Sufficient context | 0/2 | No mention of the system, domain, or tech stack. |
| Specific task | 1/2 | "Payment" narrows the domain slightly, but "code" is undefined (class? API? whole service?). |
| Complete requirements | 0/2 | No functional requirements listed. |
| Useful constraints | 0/2 | No constraints (no security, no exclusions, no style rules). |
| Defined output format | 0/2 | No indication of structure, language conventions, or presentation. |
| Technically accurate output | 1/3 | Without context the model must guess the stack; output is plausible Java but ungrounded in this system. |
| Secure coding practices | 0/3 | Nothing prompts for secure handling of payment/card data. |
| Code completeness | 1/2 | Likely returns a single class/snippet, not a full layered implementation. |
| Testability | 0/2 | No tests requested. |
| **Total** | **3 / 20** | **Vague or unreliable prompt (0–8 band).** |

---

## Step 2 — Iterative Improvement

### Iteration 1: Add Role + Context + Task
```
Act as a senior Java Spring Boot developer.
We are building a Payment Service for an e-commerce Order Management System
using Java 21, Spring Boot 3, MySQL and Kafka.
Create the REST API to process credit-card payments for an order.
```
**Score: 8/20** — Role 2, Context 2, Task 2, Requirements 0, Constraints 0, Format 0, Technical accuracy 1, Security 0, Completeness 1, Testability 0. *(Incomplete prompt band.)*

### Iteration 2: Add Requirements + Constraints
```
...(as above)...

Requirements:
- Include controller, service, repository and entity layers
- Validate orderId, customerId and amount
- Reject the payment if amount exceeds the customer's approved transaction limit
- Publish PaymentSucceeded / PaymentFailed events to Kafka after processing

Constraints:
- Do not use Lombok
- Follow clean-code practices
- Include global exception handling
- Do not store raw card numbers — accept only a tokenized cardToken
```
**Score: 15/20** — Role 2, Context 2, Task 2, Requirements 2, Constraints 2, Format 0, Technical accuracy 2, Security 2, Completeness 1, Testability 0. *(Good, but can be refined band.)*

### Iteration 3 (Final): Add Output Format + Testability + Stronger Security
```
Act as a senior Java Spring Boot developer.

We are building a Payment Service for an e-commerce Order Management System
using Java 21, Spring Boot 3, MySQL and Kafka.

Task:
Create the REST API to process credit-card payments for an order.

Requirements:
- Include controller, service, repository and entity layers, plus request/response DTOs
- Validate orderId, customerId and amount using Bean Validation
- Reject the payment (HTTP 422, reason "LIMIT_EXCEEDED") if amount exceeds the
  customer's approved transaction limit
- Use an Idempotency-Key header to prevent duplicate charges on client retry
- Publish PaymentSucceeded / PaymentFailed events to Kafka after processing

Constraints:
- Do not use Lombok
- Follow clean-code practices
- Include global exception handling via @RestControllerAdvice
- Do not store or log raw card numbers — accept only a tokenized cardToken
- Do not log the cardToken value itself

Output:
1. Project structure
2. Java code for every class (entity, DTOs, repository, service, controller,
   exception handler)
3. Unit tests (JUnit 5 + Mockito) covering: successful payment, limit-exceeded
   rejection, duplicate idempotency-key replay, and downstream Kafka publish failure
```

| Criterion | Score | Reasoning |
|---|---|---|
| Clear role | 2/2 | Senior Java Spring Boot developer, explicitly stated. |
| Sufficient context | 2/2 | Domain, tech stack (Java 21, Spring Boot 3, MySQL, Kafka), and system named. |
| Specific task | 2/2 | Single, unambiguous deliverable: payment-processing REST API. |
| Complete requirements | 2/2 | Layers, validation, business rule (limit check), idempotency, eventing all specified. |
| Useful constraints | 2/2 | No Lombok, clean code, exception handling, no raw card storage/logging. |
| Defined output format | 2/2 | Explicit ordered deliverable list (structure → code → tests). |
| Technically accurate output | 3/3 | Grounded in the real stack and prior exercises (idempotency key, DTOs, event publishing) — nothing left for the model to invent. |
| Secure coding practices | 3/3 | Tokenized card handling, no logging of sensitive token, transaction-limit enforcement, idempotency to prevent double-charge. |
| Code completeness | 2/2 | All layers plus exception handling and DTOs explicitly requested. |
| Testability | 2/2 | Named test framework and four concrete scenarios to cover. |
| **Total** | **22 / 20 (capped: 20/20)** | **Excellent prompt (17–20 band).** |

## Reflection
The prompt didn't improve by getting *longer* for its own sake — each iteration closed a specific gap identified by the rubric: first identity/context (who + what system), then scope (functional + non-functional requirements), then guarantees (security, idempotency) and verifiability (test scenarios + output shape). The rubric itself acted as a checklist for iterative refinement, the same way it would for a code review.
