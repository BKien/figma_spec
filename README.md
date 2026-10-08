# Figma Specification Repository

This repository stores independent specification packages derived from Figma designs or supplied product specifications.

Active specifications follow the supplied templates and the current [presentation and naming standard](FORMAT-STANDARD.md). Use-case files use uc-NN-function-name.md, API files use their descriptive uppercase API ID as the filename, and BR IDs use a shortened use-case name. The [template completion audit](format-audit/template-completion/REPORT.md) records the identifier mapping, completed metadata, and preservation checks.

## Repository Layout

```text
figma_spec/
├── README.md
├── skills/
│   └── figma-to-ocl-specs/
└── <Figma specification package>/
    ├── FIGMA.md
    ├── CONTEXT.md
    ├── ASSUMPTIONS.md
    ├── coverage-report.md
    ├── schema.dbml
    └── 01-inception/
        ├── uc/
        └── api/
```

Each direct child directory other than `skills` is a self-contained specification package for one Figma file or one explicitly scoped product source. Every package stores use-case and API contracts under `01-inception/`, and its DBML persistence specification targets MySQL.

## Packages

| Package | Description |
| --- | --- |
| [Euphoria Ecommerce Apparels](Euphoria%20Ecommerce%20Apparels/) | Apparel ecommerce specification: 18 use cases with 7-11 BRs each, 13 API contracts, UML/OCL and DBML; partial flows are recorded separately. |
| [100ms Video Conferencing and Live Streaming](100ms%20Video%20Conferencing%20and%20Live%20Streaming/) | Desktop and mobile real-time video-conference and live-stream specification. |
| [Travel Booking App Web & Mobile](Travel%20Booking%20App%20Web%20%26%20Mobile/) | Web and mobile travel-booking product specification. |
| [Table Booking Restaurant Application](Table%20Booking%20Restaurant%20Application/) | Restaurant discovery and table booking across customer and admin views; 20 use cases, UML/OCL, API contracts, and DBML. |
| [Clicon Ecommerce Marketplace](Clicon%20Ecommerce%20Marketplace/) | Ecommerce marketplace specification with 20 normalized use cases and all 22 supplied source specifications preserved with checksums. |
| [DH Dental Recruitment](DH%20Dental%20Recruitment/) | Dental recruitment specification with all 20 supplied use cases normalized and preserved. |
| [EdTech Education Dashboard](EdTech%20Education%20Dashboard/) | Student and instructor learning specification with 20 normalized use cases and all 21 supplied source specifications preserved with checksums. |
| [Financial Management](Financial%20Management/) | Personal financial tracking specification from the supplied Google spreadsheet: 18 use cases, 18 API contracts, local UML/OCL, MySQL DBML, preserved source and documented consistency repairs. |

## Shared Skill

The repository-level [figma-to-ocl-specs skill](skills/figma-to-ocl-specs/SKILL.md) defines package creation, use-case writing, rule isolation, validation, and multi-Figma repository conventions.
