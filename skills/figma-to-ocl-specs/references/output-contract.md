# Specification Output Contract

## Repository and package layout

```text
<repository>/
├── README.md
├── skills/
│   └── figma-to-ocl-specs/
└── <Figma file or product name>/
    ├── FIGMA.md
    ├── CONTEXT.md
    ├── ASSUMPTIONS.md
    ├── coverage-report.md
    ├── schema.dbml
    ├── uc/
    │   ├── README.md
    │   ├── shared-domain-model.md
    │   └── uc-01-<slug>.md
    └── api/
        ├── README.md
        ├── common-contract.md
        └── api-<lowercase-api-id>.md
```

Keep shared skills at the repository root. Store no `CONTEXT.md`, `ASSUMPTIONS.md`, `coverage-report.md`, `schema.dbml`, `uc/`, or `api/` directly in the repository root. Each specification package is self-contained and represents exactly one Figma file or one user-approved Figma scope.

Write all artifact content in English.

## Figma source manifest

Every package contains `FIGMA.md` with:

- package name;
- product scope;
- Figma URL and file key;
- inspected page or node boundary;
- audit date;
- an explicit note for any source identifier unavailable from the supplied evidence.

## Use-case file contract

A completed package contains 18–20 individual use-case files. Each file contains exactly one use case and these sections:

1. `# UC-NN — Name`
2. Description
3. Actors
4. Priority
5. Trigger
6. Preconditions
7. Postconditions
8. Basic Flow
9. Alternative Flows
10. Exception Flows
11. UML Model
12. Business Rules
13. Related UI
14. Related APIs
15. Notes when needed

### Rule-confidential flows

Trigger and condition items have globally unique IDs whose use-case number matches the file:

| Section | ID shape | Markdown shape |
| --- | --- | --- |
| Trigger | `TRG-UC-NN-01` | `**TRG-UC-NN-01** — ...` |
| Preconditions | `PRE-UC-NN-01` | `- **PRE-UC-NN-01** — ...` |
| Postconditions | `POST-UC-NN-01` | `- **POST-UC-NN-01** — ...` |

Every use case has exactly one Basic Flow. The Basic Flow has no identifier, and its activities are one ordered list:

```markdown
### Basic Flow

1. The actor performs an observable action.
2. The client submits the interaction.
3. The system returns an outcome.
4. The client renders the outcome.
```

Alternative and exception sections may contain multiple flows. Each flow has one identifier as a level-four heading, followed by its own ordered activity list:

```markdown
### Alternative Flows

#### AF-UC-NN-01

1. The actor chooses an alternative action.
2. The client renders the returned alternative outcome.

#### AF-UC-NN-02

1. The actor chooses another alternative.
```

Use the same shape with `EF-UC-NN-XX` under Exception Flows. Sequence `TRG`, `PRE`, `POST`, `AF`, and `EF` namespaces from `01` without gaps inside a file. Restart activity numbering at `1` for the Basic Flow and for every alternative or exception flow.

Triggers, preconditions, postconditions, and flows describe only observable state, actor action, client action, system processing, returned outcome, and visible recovery. They are self-contained and contain no rule citation, rule name, internal decision rationale, or paraphrase of domain policy.

Keep these exclusively in OCL: field validity, thresholds, formats, normalization, uniqueness, authorization, ownership, availability, eligibility, ordering, calculations, state transitions, concurrency, idempotency, and sensitive-data handling.

## API file contract

Each file contains exactly one API in a sequential layout. Do not use a property table. Put every label on its own level-two heading and place its value or field definitions immediately below it.

Use this order:

1. `# API-... — Name`
2. `## API ID`
3. `## API Name`
4. `## Related Use Case IDs`
5. `## Method`
6. `## Path`
7. `## Description`
8. `## Authentication`
9. `## Authorization`
10. `## Request Headers`
11. `## Path Parameters`
12. `## Query Parameters`
13. `## Request Body`
14. one or more `## Success Response — HTTP NNN` sections
15. one `## Error Response — HTTP NNN` section for each public error outcome
16. `## Notes`

Write `None.` for an empty request section so the absence is explicit. Define each field under a level-three heading and include the applicable metadata: type, format, requiredness, nullability, default, public allowed values, syntax-level validation, trigger, description, and example.

### Wire-contract boundary

API files describe transport shape only. They contain no UML, PlantUML, OCL, rule identifier, rule section, or domain-policy definition.

Safe API validation is limited to independently checkable wire syntax, including JSON type, HTTP encoding, MIME type, date/date-time representation, email syntax, URI syntax, opaque identifier representation, and membership in a public enum.

Keep domain thresholds, cross-field comparisons, existence and uniqueness checks, ownership, authorization rationale, availability, eligibility, quote validity, price consistency, capacity decisions, ranking, state transitions, concurrency, idempotency behavior, normalization, masking policy, and persistence effects in the use-case OCL only. Requiredness and nullability may be documented as request-schema properties, but their descriptions must not explain the domain reason.

Error triggers state only public protocol outcomes such as malformed wire input, rejected authentication context, unavailable resource response, operation conflict, upstream failure, or temporary service failure. They do not identify the hidden predicate, decision order, threshold, or failed credential component.

## OCL contract

Every Business Rule is its own fenced `ocl` block. The section contains only blank lines and OCL fences.

```ocl
-- BR-UC-04-01
-- Source: Figma | Product source | Assumption
context StayService::search(criteria: StaySearchCriteria): Sequence(StayOffer)
pre BR_UC_04_01_DestinationIsPresent:
  criteria.destinationId <> null and criteria.destinationId.trim().size() > 0
```

Rule IDs are globally unique and sequential within a use-case file. OCL constraint names use underscores because hyphens are not valid identifiers.

## UML semantic support

UML is normative vocabulary for OCL, not decoration. Every OCL name resolves to a classifier, property, association, enumeration literal, operation, or explicitly defined primitive helper. Define helpers such as `DateTime::now()`, normalization, hashing, and validation in UML before using them.

## DBML contract

`schema.dbml` must:

- persist every entity referenced by create/update business rules;
- support all ownership and response-mapping relationships;
- distinguish provider-backed `Offer`, short-lived `Quote`, and persisted `Booking`;
- encode foreign keys, uniqueness, indexes, and state enumerations implied by OCL;
- support optimistic versioning and idempotency where required;
- store password and session hashes rather than raw credentials;
- store payment references or fingerprints rather than raw card numbers, CVV, or provider tokens;
- use names and types consistent with APIs and UML;
- compile successfully with the DBML CLI.

## Traceability

- Every UC lists at least one supporting Figma node and every required API.
- Every API lists all related UC IDs.
- Every use-case rule uses vocabulary present in UML and, when persistent, DBML.
- Index files link to every individual specification.
- Unsupported Figma flows appear only in the coverage report.

## Validation gates

- Each package contains 18–20 individual UC files.
- One UC/API per file with correct filenames and one top-level heading.
- One Figma source manifest per package.
- All content is English.
- Every trigger and condition item has the correct ID namespace, matching use-case number, unique ID, and gap-free local sequence.
- Every use case contains exactly one uncoded Basic Flow whose activities form a gap-free ordered list starting at `1`.
- Every Alternative Flow and Exception Flow has a unique, correctly namespaced heading and a gap-free ordered activity list starting at `1`.
- Trigger, condition, and flow sections contain no Business Rule reference or internal policy content.
- Every rule block has one rule ID, one context, and one constraint.
- Business Rules sections contain OCL blocks only.
- Rule IDs are globally unique.
- Flow sections contain no OCL operators, rule IDs, thresholds, formulas, predicates, or decision order.
- Every API uses the required sequential section order and contains no Markdown table.
- API files contain no UML, PlantUML, OCL fence, or rule identifier.
- API field validation is syntax-only and contains no domain threshold, comparison between fields, resource-state predicate, calculation, or policy rationale.
- API error triggers expose only public protocol outcomes.
- Markdown fences and relative links are valid.
- UC-to-API references resolve in both directions.
- DBML compiles to PostgreSQL SQL.
