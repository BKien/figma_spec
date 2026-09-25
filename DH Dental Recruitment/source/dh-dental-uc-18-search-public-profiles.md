# UC-18: Search and Filter Public Candidate Profiles

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Search and Filter Public Candidate Profiles

Description:

- Allows any visitor to browse, search, filter, and paginate only the candidate profiles explicitly published through UC-17.
- Uses the source's public profile grid and filters. Search semantics, preferred-city interpretation, stable ordering, and API contract are research decisions, not evidence of an employer account or hiring authorization workflow.
- A published position is the candidate's desired position, and skills/experience are self-declared; the directory is not a professional verification service.

Primary Actor:

Visitor or signed-in user.

Preconditions:

- UC-17 publication and UC-19 detail are implemented. Private new accounts are not automatically seeded into the directory.
- Implement reloadable public `/candidate-profiles` with the query rules below. Add a clearly named Browse candidates navigation entry; this entry is an integration supplement and does not imply employer role access.
- UC-03 GET filter-options supplies the shared location, availability, and specialism vocabularies unchanged.

Postconditions:

- Success: The directory shows one coherent page of visible public snapshots with correct total counts and applied filters.
- Empty: No matching visible profiles yields an honest empty state with Clear filters.
- Failure: A distinct error permits retry without substituting source sample people or private profiles.
- Search/read/navigation does not publish a candidate, modify job preferences, contact anyone, or create an application.

Main Flow:

1. Open Browse candidates and load filter options plus page 1 of public profiles.
2. Display candidate cards with name, desired-position badge, generated summary, optional published photo, and View Profile.
3. Enter a search query, choose a preferred work city, or select availability/specialism filters; apply the search and reset to page 1.
4. Request the matching page, render the canonical filters and counts, and preserve them in the browser URL.
5. Use pagination to request another page with the same filters.
6. Select View Profile to open UC-19 `/candidate-profiles/<id>`; browser Back restores the listing URL and reloads its current results.

Alternative Flow:

A.1 — Empty filters or flexible preferences

- No filters returns all currently visible publications. No selected availability/specialism values means no restriction on that dimension.
- A candidate snapshot with availability ANY matches either Full Time or Part Time filters. A snapshot with preferredLocations [] matches any selected city because it expresses no city restriction; show Any preferred location, never the filter's city as though the candidate chose it.

A.2 — Empty results or later page

- totalItems 0 gives items [], totalPages 0, and a No matching profiles message.
- A valid page beyond totalPages returns items [] with actual totals; show No profiles on this page and First page. Do not silently clamp the requested page.

A.3 — Reset and refresh

- Clear filters clears q/location/checkboxes and requests page 1. Explicit Search applies the text field; no typing-triggered API search is required.
- Each request reflects current publications. Pages do not promise a persistent snapshot across requests; private/closed profiles disappear on the next read.

Exception Flow:

E.1 — Invalid input or unavailable options

- Invalid query values return VALIDATION_ERROR; do not silently coerce unknown city IDs or invalid enums to All.
- If options fail, show Retry and do not remove stored URL selections as though they never existed. An options failure is not evidence of an empty candidate catalog.

E.2 — Visibility changed after listing

- UC-19 can return PROFILE_NOT_AVAILABLE if a profile was made private/closed after its card was returned. Offer Back to candidates; the listing refreshes on return.
- Do not preserve inaccessible candidate data as a cached fallback after a current read reports it unavailable.

E.3 — Catalog failure

- Show CANDIDATE_DIRECTORY_UNAVAILABLE separately from a legitimate empty result. Ignore older responses after filters/page change so they cannot overwrite a newer selection.

UI Integration:

- [Public profile directory, frame `2:1700`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1700), DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`), inspected with context/screenshot on 2026-09-23.
- Preserve the desktop three-column profile grid, right filter sidebar, View Profile, and pagination. Replace repeated source sample people with unique returned publications.
- Rename Location near by you to Preferred work location: the available data is UC-06 desired cities, not current location, distance, or GPS. Rename Job Type to Preferred availability, and normalize specialism labels using UC-03 (including General Dentist).
- Replace lorem ipsum card prose with UC-17's generated summary. No fabricated profile completion, employer contact, salary, or verified badge is added.
- Default/empty/loading/error states, the Browse candidates navigation link, result count, filter-reset action, and responsive stacking are project supplements. This inspection is not a frozen dataset.
- On narrow screens place filters above cards and preserve filter labels. A null photo uses neutral initials; it is not replaced with a source stock person's face.

API Endpoint:

- `GET /api/v1/candidate-profiles`
- Reuse `GET /api/v1/jobs/filter-options` from UC-03 unchanged.

Both are public. The directory has no body and accepts only the query parameters below; no user ID, employer role, publication override, or private-profile flag is accepted.

Request Body:

None. Query parameters:

| Parameter | Rule |
| --- | --- |
| q | Optional text, trim and collapse whitespace; 0–100 Unicode code points; default empty |
| locationId | Optional single UC-03 configured city ID; omission means all |
| availability | Optional comma-separated distinct FULL_TIME/PART_TIME values; omission means all |
| specialism | Optional comma-separated distinct UC-03 specialism enums; omission means all |
| page | Decimal integer 1–10000, default 1; digits only, no sign, leading zero, fraction, or whitespace |

Reject unknown/repeated query keys, empty enum/ID values, duplicate CSV values, invalid IDs/enums, or a supplied body. pageSize is fixed at 9. Browser `/candidate-profiles` uses the same query schema; construct the URL using normal query encoding.

Apply AND across q, locationId, availability, and specialism groups; OR among values within each enum group. q is a case-insensitive literal substring match against displayName, desired-position label, or a preferred-location label. It is not regex, fuzzy search, or a search of private fields. Matching a city via q examines actual published labels; the flexible empty-city rule applies only to the locationId filter.

Candidate pool requires PUBLIC plus an ACTIVE JOB_SEEKER owner. Sort by publishedAt descending, then public profile UUID lexicographically ascending, before pagination.

Successful Response:

```json
{
  "success": true,
  "message": "Candidate profiles loaded.",
  "data": {
    "asOf": "2026-09-23T18:00:00.000Z",
    "filters": {
      "q": "",
      "locationId": null,
      "availability": [],
      "specialism": []
    },
    "items": [
      {
        "id": "2d6b20d6-3297-4457-866e-302cae08074d",
        "displayName": "Alex Morgan",
        "desiredPosition": "GENERAL_DENTIST",
        "summary": "Seeking General Dentist.",
        "photoUrl": null,
        "preferredLocations": [
          {
            "id": "sugar-land-tx-us",
            "label": "Sugar Land, Texas"
          }
        ],
        "availability": "PART_TIME",
        "publishedAt": "2026-09-23T18:00:00.000Z"
      }
    ],
    "page": 1,
    "pageSize": 9,
    "totalItems": 1,
    "totalPages": 1
  }
}
```

HTTP 200. data has exactly asOf, filters, items, page, pageSize, totalItems, and totalPages. asOf is UTC ISO 8601 for the read. filters has exactly q, locationId (null when absent), availability, and specialism. Return availability in FULL_TIME/PART_TIME order and specialism in UC-03 option order, independent of CSV input order.

items contains 0–9 distinct PublicProfileCard objects with exactly id, displayName, desiredPosition, summary, photoUrl, preferredLocations, availability, and publishedAt as shown. These fields are an unchanged subset of UC-17's snapshot, not live private values. No ratings, contacts, account ID, source revisions, or private media URLs are added to cards.

page is the requested number, pageSize always 9, totalItems is the count after filtering before pagination, and totalPages is ceil(totalItems/9), or 0 when empty. Counts and items are evaluated against the same captured visible data for this response. A successful empty result retains every key.

Error Response:

All JSON errors contain exactly success false, statusCode, code, message, timestamp (server UTC ISO 8601), and path (actual pathname without query). Only VALIDATION_ERROR additionally contains errors, mapping field paths to nonempty message arrays. Other errors omit errors. Do not add data: null. No endpoint-specific rate budget is introduced in this UC.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 503 | CANDIDATE_DIRECTORY_UNAVAILABLE | Candidate profiles are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

No 401/403 is caused by a missing session on this public endpoint. Filter-options errors keep UC-03's contract.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T18:00:00.000Z",
  "path": "/api/v1/candidate-profiles",
  "errors": {
    "page": [
      "Page must be an integer from 1 to 10000."
    ]
  }
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Use NestJS/TypeScript over UC-17 publications. Require PUBLIC and an ACTIVE owner for each eligible record; do not query private profile content to fill missing fields or search hidden text. Snapshot publication time determines order, not registration date or private edit time.

Apply filters and ordering before slicing the requested page. Count only visible matching publications and compute counts/items from the same read state. A private or closed profile must not leak through counts, related lists, image delivery, or a stale unfiltered result cache.

Use shared UC-03 vocabularies but keep this endpoint distinct from job search: availability ANY and empty preferred cities have candidate-specific flexible semantics. Do not change UC-03's original job filter meanings.

No employer account, recruitment permission, candidate contact action, recommendation model, or automatic publication is needed to read this directory.

### Frontend UI Context

Implement the source grid/filter layout with React/TypeScript/Tailwind. Display full published names, desired-position labels, and summary; keep View Profile tied to the public UUID, not a source index or Account.id.

Render location descriptions truthfully when filters are flexible. Use option labels and clear checkbox group names. Pagination shows true totals and disables unavailable directions; never duplicate cards to fill the source's nine slots.

### Frontend Logic and API Context

Treat the URL as applied filter/page state and keep a typed text draft separate until Search. Applying any filter resets page to 1. Browser Back/Forward reloads the associated current results instead of reusing another filter's cards.

Fetch options independently, preserve a visible failure if they cannot load, and send only the exact query contract. Adopt the canonical filters returned by a successful read. Ignore outdated requests after navigation/filter changes.

Session checks are only for the shared header and must not block public results. View Profile uses `/candidate-profiles/<UUID>`. The public route needs no UC-02 next extension simply to browse it.

### Validation and Error-Handling Context

Validate all query keys/types and encode q literally; do not treat it as an executable expression. Report q, locationId, availability, specialism, page, or request paths. Preserve accents in search text and use case-insensitive comparison without silently inventing synonym matching.

Separate valid empty results, out-of-range pages, invalid input, and a service outage. Publication/private/closure changes must affect later reads; previously fetched content is not proof that a candidate remains publicly visible. No current residence or licensing eligibility is inferred from desired locations/position.
