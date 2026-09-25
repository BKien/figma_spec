# UC-06: Manage Job Preferences

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Job Preferences

Description:

- Allows an authenticated Job Seeker to view and save practice interest, working availability, health-benefit needs, and preferred cities.
- The profile editor and the Recommendations modal edit one shared preference record. Saved preferences provide ranking inputs to UC-07 and a geographic comparison on UC-04 job details; they do not alter the public search filters of UC-03.
- The Figma frames support the preference fields and editing surfaces. Canonical city selection, defaults, matching meanings, concurrency behavior, and API contracts are declared research decisions, not inferred backend behavior.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER.

Preconditions:

- UC-01/02 establish the account/session. UC-03 supplies the canonical location options, availability enums, and job visibility; UC-04 supplies job details and practice-interest vocabulary.
- The profile routes `/profile/job-preferences` and `/profile/job-preferences/edit` exist and reload correctly. Once UC-07 is integrated, `/recommendations` opens the same editor in a modal.
- New accounts and profiles with no desired position are allowed to save preferences. No application, profile publication, or verified-contact requirement is introduced.

Postconditions:

- Success: All preference fields are saved together with one new revision. The profile read page and, when open, Recommendations sidebar display the same canonical values.
- Failure: Previously saved preferences remain intact; validation/conflict/service failures are visible and preserve the current draft where the session is still valid.
- Cancel, close, or Not Now saves nothing. This UC does not modify account names, desired position, job records, manually selected public-search filters, or application state.

Main Flow:

1. Open Profile → Job Preferences and load the preference record and UC-03 location options.
2. Display saved values, or the explicitly labeled initial preferences if none have been saved.
3. Select Edit. The form offers Practice Interest, Availability, Are Health Benefits Required?, and preferred-city selection.
4. Change the values and select Save Changes.
5. Submit all four preference fields with the loaded expectedRevision.
6. The server validates eligibility, accepted values, and the revision, then saves the whole record once.
7. Display `Job preferences saved.` and return to the profile read page. If editing from UC-07, close the modal and reload page 1 of recommendations with the saved preferences.

Alternative Flow:

A.1 — First visit and unrestricted preferences

- A missing record is represented by revision 0, practiceInterest ANY, availability ANY, healthBenefitsRequired false, locationIds [], and updatedAt null. GET does not create a record.
- `Any` means that dimension does not constrain preference matching. `No` for required health benefits means benefits are not required; it does not mean the actor wants jobs without benefits.
- An empty city list means Any location. Saving these defaults deliberately is valid and creates revision 1; distinguish it from never saved using revision/updatedAt, not by guessing from the values.

A.2 — Edit in the Recommendations modal

- Change Job Preferences opens the modal from the source frame. Load the latest record before initializing its draft rather than using potentially stale sidebar text.
- Use exactly the same fields, validation, endpoint, and expectedRevision semantics as the full-page editor. Not Now, close X, or Escape before submission discards the draft and restores focus to the trigger.
- While saving or reconciling an unknown result, do not dismiss the editor as though cancellation could undo a server update. A confirmed success closes it; a recoverable error leaves it open.

A.3 — Geographic preference on job detail

- After member eligibility and the current preference read succeed, compare a visible UC-04 job's location.id with locationIds.
- If locationIds is empty, there is no geographic restriction and no warning. If nonempty and the job city is not included, show `This job is outside your preferred locations.` If included, no mismatch warning is shown.
- This activates only UC-04's previously deferred geographic warning; it does not make the job unavailable or enable Apply. Geography is a preference, not an application eligibility gate.
- A preference-load failure is not equivalent to Any location. Suppress a potentially false warning, show `Location preferences could not be checked.` with Retry, and keep the job readable.

A.4 — Sign-in and public search

- This UC adds only `/profile/job-preferences` and `/profile/job-preferences/edit` to UC-02's accepted local next destinations. Other UC-02 allowlist rules remain unchanged.
- UC-03 `/jobs` remains a public, manually filtered catalog. Saving preferences neither changes its URL nor silently inserts filters on the next visit.

Exception Flow:

E.1 — Invalid preference or unavailable options

- Invalid enums, duplicate/unknown city IDs, wrong boolean type, and missing fields return VALIDATION_ERROR. Retain valid selections and focus the first invalid field.
- If location options fail to load, show the load error and Retry; do not submit a replacement list made from blank options or source-map text. Previously loaded saved IDs are not silently removed.

E.2 — Concurrent preference update

- A stale expectedRevision returns PREFERENCES_VERSION_CONFLICT. Explain that another editor saved newer preferences and offer Reload latest.
- Do not silently overwrite, merge the two records, or reinterpret a duplicate click as another independent preference update. After reviewing current values, the actor may make a new explicit save.

E.3 — Unknown save outcome or session loss

- After an ambiguous network result, GET preferences. If its canonical values match the draft, show the current saved values and proceed with a fresh recommendations read. If they differ, retain the draft for review against the current record; no automatic resubmission.
- A missing/expired/ineligible session clears private preferences and draft state and returns to UC-02. Temporary service failures preserve the last confirmed state and expose Retry.

UI Integration:

- File DH Dental Recruitment (Community), page Pages / Job Seeker (`1:2`).
- [Profile / Job Preferences, frame `2:4741`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4741): read-only preference rows and Edit.
- [Profile / Edit Job Preferences, frame `2:4811`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4811): radio groups, geography area, Cancel, and Save Changes.
- [Recommendations / Job Preferences modal, frame `2:3370`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3370): same groups, close X, Not Now, and Save Changes.
- These desktop contexts/screenshots were inspected on 2026-09-23. Responsive, loading, error, conflict, and option-selection behavior are implementation supplements, not captured source variants or a frozen dataset.
- Normalize the inconsistent `Partnership/Equality Interest` text to `Partnership / Equity Interest`, with the existing enum PARTNERSHIP_EQUITY. Preserve Any and Associate as distinct choices.
- Replace the unrelated Melbourne sample map with a labeled preferred-city multi-select and a readable list of selected cities. The city control is an explicit functional addition because the source map has no verified selection behavior. This scope uses no map drawing, radius, GPS, or external geocoding.
- The source Recommendations sidebar displays Employment: Permanent, but neither preference editor has an Employment input. Omit that saved-preference row rather than invent an employment preference; employmentType remains ordinary job-card data.
- Keep the profile tab active correctly. The modal uses named radio groups, keyboard focus containment, and focus restoration; at narrow widths, it fits the viewport and scrolls internally without hiding its action controls.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/job-preferences` | Read the current account's preference record |
| PUT | `/api/v1/job-seeker/job-preferences` | Replace the editable preference values |
| GET | `/api/v1/jobs/filter-options` | Reuse UC-03's public canonical location options unchanged |

Preference endpoints require the UC-02 browser session. GET has no body. PUT accepts application/json. No preference endpoint accepts query parameters, an account ID, or a job ID. The reused filter-options endpoint keeps the exact UC-03 success/error contract.

Request Body:

PUT body, all fields required:

```json
{
  "expectedRevision": 0,
  "practiceInterest": "ASSOCIATE",
  "availability": "PART_TIME",
  "healthBenefitsRequired": true,
  "locationIds": [
    "sugar-land-tx-us"
  ]
}
```

| Field | Exact rule |
| --- | --- |
| expectedRevision | Integer >= 0, equal to the last loaded preference revision |
| practiceInterest | ANY, ASSOCIATE, or PARTNERSHIP_EQUITY |
| availability | ANY, FULL_TIME, or PART_TIME |
| healthBenefitsRequired | Boolean, true or false |
| locationIds | Array of 0–3 distinct configured city ID strings; canonical response order is lexicographic by ID |

The research location vocabulary is exactly the UC-03 options: dallas-tx-us (Dallas, Texas), houston-tx-us (Houston, Texas), and sugar-land-tx-us (Sugar Land, Texas). Reuse the options response for display labels. Empty locationIds is unrestricted; do not send the string ANY or a null array. There is no employmentType, desiredPosition, radius, address, latitude, or longitude field in this request.

Matching semantics shared with UC-07:

- Practice ANY is inactive. For an active preference, a job matches if its requirements.practiceInterest equals the preference or the job value is ANY (open to either interest).
- Availability ANY is inactive. Otherwise job.availability must equal the selected value to match.
- healthBenefitsRequired false is inactive. When true, only job healthBenefitsOffered true matches; false and null do not satisfy a required benefit. Null means information was not provided, not that benefits are definitely absent.
- Empty locationIds is inactive. Otherwise a job matches LOCATION if job.location.id belongs to the saved city list; multiple cities are alternatives, not simultaneous requirements.
- These are comparison meanings. UC-07 defines how comparisons rank jobs; a nonmatch alone never blocks reading job details.

Successful Response:

GET and PUT return HTTP 200 with data containing exactly asOf and preferences. PUT:

```json
{
  "success": true,
  "message": "Job preferences saved.",
  "data": {
    "asOf": "2026-09-23T14:00:00.000Z",
    "preferences": {
      "revision": 1,
      "practiceInterest": "ASSOCIATE",
      "availability": "PART_TIME",
      "healthBenefitsRequired": true,
      "locationIds": [
        "sugar-land-tx-us"
      ],
      "updatedAt": "2026-09-23T14:00:00.000Z"
    }
  }
}
```

GET uses message `Job preferences loaded.` preferences contains exactly revision, practiceInterest, availability, healthBenefitsRequired, locationIds, and updatedAt. revision is a nonnegative integer. updatedAt is null only for the initial revision-0 state, otherwise a UTC ISO 8601 timestamp. locationIds is returned in canonical lexicographic order; array order does not express priority.

Initial GET before any save:

```json
{
  "success": true,
  "message": "Job preferences loaded.",
  "data": {
    "asOf": "2026-09-23T14:00:00.000Z",
    "preferences": {
      "revision": 0,
      "practiceInterest": "ANY",
      "availability": "ANY",
      "healthBenefitsRequired": false,
      "locationIds": [],
      "updatedAt": null
    }
  }
}
```

One successful PUT creates revision 1 or increments the current revision by one, even when the actor explicitly submits unchanged values. No request from this UC creates or returns a browser-session token.

Error Response:

All JSON errors use exactly `success: false`, `statusCode`, `code`, `message`, `timestamp` (UTC ISO 8601), and `path` (actual request pathname without query). Only VALIDATION_ERROR adds `errors`, an object mapping field paths to nonempty arrays of messages. Do not add `data: null`. Binary success responses are explicitly identified below; their errors still use this JSON envelope. Unknown failures use INTERNAL_ERROR rather than exposing internal details.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 409 | PREFERENCES_VERSION_CONFLICT | Your preferences changed in another session. Reload the latest version before saving. |
| 503 | JOB_PREFERENCES_UNAVAILABLE | Job preferences are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

409 applies only to PUT. A never-saved preference record returns the initial 200 representation, not 404. Unsupported JSON request media type uses 400 VALIDATION_ERROR with errors.request; no additional top-level error field is added.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T14:00:00.000Z",
  "path": "/api/v1/job-seeker/job-preferences",
  "errors": {
    "locationIds": [
      "Choose distinct locations from the available options."
    ],
    "healthBenefitsRequired": [
      "Choose Yes or No."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 409,
  "code": "PREFERENCES_VERSION_CONFLICT",
  "message": "Your preferences changed in another session. Reload the latest version before saving.",
  "timestamp": "2026-09-23T14:00:00.000Z",
  "path": "/api/v1/job-seeker/job-preferences"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Require the UC-02 browser session and an ACTIVE JOB_SEEKER account. Unverified email/mobile and an incomplete profile are allowed. Missing, expired, or account-ineligible sessions return 401 UNAUTHENTICATED; an otherwise valid unsupported-role session returns 403 ROLE_NOT_ALLOWED. Resolve the account from the session; no caller-supplied account identifier is accepted. These are feature eligibility rules, not additional verification steps.

Implement one JobPreferences record per account with revision, practiceInterest, availability, healthBenefitsRequired, locationIds, and updatedAt. GET of an absent record returns the documented defaults without writing. The preference revision is independent of UC-05 basic-profile revision: editing a name does not create a preference conflict, and editing preferences does not overwrite the desired position.

Validate the complete replacement against the UC-03 location vocabulary and the exact enums above. Canonicalize locationIds order and save all fields together. A stale revision makes no change, including concurrent first saves at revision 0. Location options are fixed for this research release; changing/removing them later requires an explicit data migration, not silent deletion of saved preferences.

The profile editor and Recommendations modal are two entry points to this same service, never separate preference stores. Store no map coordinates inferred from the screenshot. Persist no source hardcoded Employment: Permanent preference. GET and PUT do not create recommendation records, applications, notifications, or evidence of professional verification.

Use the same feature-level matching semantics in UC-07. The geographic warning can be derived in the frontend from the UC-04 public job location and this authenticated preference response; no changed UC-04 member-detail response schema or new matching endpoint is needed.

### Frontend UI Context

Reuse the React/TypeScript/Tailwind profile shell from UC-05 and one preference form component for the page and modal. Its controls show current persisted values, not the source's Full Time/Yes sample defaults. Show Any location for an empty city list; render selected labels as text even when the editor is closed.

The geography control lists the configured cities in their canonical display vocabulary, supports selecting/deselecting each, and visibly explains `No cities selected means any location.` Render no Melbourne map or guessed geospatial result. Show Yes/No for whether benefits are required; use helper text that No permits jobs with or without benefits.

Cancellation labels follow each source surface: Cancel on the page and Not Now in the modal. Clear form errors when the actor changes the associated field, while retaining a submit-level error until another confirmed result. Other unfinished navigation follows the unavailable-action policy of UC-05.

### Frontend Logic and API Context

Fetch preferences and UC-03 filter-options independently, and initialize the editor only when both have valid results. Capture expectedRevision at that point. Maintain local draft values separate from the last saved record; changing radio/city controls does not save automatically.

PUT sends the full preference object as JSON. On confirmed success, replace both the profile view and sidebar cache with the canonical response. In UC-07, discard prior recommendation results and fetch page 1; do not relabel old cards as newly calculated recommendations. A successful save followed by a failed recommendations read is still a saved preference with a separate results-load error.

After save, invalidate any visible UC-04 geographic comparison and recompute it from the saved locationIds and the currently loaded job city. Check that both results belong to the same active account/job before displaying a warning.

Keep UC-03 query state separate. Clear authenticated data on session/account changes, ignore out-of-order requests, and keep unavailable-options/service errors distinct from an intentional empty preference list. Explicitly integrate the new next destinations into UC-02 before linking unauthenticated direct-entry users to sign-in.

### Validation and Error-Handling Context

Reject unknown fields, wrong JSON types, unexpected request/query parameters, and duplicate multipart parts where applicable. Never coerce a string such as "false" to a boolean. Return all safely identifiable field validation errors together. Failed validation or a revision conflict leaves the previously saved state unchanged.

Use field paths expectedRevision, practiceInterest, availability, healthBenefitsRequired, and locationIds in errors. String booleans, null arrays, unknown cities, unsupported enum values, more than three IDs, and duplicate IDs are rejected. Do not silently interpret an invalid city list as unrestricted.

An incomplete basic profile is not a preference-save error. Missing desiredPosition is handled by UC-07 as recommendation setup, not by blocking this editor. A job outside the selected cities remains a readable job and must not cause an application or account error.

Keep the saved state intact on validation/conflict/service failure. A 401 removes private state; a 403 shows the unsupported-role state without simulating preferences for another role. Neither a lost response nor a successful save warrants an automatic second mutation.
