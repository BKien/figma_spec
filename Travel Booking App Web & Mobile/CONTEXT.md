# Travel Booking Context

This context describes the language shared by authentication, travel discovery, quoting, and booking specifications.

## Language

**Traveller**:
A person who searches travel inventory and may create a booking after authentication.
_Avoid_: Customer, passenger, user when referring to travel intent

**User**:
An identity registered with the application and capable of owning sessions and bookings.
_Avoid_: Account, traveller when referring only to authentication

**Offer**:
A provider-backed, time-sensitive representation of available travel inventory and its current price.
_Avoid_: Product, booking, quote

**Quote**:
A short-lived revalidation of one offer for one authenticated user before booking creation.
_Avoid_: Offer, reservation, price estimate

**Booking**:
A persisted request by an authenticated user to reserve a quoted stay or Taxi vehicle-and-driver rental.
_Avoid_: Offer, quote, order

**Stay**:
A bookable accommodation property displayed by the application.
_Avoid_: Hotel when referring to every accommodation type

**Stay Offer**:
An offer for a stay, date range, occupancy, and room quantity.
_Avoid_: Stay, room, stay booking

**Taxi Rental Offer**:
An offer for one vehicle and driver at one rental location between a pick-up time and a drop-off time. It includes capacity, vehicle characteristics, mileage allowance, deposit, and price. The Figma navigation label for this service is `Taxi`.
_Avoid_: Point-to-point route, ride-hail trip, destination transfer

**Flight Offer**:
A provider-backed itinerary returned by flight search. It is not bookable in the current scope.
_Avoid_: Flight booking, ticket

**Budget Trip**:
Editorial destination content with an indicative starting price.
_Avoid_: Package booking, flight offer

**Published Review**:
A traveller review approved for public display.
_Avoid_: Testimonial when referring to the persisted domain concept

