# Local UML update — 2026-10-01

All 150 active use cases in eight projects were processed. `100ms Video Conferencing and Live Streaming` is excluded and its complete file-hash inventory is unchanged.

| Project | Use cases |
| --- | ---: |
| Clicon Ecommerce Marketplace | 20 |
| DH Dental Recruitment | 20 |
| EdTech Education Dashboard | 20 |
| Euphoria Ecommerce Apparels | 18 |
| Financial Management | 18 |
| Table Booking Restaurant Application | 20 |
| Travel Booking App Web & Mobile | 18 |
| Tripma | 16 |

Each local diagram is projected from its own Business Rules. Referenced operations and properties retain their declared types and multiplicities. Signature dependencies are defined within the same diagram. Enums retain their full literal domain; value objects retain their complete value shape when used as whole values. Original relationship kinds and cardinalities are retained for relevant relations. Types used only by name carry a comment explaining that this use case does not inspect their members.

Euphoria's shared vocabulary has been copied selectively into each of its use cases, its vocabulary-import lines removed, and its shared model file deleted. Fourteen README indexes in active UC/API directories have been deleted. Package links to the removed artifacts have been updated. Historical source archives and their provenance READMEs are preserved.

## Verification

```text
python scripts/localize_uc_models.py --verify
```

The check passes for all 150 use cases. The [audit manifest](report.json) records each document's hash with the UML replaced by a placeholder, so changes to any Business Rule or behavior section fail verification. It also records each final UML hash, removed artifacts, navigation updates, and hashes for preserved project files and all excluded 100ms files. Explicit OCL classifiers, static operations, enum literals, and UML signature types are checked against each local diagram.

The projection resolves navigation and iterator types within each OCL context. Ambiguous navigation is retained conservatively on reachable classifiers; the manifest lists those member names per use case. This is a structural dependency and preservation check, not execution of the OCL rules or a proof of their domain semantics.

## Existing validation contracts

The repository's old `validate_specs.ps1` was run for all eight processed projects, with DBML compilation skipped because persistence artifacts were not changed. It fails on the current Tripma headings, `~~~` fences, and local flow identifiers. Tripma itself also lacks the manifest/layout expected by that validator. The repository-wide validator stops on the excluded 100ms package's pre-existing shared model and format requirements. The [legacy validation results](legacy-validation.json) record actual nonzero exit codes and diagnostic examples. These checks are not reported as passing.

The older Tripma presentation audit preserves every UML block and index byte from its original migration baseline. Those guarantees are superseded by this explicitly requested update; its historical baseline has not been rewritten.
