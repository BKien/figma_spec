# Domain Context

## Actors

- **Visitor:** A person browsing public restaurant content.
- **Customer:** A signed-in person who books and manages their own reservations.
- **Restaurant Manager:** An administrator assigned to a restaurant.
- **Super Admin:** An administrator with product-wide management access.

## Canonical terms

- **Restaurant:** A venue profile with address, menu, and reservation options.
- **Dining Table:** A physical table shown in the restaurant layout.
- **Reservation Slot:** A restaurant-specific date and start time with available seating capacity. It is an availability option, not a booking.
- **Booking:** A persisted customer reservation linked to a restaurant and slot. Its state is `CONFIRMED`, `CANCELLED`, or `COMPLETED`.
- **Points Used:** Loyalty points recorded against a booking. The cancellation prompt refers to these points.
- **Verification Challenge:** A code challenge used by the registration and booking confirmation views.
- **Account:** A customer, manager, or super-admin identity.
- **Session:** An authenticated access session.
- **Notification:** A message addressed to one account, optionally linked to a booking.
- **Contact Message:** A submitted message from the Contact Us form.
- **Report:** A derived view of bookings for a restaurant and period, not a separately edited record.

## Scope distinction

The UI depicts restaurant cards, slots, bookings, history, and admin lists. It does not depict a monetary offer, price quote, payment checkout, or payment provider. Therefore this package does not invent Offer or Quote entities. A selected slot is rechecked when creating a Booking.

## Source vocabulary

Labels such as `Conatct Us Page`, `registeration Otp`, and repeated `single restaurant view page` are preserved in evidence references. The specification uses normalized English terms while retaining the source node IDs.
