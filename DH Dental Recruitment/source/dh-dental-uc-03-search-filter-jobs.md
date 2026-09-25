# UC-03: Search and Filter Available Jobs

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Search and Filter Available Jobs

Description:

- Allows visitors and signed-in Job Seekers to browse open published dental jobs, search by text, filter by location/work schedule/specialism, and paginate results.
- Search, filters, and pagination are alternate ways to accomplish one job-discovery goal, not separate use cases. Results lead to UC-04 detail.
- Figma supports the list/card/filter controls. Search semantics, canonical job data, fixture normalization, API contracts, and state rules below are project decisions; this is not a Technical Report quotation.

Primary Actor:

Visitor or authenticated Job Seeker. Public job discovery does not require registration or a complete profile.

Preconditions:

- `/jobs` is reloadable and public. It replaces UC-02's standalone integration shell when this batch is installed.
- A finite experiment dataset of fictional jobs and location options is provisioned. Employer posting/admin workflows are not implied by these fixtures.
- Every visible job has a unique UUID and reference, canonical fields shared with UC-04, and a publication state. No user/account data is required to read the catalog.

Postconditions:

- Success: The actor sees the current matching jobs and result count with their applied filters represented in the URL. Selecting a card opens the same job record in UC-04.
- Empty success: No matching jobs produces a genuine empty state with reset controls, not an error or substituted recommendations.
- Failure: Preserve filter input and distinguish an unavailable catalog from zero matches. Viewing/filtering creates no application, saved preference, notification subscription, or account activity record.

Main Flow:

1. Open `/jobs`; fetch filter options and the requested result page.
2. Display matching cards in a three-column desktop grid, the filter sidebar, and pagination.
3. The actor enters text and presses Enter or the search icon. Normalize the submitted query and reset page to 1.
4. Selecting location or changing a checkbox applies the new filter combination and resets page to 1.
5. The backend evaluates visibility and all filters, sorts matching records, and returns the selected page and total counts.
6. Update the browser URL and replace cards only with a response for the latest requested state.
7. Selecting View Post opens `/jobs/:jobId`. Browser Back restores the prior list URL and fetches its current matching results.

Alternative Flow:

A.1 — Combining filters

- Empty q and no selections mean all currently visible jobs. Multiple selected availability values match any selected value; multiple specialisms likewise use OR. Different filter groups, location, and text combine with AND.
- q is a case-insensitive literal substring match against title, reference, location.label, or the canonical specialism label. Match the entire normalized q against each field independently; do not interpret wildcards, regex, or invent semantic/AI matching.
- No relevance or distance sort is implied. Sort publishedAt descending then UUID ascending for all combinations.

A.2 — Location and source corrections

- Location selects a configured city ID, not GPS detection or a radius search. Default is All locations, not the source's example Sugar Land.
- Use six canonical specialisms including General Dentist. Adding General Dentist to the filter repairs the source mismatch where a listed job category has no corresponding checkbox; normalize Office Stafs to Office Staff. Labels and enum corrections are project decisions.
- The source repeats job references and sample cards and shows conflicting Full Time/Part Time values across screens. Use one fixture record per job and consistent values; the example job J017249 is PART_TIME and PERMANENT everywhere.

A.3 — Empty or changed result set

- Zero matches returns items=[], totalItems=0, totalPages=0. Show `No jobs match your search.` and Clear filters.
- A valid page beyond totalPages returns items=[] with the requested page and true counts. Show `This result page is no longer available.` and an action to page 1; do not silently alter the URL.
- Pagination is a current read, not a frozen multi-page snapshot. New/closed jobs may change later pages; refresh uses the latest catalog.

A.4 — Signed-in browsing

- UC-02 changes the header identity but does not personalize this list. Search controls here do not save Job Preferences or claim a match to the account's geography.
- The public list remains usable if the browser session expires. Session-service failure must not be relabelled as a job-catalog failure.

Exception Flow:

E.1 — Invalid query

- Reject unsupported/duplicate query keys, unrecognized location/enums, invalid page, or excessive q with VALIDATION_ERROR. Browser UI offers reset/correction rather than crashing or silently treating invalid filters as All.

E.2 — Missing required fixture data

- A visible record lacking required identity/location/classification/publication fields is a catalog inconsistency. Return JOB_CATALOG_UNAVAILABLE rather than invent labels or publish malformed cards.
- Missing optional thumbnails are expected and use a neutral placeholder with the job title. A missing image is not proof the job is unavailable.

E.3 — Request failure or response race

- Show a catalog error and Retry while keeping the selected filters. Retain earlier results only with a stale label and their original applied-filter summary; never display them as matches for a newer query.
- Ignore superseded responses. A service failure does not clear account state or submit a new login.

UI Integration:

- [All Jobs, frame `2:1937`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1937), page Pages / Job Seeker (`1:2`), file `5PvZvQ4E6DepIhbL8D35cV`.
- Live design context/screenshot inspected on 2026-09-23: cards, View Post, Search, city selector, Full Time/Part Time, specialism checkboxes, and numbered Previous/Next pagination.
- Desktop grid/sidebar and header/footer follow the source. Supplemental UI includes All locations, corrected specialisms, Clear filters, counts, empty/error/loading states, and a single-column/mobile filter arrangement. No mobile frame or frozen dataset is asserted.
- Page size is nine to match the main source grid. Render actual counts/pages, not the source's hard-coded 1–10 examples. Disable previous/next at their applicable boundaries.
- Job Seekers navigation targets `/jobs`. Sign In/Sign Up use UC-02/01. Employer, candidate-directory, newsletter, and unimplemented footer actions remain unavailable until their contracts exist.

API Endpoint:

- `GET /api/v1/jobs/filter-options`
- `GET /api/v1/jobs`

Both are public read-only endpoints with no request body. filter-options accepts no query.

Request Body:

None. Job list accepts only these optional query keys:

| Key | Exact contract |
| --- | --- |
| q | String, trimmed with internal whitespace runs collapsed to one space; maximum 100 Unicode code points; empty means no text filter |
| locationId | One configured ID; omit for all locations; an empty value is invalid |
| availability | Comma-separated distinct values FULL_TIME,PART_TIME; omit for no restriction |
| specialism | Comma-separated distinct IDs from filter-options; omit for no restriction |
| page | Decimal integer 1–10000; default 1; no fractions/signs/exponents |

Reject repeated query keys, unknown keys, empty CSV entries, duplicate enum values, and values outside the declared sets. CSV order has no semantic effect; return applied arrays in filter-option order. No client-selected pageSize, owner, status, or sort.

Example: `/api/v1/jobs?q=dentist&locationId=sugar-land-tx-us&availability=PART_TIME&specialism=GENERAL_DENTIST,DENTIST_SPECIALIST&page=1`.

Browser `/jobs` uses exactly the same query representation. Clear filters navigates to `/jobs` with defaults. Do not put credentials or account information in the list URL.

Successful Response:

```json
{
  "success": true,
  "message": "Job filter options loaded.",
  "data": {
    "locations": [
      {
        "id": "sugar-land-tx-us",
        "label": "Sugar Land, Texas"
      },
      {
        "id": "houston-tx-us",
        "label": "Houston, Texas"
      },
      {
        "id": "dallas-tx-us",
        "label": "Dallas, Texas"
      }
    ],
    "availability": [
      {
        "id": "FULL_TIME",
        "label": "Full Time"
      },
      {
        "id": "PART_TIME",
        "label": "Part Time"
      }
    ],
    "specialisms": [
      {
        "id": "GENERAL_DENTIST",
        "label": "General Dentist"
      },
      {
        "id": "DENTIST_SPECIALIST",
        "label": "Dentist Specialist"
      },
      {
        "id": "DENTAL_HYGIENIST",
        "label": "Dental Hygienist"
      },
      {
        "id": "DENTAL_ASSISTANT",
        "label": "Dental Assistant"
      },
      {
        "id": "OFFICE_STAFF",
        "label": "Office Staff"
      },
      {
        "id": "OFFICE_MANAGER",
        "label": "Office Manager"
      }
    ]
  }
}
```

HTTP 200. Each option has exactly id and label, nonempty strings. Arrays use the order shown. Sugar Land is source-visible; Houston/Dallas and the canonical option set are research fixture choices. The catalog uses these same IDs; no geocoding service is necessary.

List HTTP 200, unfiltered example:

```json
{
  "success": true,
  "message": "Jobs loaded.",
  "data": {
    "asOf": "2026-09-23T10:00:00.000Z",
    "filters": {
      "q": "",
      "locationId": null,
      "availability": [],
      "specialism": []
    },
    "items": [
      {
        "id": "c6e6e207-0c96-49fd-8ffc-2f43550c254a",
        "reference": "J017249",
        "title": "General Dentist",
        "thumbnailUrl": null,
        "thumbnailAlt": "General Dentist vacancy",
        "location": {
          "id": "sugar-land-tx-us",
          "label": "Sugar Land, Texas"
        },
        "specialism": "GENERAL_DENTIST",
        "availability": "PART_TIME",
        "employmentType": "PERMANENT",
        "publishedAt": "2026-09-22T09:00:00.000Z"
      }
    ],
    "page": 1,
    "pageSize": 9,
    "totalItems": 1,
    "totalPages": 1
  }
}
```

- data has exactly asOf, filters, items, page, pageSize, totalItems, totalPages. asOf is server UTC. filters has exactly q (normalized string), locationId (nullable string), availability and specialism (arrays of IDs in option order).
- totalItems is the count after all filters; totalPages=ceil(totalItems/9), zero when empty. items length is 0–9. page reflects the requested page; pageSize is always 9.
- **JobCard** has exactly id, reference, title, thumbnailUrl, thumbnailAlt, location, specialism, availability, employmentType, publishedAt as shown. id is UUID; reference is a unique `[A-Z0-9-]{1,32}` display code; title is nonempty 1–160 characters; thumbnailUrl is null or configured public same-origin image URL; thumbnailAlt is nonempty descriptive text.
- location has exactly id and label from filter-options. specialism/availability use the canonical IDs. employmentType is PERMANENT, TEMPORARY, or CONTRACT, rendered as Permanent Employment, Temporary Employment, Contract Employment. Additional employment values are project enums, not inferred from source examples.
- publishedAt is UTC ISO 8601. A job is visible only when internal status=PUBLISHED, publishedAt<=asOf, and closesAt is null or strictly greater than asOf. DRAFT, CLOSED, future-dated, and expired jobs are excluded. Internal status/closesAt and all member-only fields are omitted from JobCard.
- Source image URLs are not permanent storage: implementation uses configured fixture assets or a placeholder. No salary, match score, applicant count, employer contact, or inferred certification is added to this response.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "JOB_CATALOG_UNAVAILABLE",
  "message": "Job listings are temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-23T10:00:00.000Z",
  "path": "/api/v1/jobs"
}
```

All errors use success=false, statusCode matching HTTP status, code, message, server UTC ISO 8601 timestamp, and actual pathname without query. Omit data. VALIDATION_ERROR includes errors mapping input field paths to nonempty arrays of strings. Other errors omit errors; a 429 response additionally has a positive integer retryAfterSeconds matching Retry-After. All successful fields shown or defined are required unless explicitly nullable.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 503 | JOB_CATALOG_UNAVAILABLE | Job listings are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Examples of errors keys: q, locationId, availability, specialism, page, or an unsupported query key. No 401 is required to browse these public resources.

## Project-Specific Implementation Context

### Backend Implementation Context

Implement public NestJS/TypeScript catalog reads from canonical fixture-backed Jobs. Use one visibility predicate and JobCard projection shared with UC-04. Evaluate page items/counts against one coherent read. Publication data and option identifiers are declared experiment data, not a claim that an employer management feature exists. Job reads have no account/application/preference mutation side effects.

### Frontend UI Context

Build the inspected list with React, TypeScript, and Tailwind. Keep consistent job classification labels, publication data, thumbnails, and references across cards/detail. Use the source desktop hierarchy and a supplementary narrow-screen layout, keeping all filters usable. Show fixture content as actual fictional records, not repeated unrelated cards sharing one ID.

### Frontend Logic and API Context

Use URL state as the committed filter/page state and maintain an independent unsent search-input draft. Submit search on Enter/icon; apply checkbox/location changes immediately. Reset page on filter changes, preserve browser history, and ignore responses for outdated requests. View Post uses the UUID, never the reference code, as its route identifier. This UC supplies UC-02's default working destination.

### Validation and Error-Handling Context

Validate all query values on the server and provide field-addressable errors. Distinguish no matches, an out-of-range page, malformed input, unavailable storage, and optional missing imagery. An expired session does not prevent public discovery. No mapping API, AI recommender, or saved-job operation is implied by the filter UI.
