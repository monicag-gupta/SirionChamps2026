# Exercise 11: Prompt Optimization Techniques

## Objective
Improve a prompt through multiple iterations, observing which change contributes the most.

## Iteration Walkthrough

| Step | Prompt | What Changed | Effect on Output |
|---|---|---|---|
| **Initial** | "Create an Order Service." | — | Model must guess language, framework, database, scope, and layers. Output is generic and likely mismatched to the actual system. |
| **Opt 1: Add Context** | "...for an e-commerce microservices application using Java and Spring Boot." | Domain + tech family added. | Output now assumes Spring Boot conventions instead of, say, plain Java or a different framework — but still no functional scope. |
| **Opt 2: Add Functional Requirements** | "...that can create, retrieve, update and cancel orders." | Defines the CRUD-plus-cancel surface. | Model now knows exactly which endpoints to build instead of guessing (e.g., might have only built "create" before). |
| **Opt 3: Add Technical Requirements** | "Use Java 21, Spring Boot 3, Spring Data JPA, MySQL and Maven." | Pins exact versions/tools. | Removes version drift (e.g., avoids `javax.*` vs `jakarta.*` package mismatches, Gradle vs Maven build files). |
| **Opt 4: Add Architecture & Quality Requirements** | "Use controller, service, repository and DTO layers. Include validation, exception handling, logging and unit tests." | Defines structural and quality expectations. | Output changes from "a working demo" to "a maintainable, layered, production-shaped codebase." |
| **Opt 5: Add Output Constraints** | "First provide the project structure. Then provide every Java file separately. Ensure the code is compilable. Do not omit imports or configuration." | Defines presentation and a completeness guarantee. | Output becomes directly copy-pasteable/runnable rather than partial snippets that need reassembly. |

## Reflection Question: Which Change Produced the Biggest Improvement, and Why?

**Opt 2 (Add Functional Requirements)** produced the single biggest jump in usefulness, even though Opt 4 and Opt 5 are also significant.

**Why:** Before Opt 2, the model had a tech stack (Opt 1) but no idea *what the service actually needed to do*. Without functional scope, every subsequent addition (technical stack, architecture, output format) would have been "well-built but wrong" — a beautifully layered, cleanly formatted Order Service that might only implement `createOrder` and miss `retrieve/update/cancel` entirely. Functional requirements are what make the *rest* of the requirements meaningful: architecture and quality constraints (Opt 4) only matter once you know how many endpoints/flows they need to apply to, and output formatting (Opt 5) only matters once you know how much code will actually be generated.

That said, in practice **Opt 5 (Output Constraints)** produced the biggest *practical* usability jump for a learner directly copy-pasting code — "ensure compilable, don't omit imports" is what turns a demo answer into something that actually builds. So the honest answer depends on the lens: Opt 2 fixes *correctness of scope*, Opt 5 fixes *usability of the artifact*. Both matter; Opt 2 is fixed first because scope has to be right before formatting the output for it makes sense.

## Optimization Techniques Practiced Here
- **Add missing context** → Opt 1 (domain, framework)
- **Break a large request into smaller prompts** → could be applied per-layer (entity → repository → service → controller) if the Opt 5 output were still too large for one response
- **Define acceptance criteria** → implicit in Opt 2's functional list; could be made explicit with HTTP status expectations per operation
- **Request assumptions explicitly** → not yet applied; a natural Opt 6 would be "state any assumptions you made about fields or validation rules"
- **Add examples** → not used here; could few-shot one endpoint's shape as exercise 5 did
- **Specify exclusions** → could add "do not use Lombok" as in Exercise 1/10
- **Specify the output format** → Opt 5
- **Ask the model to review its output against a checklist** → natural Opt 7: "verify every endpoint from the functional requirements is implemented before finishing"
- **Test the generated code independently** → outside the prompt itself — compile and run the generated project
- **Refine the prompt based on errors** → if compilation fails or a requirement was missed, feed that specific gap back as the next iteration (mirrors Exercise 10's rubric-driven refinement)
