---
artifact_type: ocl-utility-definitions
status: Frozen
---

# OCL Utility Definitions

```text
String.trim(): String
- Removes leading and trailing whitespace; internal whitespace is unchanged.
- Applied to actorId, requestId, payload, and executionId before nonblank checks.

DateTime::now(): DateTime
- Returns the server transaction-clock instant captured once for the education operation.
- The value is a UTC instant with millisecond precision; repeated calls in the same operation return the same value.
```

UseCaseService::execute is the operation constrained by the BRs, not a utility function. OCL standard operations such as size and allInstances are outside this catalog.

## Utility Classes

```text
class String <<Primitive>> {
  +trim(): String
}

class DateTime <<Primitive>> {
  +now(): DateTime
}

```
