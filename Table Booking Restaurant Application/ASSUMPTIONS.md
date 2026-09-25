# Assumptions Register

The design supplies screen structure and visible actions, but not backend rules. Every assumption below is implemented only by a separately identified OCL rule.

| ID | Assumption | Related use cases |
| --- | --- | --- |
| A-01 | Account email is canonicalized and unique; credentials are stored as hashes; registration becomes active after code verification. | UC-01, UC-02 |
| A-02 | Public discovery exposes published restaurants and visible menu items. Displayed restaurant names, cities, addresses, timezones, ratings, and imagery are complete; ratings range from 0 to 5. Visible menu items have a name, section, and image. | UC-03–UC-06 |
| A-03 | Reservation dates cannot precede the service date; offered slots start in the future, have enough remaining seating, and never exceed their configured capacity. | UC-04, UC-07, UC-08, UC-10, UC-16 |
| A-04 | Booking confirmation uses a short-lived code challenge and records only its hash. | UC-08 |
| A-05 | Booking creation is keyed by a client-supplied idempotency key and atomically consumes slot capacity. | UC-08 |
| A-06 | Customers can read only their own bookings and change or cancel only future confirmed bookings; optimistic versions protect edits and cancellation. Cancellation preserves the owner, restaurant, and slot. | UC-09–UC-11 |
| A-07 | Notifications and profiles are account-scoped. Notification title, body, timestamp, and optional linked booking are valid for the recipient; profile name and canonical email reflect the account. | UC-12, UC-13 |
| A-08 | Contact submissions require a nonblank name, email, and message and are stored with an identifier and creation time. | UC-14 |
| A-09 | Managers may inspect and edit only assigned restaurant data; super admins may manage restaurants and users. Admin booking lists retain valid owner and slot references; restaurant tables have unique labels, positive capacity, and nonnegative layout coordinates. | UC-15–UC-19 |
| A-10 | Report totals are derived from bookings in the selected restaurant and period, remain nonnegative, and identify their source scope and period. | UC-20 |
| A-11 | The location control resolves to a city; cuisine and meal labels are searchable; restaurant timezone is derived from its address. | UC-04, UC-18 |
| A-12 | The rating shown on restaurant cards is a read-only catalog value; its calculation and review source are outside this package. | UC-04, UC-05 |
| A-13 | Sign-in requires supplied credentials and creates a session for the matching active account with a finite validity window. | UC-02 |
| A-14 | Collection results contain distinct records; displayed booking parties are positive, points are nonnegative, and event timestamps are not in the future. | UC-03, UC-06, UC-07, UC-09, UC-12, UC-15, UC-17 |
| A-15 | Restaurant search requires a location, cuisine, meal, date, and positive party size; the selected date is today or later. | UC-04 |
| A-16 | User edits require a nonblank display name and preserve the account email. | UC-19 |

No cancellation cutoff before the slot start, reservation duration, maximum party size, code lifetime, or message retention period is asserted from Figma. These require a product decision before implementation.
