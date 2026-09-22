# Figma Specification Repository

This repository stores multiple independent Figma-derived specification packages.

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
    ├── uc/
    └── api/
```

Each direct child directory other than `skills` is a self-contained specification package for one Figma file or one explicitly scoped Figma product.

## Packages

| Package | Description |
| --- | --- |
| [100ms Video Conferencing and Live Streaming](100ms%20Video%20Conferencing%20and%20Live%20Streaming/) | Desktop and mobile real-time video-conference and live-stream specification. |
| [Travel Booking App Web & Mobile](Travel%20Booking%20App%20Web%20%26%20Mobile/) | Web and mobile travel-booking product specification. |

## Shared Skill

The repository-level [figma-to-ocl-specs skill](skills/figma-to-ocl-specs/SKILL.md) defines package creation, use-case writing, rule isolation, validation, and multi-Figma repository conventions.
