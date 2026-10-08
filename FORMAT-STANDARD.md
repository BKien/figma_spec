# Specification Presentation Standard

## Current naming and completion rules — 2026-10-07

The user-supplied directory D:/000-template/template/ and the explicit corrections on 2026-10-07 govern the active UC/API specifications. The previous migration notes below describe historical snapshots and do not override these corrections.

- UC IDs use UC-NN and filenames use uc-NN-function-name.md. Existing use-case numbering and descriptive filenames remain valid.
- API IDs use API-RESOURCE-OPERATION. Each API filename is exactly its uppercase ID plus .md. Generic API-UC-NN-NN identifiers are replaced with descriptive operation names; separate existing contracts for the same HTTP operation retain distinct names reflecting their use-case context.
- BR IDs use BR-SHORT-USE-CASE-NAME-NN, with a gap-free local sequence. Existing descriptive Tripma names and three-digit sequences remain valid. Constraint identifiers use the same words joined with underscores.
- Inline backtick delimiters are removed from active specification values and prose. Markdown block fences remain, as shown in the supplied utility example.
- UML uses a plantuml block. Business Rules use text blocks with a bare BR ID and rule name, followed by source metadata and the OCL expressions. Prose bullet prefixes and the dash prefixes of BR metadata are removed; UML relationships and mathematical operators retain their meaning.
- All formerly unspecified fields receive context-based values. Existing known wire schemas and business expressions remain authoritative. Trigger states when a field is sent or returned; Note describes its transport meaning, or None when no extra note applies. Existing format values remain; missing header formats are specified according to the header.
- An entirely client-local UC with no API has exactly None in Related API IDs. Any explanatory sentence belongs in Notes.
- Each OCL-UTILITY-DEFINITIONS.md uses only artifact_type: ocl-utility-definitions and status: Frozen in frontmatter. Its body contains a text block of domain-specific function signatures and descriptions, explanatory prose, and a Utility Classes section with a second text block. The 100ms definitions follow the user's supplied content; other products keep their own utilities and domain semantics.

Source archives and persistence schemas are preserved. Identifier aliases and filename changes are applied to active specifications and supporting Markdown links. The audit baseline captures the pre-correction working tree, including earlier uncommitted edits.

Verify the current format, resolved metadata, links, bidirectional UC/API associations, and preservation of the formal expressions with:

~~~text
python scripts/verify_template_completion.py
~~~

See format-audit/template-completion/REPORT.md for results and format-audit/template-completion/naming-plan.json for the complete scoped identifier mapping. Earlier preservation audits apply to their recorded historical baselines; their placeholder values and old names are superseded by this update.

## Historical supplied-template migration — 2026-10-07

The UC and API templates in the user-supplied `D:/000-template/template.zip` now govern all 411 active specifications in the nine project packages, including Tripma. This update supersedes the historical Draft status and unanchored branch numbering described below.

All UC/API frontmatter uses `status: Frozen`; existing identities, names and single or multiple related UC associations are retained. Use cases follow the template's Functional Use-Case Specification hierarchy, include Notes, and retain the separate UML Model and Business Rules sections. Each alternative and exception flow has a title and activities labeled with its Basic Flow step and increasing letters, such as `5a:`, `5b:`. Previously unanchored flows use the editorial mappings and reasons saved in the [branch mapping A](format-audit/template-format/branch-map-a.json) and [branch mapping B](format-audit/template-format/branch-map-b.json). Activity wording and existing anchored branch titles remain unchanged.

API contracts follow General Information, Request Header(s), Path Parameter(s), Query Parameter(s), Request Body, the existing success/error response sections, and Notes. Headers use `headers.` field names; path and query fields use `path.` and `query.`. Type, applicable Format, Required and Nullable share one metadata line. Trigger, Description and Example appear on separate lines; header and error fields also include Note. Missing template metadata reads `Not specified.`. Existing values, defaults, validation statements, public enums, examples, statuses and other notes remain authoritative. The template's sample HTTP outcomes do not introduce additional responses into an existing endpoint.

The eight existing OCL utility documents begin with exactly these two frontmatter fields, matching the two-row metadata preview in the supplied image:

```yaml
artifact_type: ocl-utility-definitions
status: Frozen
```

Additional source provenance is retained in each document's Source Metadata section. Existing UML and Business Rule code languages and bodies, utilities, schemas, source archives, shared contracts and supporting documents are preserved.

The [current template audit](format-audit/template-format/REPORT.md) records the baseline and preservation checks. Re-run the current check with:

```text
python scripts/format_from_template.py --verify
```

## Historical Tripma presentation migration

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
