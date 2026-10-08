# Supplied template formatting — 2026-10-07

Status: PASS for the current presentation and preservation audit.

The user-supplied `D:/000-template/template.zip` contains one UC template and one API template. Its SHA-256 is recorded in [manifest.json](manifest.json). The supplied OCL image shows the rendered two-field YAML metadata table: `artifact_type: ocl-utility-definitions`, `status: Frozen`.

| Package | UC | API | OCL utilities |
| --- | ---: | ---: | ---: |
| 100ms Video Conferencing and Live Streaming | 18 | 15 | 1 |
| Clicon Ecommerce Marketplace | 20 | 49 | 1 |
| DH Dental Recruitment | 20 | 42 | 1 |
| EdTech Education Dashboard | 20 | 50 | 1 |
| Euphoria Ecommerce Apparels | 18 | 13 | 1 |
| Financial Management | 18 | 18 | 1 |
| Table Booking Restaurant Application | 20 | 24 | 1 |
| Travel Booking App Web & Mobile | 18 | 16 | 1 |
| Tripma | 16 | 16 | 0 |
| Total | 168 | 243 | 8 |

## Presentation changes

- All 411 active UC/API specifications use Frozen frontmatter and the supplied hierarchy.
- Seventeen use cases gain a Notes section reading `None.` where there was no source note.
- All 468 branch flows have titles and lettered activity labels. The 359 previously unanchored branches are mapped to an existing Basic Flow step in [branch-map-a.json](branch-map-a.json) and [branch-map-b.json](branch-map-b.json). Each mapping records the reason; the titles and anchors organize existing activities without changing their text. Existing Tripma branch titles and anchor/letter identities are preserved.
- All 3,036 API fields follow the template's combined core metadata line and sequential supplementary labels. Header/path/query names carry their transport namespace. Missing labels explicitly read `Not specified.`; no examples, triggers or other missing values are inferred.
- Two Tripma APIs gain the previously omitted empty Path Parameter(s) section. Existing Query Parameter(s) sections and all HTTP outcomes are retained, including outcomes beyond the template's examples.
- Eight existing OCL utility documents have exactly the screenshot's two header fields and the OCL Utility Definitions title. Seven retain their four additional provenance fields in a Source Metadata section; Financial Management gains the header and standard title.

## Preservation verification

The [pre-change archive](before.zip) captures all 584 existing files in the nine packages. The [manifest](manifest.json) records their original hashes and the final hashes of all 419 formatted documents. This baseline is not replaced when formatting is repeated.

The dedicated audit passes for all 419 formatted documents and confirms:

- every original behavior activity and functional section remains present;
- every API field name, value, requiredness, nullability, public enum, example and response status is retained;
- UC/API identity metadata is unchanged apart from the requested status;
- all 1,395 UML/Business Rule code blocks retain their language and exact body bytes;
- every OCL utility definition and source provenance value is preserved; the Financial Management title is standardized;
- all 165 protected supporting files, source files, schemas, common contracts and existing shared models remain byte-identical;
- reference targets are unchanged, with no missing local targets in the formatted documents.

Run from the repository root:

```text
python scripts/format_from_template.py --verify
```

The machine-readable result is [verification.json](verification.json). Verification checks the formatting and preservation requested here; it does not execute OCL or assert new domain or database validation. Earlier Tripma/local-UML audits retain their historical baselines and requirements. The legacy skill validators require a different heading, fence and behavior-ID format and are not the authority for the supplied template.

The existing `validate_specs.ps1` was also run against all eight packages with FIGMA.md, and `validate_repository.ps1` against the repository, with DBML compilation skipped because schemas are unchanged. All nine runs returned exit code 1: these validators require em-dash titles, backtick fences and the previous namespaced behavior IDs, whereas the supplied template uses colon titles, tilde fences and local IDs. The 100ms shared model and missing contract markers are additional pre-existing failures. Those results are not reported as passing. Tripma has no FIGMA.md and retains its supplied directory layout.
