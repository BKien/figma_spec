# Use-Case Coverage Report

This report compares the specification package with the supplied Figma Community resource and its creator-linked public prototype video. Node IDs are recorded when they were visible in prototype URLs; other evidence is identified by visible screen text.

| Candidate ID | Actor goal | Figma evidence | Variant evidence | Status | Gap |
| --- | --- | --- | --- | --- | --- |
| UC-01 | Register an account | `Create Account` form | Desktop | Supported | Success navigation is demonstrated as the prototype continues into the product. |
| UC-02 | Log in | `Log In` form and authenticated home | Desktop | Supported | Error variants are not shown and remain policy assumptions. |
| UC-03 | View the home page | `Wander Without Limits`; destination, stay, review and `Your Next Trip` sections | Desktop and mobile | Supported | Exact canvas inventory is unavailable. |
| UC-04 | Search for stays | Location, dates, rooms and guest controls | Desktop and mobile | Supported | Error variants are not shown. |
| UC-05 | View stay results | Stay result cards and `Load more` | Desktop and mobile | Supported | Empty state is not shown. |
| UC-06 | Filter and sort stay results | Filter sidebar and `Our top picks` sort | Desktop and mobile | Supported | Every hidden sort option is not observable. |
| UC-07 | View stay details | `Hotel Southern - Galle`, gallery, rating, amenities and Reserve action | Desktop and mobile | Supported | Optional unavailable sections are not shown. |
| UC-08 | Book a stay | Node `2002:2197`; checkout stepper, guest/contact/address/card fields, save-card and `Book now` | Desktop and mobile | Partial | Checkout and submission are visible; a post-submit success or failure screen is not demonstrated. The contract therefore keeps the returned presentation generic. |
| UC-09 | Search for Taxi rentals | Node `182:821`; one location, pick-up, drop-off and passengers | Desktop and mobile | Supported | Product label is `Taxi`; interaction is a timed vehicle-and-driver rental rather than a point-to-point route. |
| UC-10 | View Taxi rental results | Node `187:1505`; car cards with seats, transmission, bags, mileage and price | Desktop and mobile | Supported | Empty state is not shown. |
| UC-11 | Filter and sort Taxi rental results | Car category, pick-up deposit, electric cars and `Our top picks` | Desktop and mobile | Supported | Additional sort-menu values are not observable and are not specified. |
| UC-12 | View Taxi rental and driver details | `Bajaj Details`; driver name, registration, phone, vehicle facts, period and price | Mobile; desktop checkout summary | Supported | Optional section absence is not shown. |
| UC-13 | Book a Taxi rental | Nodes `189:2050` and `4084:2364`; reservation form, pay-driver copy, confirmation action, driver follow-up and SMS text | Desktop and mobile | Supported | Failure and retry visuals are not shown. |
| UC-14 | Search for flights | Origin, destination, depart/return dates and passengers | Desktop | Supported | Error variants are not shown. |
| UC-15 | View, filter and sort flight results | Booking-site, duration and price filters; Cheapest, Best and Quickest tabs | Desktop | Supported | No flight purchase flow is demonstrated. |
| UC-16 | Browse budget trips | Budget destination grid and `See More` | Desktop and mobile | Supported | Empty state is not shown. |
| UC-17 | View budget-trip details | `Journey to Jaffna`, article, gallery, rating and Trip Master contact | Desktop and mobile | Supported | Share, translate and save outcomes are not demonstrated. |
| UC-18 | View traveller reviews | Home review section and dedicated Reviews page | Desktop | Supported | Search-result and empty-state outcomes are not demonstrated. |
| C-19 | View a flight-offer detail | `View Deal` action only | No complete detail screen | Partial | Trigger is visible but the detail outcome is absent. |
| C-20 | Book a flight | No flight checkout or confirmation screen | None | Missing | Purchase interaction is absent. |
| C-21 | Manage saved items | `Saved` bottom-navigation label and favourite icons | Mobile and content cards | Partial | No Saved page or save/remove outcome is demonstrated. |
| C-22 | Manage bookings or itinerary | `Bookings` bottom-navigation label and `Your Next Trip` notification | Mobile navigation and desktop notification | Partial | No bookings list or itinerary-management screen is demonstrated. |
| C-23 | Use Help Centre | `Help Centre`, 24/7 support and Trip Master contact entry points | Mobile and trip detail | Partial | No support workflow or result screen is demonstrated. |
| C-24 | Share or translate a budget trip | Share and `Translate to Sinhala` actions | Desktop trip detail | Partial | No resulting state is demonstrated. |
