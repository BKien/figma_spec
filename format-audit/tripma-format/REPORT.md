# Tripma Format Migration — Preservation Report

Date: 2026-09-30, Asia/Saigon.

Result: **PASS**. All 152 active use cases and 227 active API contracts across eight projects use the [Tripma presentation standard](../../FORMAT-STANDARD.md). Their original substantive content is preserved in full.

## Coverage

| Project | Use cases | API contracts |
| --- | ---: | ---: |
| 100ms Video Conferencing and Live Streaming | 18 | 15 |
| Clicon Ecommerce Marketplace | 20 | 49 |
| DH Dental Recruitment | 20 | 42 |
| EdTech Education Dashboard | 20 | 50 |
| Euphoria Ecommerce Apparels | 18 | 13 |
| Financial Management | 18 | 18 |
| Table Booking Restaurant Application | 20 | 24 |
| Travel Booking App Web & Mobile | 18 | 16 |
| **Total** | **152** | **227** |

Tripma is the reference and remains unchanged.

## Presentation changes

- Adopted Tripma metadata and colon-separated specification titles.
- Grouped use-case information under Functional Use-Case Specification and placed Related UI, Related API IDs, and Notes ahead of the top-level UML Model and Business Rules sections.
- Adopted Tripma's section labels and local `PRE-1`, `POST-1`, `AF-1`, `EF-1` naming. Trigger text is displayed without an identifier; all original trigger and flow identifiers remain recoverable in the alias mapping.
- Grouped API identity, method, path, description, authentication, and authorization under General Information.
- Applied Tripma's request-section labels, field headings, sequential metadata labels, and tilde code fences.

Original activity numbering is retained where a source does not specify a Basic Flow branching point. No branch title, branch anchor, requirement, policy, or missing behavior was inferred. Existing UC/API/BR identities, API filenames, project paths, and links remain unchanged.

## Preservation evidence

| Check | Result |
| --- | --- |
| Independent comparison of every original UC/API section | PASS: all original text, activities, field metadata, examples, and references retained |
| Code fence language and body comparison | PASS: all 1,380 code blocks retained exactly, apart from fence delimiter presentation |
| Business Rules | PASS: all 1,211 existing rule definitions retained |
| Other package files | PASS: all 220 files byte-for-byte unchanged, including all 33 Tripma files |
| Source files, schemas, utilities, and evidence | PASS: unchanged SHA-256 hashes |
| Identifier mapping | PASS: 857 previous identifiers mapped to their local identifier or trigger section |
| Relative links in rewritten specifications | PASS: no new missing relative targets |
| Original and formatted file hashes | PASS |
| Expected Tripma document layout | PASS |

The baseline is the workspace state immediately before this migration, including all pre-existing uncommitted changes. Preservation was not compared against an older Git commit.

The content comparison ignores only explicitly permitted presentation changes: document hierarchy, section ordering and spelling, identifier aliases, metadata bullet markers, field-heading backticks, blank lines outside code, and fence delimiters. It preserves all code-body whitespace and checks code blocks separately. The new metadata repeats document identity and adopts Tripma's Draft presentation. It does not replace any original requirement or lifecycle statement.

The audit was also challenged with four deliberate in-memory changes: a changed requirement, a missing branch activity, a changed OCL expression, and a missing UML declaration. Every change was detected. No package file was altered by these negative checks.

## Audit artifacts

- [Complete original package snapshot](before.zip): all 599 original files, stored before any specification was written.
- [SHA-256 manifest and identifier aliases](manifest.json).
- [Readable identifier mapping](id-mapping.csv): specification path, original identifier, new local identifier or trigger locator.
- [Verification results](verification.json).
- [Formatter and preservation checker](../../scripts/format_tripma.py).

To re-run verification from the repository root:

```text
python scripts/format_tripma.py --verify
```

This result confirms presentation consistency and content preservation. It does not assert a new Figma audit or re-evaluate the existing domain policies and assumptions.
