---
name: figma-to-ocl-specs
description: Inspect a Figma product and create or update a self-contained per-Figma specification package with use cases, policy-isolated OCL/UML, wire-only API contracts, and DBML. Use for Figma-derived functional specifications, business rules, API contracts, data models, or repositories that contain specifications for multiple Figma files.
---

# Figma to OCL Specifications

Convert observable product design into a traceable specification package without modifying the Figma file or mixing evidence from different Figma sources.

Before creating artifacts, read:

- [references/figma-audit.md](references/figma-audit.md) for evidence collection and scope decisions.
- [references/output-contract.md](references/output-contract.md) for required files, OCL isolation, UML semantics, API completeness, DBML consistency, and validation gates.

## Workflow

1. **Select the package boundary.** In a multi-Figma repository, keep `skills/` at the repository root and store each Figma specification in its own sibling directory. Resolve an existing package by its `FIGMA.md`; otherwise create a package directory from the Figma file or product name. Keep root-level specification artifacts out of the repository root.

2. **Audit the Figma evidence.** Enumerate pages, top-level product screens, nested states, overlays, mobile/desktop variants, and action labels. Distinguish product screens from components and decorative frames. Capture screenshots for ambiguous frames. Record the source identity in `FIGMA.md`.

3. **Freeze supported scope.** Build a candidate use-case matrix and classify each candidate as supported, partial, or missing. Create specifications only for supported use cases unless the user explicitly authorizes inferred or planned flows. Record partial and missing flows separately.

4. **Establish the domain language.** Create or update package-local `CONTEXT.md` with canonical terms. In booking domains, keep `Offer`, `Quote`, and `Booking` distinct. Use the same terms in filenames, UML, OCL, APIs, and DBML.

5. **Create one specification per file.** Write every use case to `uc/uc-<two-digit-sequence>-<slug>.md` and every API to `api/api-<lowercase-api-id>.md`. Generate indexes in both folders.

6. **Write structured observable behavior.** Give every trigger, precondition, and postcondition item its own `TRG`, `PRE`, or `POST` ID. Write exactly one Basic Flow as a numbered activity list with no flow ID and no step IDs. Give each Alternative Flow and Exception Flow its own `AF` or `EF` heading, then number the activities beneath that heading from `1`. Keep these sections policy-neutral and self-contained. Describe only actor, client, and system interactions and returned outcomes; omit rule names, rule IDs, predicates, thresholds, formulas, eligibility, authorization rationale, ordering logic, and internal decision sequence.

7. **Isolate domain policy.** Put validation, authorization, ownership, availability, eligibility, ordering, calculations, state transitions, concurrency, idempotency, normalization, and sensitive-data handling exclusively in separately identified OCL blocks inside use-case specifications. Do not copy or paraphrase that policy into API field validation or error triggers.

8. **Model before constraining.** Place a PlantUML model immediately before Business Rules in every use-case specification. Every classifier, property, enumeration, association, and operation referenced by OCL must exist in that local model or in `uc/shared-domain-model.md`. API specifications contain neither UML nor OCL.

9. **Complete APIs and persistence.** Write every API as an English sequential contract in which each label is followed by its value or field definitions. Describe transport shape, wire types, requiredness, nullability, public enums, examples, response envelopes, and public error outcomes. Use only syntax-level field validation; omit domain thresholds, cross-field comparisons, existence or ownership checks, availability, eligibility, calculations, ranking, state transitions, concurrency, idempotency behavior, and sensitive-data policy. Create package-local `schema.dbml` for persistent concepts, constraints, references, indexes, state enumerations, concurrency, idempotency, and secret-safe references.

10. **Validate the package and repository.** Run `scripts/validate_specs.ps1 -Root <package-directory>`, then `scripts/validate_repository.ps1 -Root <repository-directory>`. Fix every failure. Stop only when behavior IDs, rule IDs, package isolation, policy isolation, traceability, Markdown structure, English-only content, and DBML compilation all pass.

## Assumptions

Figma rarely supplies every policy value. Prefer an explicit product source supplied by the user. When a complete contract requires a value that has no source, choose a conservative domain-appropriate assumption, record it in package-local `ASSUMPTIONS.md`, and add `-- Source: Assumption` inside the corresponding OCL block. Keep assumptions out of triggers, conditions, and flows.

## Completion

The task is complete only when the selected package satisfies every invariant in `references/output-contract.md`, the validator passes against that package directory, DBML compiles, the single Basic Flow is an uncoded ordered list, every branch-flow ID is unique and correctly namespaced, every API is sequential and policy-neutral, and every UC/API ID resolves bidirectionally.
