# Figma Audit

## Purpose

Determine what the design actually supports before naming use cases or APIs. The count of frames is not the count of use cases.

## Evidence collection

1. Use the Figma connector in read-only mode.
2. Record the Figma file name, URL, file key, inspected pages, and audit date in the package-local `FIGMA.md`.
3. List every top-level page before inspecting nodes.
4. For each page, collect top-level node ID, name, type, visibility, size, and parent relationship.
5. Drill into likely product screens and extract visible text, inputs, controls, actions, navigation, and embedded states.
6. Request screenshots for nodes whose names do not establish their purpose. A frame named `details` may still be a result list.
7. Identify mobile/desktop variants without counting them as separate user goals.

## Classification

Classify each candidate user goal:

- **Supported**: the design contains enough observable UI to specify the trigger, interaction boundary, and outcome.
- **Partial**: the design begins the goal but lacks a required outcome or continuation.
- **Missing**: the goal is named or implied but has no usable product screen.

Do not promote components, date pickers, search bars, cards, navigation, notifications, or decorative groups into standalone use cases unless they represent an independent actor goal.

## Scope matrix

Record at least:

| Candidate ID | Actor goal | Figma node IDs | Desktop/mobile evidence | Status | Gap |
| --- | --- | --- | --- | --- | --- |

Create UC specifications only from `Supported` rows. Report `Partial` and `Missing` rows in `coverage-report.md` unless the user asks to include planned behavior.

## Scope cardinality

A completed specification package contains 18–20 supported actor-goal use cases.

- When the audit produces fewer than 18 supported goals, inspect nested states, overlays, and distinct outcomes again. If the evidence still supports fewer than 18, record the shortfall in `coverage-report.md`, request the missing evidence or explicit authorization for planned behavior, and leave the package incomplete.
- When the audit produces more than 20 supported goals, select a user-approved product boundary or combine only variants that deliver the same actor goal. Record supported candidates excluded from the selected boundary in `coverage-report.md`.
- Preserve evidence quality while meeting the range. A component, control, responsive variant, or decorative frame remains supporting evidence for a goal rather than becoming a standalone use case.

## Evidence boundary

Treat Figma as evidence for product interaction, not as a source of hidden policies, provider behavior, database constraints, security thresholds, or pricing formulas. Resolve those from user-provided sources or explicit assumptions.

Treat each Figma file as an independent evidence boundary. Do not reuse screens, node IDs, terminology, assumptions, APIs, or rules from another package unless the user explicitly identifies a shared source.
