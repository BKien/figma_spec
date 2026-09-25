# Figma Coverage Report

The requester selected the combined customer and administration boundary on 2026-09-24. Each selected row represents a distinct actor goal, not a responsive variant or a component.

| Candidate ID | Actor goal | Figma node IDs | Desktop/mobile evidence | Status | Gap |
| --- | --- | --- | --- | --- | --- |
| UC-01 | Visitor: Register an Account | 339:1015, 2178:2751, 395:748 | Web | Supported | None for the visible interaction boundary. |
| UC-02 | Customer: Sign In | 394:488, 2178:2715 | Web | Supported | None for the visible interaction boundary. |
| UC-03 | Visitor: Browse the Restaurant Home Page | 102:170, 278:790, 173:362 | Web | Supported | None for the visible interaction boundary. |
| UC-04 | Visitor: Search Restaurants | 102:170, 12:299 | Web and wireframe | Supported | None for the visible interaction boundary. |
| UC-05 | Visitor: View Restaurant Details | 88:41, 4594:4056 | Web and mobile | Supported | None for the visible interaction boundary. |
| UC-06 | Visitor: View a Restaurant Menu | 321:429, 88:41 | Web | Supported | None for the visible interaction boundary. |
| UC-07 | Customer: Check Table Availability | 772:1137, 772:1139, 772:1127, 88:41, 4611:4460 | Web, mobile, and components | Supported | None for the visible interaction boundary. |
| UC-08 | Customer: Book a Table | 295:495, 2383:2998, 772:1193 | Web and components | Supported | None for the visible interaction boundary. |
| UC-09 | Customer: View Booking History | 4611:4772, 772:1244, 772:1245, 772:1246 | Mobile and components | Supported | None for the visible interaction boundary. |
| UC-10 | Customer: Change a Booking | 3890:2970, 4611:4659 | Web and mobile | Supported | None for the visible interaction boundary. |
| UC-11 | Customer: Cancel a Booking | 772:1196, 772:1245, 4611:4772, 4611:4710 | Mobile and components | Supported | None for the visible interaction boundary. |
| UC-12 | Customer: View Notifications | 4611:4549, 4594:4145 | Mobile | Supported | None for the visible interaction boundary. |
| UC-13 | Customer: View Profile | 4611:5055, 770:1085 | Mobile and components | Supported | None for the visible interaction boundary. |
| UC-14 | Visitor: Contact Support | 2345:2682, 2375:2627 | Web and mobile | Supported | None for the visible interaction boundary. |
| UC-15 | Restaurant Manager: View Admin Bookings | 1000:2063, 1000:4522 | Admin web | Supported | None for the visible interaction boundary. |
| UC-16 | Restaurant Manager: Update a Booking as Admin | 3769:3135, 1000:2063 | Admin web | Supported | None for the visible interaction boundary. |
| UC-17 | Restaurant Manager: View Table Layout | 3387:3558, 4657:6383 | Admin web | Supported | None for the visible interaction boundary. |
| UC-18 | Super Admin: Manage Restaurants | 1000:3691, 1000:4522 | Admin web | Supported | None for the visible interaction boundary. |
| UC-19 | Super Admin: Manage Users | 1016:4816, 1000:4208 | Admin web | Supported | None for the visible interaction boundary. |
| UC-20 | Restaurant Manager: View Reports | 1913:2633, 1000:1746 | Admin web | Supported | None for the visible interaction boundary. |

## Supported candidates outside the selected 20-goal boundary

| Candidate | Evidence | Disposition |
| --- | --- | --- |
| Manage restaurant opening times | `3387:2714` restaurant timings | Excluded to keep the approved combined scope at 20 goals. |
| Manage restaurant managers | `1843:2600` Manager Edit / add | Excluded to keep the approved combined scope at 20 goals. |
| View privacy policy | `4354:2976` Privacy policy | Informational content outside the operational boundary. |

## Partial and missing flows

| Candidate | Evidence | Status | Gap |
| --- | --- | --- | --- |
| Recover account access | Login states | Partial | No complete recovery outcome was observed. |
| Pay for a reservation | No payment screen in the audited boundary | Missing | No checkout or payment outcome is shown. |
| Post a restaurant review | Restaurant detail screens | Missing | No review submission screen or outcome was observed. |

## Evidence quality

The Figma MCP call limit prevented direct metadata export. The browser layer tree supplied the referenced node IDs and canvas inspection confirmed the main web/admin groupings. The source does not define internal policies; all policy assumptions are listed in [ASSUMPTIONS.md](ASSUMPTIONS.md).
