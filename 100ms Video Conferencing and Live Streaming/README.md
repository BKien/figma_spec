# 100ms Video Conferencing and Live Streaming Specifications

This package contains 18 supported use cases, their domain rules, 14 application API contracts, and a PostgreSQL persistence specification.

- [Source manifest](FIGMA.md)
- [Domain vocabulary and integration boundaries](CONTEXT.md)
- [Assumption register](ASSUMPTIONS.md)
- [Coverage](coverage-report.md)
- [Use cases](uc/README.md)
- [API contracts](api/README.md)
- [DBML schema](schema.dbml)
- [PostgreSQL persistence supplement](persistence.sql)
- [Review corrections and verification](RESOLUTION-2026-09-22.md)

## Persistence build

Compile schema.dbml with `dbml2sql schema.dbml --postgres -o schema.sql`, then apply the generated SQL followed by persistence.sql to a fresh PostgreSQL schema. The supplement supplies aggregate capacity enforcement and additional checks; compiling DBML alone does not include that supplement. This package describes a fresh schema, not a migration of an existing deployed database.

## Validation

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\skills\figma-to-ocl-specs\scripts\validate_specs.ps1 -Root '.\100ms Video Conferencing and Live Streaming'
powershell -NoProfile -ExecutionPolicy Bypass -File .\skills\figma-to-ocl-specs\scripts\validate_repository.ps1 -Root .
python '.\100ms Video Conferencing and Live Streaming\scripts\validate_contract.py'
```

The package check is targeted structural/model-reference validation, not a general-purpose OCL compiler. Database scenarios are available in [verify_schema.mjs](scripts/verify_schema.mjs). Pass the compiled PostgreSQL SQL path as its first argument. Install `@electric-sql/pglite` in an isolated working directory and pass the absolute path of its `dist/index.js` as the second argument, or make that package resolvable normally by Node.

```text
node scripts/verify_schema.mjs /path/to/schema.sql /path/to/node_modules/@electric-sql/pglite/dist/index.js
```
