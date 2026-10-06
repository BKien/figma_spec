# Product Source Manifest

- **Package:** Financial Management
- **Product scope:** Personal financial tracking: identity, manually tracked financial accounts, transaction history and entry, spending reports, upcoming bills, financial goals and savings comparisons.
- **Authoritative supplied source:** [Financial Management Specification](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit).
- **Spreadsheet title:** `[VibeTesting] Financial_Management_Specification`.
- **Spreadsheet ID:** `1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM`.
- **Inspected boundary:** Both tabs: `Use cases` (gid `0`, declared grid A1:X1080) and `API contract` (gid `439687549`, declared grid A1:Y993). Read in bounded row chunks; all returned cell values, including continuation rule rows, are preserved in `source/`.
- **Figma URL, file key, node IDs:** Not supplied. Figma-related remarks inside source cells are unverified source claims; no design audit was performed.
- **Audit date:** 2026-09-30, Asia/Saigon.
- **Specification contract:** `self-contained-uml-v1`.

This filename follows repository convention; the actual evidence is a Google spreadsheet. Do not treat this package as a live Figma audit. The supplied scope and permission to repair specifications support a reviewed product-source package. The 17 source use-case entries comprise 16 actor goals and one quick-edit variant. The normalized boundary contains 18 use cases; filter history is extracted from UC-03 and category selection is extracted from existing form/API evidence. Category detail presentation is explicitly proposed.

See [coverage](coverage-report.md), [review decisions](consistency-review.md), and [source preservation](source/README.md).
