# UC-07: View Personalized Job Recommendations

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View Personalized Job Recommendations

Description:

- Allows an authenticated Job Seeker to browse visible jobs in their saved desired position, ordered by how many active job preferences they satisfy.
- Uses UC-05 basic information and UC-06 preferences to provide a reproducible personalized listing. It differs from UC-03 manual public search and UC-04 related jobs; it creates no application or saved-job state.
- Figma supplies the Recommendations page, cards, sidebar, pagination, and preference-modal entry point. The recommendation rules, explanations, setup/empty/error states, route, and API contract are explicit research decisions. This is a deterministic feature; the UI does not claim AI prediction, a professional suitability score, or verified qualifications.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER.

Preconditions:

- UC-01/02 provide the account/session; UC-03 provides canonical jobs, JobCard, location/specialism labels, visibility, and public search.
- UC-04 job detail is reachable through `/jobs/:jobId`. UC-05 and UC-06 are implemented before this feature, including basic-profile and preference revisions.
- `/recommendations` is a real reloadable route, exposed through the authenticated Recommendations navigation. A saved desiredPosition is necessary for results, but the page also handles missing setup without an error or broken route.

Postconditions:

- Success: The actor sees a coherent listing computed from one captured desired position, preference record, and visible job set, with result count, current page, and understandable preference comparisons.
- Missing setup: Show how to supply a desired position and return no supposedly personalized cards. Empty catalog: Show no-results with a working public-search link.
- Failure: Show a separate unavailable state; never label cached results from an earlier account or preference version as current.
- Reading, paging, and opening a job do not change preferences, mark an application, record interest, send email, or publish the actor's profile.

Main Flow:

1. Select Recommendations after sign-in or open `/recommendations` directly.
2. Confirm the UC-02 session and request recommendations for page 1 (or the valid requested page).
3. The server captures the current UC-05 desiredPosition/basic revision and UC-06 preference values/revision, then determines the eligible visible jobs.
4. If desiredPosition is absent, show the setup state; otherwise rank the candidates by the rule below and paginate the result.
5. Render the desired-position heading, current saved-preference sidebar, job cards, match explanations, result count, and pagination.
6. Select View Post to open the UC-04 job-detail route. The current recommendation page remains available through browser Back.
7. Optionally open Change Job Preferences; UC-06 saves any changes, after which the listing reloads page 1 with the updated preferences.

Alternative Flow:

A.1 — Desired position not supplied

- Return HTTP 200 with state SETUP_REQUIRED, desiredPosition null, items [], activeCriteria [], totalItems 0, and totalPages 0. Include the current basicProfileRevision and preferences snapshot; no preferences are lost.
- Display `Choose your desired position to see job recommendations.` Link to `/profile/basic/edit`, whose save follows UC-05 and returns to its read page. The working Recommendations navigation then returns here; do not invent an unsupported auto-return parameter.
- The actor may still use Change Job Preferences or Browse all jobs. Do not substitute all jobs while calling them personalized.

A.2 — Preferences not saved or unrestricted

- Use the UC-06 initial representation if no record exists. No requirement to save default preferences is imposed.
- With all preference dimensions inactive, include all visible jobs in the desired position and sort by publishedAt descending, then job ID ascending. Match explanations say `No additional preferences selected.` rather than 100% match.

A.3 — Partial matches and no results

- Desired position is the only profile-based inclusion rule. Practice interest, availability, required health benefits, and selected cities affect order, not eligibility or visibility.
- Include partial and zero-preference matches after better matches, so the actor can inspect alternatives. Clearly show which active criteria are not met; do not label a partial match as satisfying all requirements.
- If no currently visible jobs have the desired specialism, return state READY with items [], totals 0, and offer `/jobs`. Never silently broaden the category or display a closed job.

A.4 — Paging, refresh, and newer profile settings

- A valid requested page beyond totalPages returns no items with the true totals. Show `No results on this page.` and a First page action; do not silently replace the page number.
- Each load captures current data. A later request may legitimately use newer preferences or job visibility. Page navigation and browser Back trigger a fresh read; this UC does not claim a persistent multi-request snapshot.
- When the returned basic/preference revision differs from the currently displayed revision, discard the old list. If the requested page is not 1, request page 1 once using current state, so a changed preference set does not strand the actor on an unrelated later page.
- Refresh is a new read, not a mutation or forced preference save.

Exception Flow:

E.1 — Session or account no longer eligible

- A 401 clears private recommendations and preferences and opens UC-02 sign-in. A 403 shows that this feature is unavailable for the current role.
- This UC extends the UC-02 next allowlist with `/recommendations` and `/recommendations?page=<valid integer>`, using exactly the page rule below and no other query keys/fragments. Encode the complete local destination as the value of the next query parameter when building the sign-in URL. Existing default `/jobs` behavior stays unchanged.

E.2 — Data source failure

- A failed preference/profile/catalog read returns RECOMMENDATIONS_UNAVAILABLE; do not replace it with revision-0 defaults or a successful empty list. A genuinely absent optional profile/preference record uses its documented initial representation.
- If preference saving succeeds but loading new recommendations fails, retain the confirmed sidebar settings and show a results retry panel. Do not roll back saved preferences or show earlier cards as current.

E.3 — A recommended job closes

- The next recommendations request omits it. If it closes after a card was returned, UC-04 returns JOB_NOT_AVAILABLE on detail access; provide Back and Browse all jobs.
- A card is not a guarantee of continued visibility, available positions, application acceptance, or matching benefits.

UI Integration:

- File DH Dental Recruitment (Community), page Pages / Job Seeker (`1:2`).
- [Job Seeker / Recommendations, frame `2:2956`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2956): desktop card grid, saved-preferences sidebar, Change Job Preferences, and pagination.
- [Job Preferences modal, frame `2:3370`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3370): UC-06's shared editor; do not create another preference contract.
- [Member job detail, frame `2:3837`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3837): UC-04 destination, with UC-06's now-defined geographic warning when appropriate.
- Recommendation and modal contexts/screenshots inspected on 2026-09-23; the detail frame was inspected for UC-04. These references are not a frozen dataset or evidence of source-defined ranking behavior.
- Normalize repeated sample cards to unique canonical job IDs. Keep UC-03/04 values consistent, including PART_TIME for fixture J017249, even where source card samples say Full Time.
- The source `$200,000/Year` has no amount/currency/pay-period contract in UC-03/04. Omit the salary row in this release; compensationType from member detail is not a salary amount and must not be substituted for one.
- Sidebar values come from the returned preferences snapshot. Omit the source's unsupported Employment preference row and Melbourne map; reuse UC-06 selected-city labels. The job cards still display their actual employmentType.
- Match explanations, setup/empty/loading/error states, Refresh, and narrow-screen composition are explicit UI supplements. Use a three-column card grid where space permits and stack cards/sidebar on narrow screens without changing result order.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/recommendations` | Read personalized ranked jobs for the signed-in account |

Dependencies are reused unchanged: UC-02 GET session; UC-03 GET filter-options for display labels; UC-05 profile read/edit; UC-06 GET/PUT job-preferences; UC-04 job detail. This UC introduces no recommendation-write, Apply, or AI-service endpoint.

Request Body:

None. GET accepts only the optional query parameter page:

| Parameter | Rule |
| --- | --- |
| page | Base-10 integer from 1 through 10000, default 1; digits only, no leading zero, sign, decimal, whitespace, or repeated key |

Example: `GET /api/v1/job-seeker/recommendations?page=1`.

Reject unsupported/repeated query parameters or a request body with 400 VALIDATION_ERROR. pageSize is fixed at 9 and cannot be supplied. The browser route uses the same page query rule; `/recommendations` represents page 1.

Do not accept an account ID, desiredPosition, preferences, sort field, match threshold, or client-computed score. The server reads authoritative saved values for the current session account. UI drafts in an open preference modal are not inputs until UC-06 confirms their save.

Successful Response:

HTTP 200, example with one matching job:

```json
{
  "success": true,
  "message": "Job recommendations loaded.",
  "data": {
    "asOf": "2026-09-23T14:00:00.000Z",
    "state": "READY",
    "basicProfileRevision": 1,
    "desiredPosition": "GENERAL_DENTIST",
    "preferences": {
      "revision": 1,
      "practiceInterest": "ASSOCIATE",
      "availability": "PART_TIME",
      "healthBenefitsRequired": true,
      "locationIds": [
        "sugar-land-tx-us"
      ],
      "updatedAt": "2026-09-23T14:00:00.000Z"
    },
    "activeCriteria": [
      "PRACTICE_INTEREST",
      "AVAILABILITY",
      "HEALTH_BENEFITS",
      "LOCATION"
    ],
    "items": [
      {
        "job": {
          "id": "c6e6e207-0c96-49fd-8ffc-2f43550c254a",
          "reference": "J017249",
          "title": "General Dentist",
          "thumbnailUrl": null,
          "thumbnailAlt": "General Dentist vacancy in Sugar Land, Texas",
          "location": {
            "id": "sugar-land-tx-us",
            "label": "Sugar Land, Texas"
          },
          "specialism": "GENERAL_DENTIST",
          "availability": "PART_TIME",
          "employmentType": "PERMANENT",
          "publishedAt": "2026-09-22T09:00:00.000Z"
        },
        "matchedCriteria": [
          "PRACTICE_INTEREST",
          "AVAILABILITY",
          "HEALTH_BENEFITS",
          "LOCATION"
        ],
        "unmatchedCriteria": []
      }
    ],
    "page": 1,
    "pageSize": 9,
    "totalItems": 1,
    "totalPages": 1
  }
}
```

Exact contract:

| Field | Meaning |
| --- | --- |
| asOf | UTC ISO 8601 time captured for this read and UC-03 visibility evaluation |
| state | READY or SETUP_REQUIRED |
| basicProfileRevision | Current UC-05 nonnegative revision, including 0 for its initial state |
| desiredPosition | UC-05 desiredPosition enum; null only for SETUP_REQUIRED |
| preferences | Complete UC-06 preference representation with its own revision and updatedAt |
| activeCriteria | Ordered subset of PRACTICE_INTEREST, AVAILABILITY, HEALTH_BENEFITS, LOCATION; [] for SETUP_REQUIRED |
| items | 0–9 distinct RecommendationItem objects |
| page | Requested page, including when empty or setup is required |
| pageSize | Always 9 |
| totalItems | Candidate count before pagination, not only fully matching jobs |
| totalPages | ceil(totalItems / 9), or 0 if totalItems is 0 |

Each RecommendationItem contains exactly job, matchedCriteria, and unmatchedCriteria. job is the unchanged exact UC-03 JobCard object shown above. Both criterion arrays use the activeCriteria order, contain no duplicates, and partition activeCriteria: every active criterion appears exactly once in one of them. No numerical probability, private contact details, or separate salary field is returned.

All data-object keys appear for READY and SETUP_REQUIRED. For SETUP_REQUIRED use the zero/empty values specified in A.1 while preserving page, pageSize, asOf, basicProfileRevision, and the actual preference representation. For a READY page outside the result range, retain actual totals and activeCriteria with items []. Never omit fields or return null instead of arrays.

The ranking is defined as follows, independent of pagination:

1. Include only UC-03-visible jobs: PUBLISHED, publishedAt <= asOf, and closesAt absent/null or > asOf. Include only specialism equal to desiredPosition. Desired position is an exact enum comparison, not title text matching.
2. Activate PRACTICE_INTEREST when preference is not ANY; AVAILABILITY when not ANY; HEALTH_BENEFITS only when required true; LOCATION only when locationIds is nonempty.
3. Evaluate every active criterion with UC-06's exact matching semantics. For the sample above, the seeded job has practiceInterest ANY (as specified in UC-04), PART_TIME, healthBenefitsOffered true, and city sugar-land-tx-us. Its member-detail data must agree with those values.
4. Order jobs by matchedCriteria.length descending, then publishedAt descending, then UUID lexicographically ascending. Each active criterion has equal weight; no hidden popularity, account age, verification, gender, name, language, or start-date factor is added.
5. Count the complete candidate set, then slice nine items for the requested page. No randomized filling or duplicate job cards.

The desired position narrows the candidate pool; criterion matches only order it. HEALTH_BENEFITS in unmatchedCriteria means a required benefit is not confirmed (false or null). Display `Health benefits requirement not confirmed` instead of asserting benefits are absent. For zero active criteria, both item arrays are empty and recency/ID determine order.

Error Response:

All errors use exactly success false, statusCode, code, message, timestamp (UTC ISO 8601), and path (the actual pathname without query). VALIDATION_ERROR additionally supplies errors as field-path keys with nonempty message arrays. Do not add data: null.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 503 | RECOMMENDATIONS_UNAVAILABLE | Job recommendations are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Missing desired position, a never-saved preference record, zero matches, and a valid page beyond the result range are 200 states, not 404/409 errors.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T14:00:00.000Z",
  "path": "/api/v1/job-seeker/recommendations",
  "errors": {
    "page": [
      "Page must be an integer from 1 to 10000."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 503,
  "code": "RECOMMENDATIONS_UNAVAILABLE",
  "message": "Job recommendations are temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-23T14:00:00.000Z",
  "path": "/api/v1/job-seeker/recommendations"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Require the UC-02 browser session and an ACTIVE JOB_SEEKER account. Unverified email/mobile and an incomplete profile are allowed. Missing, expired, or account-ineligible sessions return 401 UNAUTHENTICATED; an otherwise valid unsupported-role session returns 403 ROLE_NOT_ALLOWED. Resolve the account from the session; no caller-supplied account identifier is accepted. These are feature eligibility rules, not additional verification steps.

Use a read-only recommendation service in the proposed NestJS backend. Reuse UC-03 Job data and UC-04's canonical practiceInterest and healthBenefitsOffered values; do not parse screenshot labels or maintain recommendation-only duplicates. Use UC-05 desiredPosition and UC-06 preferences for the current account.

Capture one coherent profile/preference representation and job set for each response. Evaluate visibility against the single asOf and compute items/counts from the same captured candidate set. The echoed revisions identify the settings used for that response; do not read updated sidebar preferences later and attach them to cards ranked with old values.

Apply the declared deterministic ordering before pagination. Reuse the exact JobCard serialization of UC-03, without altering its public endpoint or its request schema. Member-only benefits data is used internally to compute the authenticated match criterion; unrelated office details/media remain in UC-04.

If the desired position is missing, return SETUP_REQUIRED with the actual preference snapshot and no ranking. Missing optional records use their defined defaults; read failures return 503. Do not add an overall profile-completion or contact-verification gate.

This feature needs no ML model, external AI API, training pipeline, automatic emails, application submission, persisted recommendation history, or background profile mutation. Its reproducible rule is a functional project decision necessary to define observable personalized behavior.

### Frontend UI Context

Reuse the authenticated shell and UC-03 job-card component. Add the source Recommendations active navigation and a sidebar showing practice interest, availability, whether benefits are required, and preferred-city labels from the returned snapshot. Heading uses the returned desired-position label, not a hardcoded General Dentist.

Under each card, show a concise preference summary such as `Matches 3 of 4 selected preferences`, plus readable matching/unmatched criteria. This is a count, not a probability or qualification claim. With no active criteria show `No additional preferences selected.` Do not use a misleading match percentage.

For partial matches, make the unmet dimensions discoverable without opening the job. Geography nonmatch is explained as outside preferred locations; benefits nonmatch uses not confirmed because null data is possible. Treat optional thumbnail null through the same UC-03 neutral card treatment.

Keep Change Job Preferences available in READY, empty, and SETUP_REQUIRED states. Link Browse all jobs to `/jobs` without copying private preferences into its query. Disable Previous/Next at boundaries, including totalPages 0; out-of-range pages offer First page. Preserve a distinct setup message and load error rather than one generic empty illustration.

### Frontend Logic and API Context

Load the session before calling the authenticated recommendation endpoint. Fetch display options independently; recommendation response values/revisions remain the authority for its heading/sidebar, even if a separately cached profile/preferences object is newer. Do not fabricate option labels from a failed options request; show an explicit retry state for missing labels.

Key displayed results by account, page, and returned profile/preference revisions. Cancel or ignore older in-flight responses after account/page/save changes. Refresh on route entry and browser Back; after a preference save or a detected changed desiredPosition, replace prior results with loading state and request page 1.

After UC-06 Save succeeds, adopt that canonical sidebar record and fetch recommendations. If the response reveals an even newer preference revision, display its coherent snapshot and inform the actor that newer preferences were loaded; do not overwrite it with the earlier save response. Do not continue showing cards that were ranked from the earlier values.

View Post navigates to the existing `/jobs/<UUID>` route and preserves the recommendation URL in browser history. Its details revalidate visibility through UC-04; source Interested/Apply controls do not become functional through this UC.

Browser query parsing follows the API page grammar. Invalid route input shows a validation state with a working First page action instead of coercing it to another page. Extend UC-02's specific next allowlist as declared, without permitting arbitrary nested next parameters or external navigation.

### Validation and Error-Handling Context

Validate page and reject unknown/repeated query keys before producing a successful response. Use errors.page for an invalid page and errors.request for unsupported input. No body means absent, not an object carrying client-side preference overrides.

Return only the two declared success states. Enforce exact candidate specialism and UC-03 visibility, unique job IDs, complete criterion partitions, consistent totals, and deterministic tie order. An unmet preference must not turn into a hidden eligibility block or category broadening.

Treat null benefits as unconfirmed for a required criterion. Treat ANY and empty locationIds as inactive criteria, not automatic points that inflate the displayed match count. Do not count desiredPosition as another scored criterion because all returned jobs already satisfy that inclusion rule.

A service failure must not be mistaken for no jobs, missing preferences, or SETUP_REQUIRED. Clear account-specific results on authentication loss, keep options/API errors separate, and allow deliberate read retries without changing saved preferences.
