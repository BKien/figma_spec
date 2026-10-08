---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-04
uc_name: "Select Seats"
---

# UC-04: Select Seats

## Functional Use-Case Specification

### Use Case ID

UC-04

### Use Case Name

Select Seats

### Description

As a visitor, I want to choose seats for my Tripma itinerary so that I can continue preparing my booking.

### Actor(s)

Visitor

### Priority

High

### Trigger

The visitor enters the Tripma seat-selection experience from the passenger-information step.

### Pre-Condition(s)

PRE-1: A prepared passenger-information context is available.

PRE-2: The related flight-selection context can be accessed.

### Post-Condition(s)

POST-1: When the selection is accepted, Tripma makes a completed seat-selection context available to the payment experience.

POST-2: Tripma preserves the preceding booking-workflow contexts.

POST-3: When the selection cannot be accepted, Tripma keeps the visitor in the seat-selection experience and reports the outcome.

### Basic Flow

1. Tripma opens the seat-selection experience for the current booking workflow.
2. Tripma requests seat information through API-SEATS-LIST.
3. The seat service evaluates the request according to the Business Rules of this use case.
4. The seat service returns the corresponding seat information.
5. Tripma presents the seat-selection controls.
6. The visitor chooses a seat.
7. Tripma updates the current selection according to the Business Rules.
8. Tripma presents any remaining seat-selection activity.
9. The visitor completes the remaining activity, when applicable.
10. Tripma evaluates the current seat-selection state according to the Business Rules.
11. The visitor chooses to continue.
12. Tripma completes the required continuation processing according to the Business Rules.
13. Tripma creates the completed seat-selection context.
14. Tripma opens the payment experience.

### Alternative Flow

AF-1: Change a seat choice

6a: The visitor chooses a different seat for the current selection position.

6b: Tripma updates the selection according to the Business Rules.

6c: The Basic Flow resumes at step 8.

AF-2: Confirm a prompted seat change

7a: Tripma presents a confirmation requested by the Business Rules.

7b: The visitor confirms the change.

7c: Tripma applies the pending selection.

7d: The Basic Flow resumes at step 8.

AF-3: Cancel a prompted seat change

7e: The visitor cancels the pending change.

7f: Tripma preserves the preceding selection.

7g: The Basic Flow resumes at step 8.

AF-4: Continue to another selection position

8a: The visitor moves to another position offered by the seat-selection experience.

8b: Tripma presents its current seat information.

8c: The Basic Flow resumes at step 6.

AF-5: Save and close the in-progress selection

10a: The visitor chooses Save and Close.

10b: Tripma processes the current state according to the Business Rules.

10c: The use case ends without entering the payment experience.

AF-6: Resume an in-progress selection

1a: Tripma finds a previously saved seat selection.

1b: Tripma evaluates and restores it according to the Business Rules.

1c: The Basic Flow resumes at step 2.

### Exception Flow

EF-1: No seat options returned

4a: If the service returns no seat options, Tripma presents an informational empty state.

4b: The visitor remains in the seat-selection experience.

EF-2: Current selection cannot be accepted

12a: If continuation processing rejects part of the current selection, Tripma identifies the affected position.

12b: Tripma keeps the visitor in the seat-selection experience and returns to step 5.

EF-3: Seat request cannot be completed

2a: If Tripma cannot complete an API-SEATS-LIST request, it presents a recoverable error state.

2b: Tripma does not open the payment experience.

EF-4: Selection is not ready to continue

10d: If the current state does not satisfy the Business Rules, Tripma identifies the incomplete selection activity.

10e: The continuation action remains unavailable.

EF-5: In-progress selection cannot be saved or restored

10f: If Tripma cannot process the in-progress selection, it preserves the current usable state and presents a recoverable outcome.

### Related UI

Seat-selection step of the booking page (/booking); seat map; seat-class information; selection details; confirmation overlay; Save and Close action; payment action

### Related API IDs

API-SEATS-LIST

### Notes

Scope clarification: This use case prepares the seat-selection context used by the next Tripma booking step.

## UML Model

~~~plantuml
@startuml
hide empty members

enum SeatClass {
  ECONOMY
  BUSINESS
}

enum FlightLeg {
  DEPARTING
  RETURNING
}

class Flight <<Entity>> {
  id: UUID [1]
}

class Seat <<Entity>> {
  id: UUID [1]
  available: Boolean [1]
}

class PassengerInfo <<Entity>> {
  id: UUID [1]
}

class SeatAssignment <<Entity>> {
  id: UUID [1]
}

class SeatDto <<DTO>> {
  id: UUID [1]
  flightId: UUID [1]
  seatClass: SeatClass [1]
  available: Boolean [1]
  price: Decimal [1]
  currency: String [1]
}

class SeatListDataDto <<DTO>> {
  flightId: UUID [1]
  currency: String [1]
  businessSeats: SeatDto [0..*]
  economySeats: SeatDto [0..*]
}

class SeatListResponseDto <<DTO>> {
  success: Boolean [1]
  data: SeatListDataDto [0..1]
}

class SeatSelectionInputContextDto <<DTO>> {
  passengerContextKey: String [1]
  selectionContextKey: String [1]
  passengerRefs: String [1..*]
  departingFlightId: UUID [1]
  returningFlightId: UUID [0..1]
  currency: String [1]
}

class SeatChoiceDto <<DTO>> {
  passengerRef: String [1]
  flightId: UUID [1]
  flightLeg: FlightLeg [1]
  seat: SeatDto [1]
  upgradeAmount: Decimal [1]
}

class PendingSeatUpgradeDto <<DTO>> {
  passengerRef: String [1]
  flightId: UUID [1]
  requestedSeat: SeatDto [1]
  upgradeAmount: Decimal [1]
  currency: String [1]
}

class SeatSelectionState <<State>> {
  inputContext: SeatSelectionInputContextDto [1]
  availableSeats: SeatListDataDto [1..*]
  choices: SeatChoiceDto [0..*]
  pendingUpgrade: PendingSeatUpgradeDto [0..1]
}

class SeatSelectionContextDto <<DTO>> {
  seatSelectionContextKey: String [1]
  passengerContextKey: String [1]
  selectionContextKey: String [1]
  choices: SeatChoiceDto [1..*]
  totalUpgradeAmount: Decimal [1]
  currency: String [1]
  preparedAt: DateTime [1]
}

class SavedSeatSelectionDto <<DTO>> {
  passengerContextKey: String [1]
  choices: SeatChoiceDto [0..*]
  savedAt: DateTime [1]
}

class SeatService <<Service>> {
  listAvailableSeats(flightId: UUID): SeatListResponseDto
  isSeatNumberAscending(seats: SeatDto [0..*]): Boolean {query}
}

class SeatSelectionService <<Service>> {
  selectSeat(state: SeatSelectionState, passengerRef: String, flightLeg: FlightLeg, seat: SeatDto): SeatSelectionState
  confirmUpgrade(state: SeatSelectionState): SeatSelectionState
  cancelUpgrade(state: SeatSelectionState): SeatSelectionState
  canContinue(state: SeatSelectionState): Boolean
  createContext(state: SeatSelectionState): SeatSelectionContextDto
  saveSelection(state: SeatSelectionState): SavedSeatSelectionDto
  restoreSelection(state: SeatSelectionState, saved: SavedSeatSelectionDto): SeatSelectionState
  hasCompleteSeatCoverage(state: SeatSelectionState): Boolean {query}
}

class Booking <<Entity>> {
  id: UUID [1]
}

SeatListDataDto "1" *-- "0..*" SeatDto : business seats
SeatListDataDto "1" *-- "0..*" SeatDto : economy seats
SeatListResponseDto "1" *-- "0..1" SeatListDataDto : data
SeatChoiceDto "1" *-- "1" SeatDto : selected seat
PendingSeatUpgradeDto "1" *-- "0..1" SeatDto : previous seat
PendingSeatUpgradeDto "1" *-- "1" SeatDto : requested seat
SeatSelectionState "1" *-- "1" SeatSelectionInputContextDto : uses
SeatSelectionState "1" *-- "1..*" SeatListDataDto : presents
SeatSelectionState "1" *-- "0..*" SeatChoiceDto : contains
SeatSelectionState "1" *-- "0..1" PendingSeatUpgradeDto : proposes
SeatSelectionContextDto "1" *-- "1..*" SeatChoiceDto : contains
SavedSeatSelectionDto "1" *-- "0..*" SeatChoiceDto : contains
SeatDto ..> Seat : maps from
SeatAssignment ..> SeatChoiceDto : later maps from
SeatService ..> SeatListResponseDto
SeatSelectionService ..> SeatSelectionState
SeatSelectionService ..> SeatSelectionContextDto
SeatSelectionService ..> SavedSeatSelectionDto
SeatDto --> "1" SeatClass : seatClass
SeatChoiceDto --> "1" FlightLeg : flightLeg

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-SEAT-001 - Listed seats belong to the requested flight
context SeatService::listAvailableSeats(
  flightId : UUID
) : SeatListResponseDto
post BR_SEAT_001_RequestedFlight:
  result.success implies
    result.data.flightId = flightId and
    result.data.businessSeats->forAll(seat | seat.flightId = flightId) and
    result.data.economySeats->forAll(seat | seat.flightId = flightId)


BR-SEAT-002 - Only available seats are listed
context SeatService::listAvailableSeats(
  flightId : UUID
) : SeatListResponseDto
post BR_SEAT_002_AvailableSeats:
  result.success implies
    result.data.businessSeats->forAll(seat | seat.available = true) and
    result.data.economySeats->forAll(seat | seat.available = true)


BR-SEAT-003 - Seats are grouped by class
context SeatService::listAvailableSeats(
  flightId : UUID
) : SeatListResponseDto
post BR_SEAT_003_SeatClasses:
  result.success implies
    result.data.businessSeats->forAll(seat |
      seat.seatClass = SeatClass::BUSINESS) and
    result.data.economySeats->forAll(seat |
      seat.seatClass = SeatClass::ECONOMY)


BR-SEAT-004 - Seats are ordered by seat number
context SeatService::listAvailableSeats(
  flightId : UUID
) : SeatListResponseDto
post BR_SEAT_004_AscendingOrder:
  result.success implies
    isSeatNumberAscending(result.data.businessSeats) and
    isSeatNumberAscending(result.data.economySeats)


BR-SEAT-005 - One choice per passenger and flight
context SeatSelectionService::selectSeat(
  state : SeatSelectionState,
  passengerRef : String,
  flightLeg : FlightLeg,
  seat : SeatDto
) : SeatSelectionState
post BR_SEAT_005_SingleChoice:
  not (
    seat.seatClass = SeatClass::BUSINESS and
    state.choices->exists(choice |
      choice.passengerRef = passengerRef and
      choice.flightId = seat.flightId and
      choice.seat.seatClass = SeatClass::ECONOMY and
      choice.seat.id <> seat.id)
  ) implies
    result.choices->one(choice |
      choice.passengerRef = passengerRef and
      choice.flightId = seat.flightId)


BR-SEAT-006 - A seat cannot be shared on the same flight
context SeatSelectionState
inv BR_SEAT_006_UniqueSeatPerFlight:
  choices->isUnique(choice |
    Tuple {
      flightId : UUID = choice.flightId,
      seatId : UUID = choice.seat.id
    }
  )


BR-SEAT-007 - Business upgrade requires confirmation
context SeatSelectionService::selectSeat(
  state : SeatSelectionState,
  passengerRef : String,
  flightLeg : FlightLeg,
  seat : SeatDto
) : SeatSelectionState
post BR_SEAT_007_UpgradePending:
  (seat.seatClass = SeatClass::BUSINESS and
   state.choices->exists(choice |
     choice.passengerRef = passengerRef and
     choice.flightId = seat.flightId and
     choice.seat.seatClass = SeatClass::ECONOMY and
     choice.seat.id <> seat.id)) implies
    not result.pendingUpgrade.oclIsUndefined() and
    result.pendingUpgrade.passengerRef = passengerRef and
    result.pendingUpgrade.flightId = seat.flightId and
    result.pendingUpgrade.requestedSeat = seat and
    result.choices = state.choices


BR-SEAT-008 - Other seat changes apply immediately
context SeatSelectionService::selectSeat(
  state : SeatSelectionState,
  passengerRef : String,
  flightLeg : FlightLeg,
  seat : SeatDto
) : SeatSelectionState
post BR_SEAT_008_ImmediateSelection:
  not (
    seat.seatClass = SeatClass::BUSINESS and
    state.choices->exists(choice |
      choice.passengerRef = passengerRef and
      choice.flightId = seat.flightId and
      choice.seat.seatClass = SeatClass::ECONOMY and
      choice.seat.id <> seat.id)
  ) implies
    let choice : SeatChoiceDto = result.choices->any(item |
      item.passengerRef = passengerRef and
      item.flightId = seat.flightId)
    in
      choice.flightLeg = flightLeg and
      choice.seat = seat


BR-SEAT-009 - Upgrade amount
context SeatSelectionService::selectSeat(
  state : SeatSelectionState,
  passengerRef : String,
  flightLeg : FlightLeg,
  seat : SeatDto
) : SeatSelectionState
post BR_SEAT_009_UpgradeAmount:
  (seat.seatClass = SeatClass::BUSINESS and
   state.choices->exists(choice |
     choice.passengerRef = passengerRef and
     choice.flightId = seat.flightId and
     choice.seat.seatClass = SeatClass::ECONOMY and
     choice.seat.id <> seat.id)) implies
    let currentChoice : SeatChoiceDto = state.choices->any(choice |
      choice.passengerRef = passengerRef and
      choice.flightId = seat.flightId)
    in
      result.pendingUpgrade.upgradeAmount =
        if seat.price > currentChoice.seat.price then
          seat.price - currentChoice.seat.price
        else 0 endif and
      result.pendingUpgrade.currency = seat.currency


BR-SEAT-010 - Confirm a pending upgrade
context SeatSelectionService::confirmUpgrade(
  state : SeatSelectionState
) : SeatSelectionState
pre BR_SEAT_010_UpgradeExists:
  not state.pendingUpgrade.oclIsUndefined()
post BR_SEAT_010_UpgradeApplied:
  let upgradedChoice : SeatChoiceDto = result.choices->any(choice |
    choice.passengerRef = state.pendingUpgrade.passengerRef and
    choice.flightId = state.pendingUpgrade.flightId)
  in
    upgradedChoice.seat = state.pendingUpgrade.requestedSeat and
    upgradedChoice.upgradeAmount = state.pendingUpgrade.upgradeAmount and
    result.pendingUpgrade.oclIsUndefined()


BR-SEAT-011 - Cancel a pending upgrade
context SeatSelectionService::cancelUpgrade(
  state : SeatSelectionState
) : SeatSelectionState
pre BR_SEAT_011_UpgradeExists:
  not state.pendingUpgrade.oclIsUndefined()
post BR_SEAT_011_SelectionPreserved:
  result.choices = state.choices and
  result.pendingUpgrade.oclIsUndefined()


BR-SEAT-012 - Required seat coverage
context SeatSelectionService::canContinue(
  state : SeatSelectionState
) : Boolean
post BR_SEAT_012_Result:
  result = hasCompleteSeatCoverage(state)


BR-SEAT-013 - Selected seats remain available
context SeatSelectionService::createContext(
  state : SeatSelectionState
) : SeatSelectionContextDto
pre BR_SEAT_013_CurrentAvailability:
  state.choices->forAll(choice |
    state.availableSeats->exists(seatList |
      seatList.flightId = choice.flightId and
      (seatList.businessSeats->union(seatList.economySeats))->exists(seat |
        seat.id = choice.seat.id and seat.available = true))
  )
Technical constraints:
Seat information must be refreshed before this precondition is evaluated; an earlier list response is not treated as a reservation.


BR-SEAT-014 - Completed seat-selection context
context SeatSelectionService::createContext(
  state : SeatSelectionState
) : SeatSelectionContextDto
pre BR_SEAT_014_ReadyToCreate:
  self.canContinue(state)
post BR_SEAT_014_Context:
  not result.seatSelectionContextKey.oclIsUndefined() and
  trim(result.seatSelectionContextKey).size() > 0 and
  result.passengerContextKey = state.inputContext.passengerContextKey and
  result.selectionContextKey = state.inputContext.selectionContextKey and
  result.choices = state.choices and
  result.totalUpgradeAmount =
    state.choices->collect(choice | choice.upgradeAmount)->sum() and
  result.currency = state.inputContext.currency and
  not result.preparedAt.oclIsUndefined()


BR-SEAT-015 - Save the current seat selection
context SeatSelectionService::saveSelection(
  state : SeatSelectionState
) : SavedSeatSelectionDto
post BR_SEAT_015_SavedSelection:
  result.passengerContextKey = state.inputContext.passengerContextKey and
  result.choices = state.choices and
  not result.savedAt.oclIsUndefined()


BR-SEAT-016 - Restore a saved seat selection
context SeatSelectionService::restoreSelection(
  state : SeatSelectionState,
  saved : SavedSeatSelectionDto
) : SeatSelectionState
pre BR_SEAT_016_CurrentPassengerContext:
  saved.passengerContextKey = state.inputContext.passengerContextKey
post BR_SEAT_016_RestoredChoices:
  result.choices = saved.choices->select(choice |
    state.availableSeats->exists(seatList |
      seatList.flightId = choice.flightId and
      (seatList.businessSeats->union(seatList.economySeats))->exists(seat |
        seat.id = choice.seat.id and seat.available = true))
  ) and
  result.pendingUpgrade.oclIsUndefined()
Technical constraints:
Saved choices must use protected, time-limited storage and must be discarded when their passenger or flight-selection context changes.


BR-SEAT-017 - Seat selection has no reservation side effects
Selecting or preparing seats shall not create, update, or delete Booking,
PassengerInfo, SeatAssignment, Flight, or Seat records.


BR-SEAT-018 - Seat-list currency consistency
context SeatService::listAvailableSeats(
  flightId : UUID
) : SeatListResponseDto
post BR_SEAT_018_Currency:
  result.success implies
    not result.data.currency.oclIsUndefined() and
    result.data.businessSeats->forAll(seat |
      seat.currency = result.data.currency) and
    result.data.economySeats->forAll(seat |
      seat.currency = result.data.currency)
Technical constraints:
Currency uses an ISO 4217 code, and monetary calculations use the approved fixed-precision rounding policy.


BR-SEAT-019 - Eligible seat choice
context SeatSelectionService::selectSeat(
  state : SeatSelectionState,
  passengerRef : String,
  flightLeg : FlightLeg,
  seat : SeatDto
) : SeatSelectionState
pre BR_SEAT_019_EligibleChoice:
  state.inputContext.passengerRefs->includes(passengerRef) and
  (if flightLeg = FlightLeg::DEPARTING then
     seat.flightId = state.inputContext.departingFlightId
   else
     not state.inputContext.returningFlightId.oclIsUndefined() and
     seat.flightId = state.inputContext.returningFlightId
   endif) and
  state.availableSeats->exists(seatList |
    seatList.flightId = seat.flightId and
    (seatList.businessSeats->union(seatList.economySeats))->exists(candidate |
      candidate.id = seat.id and candidate.available = true))
~~~
