# Exercise 2: Prompt Design Principles

## Objective
Apply clarity, specificity, context, constraints, and output formatting when designing a prompt.

## Poorly Designed Prompt
```
Tell me about Kafka.
```
**Why it's weak:** No audience level, no tech stack tie-in, no business scenario, no scope of concepts, no output structure, no length limit. The model could respond with anything from a one-line definition to a 5000-word deep dive on internals.

## Learner Task — Improved Prompt

```
Explain Apache Kafka to a Java developer who is comfortable with Spring Boot
REST APIs but has no prior experience with event-driven or message-based
architectures.

Use our e-commerce Order Management System as the business scenario, where
the Order Service must notify the Inventory Service and Payment Service
whenever an order is placed, without calling them synchronously.

Cover:
1. What a message broker is and why Kafka is used instead of direct
   REST calls between services
2. Core concepts: topics, partitions, producers, consumers, consumer groups
3. How Order Service (producer) publishes an "OrderPlaced" event and how
   Inventory Service and Payment Service (consumers) react to it
4. At-least-once delivery and basic fault tolerance (broker/consumer restarts)
5. How Kafka fits alongside the REST APIs already used between the API
   Gateway and the microservices

Keep the explanation within 600 words, and include one diagram-style text
flow (Order Service -> Kafka Topic -> Inventory Service / Payment Service)
plus one comparison table between REST-based synchronous communication and
Kafka-based asynchronous communication.
```

## Component Mapping

| Prompt Design Element | How It Was Applied |
|---|---|
| **Learner Level** | "Java developer comfortable with Spring Boot REST APIs but no prior event-driven/message-based experience" — sets the right depth, avoids re-explaining REST basics or over-simplifying Kafka internals. |
| **Java Technology** | Explicitly ties Kafka to the Spring Boot microservices stack already used in the case study, not Kafka in the abstract. |
| **Business Scenario** | Order Management System: Order Service notifying Inventory Service and Payment Service asynchronously — makes the explanation concrete and reusable across the exercise series. |
| **Concepts to Cover** | Numbered list (message broker rationale, topics/partitions/producers/consumers, event flow example, fault tolerance, coexistence with REST) — bounds scope so the answer doesn't wander into unrelated Kafka features (e.g., Kafka Streams, Connect). |
| **Output Structure** | Requests a text-based flow diagram and a comparison table — turns an abstract explanation into a structured, skimmable artifact. |
| **Length Restriction** | "Within 600 words" — forces a concise, focused answer instead of an exhaustive essay. |

## Key Takeaway
Good prompt design isn't just adding more words — it's adding the *right* constraints: who the answer is for (level), what world it lives in (tech + scenario), what must be covered (scope), and how it should look (format + length). Each constraint removes a degree of freedom the model would otherwise have to guess, which is what makes the output predictable and directly usable.
