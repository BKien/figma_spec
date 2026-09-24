# Validation Report

Audit date: 2026-09-24.

## Results

| Gate | Result | Evidence |
| --- | --- | --- |
| Package validator | PASS | 18 use cases, 13 sequential APIs, 90 coded conditions/branches, 178 flow activities, 138 OCL blocks |
| Use-case count and rule minimum | PASS | 18 use cases; every use case has 7-11 BRs |
| Policy isolation in conditions and flows | PASS | All 18 interaction sections checked for BR references, predicates, thresholds and policy language; manual prose review also completed |
| Rule identity and uniqueness | PASS | Correct UC namespace, gap-free rule numbering, and no repeated predicate within an individual use case |
| Repository validator | PASS | All three Figma packages; package separation and structure preserved |
| DBML compilation | PASS | 22 tables compiled to PostgreSQL with @dbml/cli 9.1.1 |
| UC/API references | PASS | Every relationship checked in both directions |
| Source-node references | PASS | All UC screen links resolve to the stored 20-frame inventory |
| Wire objects and examples | PASS | 29 object definitions and 17 JSON request/response examples; field examples also checked |
| Example arithmetic | PASS | Cart, line, and checkout-summary examples checked against their displayed amounts |
| Local links and Markdown fences | PASS | All package Markdown documents checked |
| OCL context vocabulary | PASS | Context classifiers and operation names checked against the local/shared UML declarations |

Machine-readable results: [consistency-results.json](evidence/consistency-results.json). Compiled schema: [schema.sql](evidence/schema.sql).

## Reproduce

Run from the repository using an installed Python runtime and PowerShell 7:

```powershell
npm exec --yes --package @dbml/cli@9.1.1 -- pwsh -NoProfile -File '.\Euphoria Ecommerce Apparels\scripts\validate.ps1'
```

The wrapper runs the package validator, the full repository validator, and the package consistency checker. It compiles DBML during package and repository checks. The dependency version is pinned because the environment's cached @dbml/core 10.2.0 package lacked its advertised runtime files; an older 3.13.1 compiler also did not support the schema's check-constraint syntax. Version 9.1.1 compiled the unchanged schema successfully. No global dependency or shared validator was changed.

## Verification limits

The checks validate document structure, traceability, declared wire shapes, selected example arithmetic, model context declarations, and DBML compilation. They do not execute a backend, run a formal OCL type checker/model solver, or test a deployed database migration. The predicates received a manual consistency review, including checkout retry identity, cart revisions, address defaults, snapshot totals, and stock updates. Cross-row rules still require implementation and runtime tests.

Figma prototype wiring, Styleguide details, hidden states, and complete instance overrides were not verified after the connector reached its plan limit. The [coverage report](coverage-report.md) explicitly separates these gaps from the supported scope. Passing validators does not promote partial flows to supported requirements.
