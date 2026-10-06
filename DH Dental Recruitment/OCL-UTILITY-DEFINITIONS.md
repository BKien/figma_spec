---
artifact_type: ocl-utility-definitions
status: Frozen
source_spreadsheet_id: 1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM
source_sheet: "Use cases"
source_range: "A2:B2"
retrieved_at: 2026-09-28T15:29:00Z
---

# OCL Utility Definitions

> The spreadsheet row supplies the utility-definition format and the `trim` behavior. The project-specific inventory below is derived from `01-inception/uc/` Business Rules and their local UML. The spreadsheet does not define this project's clock. No additional semantics are implied.

```text
String.trim(): String
- Removes leading and trailing whitespace; internal whitespace is unchanged.
- Applied to actorId, requestId, payload, and executionId before nonblank checks.

DateTime::now(): DateTime
- Returns the current instant used by BR result-timestamp comparisons.
- The clock source, precision, and timezone are not specified by the BRs.
```

`UseCaseService::execute` is the operation constrained by the BRs, not a utility function. OCL standard operations such as `size` and `allInstances` are outside this catalog.

## Utility Classes

```text
class String <<Primitive>> {
  +trim(): String
}

class DateTime <<Primitive>> {
  +now(): DateTime
}

```
