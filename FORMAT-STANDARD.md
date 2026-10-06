# Tripma Specification Presentation Standard

Reference: the existing [Tripma use cases](Tripma/01-inception/use-cases/) and [Tripma API contracts](Tripma/01-inception/api-constracts/).

This standard governs document presentation. The existing content of every project remains authoritative: requirements, actors, conditions, activities, rule expressions, models, examples, references, and source evidence are preserved.

## Use-case presentation

Use Tripma's YAML metadata, `# UC-NN: Name` title, and section hierarchy:

1. `## Functional Use-Case Specification`
2. `### Use Case ID`
3. `### Use Case Name`
4. `### Description`
5. `### Actor(s)`
6. `### Priority`
7. `### Trigger`
8. `### Pre-Condition(s)`
9. `### Post-Condition(s)`
10. `### Basic Flow`
11. `### Alternative Flow`
12. `### Exception Flow`
13. `### Related UI`
14. `### Related API IDs`
15. `### Notes`, when present in the original
16. `## UML Model`
17. `## Business Rules`

Use local condition and branch identifiers, restarting within each use case and namespace: `PRE-1`, `POST-1`, `AF-1`, `EF-1`. Render conditions as `PRE-1: Original condition text` and branch labels as `AF-1:` or `EF-1:`. Present the trigger as its original text, as Tripma does. Record every previous identifier, including trigger identifiers, in the [identifier mapping](format-audit/tripma-format/id-mapping.csv), scoped by the specification path.

Preserve the Basic Flow's original activities and numbers. Preserve branch activities and their numbers whenever the original does not identify a Basic Flow branching step. Tripma's lettered references such as `13a` express a specific Basic Flow anchor; introducing such an anchor into an unanchored source would add information. Retain existing branch titles when available, and do not invent titles or branching points.

Use Tripma's `~~~` fence delimiters. Preserve each code block's original language and entire body. Existing OCL fences retain the `ocl` language; models retain `plantuml`. Business Rule IDs and expressions remain unchanged.

## API presentation

Use Tripma's YAML metadata and `# API-ID: Name` title. Group these original fields under `## General Information`, with each field as a level-three heading:

1. API ID
2. API Name
3. Related Use Case IDs
4. Method
5. Path
6. Description
7. Authentication
8. Authorization

Use `## Request Header(s)`, `## Path Parameter(s)`, `## Query Parameter(s)`, and `## Request Body`. Preserve every success response, error response, and note in its original order. Render individual fields as level-three headings and their metadata as sequential labels, preserving all original values, examples, wire types, requiredness, nullability, validations, and descriptions.

## Preservation and verification

Existing project folders, filenames, source archives, schema, utilities, indexes, generators, and reference targets remain at their current paths. This migration does not change the domain or regenerate specifications from a template. The metadata adopts Tripma's Draft presentation without rewriting any original lifecycle statements.

The [audit report](format-audit/tripma-format/REPORT.md) documents the completed migration. It includes a complete pre-change package snapshot, file hashes, identifier aliases, and a section-by-section preservation check. Existing documents describing the previous format remain preserved as historical material; this file describes the current presentation.

Re-run the dedicated presentation and preservation audit from the repository root:

```text
python scripts/format_tripma.py --verify
```

This audit validates the presentation migration and preservation of existing content. Domain-validation scripts that require the previous heading structure or namespaced flow codes have a different contract; their requirements are not used to rewrite or remove existing content during this migration.

## Local UML update — 2026-10-01

For all active specification packages except `100ms Video Conferencing and Live Streaming`, each use-case UML now contains only the vocabulary needed by that use case's own Business Rules: context operations, referenced members, enum definitions, and the types needed to close their signatures. Complete value objects remain available where rules use their whole values. A type used only in a signature is explicitly documented as opaque within that local diagram. Overlapping definitions are repeated locally; there is no shared model dependency.

README indexes in the active UC/API directories and the Euphoria shared model have been removed. Package navigation links now point to the specification directories. This requested update supersedes the earlier preservation requirement for UML blocks, those indexes, and references to them. Source archives, Business Rules, behavior sections, API contracts, and persistence artifacts remain preserved.

The earlier presentation audit remains a historical check of its original migration baseline. Verify the current local UML update with:

```text
python scripts/localize_uc_models.py --verify
```

See the [local UML audit](format-audit/local-uml/REPORT.md) for scope, preservation checks, and legacy-validator limitations.
