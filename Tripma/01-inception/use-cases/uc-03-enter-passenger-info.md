---
artifact_type: business-use-case-specification
status: Frozen
uc_id: UC-03
uc_name: "Enter Passenger Information"
---

# UC-03: Enter Passenger Information

## Functional Use-Case Specification

### Use Case ID

UC-03

### Use Case Name

Enter Passenger Information

### Description

As a visitor, I want to provide passenger and emergency-contact information for my selected Tripma itinerary so that I can continue to seat selection.

### Actor(s)

Visitor

### Priority

High

### Trigger

The visitor enters the Tripma passenger-information experience from a completed flight selection.

### Pre-Condition(s)

PRE-1: A completed Tripma flight-selection context is available.

PRE-2: The passenger-information experience can access that context.

### Post-Condition(s)

POST-1: When the submitted information is accepted, Tripma makes a passenger-information context available to the seat-selection experience.

POST-2: Tripma preserves the current flight-selection context throughout this use case.

POST-3: When the submitted information cannot be accepted, Tripma keeps the visitor in the passenger-information experience and reports the outcome.

### Basic Flow

1. Tripma opens the passenger-information experience for the current flight selection.
2. Tripma presents the passenger, emergency-contact, and baggage controls for the current trip.
3. The visitor provides passenger information.
4. The visitor provides emergency-contact information.
5. The visitor provides baggage information.
6. Tripma evaluates the current form according to the Business Rules of this use case.
7. Tripma makes the seat-selection action available when the form is ready to continue.
8. The visitor chooses to continue to seat selection.
9. Tripma submits the current information through API-PASSENGER-INFO-PREPARE.
10. The passenger-information service evaluates and normalizes the request according to the Business Rules of this use case.
11. The service returns the prepared passenger-information context.
12. Tripma stores the returned context for the current booking workflow.
13. Tripma opens the seat-selection experience.

### Alternative Flow

AF-1: Use passenger information for the emergency contact

4a: The visitor chooses the corresponding contact option.

4b: Tripma updates the form according to the Business Rules.

4c: The Basic Flow resumes at step 5.

AF-2: Provide a separate emergency contact

4d: The visitor chooses the separate-contact path.

4e: Tripma presents the corresponding controls.

4f: The visitor provides the requested information.

4g: The Basic Flow resumes at step 5.

AF-3: Use an alternate permitted form state

3a: The visitor uses an alternate input path offered by the form.

3b: Tripma retains the current form state according to the Business Rules.

3c: The Basic Flow resumes at step 4.

AF-4: Save and close the in-progress form

7a: The visitor chooses Save and Close.

7b: Tripma processes the current form according to the Business Rules.

7c: The use case ends without entering the seat-selection experience.

AF-5: Resume an in-progress form

1a: Tripma finds a previously saved passenger form.

1b: Tripma evaluates and restores it according to the Business Rules.

1c: The Basic Flow resumes at step 2.

AF-6: Correct submitted information

10a: The service identifies information that needs attention.

10b: Tripma associates the returned outcome with the affected form control.

10c: The visitor updates the information.

10d: The Basic Flow resumes at step 6.

### Exception Flow

EF-1: Passenger form is not ready to continue

6a: If the current form does not satisfy the Business Rules, Tripma keeps the visitor in the passenger-information experience and identifies the affected input.

6b: The seat-selection action remains unavailable.

EF-2: Passenger-information request is rejected

10e: If the service rejects the request, it returns the API-PASSENGER-INFO-PREPARE client-error response.

10f: Tripma preserves the visitor's current form and presents a recoverable outcome.

EF-3: Passenger-information service is unavailable

9a: If Tripma cannot complete the request because of a technical failure, it preserves the visitor's current form and presents a retryable error state.

9b: Tripma does not open the seat-selection experience.

EF-4: In-progress form cannot be saved or restored

7d: If Tripma cannot process an in-progress form, it preserves the current usable state and presents a recoverable outcome.

### Related UI

Passenger-information step of the booking page (/booking); passenger form; emergency-contact form; baggage controls; Save and Close action; seat-selection action

### Related API IDs

API-PASSENGER-INFO-PREPARE

### Notes

Scope clarification: This use case prepares the passenger-information context used by the next Tripma booking step.

## UML Model

~~~plantuml
@startuml
hide empty members

enum PassengerType {
  ADULT
  MINOR
}

class Booking <<Entity>> {
  id: UUID [1]
}

class PassengerInfo <<Entity>> {
  id: UUID [1]
}

class EmergencyContact <<Entity>> {
  id: UUID [1]
}

class PassengerBaggage <<Entity>> {
  id: UUID [1]
}

class SelectedFlightContextDto <<DTO>> {
  selectionContextKey: String [1]
  type: Boolean [1]
  departingFlight: FlightDto [1]
  returningFlight: FlightDto [0..1]
}

class SearchDto <<DTO>> {
  adults: Integer [1]
  minors: Integer [1]
  type: Boolean [1]
}

class FlightDto <<DTO>> {
  fromCity: String [1]
  date: DateTime [1]
}

class PassengerTripContextDto <<DTO>> {
  selectedFlights: SelectedFlightContextDto [1]
  searchParams: SearchDto [1]
  departingMaxCheckedBagsPerPassenger: Integer [1]
  returningMaxCheckedBagsPerPassenger: Integer [0..1]
}

class PassengerInputDto <<DTO>> {
  passengerRef: String [1]
  passengerType: PassengerType [1]
  firstName: String [1]
  lastName: String [1]
  dateOfBirth: Date [1]
  email: String [0..1]
  phone: String [0..1]
}

class PassengerBaggageInputDto <<DTO>> {
  passengerRef: String [1]
  departingCheckedBags: Integer [1]
  returningCheckedBags: Integer [0..1]
}

class EmergencyContactInputDto <<DTO>> {
  usePrimaryPassenger: Boolean [1]
  firstName: String [0..1]
  lastName: String [0..1]
  email: String [0..1]
  phone: String [0..1]
}

class PassengerFormDto <<DTO>> {
  selectionContextKey: String [1]
  primaryPassengerRef: String [1]
  passengers: PassengerInputDto [1..*]
  baggage: PassengerBaggageInputDto [1..*]
  emergencyContact: EmergencyContactInputDto [1]
}

class PreparedPassengerContextDto <<DTO>> {
  passengerContextKey: String [1]
  selectionContextKey: String [1]
  primaryPassengerRef: String [1]
  passengers: PassengerInputDto [1..*]
  baggage: PassengerBaggageInputDto [1..*]
  emergencyContact: EmergencyContactInputDto [1]
  preparedAt: DateTime [1]
}

class SavedPassengerFormDto <<DTO>> {
  selectionContextKey: String [1]
  form: PassengerFormDto [1]
  savedAt: DateTime [1]
}

class PassengerInformationService <<Service>> {
  canContinue(tripContext: PassengerTripContextDto, form: PassengerFormDto): Boolean
  prepare(tripContext: PassengerTripContextDto, form: PassengerFormDto): PreparedPassengerContextDto
  saveForm(tripContext: PassengerTripContextDto, form: PassengerFormDto): SavedPassengerFormDto
  restoreForm(tripContext: PassengerTripContextDto, saved: SavedPassengerFormDto): PassengerFormDto
  normalizePassengers(passengers: PassengerInputDto [1..*]): PassengerInputDto [1..*] {query}
  emergencyContactOf(form: PassengerFormDto): EmergencyContactInputDto {query}
}

class Flight <<Entity>> {
  id: UUID [1]
}

class Seat <<Entity>> {
  id: UUID [1]
}

SelectedFlightContextDto "1" *-- "1" FlightDto : departing
SelectedFlightContextDto "1" *-- "0..1" FlightDto : returning
PassengerTripContextDto "1" *-- "1" SelectedFlightContextDto : selected flights
PassengerTripContextDto "1" *-- "1" SearchDto : search parameters
PassengerFormDto "1" *-- "1..*" PassengerInputDto : passengers
PassengerFormDto "1" *-- "1..*" PassengerBaggageInputDto : baggage
PassengerFormDto "1" *-- "1" EmergencyContactInputDto : emergency contact
PreparedPassengerContextDto "1" *-- "1..*" PassengerInputDto : passengers
PreparedPassengerContextDto "1" *-- "1..*" PassengerBaggageInputDto : baggage
PreparedPassengerContextDto "1" *-- "1" EmergencyContactInputDto : emergency contact
PassengerInformationService ..> PassengerTripContextDto
PassengerInformationService ..> PassengerFormDto
PassengerInformationService ..> PreparedPassengerContextDto
PassengerInformationService ..> SavedPassengerFormDto
PassengerInfo ..> PassengerInputDto : later maps from
EmergencyContact ..> EmergencyContactInputDto : later maps from
PassengerBaggage ..> PassengerBaggageInputDto : later maps from
PassengerInputDto --> "1" PassengerType : passengerType
SavedPassengerFormDto --> "1" PassengerFormDto : form

note right of SelectedFlightContextDto
  type = false represents one-way.
  type = true represents round-trip.

  This DTO and FlightDto are shared with UC-02.
  SearchDto is shared with UC-01 and UC-02.
end note

note right of PassengerFormDto
  passengerRef is a booking-workflow reference,
  not a persisted passenger identifier.
end note

note bottom of PreparedPassengerContextDto
  This is a transient booking-workflow context.
  API-PASSENGER-INFO-PREPARE does not persist it.
end note

note bottom of Booking
  Persistence occurs later in UC-05.
end note

@enduml
~~~

## Business Rules

The following rules are authoritative for Prompt E. OCL is preserved where applicable; technical or non-OCL constraints remain authoritative natural-language requirements.

~~~text
BR-PASS-001 - Current trip context
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_001_CurrentSelection:
  form.selectionContextKey =
    tripContext.selectedFlights.selectionContextKey

pre BR_PASS_001_TripTypeConsistent:
  tripContext.searchParams.type = tripContext.selectedFlights.type


BR-PASS-002 - Passenger coverage
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_002_PassengerCount:
  form.passengers->size() =
    tripContext.searchParams.adults + tripContext.searchParams.minors

pre BR_PASS_002_PassengerTypesMatchSearch:
  form.passengers->select(p |
    p.passengerType = PassengerType::ADULT)->size() =
      tripContext.searchParams.adults and
  form.passengers->select(p |
    p.passengerType = PassengerType::MINOR)->size() =
      tripContext.searchParams.minors


BR-PASS-003 - Unique passenger references
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_003_UniqueReferences:
  form.passengers->isUnique(p | p.passengerRef)


BR-PASS-004 - Primary passenger
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_004_PrimaryPassenger:
  form.passengers->one(passenger |
    passenger.passengerRef = form.primaryPassengerRef and
    passenger.passengerType = PassengerType::ADULT)


BR-PASS-005 - Required passenger information
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_005_RequiredValues:
  form.passengers->forAll(passenger |
    not passenger.passengerRef.oclIsUndefined() and
    trim(passenger.passengerRef).size() > 0 and
    not passenger.firstName.oclIsUndefined() and
    trim(passenger.firstName).size() > 0 and
    not passenger.lastName.oclIsUndefined() and
    trim(passenger.lastName).size() > 0 and
    not passenger.dateOfBirth.oclIsUndefined()
  )


BR-PASS-006 - Date of birth precedes departure
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_006_BirthDatesPrecedeDeparture:
  let departureDate : Date = localDate(
        tripContext.selectedFlights.departingFlight.date,
        timeZoneForCity(
          tripContext.selectedFlights.departingFlight.fromCity
        )
      )
  in
    form.passengers->forAll(passenger |
      passenger.dateOfBirth < departureDate)


BR-PASS-007 - Passenger type matches age at departure
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_007_PassengerTypesMatchAgeOnDeparture:
  let departureDate : Date = localDate(
        tripContext.selectedFlights.departingFlight.date,
        timeZoneForCity(
          tripContext.selectedFlights.departingFlight.fromCity
        )
      )
  in
    form.passengers->forAll(passenger |
      let age : Integer = ageOn(passenger.dateOfBirth, departureDate)
      in
      (passenger.passengerType = PassengerType::ADULT implies age >= 18) and
      (passenger.passengerType = PassengerType::MINOR implies age < 18)
    )


BR-PASS-008 - Optional passenger contact information
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_008_PassengerChannelsWhenPresent:
  form.passengers->forAll(passenger |
    (passenger.email.oclIsUndefined() or
      isEmail(lower(trim(passenger.email)))) and
    (passenger.phone.oclIsUndefined() or
      isPhone(trim(passenger.phone)))
  )


BR-PASS-009 - Emergency contact
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_009_ContactSource:
  if form.emergencyContact.usePrimaryPassenger then
    let primary : PassengerInputDto = form.passengers->any(passenger |
      passenger.passengerRef = form.primaryPassengerRef)
    in
      not primary.email.oclIsUndefined() and
      isEmail(lower(trim(primary.email))) and
      not primary.phone.oclIsUndefined() and
      isPhone(trim(primary.phone))
  else
    not form.emergencyContact.firstName.oclIsUndefined() and
    trim(form.emergencyContact.firstName) <> '' and
    not form.emergencyContact.lastName.oclIsUndefined() and
    trim(form.emergencyContact.lastName) <> '' and
    not form.emergencyContact.email.oclIsUndefined() and
    isEmail(lower(trim(form.emergencyContact.email))) and
    not form.emergencyContact.phone.oclIsUndefined() and
    isPhone(trim(form.emergencyContact.phone))
  endif


BR-PASS-010 - One baggage entry per passenger
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_010_OneEntryPerPassenger:
  form.baggage->size() = form.passengers->size() and
  form.baggage->isUnique(item | item.passengerRef) and
  form.baggage->forAll(item |
    form.passengers->exists(passenger |
      passenger.passengerRef = item.passengerRef))


BR-PASS-011 - Departing checked-baggage limit
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_011_DepartingRange:
  form.baggage->forAll(item |
    item.departingCheckedBags >= 0 and
    item.departingCheckedBags <=
      tripContext.departingMaxCheckedBagsPerPassenger)


BR-PASS-012 - Returning checked-baggage limit
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
pre BR_PASS_012_ReturningRange:
  if tripContext.selectedFlights.type = true then
    not tripContext.selectedFlights.returningFlight.oclIsUndefined() and
    not tripContext.returningMaxCheckedBagsPerPassenger.oclIsUndefined() and
    form.baggage->forAll(item |
      not item.returningCheckedBags.oclIsUndefined() and
      item.returningCheckedBags >= 0 and
      item.returningCheckedBags <=
        tripContext.returningMaxCheckedBagsPerPassenger)
  else
    tripContext.selectedFlights.returningFlight.oclIsUndefined() and
    tripContext.returningMaxCheckedBagsPerPassenger.oclIsUndefined() and
    form.baggage->forAll(item |
      item.returningCheckedBags.oclIsUndefined())
  endif
Technical constraints:
The service obtains baggage limits from the authoritative selected-flight data addressed by the request; it does not accept a client-supplied baggage limit as authoritative.


BR-PASS-013 - Prepared passenger context
context PassengerInformationService::prepare(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : PreparedPassengerContextDto
post BR_PASS_013_ContextIdentity:
  not result.passengerContextKey.oclIsUndefined() and
  trim(result.passengerContextKey).size() > 0 and
  result.selectionContextKey = tripContext.selectedFlights.selectionContextKey and
  result.primaryPassengerRef = form.primaryPassengerRef and
  not result.preparedAt.oclIsUndefined()

post BR_PASS_013_ContextData:
  result.passengers = normalizePassengers(form.passengers) and
  result.baggage = form.baggage and
  result.emergencyContact = emergencyContactOf(form)


BR-PASS-014 - Completion readiness
context PassengerInformationService::canContinue(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : Boolean
post BR_PASS_014_Result:
  result =
    let departureDate : Date = localDate(
      tripContext.selectedFlights.departingFlight.date,
      timeZoneForCity(
        tripContext.selectedFlights.departingFlight.fromCity))
    in
    form.selectionContextKey =
      tripContext.selectedFlights.selectionContextKey and
    tripContext.searchParams.type = tripContext.selectedFlights.type and
    form.passengers->size() =
      tripContext.searchParams.adults + tripContext.searchParams.minors and
    form.passengers->select(passenger |
      passenger.passengerType = PassengerType::ADULT)->size() =
        tripContext.searchParams.adults and
    form.passengers->select(passenger |
      passenger.passengerType = PassengerType::MINOR)->size() =
        tripContext.searchParams.minors and
    form.passengers->isUnique(passenger | passenger.passengerRef) and
    form.passengers->one(passenger |
      passenger.passengerRef = form.primaryPassengerRef and
      passenger.passengerType = PassengerType::ADULT) and
    form.passengers->forAll(passenger |
      not passenger.passengerRef.oclIsUndefined() and
      trim(passenger.passengerRef) <> '' and
      not passenger.firstName.oclIsUndefined() and
      trim(passenger.firstName) <> '' and
      not passenger.lastName.oclIsUndefined() and
      trim(passenger.lastName) <> '' and
      not passenger.dateOfBirth.oclIsUndefined() and
      passenger.dateOfBirth < departureDate and
      (passenger.passengerType = PassengerType::ADULT implies
        ageOn(passenger.dateOfBirth, departureDate) >= 18) and
      (passenger.passengerType = PassengerType::MINOR implies
        ageOn(passenger.dateOfBirth, departureDate) < 18) and
      (passenger.email.oclIsUndefined() or
        isEmail(lower(trim(passenger.email)))) and
      (passenger.phone.oclIsUndefined() or
        isPhone(trim(passenger.phone)))) and
    (if form.emergencyContact.usePrimaryPassenger then
       let primary : PassengerInputDto = form.passengers->any(passenger |
         passenger.passengerRef = form.primaryPassengerRef)
       in
         not primary.email.oclIsUndefined() and
         isEmail(lower(trim(primary.email))) and
         not primary.phone.oclIsUndefined() and
         isPhone(trim(primary.phone))
     else
       not form.emergencyContact.firstName.oclIsUndefined() and
       trim(form.emergencyContact.firstName) <> '' and
       not form.emergencyContact.lastName.oclIsUndefined() and
       trim(form.emergencyContact.lastName) <> '' and
       not form.emergencyContact.email.oclIsUndefined() and
       isEmail(lower(trim(form.emergencyContact.email))) and
       not form.emergencyContact.phone.oclIsUndefined() and
       isPhone(trim(form.emergencyContact.phone))
     endif) and
    form.baggage->size() = form.passengers->size() and
    form.baggage->isUnique(item | item.passengerRef) and
    form.baggage->forAll(item |
      form.passengers->exists(passenger |
        passenger.passengerRef = item.passengerRef) and
      item.departingCheckedBags >= 0 and
      item.departingCheckedBags <=
        tripContext.departingMaxCheckedBagsPerPassenger) and
    (if tripContext.selectedFlights.type = true then
       not tripContext.selectedFlights.returningFlight.oclIsUndefined() and
       not tripContext.returningMaxCheckedBagsPerPassenger.oclIsUndefined() and
       form.baggage->forAll(item |
         not item.returningCheckedBags.oclIsUndefined() and
         item.returningCheckedBags >= 0 and
         item.returningCheckedBags <=
           tripContext.returningMaxCheckedBagsPerPassenger)
     else
       tripContext.selectedFlights.returningFlight.oclIsUndefined() and
       tripContext.returningMaxCheckedBagsPerPassenger.oclIsUndefined() and
       form.baggage->forAll(item |
         item.returningCheckedBags.oclIsUndefined())
     endif)


BR-PASS-015 - Save the current passenger form
context PassengerInformationService::saveForm(
  tripContext : PassengerTripContextDto,
  form : PassengerFormDto
) : SavedPassengerFormDto
pre BR_PASS_015_CurrentContextToSave:
  form.selectionContextKey = tripContext.selectedFlights.selectionContextKey
post BR_PASS_015_SavedForm:
  result.selectionContextKey = tripContext.selectedFlights.selectionContextKey and
  result.form = form and
  not result.savedAt.oclIsUndefined()


BR-PASS-016 - Restore a saved passenger form
context PassengerInformationService::restoreForm(
  tripContext : PassengerTripContextDto,
  saved : SavedPassengerFormDto
) : PassengerFormDto
pre BR_PASS_016_SameSelectionContext:
  saved.selectionContextKey = tripContext.selectedFlights.selectionContextKey and
  saved.form.selectionContextKey = tripContext.selectedFlights.selectionContextKey
post BR_PASS_016_RestoredForm:
  result = saved.form
Technical constraints:
Saved passenger data must use protected, time-limited storage. It must be removed when the flight selection changes, the booking finishes, the visitor discards the form, or the retention period expires.
A saved form that cannot be read safely or no longer belongs to the current selection is ignored without replacing the current usable form.


BR-PASS-017 - Preparation has no persistence side effects
API-PASSENGER-INFO-PREPARE shall not create, update, or delete Booking,
PassengerInfo, EmergencyContact, PassengerBaggage, Flight, or Seat records.
Technical constraints:
Passenger information is sent only in an HTTPS request body. Query strings, URLs, analytics payloads, and application logs must not contain raw passenger or emergency-contact values.
~~~
