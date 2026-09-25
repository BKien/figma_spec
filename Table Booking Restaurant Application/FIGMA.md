# Figma Source Manifest

- **Package:** Table Booking Restaurant Application
- **Product scope:** Customer restaurant discovery and table booking on web/mobile, plus restaurant management and super-admin views. The customer and admin boundary was confirmed by the requester on 2026-09-24.
- **Figma file:** Table Booking Restaurant Application (Web + Mobile + Admin Panels) (Community) (Copy)
- **File key:** `BKc1SojjRCQwSPPzZpvDn2`
- **Source URL:** https://www.figma.com/design/BKc1SojjRCQwSPPzZpvDn2/Table-Booking-Restaurant-Application--Web---Mobile---Admin-Panels---Community---Copy-?node-id=38-14
- **Entry node:** `38:14`; this is a file entry point, not the sole product boundary.
- **Audit date:** 2026-09-24
- **Specification contract:** `self-contained-uml-v1`

## Inspected pages

The browser-accessible Figma layer tree exposed these pages: Styles, Wireframes, UI WEB, web v2, renewed, Components, UI MOBILE, UI Mobile V2, and Page 5. The product audit focused on the named screens and states under UI WEB and UI Mobile V2, with booking-state support from Components and search-state support from Wireframes. Styles and generic components were excluded as independent goals. The other variant pages were checked for duplicate or exploratory frames.

## Evidence method and limit

The Figma MCP connector returned a Starter-plan call-limit response. Read-only inspection continued in the Figma browser interface. Node IDs in the use-case files were read from the layer tree; screen labels and visible relationships were also inspected on the canvas. Figma did not expose hidden product policies, backend behavior, or complete field constraints. Such choices are recorded as assumptions and isolated in OCL. Some top-level page identifiers and dimensions could not be reliably captured through this route, so they are not asserted here.

The mobile history cancellation prompt at node `4611:4710` explicitly states that used points are not refunded. That visible policy is marked as Figma-sourced in UC-11.
