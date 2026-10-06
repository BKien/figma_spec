# Financial Management

A reviewed personal financial tracking specification imported from the supplied [Google spreadsheet](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit). The package contains 18 normalized use cases, 18 API contracts, complete local UML/OCL, and a MySQL persistence specification. The supplied source is preserved separately; contradictions and deliberate contract changes are documented.

## Package Contents

- [Source identity and scope](FIGMA.md)
- [Domain glossary](CONTEXT.md)
- [Assumptions and product decisions](ASSUMPTIONS.md)
- [Coverage and source-to-package mapping](coverage-report.md)
- [Source consistency review](consistency-review.md)
- [Use case index](01-inception/uc/)
- [API index](01-inception/api/)
- [Common wire contract](01-inception/api/common-contract.md)
- [OCL utility semantics](OCL-UTILITY-DEFINITIONS.md)
- [MySQL DBML schema](schema.dbml)
- [Supplementary MySQL constraints](persistence.sql)
- [Preserved source and checksums](source/README.md)
- [Validation results and limits](validation-report.md)

## Reviewed Behavior

The package preserves identity, account CRUD, history, transaction entry, spending reports, upcoming bills and financial goals. Quick edit is an alternative within account editing. Transaction filtering and category selection provide two explicit goals from existing source evidence. The category-detail presentation is a proposed extension grounded in the supplied endpoint.

Completed transactions affect balances and report totals; Pending and Failed remain visible without changing realized cash flow. Manual balance edits are audited corrections. Resource versions prevent concurrent writes from silently overwriting account balances or goal targets. Goal creation serializes inclusive date-overlap checks. Reports use exact decimals, recorded transaction dates and Asia/Saigon calendar boundaries.

No application implementation, live Figma design, financial institution integration, payment execution or deployment is included. The review deliberately changes parts of the supplied contract, including response envelopes and required version fields; see [compatibility decisions](consistency-review.md).

## Regeneration and Validation

Run from the repository root:

```powershell
python 'Financial Management/scripts/build_specs.py'
python 'Financial Management/scripts/verify_package.py'
& 'skills/figma-to-ocl-specs/scripts/validate_specs.ps1' -Root 'Financial Management'
& 'skills/figma-to-ocl-specs/scripts/validate_repository.ps1' -Root '.'
```

The authoring script regenerates individual use-case/API files, indexes, coverage and source checksums from the preserved source and explicit reviewed rules. Static glossary, review and assumption documents remain hand-authored. Validation is structural and source-grounded; it does not establish that a backend implements the specification or that OCL has been executed by a formal engine.
