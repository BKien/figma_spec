# Euphoria Ecommerce Apparels — Functional Specification

An English specification package for the user-supplied Euphoria Figma copy, audited on 2026-09-24. It contains 18 supported use cases with 138 OCL business rules (7-11 per use case), 13 proposed API contracts, UML/OCL domain models, a DBML persistence schema, and node-level source traceability.

## Read first

1. [Scope and coverage](coverage-report.md): supported goals, partial/missing flows, and design discrepancies.
2. [Use cases](uc/README.md): observable activities and isolated domain constraints.
3. [API contracts](api/README.md): sequential wire contracts and reusable object definitions.
4. [Domain glossary](CONTEXT.md), [shared UML model](uc/shared-domain-model.md), and [database schema](schema.dbml).
5. [Assumptions](ASSUMPTIONS.md), [Figma source manifest](FIGMA.md), and [validation report](validation-report.md).

## Authoring requirements

Each use case contains at least seven distinct OCL business rules. Trigger, precondition, postcondition, basic-flow, alternative-flow and exception-flow prose describe observable interaction only. Rule identifiers, rule names, predicates, thresholds and policy explanations are isolated from those sections. The consistency checker enforces the count and scans for policy leakage; semantic review complements the scan.

## Functional boundary

Covered: storefront discovery; category browsing, filtering and sorting; product details; cart review; checkout review and COD order placement using the billing address for shipping; reset-email request and resend; contact details and address-book viewing; address creation; wishlist and recently viewed products; order history, status filtering, and order detail.

Partial flows are explicitly separated in the coverage report. This is not an implementation specification for authentication completion, card/PayPal processing, cart mutations, wishlist mutations, refunds, or mobile screens.

## Design fidelity

The audit obtained the Webpage hierarchy containing 20 desktop frames. Checkout and Add Address fields were additionally read from the browser canvas. Styleguide details, instance overrides, and prototype wiring were not fully accessible after the Figma connector reached its plan limit. Every policy is a labeled assumption; static sample prices and contradictory totals are not treated as business rules.

## Repository isolation

This directory is the sole specification boundary for file `WcpUgAYaQJA4J00rMaMgj8`. It uses no screen, API, or rule from the repository's other Figma packages. The original Community listing is provenance only. The source Figma file was not edited.
