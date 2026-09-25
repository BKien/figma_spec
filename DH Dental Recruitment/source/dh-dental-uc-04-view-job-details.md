# UC-04: View Job Details

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View Job Details

Description:

- Allows a visitor to inspect a published job's public description, requirements, and office summary. An authenticated eligible Job Seeker can additionally view the member-only office information and available media.
- Reuses the public and signed-in detail compositions without inventing a complete Apply flow. Viewing, signing in, and opening media do not create an application or record interest.
- Figma provides the visible detail sections. Audience boundaries, null handling, related-job ranking, media delivery, and API contracts are project decisions; backend behavior is not established by a static frame.

Primary Actor:

Visitor or authenticated ACTIVE JOB_SEEKER. An incomplete profile and unverified contacts do not prevent reading member details under UC-01/02.

Preconditions:

- UC-03 defines canonical Jobs, JobCard, options, and visibility. UC-02 provides browser login/session.
- `/jobs/:jobId` is reloadable. Member media fixtures, when present, resolve to usable files associated with this job; fixtures use fictional practice information.
- There is no application-submission, professional verification, job-preference matching, or employer management service in this batch.

Postconditions:

- Success: Public sections show one canonical job and related jobs. Eligible authenticated readers can load additional office data and available media.
- Failure: Show unavailable/error state without stale member data from another job or account. A missing optional photo/video is displayed as unavailable content, not a failed job read.
- No application, saved job, recruiter contact, profile change, preference update, or notification is created by a detail read or login on this page.

Main Flow:

1. Open a View Post link from UC-03 or a direct `/jobs/:jobId` URL.
2. Fetch public job detail and check the current browser session independently.
3. Display job title/reference, city, publication date, description, availability, employment type, practice interest, office type/operatories, and related jobs.
4. For a visitor, show the compact UC-02 form and the source invitation to log in for further office information. Interested in this job focuses that form; it does not submit interest.
5. The Job Seeker signs in through UC-02. Confirm the browser session and reload the public visibility state plus member-only detail for this job.
6. Display health benefits, compensation type, equipment, geographic information, photos, and introduction video when supplied.
7. The actor can browse available photos, play/pause the video, open a related job, copy the canonical job link, or return to jobs.

Alternative Flow:

A.1 — Already authenticated

- After confirming the current session, load member detail directly. Hide the redundant login form. An incomplete profile is not a reason to display a fabricated 90% progress bar or block office information.
- Do not show the source's out-of-preferred-geography warning until a future Job Preferences UC defines a matching rule and supporting data. Omit the sample Profile Completion percentage until its calculation exists.

A.2 — Missing optional content

- Null healthBenefitsOffered or compensationType displays `Not provided`, not No or a guessed salary. Equipment values null are distinct from false.
- Empty officePhotos shows `No office photos provided.` Null introductionVideo shows `No introduction video provided.` Optional media is not replaced with unrelated source stock footage.
- No map image shows the provided address and, if both are present, coordinates; never display the source's unrelated example map. No live geocoding or external map service is required.

A.3 — Related jobs and navigation

- Return at most four other currently visible jobs. Rank by same specialism first, then same location, publishedAt descending, UUID ascending. Exclude the current job and duplicates; do not fill remaining spaces with closed jobs.
- Use the same relatedJobs array for the side list and optional bottom recommendations section. It is rule-based related content, not personalized recommendations.
- Browser Back returns to the prior listing filters where available. A supplementary Back to jobs link always opens `/jobs` for direct-entry users.

A.4 — Apply, registration, and sharing boundaries

- For a signed-in Job Seeker, preserve Apply for this job as a disabled action with `Applications are not available yet.` A later application UC must define submission, duplicate handling, and confirmation before enabling it.
- Register opens UC-01 `/sign-up`. This UC does not extend that registration contract with job IDs or promise automatic return/application. Registration success continues through the standard sign-in flow.
- Enable only the source copy-link share action: copy the application-origin `/jobs/<UUID>` URL without filters, session data, or private asset links. Announce success only after clipboard success; if unavailable, present selectable URL text. Other external social-share buttons remain unavailable in this scope.

Exception Flow:

E.1 — Unavailable job

- Unknown/malformed job IDs, unpublished/closed/future/expired jobs all return JOB_NOT_AVAILABLE. A previously listed job can close before detail or media access; show the same unavailable result with Back to jobs.
- Public detail, member detail, and each media request recheck current UC-03 visibility. A session does not grant access to closed or draft jobs.

E.2 — Missing or wrong-role session

- Member detail/media requires a valid ACTIVE JOB_SEEKER session. Missing, expired, or account-ineligible sessions return UNAUTHENTICATED; an otherwise valid session with a role unsupported by this feature returns ROLE_NOT_ALLOWED.
- Clear rendered member data/media on loss of eligibility, and retain/refetch public detail. Current UC-02 only establishes JOB_SEEKER sessions; the explicit role boundary also prevents accidental access if later roles are added.

E.3 — Media or service failure

- Missing/wrong-job/unconfigured asset returns JOB_MEDIA_NOT_AVAILABLE. Backend media service failure uses JOB_DETAILS_UNAVAILABLE; image/video decode failure shows an inline media error and does not invent alternate content.
- Member-detail failure must not be displayed as an empty successful response. Keep public content with a distinct retry panel. Public-detail failure must not show an earlier job as the selected one.
- Ignore stale responses after job/account changes and stop media from the prior page. Session checks do not themselves publish private profile or contact data.

UI Integration:

- File DH Dental Recruitment (Community), `5PvZvQ4E6DepIhbL8D35cV`, page Pages / Job Seeker (`1:2`).
- [Job Details, public frame `2:2309`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-2309): public summary, requirements, office description, compact login, related jobs, and sign-in invitation.
- [Job Seeker / Recommendations / Details, frame `2:3837`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3837): additional requirements/equipment, geography/map, office photos, video, and Apply action. Reuse its authenticated detail sections without claiming its personalized recommendation flow is implemented.
- Both contexts/screenshots inspected on 2026-09-23. These are desktop references, not a frozen dataset or proof of complete prototype behavior. Error/null/loading states, inactive actions, media controls, and responsive layout are project supplements.
- Normalize duplicate requirements blocks to one displayed section. Use the same job values as UC-03; never mix a Full Time card with this Part Time detail for the same ID. Replace historic sample publication dates with actual fixture publishedAt, formatted as an unambiguous UTC date.
- On narrow screens show main description before supplemental panels. Photo navigation has named Previous/Next controls, with no wrap at boundaries; video uses ordinary browser playback controls and never autoplays.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/jobs/:jobId` | Public detail and related jobs |
| GET | `/api/v1/job-seeker/jobs/:jobId/details` | Member-only data |
| GET | `/api/v1/job-seeker/jobs/:jobId/assets/:assetId` | Member-only image/video bytes |

Login uses UC-02; no Apply or Record interest write endpoint exists in this UC.

Request Body:

None. All endpoints reject query parameters; jobId and assetId are UUIDs. Media may receive the browser's byte Range header, as described below; it is not an application query. No client-supplied account, role, profile-completion, or location-preference fields.

Successful Response:

```json
{
  "success": true,
  "message": "Job details loaded.",
  "data": {
    "asOf": "2026-09-23T10:00:00.000Z",
    "job": {
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
    },
    "description": "A fictional dental practice is seeking a part-time general dentist for scheduled outpatient appointments.",
    "requirements": {
      "practiceInterest": "ANY"
    },
    "office": {
      "type": "GENERAL_PRACTICE",
      "numberOfOperatories": 7
    },
    "relatedJobs": []
  }
}
```

Public detail HTTP 200:

- data has exactly asOf, job, description, requirements, office, relatedJobs. job and each relatedJobs entry use the exact UC-03 JobCard. description is plain text, 1–20,000 characters.
- requirements has exactly practiceInterest: ANY, ASSOCIATE, or PARTNERSHIP_EQUITY, rendered Any, Associate, Partnership/Equity Interest. This finite canonical set is a project normalization.
- office has exactly type and numberOfOperatories. type is GENERAL_PRACTICE, SPECIALIST_PRACTICE, or null (Not provided); numberOfOperatories is integer 1–100 or null. It is not an applicant count.
- relatedJobs length is 0–4 using A.3. No authenticated media URLs, detailed address, coordinates, compensation, equipment, or applicant/contact data is included in the public response, regardless of whether the caller happens to be signed in.

Member detail HTTP 200:

```json
{
  "success": true,
  "message": "Member job details loaded.",
  "data": {
    "asOf": "2026-09-23T10:00:00.000Z",
    "jobId": "c6e6e207-0c96-49fd-8ffc-2f43550c254a",
    "healthBenefitsOffered": true,
    "compensationType": null,
    "equipment": {
      "hardTissueLaser": false,
      "softTissueLaser": true,
      "microscope": false,
      "digitalIntraoralRadiography": true,
      "extraoralImaging": true,
      "inOfficeMilling": false
    },
    "geographicLocation": {
      "address": "Fictional Practice, Sugar Land, Texas",
      "latitude": null,
      "longitude": null,
      "mapImage": null
    },
    "officePhotos": [],
    "introductionVideo": null
  }
}
```

- data has exactly asOf, jobId, healthBenefitsOffered, compensationType, equipment, geographicLocation, officePhotos, introductionVideo. asOf is server UTC; jobId must match the requested public job.
- healthBenefitsOffered is boolean or null. compensationType is SALARY, HOURLY, PRODUCTION_BASED, or null; display Salary, Hourly, Production-based, Not provided. No amount is inferred from a type.
- equipment has exactly the six shown keys, each boolean or null. Correct source text Digital Intraloral Radiography to Digital Intraoral Radiography without changing its meaning.
- geographicLocation is null or exactly {address,latitude,longitude,mapImage}. address is a nonempty display string, at most 500 characters; coordinates are both null or numbers latitude -90..90/longitude -180..180. mapImage is null or an ImageAsset as defined below.
- officePhotos is an ordered array of 0–10 ImageAssets; introductionVideo is null or VideoAsset. IDs are unique per asset within a job. Source absence of a photo/video is represented by []/null, not a public third-party URL.
- **ImageAsset** has exactly {id,url,alt}; id UUID, url the same-origin member asset endpoint for this job, alt nonempty text. **VideoAsset** has exactly {id,url,poster,durationSeconds}; poster null or ImageAsset, durationSeconds positive integer matching the configured media to within one second. No arbitrary external asset URL or filesystem path is exposed.
- Missing optional fixture values remain null. A configured but broken media reference is reported on media loading rather than silently rewritten as no media.

Media HTTP 200 returns actual image/video bytes, not the JSON envelope, with the matching Content-Type (image/jpeg, image/png, image/webp, video/mp4, or video/webm). A satisfiable single bytes Range returns 206 with corresponding Content-Range, Content-Length, and bytes. An invalid/unsupported range returns 416 RANGE_NOT_SATISFIABLE and `Content-Range: bytes */<full-size>`. Multiple ranges are unsupported. Media requests require the same current session, job visibility, and asset/job association checks as member detail. No photo/video upload pipeline is part of this read-only UC.

Error Response:

```json
{
  "success": false,
  "statusCode": 404,
  "code": "JOB_NOT_AVAILABLE",
  "message": "This job is not available.",
  "timestamp": "2026-09-23T10:00:00.000Z",
  "path": "/api/v1/jobs/c6e6e207-0c96-49fd-8ffc-2f43550c254a"
}
```

All errors use success=false, statusCode matching HTTP status, code, message, server UTC ISO 8601 timestamp, and actual pathname without query. Omit data. VALIDATION_ERROR includes errors mapping input field paths to nonempty arrays of strings. Other errors omit errors; a 429 response additionally has a positive integer retryAfterSeconds matching Retry-After. All successful fields shown or defined are required unless explicitly nullable.

| Endpoint | HTTP | Code | Exact message |
| --- | --- | --- | --- |
| All | 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| Member/media | 401 | UNAUTHENTICATED | Please sign in to continue. |
| Member/media | 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| All | 404 | JOB_NOT_AVAILABLE | This job is not available. |
| Media | 404 | JOB_MEDIA_NOT_AVAILABLE | This job media is not available. |
| Media | 416 | RANGE_NOT_SATISFIABLE | This media range is not available. |
| All | 503 | JOB_DETAILS_UNAVAILABLE | Job details are temporarily unavailable. Please try again later. |
| All | 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Errors are JSON, including media errors. Malformed job IDs use JOB_NOT_AVAILABLE; malformed/foreign asset IDs under an otherwise available job use JOB_MEDIA_NOT_AVAILABLE. Member authentication is evaluated before returning member data. Public detail never requires authentication.

## Project-Specific Implementation Context

### Backend Implementation Context

Use NestJS/TypeScript with UC-03 Jobs and visibility. Build separate public and member projections so unavailable member sections are not merely hidden after transmitting them in public JSON. Serve configured member asset bytes through the declared account/job-scoped resource. Read operations never create applications or interaction records. Related jobs share the public visibility/card projection, and closed jobs disappear consistently from both list and detail reads.

### Frontend UI Context

Implement the public and signed-in compositions in React/TypeScript/Tailwind using source spacing, cards, typography, teal actions, and office sections. Reuse UC-02's compact login component. Distinguish Not provided from No, media errors from no media, and job closure from a service outage. Omit unimplemented match/progress claims and explain disabled Apply.

### Frontend Logic and API Context

Load public content independently of member authentication. Key private caches by current account and job; clear them when either changes or session becomes unusable. After inline sign-in, confirm the session and fetch current member detail; never derive member eligibility from the submitted email. Photo/video URLs are resolved from member responses, not guessed from asset filenames. Copy only the public canonical job URL.

### Validation and Error-Handling Context

Validate UUID nesting, current visibility, session eligibility, asset membership, and range semantics on the server. Keep the source-inspired public/member distinction observable without prescribing security algorithms. This UC is complete as a viewing goal; the later application UC must explicitly replace the unavailable action before any submission can occur.
