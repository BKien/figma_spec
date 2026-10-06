---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-02
uc_name: "Select Flight"
---

# UC-02: Select Flight

## Functional Use-Case Specification

### Use Case ID

UC-02

### Use Case Name

Select Flight

### Description

As a visitor, I want to choose flight options from Tripma search results so that I can continue preparing my trip.

### Actor(s)

Visitor

### Priority

High

### Trigger

The visitor chooses a flight option from the Tripma results experience.

### Pre-Condition(s)

PRE-1: A Tripma flight-results experience is available.
PRE-2: The current search context and its flight options can be accessed.

### Post-Condition(s)

POST-1: When the selection is accepted, Tripma makes the completed flight-selection context available to the passenger-information experience.
POST-2: Tripma reflects the visitor's current choices in the flight-results experience.
POST-3: When continuation cannot be completed, Tripma keeps the visitor in the flight-results experience and reports the outcome.

### Basic Flow

1. Tripma presents flight options for the current search context.
2. The visitor chooses an option for the flight leg currently presented.
3. Tripma marks the chosen flight card as selected and updates the selection summary.
4. Tripma presents any remaining selection activity required by the Business Rules.
5. The visitor completes the remaining selection activity, when applicable.
6. Tripma evaluates the current flight-selection state according to the Business Rules of this use case.
7. Tripma presents the current selection summary and continuation action.
8. The visitor chooses to continue to passenger information.
9. Tripma creates the completed flight-selection context.
10. Tripma opens the passenger-information experience.

### Alternative Flow

AF-1: Change the current flight choice
3a. The visitor chooses a different option for the currently presented flight leg.
3b. Tripma updates the flight-selection state and any dependent selection state according to the Business Rules.
3c. The Basic Flow resumes at step 4.

AF-2: Change a subsequent flight choice
7a. The visitor chooses a different option from the subsequent flight-leg results.
7b. Tripma updates the flight-selection state and summary.
7c. The Basic Flow resumes at step 6.

AF-3: Save and close the in-progress selection
7d. The visitor chooses Save and Close.
7e. Tripma processes the in-progress selection according to the Business Rules.
7f. The use case ends without entering the passenger-information experience.

AF-4: Resume an in-progress selection
1a. Tripma finds a previous in-progress selection.
1b. Tripma evaluates and restores it according to the Business Rules.
1c. The Basic Flow resumes at step 3.

AF-5: View more flight options
2a. The visitor requests the remaining options for the currently presented flight leg.
2b. Tripma updates the current result presentation according to the Business Rules.
2c. The Basic Flow resumes at step 2.

### Exception Flow

EF-1: Selection is not ready to continue
6a. If the current selection does not satisfy the Business Rules, Tripma keeps the visitor in the flight-results experience and makes the continuation action unavailable.

EF-2: Flight-selection context cannot be completed
9a. If Tripma cannot create the completed flight-selection context because of a technical failure, it presents a recoverable error state.
9b. Tripma does not open the passenger-information experience.

EF-3: In-progress selection cannot be saved or restored
7g. If Tripma cannot process the in-progress selection, it presents a recoverable outcome according to the Business Rules.

### Related UI

Flight-results page (`/flights`); flight card; flight-selection summary; passenger-information action; passenger-information page (`/booking`)

### Related API IDs

None

### Notes

Scope clarification: This use case covers choosing flight options and handing the selection to the passenger-information experience. It consumes the search-result context established by UC-01 but does not define a server API. Seat assignment and booking creation are outside scope.

## UML Model

~~~plantuml
@startuml
hide empty members

class SearchDto <<DTO>> {
  type: Boolean [1]
}

class FlightDto <<DTO>> {
  flightId: UUID [1]
  type: Boolean [1]
  subtotalPrice: Decimal [1]
  taxesAndFees: Decimal [1]
  date: DateTime [1]
  arrivalAt: DateTime [1]
}

enum FlightLeg {
  DEPARTING
  RETURNING
}

class FlightResultViewState <<State>> {
  activeLeg: FlightLeg [1]
  summaryOpen: Boolean [1]
  departingExpanded: Boolean [1]
  returningExpanded: Boolean [1]
}

class FlightBookingState <<State>> {
  searchContextKey: String [1]
  searchParams: SearchDto [1]
  currency: String [1]
  viewState: FlightResultViewState [1]
  departingOptions: FlightDto [0..*]
  returningOptions: FlightDto [0..*]
  selectedDepartingFlight: FlightDto [0..1]
  selectedReturningFlight: FlightDto [0..1]
}

class SelectedFlightContextDto <<DTO>> {
  selectionContextKey: String [1]
  searchContextKey: String [1]
  type: Boolean [1]
  currency: String [1]
  departingFlight: FlightDto [1]
  returningFlight: FlightDto [0..1]
}

class SavedFlightSelectionDto <<DTO>> {
  searchContextKey: String [1]
  type: Boolean [1]
  departingFlightId: UUID [0..1]
  returningFlightId: UUID [0..1]
  savedAt: DateTime [1]
}

class FlightSelectionSummaryDto <<DTO>> {
  subtotalAmount: Decimal [1]
  taxesAndFeesAmount: Decimal [1]
  totalAmount: Decimal [1]
  currency: String [1]
}

class FlightSelectionService <<Service>> {
  select(state: FlightBookingState, leg: FlightLeg, flight: FlightDto): FlightBookingState
  canContinue(state: FlightBookingState): Boolean
  summarize(state: FlightBookingState): FlightSelectionSummaryDto
  saveSelection(state: FlightBookingState): SavedFlightSelectionDto
  restoreSelection(state: FlightBookingState, saved: SavedFlightSelectionDto): FlightBookingState
  expandResults(state: FlightBookingState, leg: FlightLeg): FlightBookingState
  createContext(state: FlightBookingState): SelectedFlightContextDto
}

FlightBookingState "1" *-- "1" SearchDto : uses
FlightBookingState "1" *-- "1" FlightResultViewState : presents through
FlightBookingState "1" *-- "0..*" FlightDto : departing options
FlightBookingState "1" *-- "0..*" FlightDto : returning options
FlightBookingState "1" --> "0..1" FlightDto : selected departing
FlightBookingState "1" --> "0..1" FlightDto : selected returning
SelectedFlightContextDto "1" *-- "1" FlightDto : departing
SelectedFlightContextDto "1" *-- "0..1" FlightDto : returning
FlightSelectionService ..> FlightBookingState
FlightSelectionService ..> FlightLeg
FlightSelectionService ..> FlightSelectionSummaryDto
FlightSelectionService ..> SavedFlightSelectionDto
FlightSelectionService ..> SelectedFlightContextDto
FlightResultViewState --> "1" FlightLeg : activeLeg

note right of SearchDto
  type = false represents one-way.
  type = true represents round-trip.
end note

note bottom of FlightBookingState
  departingOptions and returningOptions are supplied by
  API-FLIGHTS-SEARCH for the current SearchDto.

  This state is an application/client selection context,
  not a database entity and not a seat reservation.
end note

note right of FlightDto
  FlightDto is shared with UC-01 and
  API-FLIGHTS-SEARCH. It is not a new
  persistence entity introduced by UC-02.
end note

note right of SavedFlightSelectionDto
  This DTO may be stored in client-side selection storage.
  It is not a database entity and is distinct from the
  completed SelectedFlightContextDto.
end note

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-SELECT-001: Selected option belongs to the requested leg
context FlightSelectionService::select(
  state : FlightBookingState,
  leg : FlightLeg,
  flight : FlightDto
) : FlightBookingState
pre BR_SELECT_001_OptionBelongsToLeg:
  if leg = FlightLeg::DEPARTING then
    state.departingOptions->includes(flight)
  else
    state.returningOptions->includes(flight)
  endif


BR-SELECT-002: Leg matches the trip type
context FlightSelectionService::select(
  state : FlightBookingState,
  leg : FlightLeg,
  flight : FlightDto
) : FlightBookingState
pre BR_SELECT_002_TripTypeMatches:
  flight.type = state.searchParams.type
pre BR_SELECT_002_ReturningLegSupported:
  leg = FlightLeg::RETURNING implies state.searchParams.type = true


BR-SELECT-003: Single selection for each leg
context FlightSelectionService::select(
  state : FlightBookingState,
  leg : FlightLeg,
  flight : FlightDto
) : FlightBookingState
post BR_SELECT_003_DepartingSelection:
  leg = FlightLeg::DEPARTING implies
    result.selectedDepartingFlight = flight and
    result.selectedReturningFlight.oclIsUndefined()
post BR_SELECT_003_ReturningSelection:
  leg = FlightLeg::RETURNING implies
    result.selectedReturningFlight = flight and
    result.selectedDepartingFlight = state.selectedDepartingFlight
post BR_SELECT_003_ContextPreserved:
  result.searchContextKey = state.searchContextKey and
  result.searchParams = state.searchParams and
  result.currency = state.currency and
  result.departingOptions = state.departingOptions and
  result.returningOptions = state.returningOptions


BR-SELECT-004: Presentation after selection
context FlightSelectionService::select(
  state : FlightBookingState,
  leg : FlightLeg,
  flight : FlightDto
) : FlightBookingState
post BR_SELECT_004_Presentation:
  result.viewState.summaryOpen = true and
  result.viewState.activeLeg =
    if leg = FlightLeg::DEPARTING and state.searchParams.type = true then
      FlightLeg::RETURNING
    else
      leg
    endif


BR-SELECT-005: Returning-flight chronological compatibility
context FlightSelectionService::select(
  state : FlightBookingState,
  leg : FlightLeg,
  flight : FlightDto
) : FlightBookingState
pre BR_SELECT_005_DepartingSelectedFirst:
  leg = FlightLeg::RETURNING implies
    not state.selectedDepartingFlight.oclIsUndefined()
pre BR_SELECT_005_ReturnAfterOutboundArrival:
  leg = FlightLeg::RETURNING implies
    flight.date >= state.selectedDepartingFlight.arrivalAt


BR-SELECT-006: Selected flights remain chronologically compatible
context FlightBookingState
inv BR_SELECT_006_ConsistentSelectionState:
  not selectedReturningFlight.oclIsUndefined() implies
    not selectedDepartingFlight.oclIsUndefined() and
    searchParams.type = true and
    selectedReturningFlight.date >= selectedDepartingFlight.arrivalAt
Technical constraints:
- Compatibility compares normalized timezone-aware instants rather than display strings or isolated local-time components.


BR-SELECT-007: Completion readiness
context FlightSelectionService::canContinue(
  state : FlightBookingState
) : Boolean
post BR_SELECT_007_Result:
  result =
    if state.searchParams.type = true then
      not state.selectedDepartingFlight.oclIsUndefined() and
      not state.selectedReturningFlight.oclIsUndefined() and
      state.selectedReturningFlight.date >=
        state.selectedDepartingFlight.arrivalAt
    else
      not state.selectedDepartingFlight.oclIsUndefined() and
      state.selectedReturningFlight.oclIsUndefined()
    endif


BR-SELECT-008: Completed selection context
context FlightSelectionService::createContext(
  state : FlightBookingState
) : SelectedFlightContextDto
pre BR_SELECT_008_ReadyToCreate:
  self.canContinue(state)
post BR_SELECT_008_ContextMatchesSelection:
  not result.selectionContextKey.oclIsUndefined() and
  trim(result.selectionContextKey).size() > 0 and
  result.searchContextKey = state.searchContextKey and
  result.type = state.searchParams.type and
  result.currency = state.currency and
  result.departingFlight = state.selectedDepartingFlight and
  result.returningFlight = state.selectedReturningFlight
Technical constraints:
- The completed context is written atomically before navigation; failure preserves the previous completed context and prevents navigation.


BR-SELECT-009: Selection does not reserve inventory
Selecting a flight shall not create a booking or modify flight or seat inventory. The booking workflow rechecks the selected flights and capacity before committing a reservation.


BR-SELECT-010: Selection summary amounts
context FlightSelectionService::summarize(
  state : FlightBookingState
) : FlightSelectionSummaryDto
post BR_SELECT_010_Subtotal:
  result.subtotalAmount =
    (if state.selectedDepartingFlight.oclIsUndefined() then 0
     else state.selectedDepartingFlight.subtotalPrice endif) +
    (if state.selectedReturningFlight.oclIsUndefined() then 0
     else state.selectedReturningFlight.subtotalPrice endif)
post BR_SELECT_010_TaxesAndFees:
  result.taxesAndFeesAmount =
    (if state.selectedDepartingFlight.oclIsUndefined() then 0
     else state.selectedDepartingFlight.taxesAndFees endif) +
    (if state.selectedReturningFlight.oclIsUndefined() then 0
     else state.selectedReturningFlight.taxesAndFees endif)
post BR_SELECT_010_Total:
  result.totalAmount = result.subtotalAmount + result.taxesAndFeesAmount


BR-SELECT-011: Selection-summary currency
context FlightSelectionService::summarize(
  state : FlightBookingState
) : FlightSelectionSummaryDto
post BR_SELECT_011_Currency:
  result.currency = state.currency
Technical constraints:
- Displayed amounts use the UC-01 response currency and its approved monetary rounding and formatting policy.


BR-SELECT-012: Save the current selection
context FlightSelectionService::saveSelection(
  state : FlightBookingState
) : SavedFlightSelectionDto
pre BR_SELECT_012_HasSelectionToSave:
  not state.selectedDepartingFlight.oclIsUndefined() or
  not state.selectedReturningFlight.oclIsUndefined()
post BR_SELECT_012_SavedIdentity:
  result.searchContextKey = state.searchContextKey and
  result.type = state.searchParams.type and
  not result.savedAt.oclIsUndefined()
post BR_SELECT_012_SavedFlightIdentifiers:
  result.departingFlightId =
    if state.selectedDepartingFlight.oclIsUndefined() then null
    else state.selectedDepartingFlight.flightId endif and
  result.returningFlightId =
    if state.selectedReturningFlight.oclIsUndefined() then null
    else state.selectedReturningFlight.flightId endif


BR-SELECT-013: Saved selection matches the current search
context FlightSelectionService::restoreSelection(
  state : FlightBookingState,
  saved : SavedFlightSelectionDto
) : FlightBookingState
pre BR_SELECT_013_SameSearchContext:
  saved.searchContextKey = state.searchContextKey and
  saved.type = state.searchParams.type and
  (saved.type = true or saved.returningFlightId.oclIsUndefined())


BR-SELECT-014: Saved flights are still available
context FlightSelectionService::restoreSelection(
  state : FlightBookingState,
  saved : SavedFlightSelectionDto
) : FlightBookingState
pre BR_SELECT_014_SavedOptionsStillExist:
  (saved.departingFlightId.oclIsUndefined() or
    state.departingOptions->exists(flight |
      flight.flightId = saved.departingFlightId)) and
  (saved.returningFlightId.oclIsUndefined() or
    state.returningOptions->exists(flight |
      flight.flightId = saved.returningFlightId))


BR-SELECT-015: Saved flight sequence remains compatible
context FlightSelectionService::restoreSelection(
  state : FlightBookingState,
  saved : SavedFlightSelectionDto
) : FlightBookingState
pre BR_SELECT_015_SavedSequenceStillValid:
  saved.returningFlightId.oclIsUndefined() or
  (not saved.departingFlightId.oclIsUndefined() and
    saved.type = true and
    state.returningOptions->any(returningFlight |
      returningFlight.flightId = saved.returningFlightId).date >=
    state.departingOptions->any(departingFlight |
      departingFlight.flightId = saved.departingFlightId).arrivalAt)
Technical constraints:
- An invalid saved selection is ignored without replacing valid current state; a storage failure leaves the summary open and is retryable.


BR-SELECT-016: Restore an eligible saved selection
context FlightSelectionService::restoreSelection(
  state : FlightBookingState,
  saved : SavedFlightSelectionDto
) : FlightBookingState
post BR_SELECT_016_RestoredSelection:
  result.selectedDepartingFlight =
    if saved.departingFlightId.oclIsUndefined() then null
    else state.departingOptions->any(flight |
      flight.flightId = saved.departingFlightId) endif and
  result.selectedReturningFlight =
    if saved.returningFlightId.oclIsUndefined() then null
    else state.returningOptions->any(flight |
      flight.flightId = saved.returningFlightId) endif and
  result.searchContextKey = state.searchContextKey and
  result.searchParams = state.searchParams and
  result.currency = state.currency


BR-SELECT-017: Expand the current flight result presentation
context FlightSelectionService::expandResults(
  state : FlightBookingState,
  leg : FlightLeg
) : FlightBookingState
post BR_SELECT_017_RequestedLegExpanded:
  if leg = FlightLeg::DEPARTING then
    result.viewState.departingExpanded = true
  else
    result.viewState.returningExpanded = true
  endif
post BR_SELECT_017_SelectionPreserved:
  result.selectedDepartingFlight = state.selectedDepartingFlight and
  result.selectedReturningFlight = state.selectedReturningFlight
post BR_SELECT_017_OptionsPreserved:
  result.departingOptions = state.departingOptions and
  result.returningOptions = state.returningOptions
Technical constraints:
- Expanding locally available results must not trigger a redundant request for options already held by the client.


BR-SELECT-018: Selected-card and active-leg presentation
context FlightBookingState
inv BR_SELECT_018_UniqueOptionIdentifiers:
  departingOptions->isUnique(flight | flight.flightId) and
  returningOptions->isUnique(flight | flight.flightId)
inv BR_SELECT_018_SelectedOptionsRemainCanonical:
  (selectedDepartingFlight.oclIsUndefined() or
    departingOptions->includes(selectedDepartingFlight)) and
  (selectedReturningFlight.oclIsUndefined() or
    returningOptions->includes(selectedReturningFlight))
Technical constraints:
- Selected-card rendering is keyed by flight identifier so replacement cannot leave more than one card marked for the same leg.

~~~
