# Exercise 1: Prompt Anatomy

## Objective
Understand the major components of a well-structured prompt: Role, Context, Task, Requirements, Constraints, Input, Output Format.

## Weak Prompt
```
Create an order microservice.
```
**Why it's weak:** No role, no context, no requirements, no constraints, no output format. The model has to guess the tech stack, layers, validation rules, and how to present the result.

## Improved Prompt
```
Role:
Act as a senior Java microservices developer.

Context:
We are developing an e-commerce Order Service using Java 21 and Spring Boot 3.

Task:
Create a REST API to place and retrieve customer orders.

Requirements:
- Use Spring Web
- Use Spring Data JPA
- Use MySQL
- Include controller, service, repository and entity layers
- Validate customerId and productId
- Return suitable HTTP status codes

Constraints:
- Do not use Lombok
- Follow clean-code practices
- Include exception handling

Output:
Provide the project structure followed by the Java code for each class.
```

## Learner Activity — Labeled Breakdown

| Prompt Component | Text from the Prompt | Purpose |
|---|---|---|
| **Role** | "Act as a senior Java microservices developer." | Sets the expertise level and perspective the model should respond from — shapes tone, depth, and design decisions. |
| **Context** | "We are developing an e-commerce Order Service using Java 21 and Spring Boot 3." | Gives the background/domain and tech stack so the output fits the existing system instead of a generic guess. |
| **Task** | "Create a REST API to place and retrieve customer orders." | States the concrete deliverable — what the model must actually produce. |
| **Requirements** | "Use Spring Web / Spring Data JPA / MySQL; include controller, service, repository, entity layers; validate customerId and productId; return suitable HTTP status codes." | Specifies functional and technical must-haves — the "what good looks like" checklist. |
| **Constraints** | "Do not use Lombok; follow clean-code practices; include exception handling." | Sets boundaries and non-negotiables — things to avoid or always include, narrowing the solution space. |
| **Input** | *(implicit — customerId, productId via the order placement request)* | The data the API will consume. Not explicitly labeled in this prompt, but implied by the requirement to validate customerId and productId. |
| **Output Format** | "Provide the project structure followed by the Java code for each class." | Tells the model exactly how to structure its response (structure first, then code, class by class). |

## Key Takeaway
A weak prompt forces the model to guess intent. A well-structured prompt removes ambiguity by explicitly separating **who** should answer (Role), **why/where** (Context), **what** to build (Task), **how** it must be built (Requirements/Constraints), **what data** it works with (Input), and **how to present** the answer (Output Format). This consistently produces more accurate, complete, and directly usable responses.
