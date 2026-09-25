# UC-20: Submit a Job Application

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Submit a Job Application

Description:

- Allows an authenticated Job Seeker to review the profile information included in an application and explicitly submit it for a currently visible job. The system stores one application per account/job and returns a persistent receipt.
- This activates UC-04's previously disabled Apply for this job action. It does not turn viewing a job, registering, logging in, or saving an introduction video into an application.
- Figma supports the Apply entry point only. Review/confirmation, submitted state, application persistence, eligibility, duplicate handling, and contracts are explicit research additions; no complete application or Hiring Manager workflow has been verified in the source.
- SUBMITTED means recorded by this research application. Employer delivery, employer review, interview scheduling, email/SMS, and a hiring decision are not implemented or implied.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER applying for a visible job.

Preconditions:

- UC-02 supplies the browser session. UC-03/04 supply visible jobs and the real `/jobs/:jobId` detail route.
- UC-05 supplies saved basic information with a non-null desiredPosition. UC-08/09 supply optional experience/education sections, including their documented initial states when never saved.
- Implement the review panel and application receipt on the existing job-detail route; no new dashboard or missing destination is required.
- UC-14 closure can remove application records and snapshots as part of the same account-data removal. UC-17 public visibility is independent: a private profile can apply without being published.

Postconditions:

- New success: Exactly one application and its immutable applicant snapshot are stored together for the account/job, with a submitted timestamp and receipt.
- Duplicate: An existing application returns its original receipt without changing its snapshot or timestamp, even if the profile has changed since submission.
- Failure: Invalid, ineligible, stale-preview, or unavailable-job requests create no application. An ambiguous response is reconciled through the application read endpoint before another deliberate action.
- No automatic recruiter message, public profile publication, resume/video sharing, contact verification, global profile-completion change, or employer workflow occurs.

Main Flow:

1. Open the UC-04 job detail and confirm the current account session.
2. Load this account's application state for the job. If an application already exists, display its receipt and Applied state.
3. Otherwise select Apply for this job. Load the current UC-05 basic, UC-08 work-experience, and UC-09 education sections, capturing their revisions; use UC-02's current account mobile number for the review.
4. Show the exact applicant fields to be recorded, the selected job title/reference, and the research delivery notice. If basic information is incomplete, offer its real edit route instead of Submit.
5. The actor selects Confirm application. Submit the reviewed account identity guard, captured section revisions, and confirmed true; do not submit a writable copy of account/profile fields.
6. The backend rechecks session/account eligibility and expected identity, current job visibility, absence of an existing application, and the reviewed source revisions, then stores the application and snapshot together.
7. Display `Application recorded.` with its reference/time, and replace Apply with Applied on the same detail page. No email or employer-delivery success is announced.

Alternative Flow:

A.1 — Visitor or missing setup

- A visitor uses UC-04's existing login form; sign-in only returns to the job page. It never submits an application automatically.
- Missing desiredPosition blocks only new application submission. Link to `/profile/basic/edit`; after saving, the actor returns to the chosen job through existing navigation/history and reviews again. Do not invent an unsupported return query on the profile editor.
- INCOMPLETE global profile status, unverified contacts, absent resume/video, empty education, and null experience/ratings do not block submission. No fabricated 90% threshold is used.

A.2 — Cancel review

- Cancel closes the review panel without a write. Reopening loads current profile sections and revisions again.
- Profile edits, job-view reads, public-profile publication, and video recording do not implicitly confirm an application. The review is not an editable duplicate profile form.

A.3 — Repeat submission or concurrent tabs

- One account/job pair has at most one application in this scope. A repeated valid POST returns the original receipt as HTTP 200, not a second application or a profile update.
- For an existing application, an outdated but well-formed source version does not block returning its receipt. Existing receipt lookup precedes readiness/source-version/job-visibility checks for a new application.
- Application withdrawal, editing, resubmission after withdrawal, and application-history listing have no inspected UI and are not separate features in this release.

A.4 — Job closes after submission

- A committed application remains recorded even when its job is no longer publicly visible. Its owner can read the receipt, which contains only the submission-time title/reference/ID, not closed job details.
- A direct `/jobs/:jobId` visit with a valid session checks application state independently. If public detail is unavailable but an owned receipt exists, show that receipt with `This job is no longer available.` and Back to jobs. This is a declared integration extension to UC-04's unavailable view.
- If no receipt exists and the job is not visible, return JOB_NOT_AVAILABLE. A closed job never accepts a new application.

A.5 — Applicant edits or makes public profile private

- Later changes to private profile fields or UC-17 visibility do not revise or remove an existing application snapshot. The review explicitly explains that it records the shown values at submission time.
- UC-14 account closure removes all owned application records and snapshots. A fresh account with the same email is a different applicant and never receives old receipts.

Exception Flow:

E.1 — Profile changed during review

- For a new application, a changed basic/work/education revision returns APPLICATION_PROFILE_CHANGED. Preserve no silently refreshed submission; reload the review and require confirmation again.
- Missing desiredPosition returns APPLICATION_PROFILE_NOT_READY. An absent optional work/education section is a valid revision-0 source, not a service error.

E.2 — Job or account becomes unavailable

- Unknown/malformed job IDs and jobs that are draft, closed, not yet published, or expired cannot receive new applications. Return JOB_NOT_AVAILABLE without storing a partial application.
- Missing/expired/ineligible session returns UNAUTHENTICATED; an otherwise valid unsupported role returns ROLE_NOT_ALLOWED. Check continued account eligibility at commit so closure cannot be followed by a late application record.

E.3 — Service failure or lost response

- On failure to persist both application and snapshot, no success receipt is returned. Keep the review with an explicit retry option.
- If the POST result is unknown, GET this account's application state. A returned receipt confirms an application exists; show its actual timestamp/ID, without assuming a losing concurrent request supplied its data.
- An application null response means none existed at that read, not proof an earlier in-flight POST can never finish. A deliberate retry remains safe through account/job uniqueness; do not create another logical application ID on every click.
- If reconciliation fails, show outcome unknown and Retry read. Do not send an email, retry credentials, or silently switch to a new account to recover.

UI Integration:

- File DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`).
- [Member job detail, frame `2:3837`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-3837): Apply for this job entry point; live context/screenshot inspected again for this UC on 2026-09-23.
- Replace UC-04's Applications are not available yet disabled behavior with this full flow only once the endpoints and review/receipt states are implemented. Guest sign-in, job visibility, and existing detail contracts stay unchanged.
- Review panel, missing-setup link, confirmation, Applied state, receipt, closed-job receipt state, loading/errors, and responsive behavior are explicit supplements; no full source application flow or frozen dataset is claimed.
- Before confirmation state: `This records an application in the research prototype using the profile information shown below. It does not send an email or deliver information to an employer. Your resume, profile photo and introduction video are not included. Later profile edits will not update this recorded application.`
- Show names, email/mobile, desired position, languages/start availability, experience/certification declarations, ratings, and education using labels from their owning UCs. Mark optional missing values clearly and self-declarations as unverified.
- Do not copy the source's 90% completion bar or infer that recommendations/geographic preference are eligibility requirements. Keep Cancel and Confirm application keyboard-accessible; submitting disables duplicate confirmation.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/jobs/:jobId/application` | Read the owner's receipt or no-application state |
| POST | `/api/v1/job-seeker/jobs/:jobId/application` | Record one application, or return the existing receipt |

Both require the UC-02 session, reject query parameters, and derive the applicant from that session. GET has no body; POST accepts application/json. Reuse existing profile reads for review; this UC changes none of their response schemas.

Request Body:

```json
{
  "expectedAccountId": "137a3a0f-dc84-460d-9c97-03f3cf6dcae7",
  "expectedProfileVersions": {
    "basic": 1,
    "workExperience": 1,
    "education": 1
  },
  "confirmed": true
}
```

Exactly three required top-level keys. expectedAccountId is a UUID captured from the account shown in review. It is a comparison guard, not an account selector; it must equal the current session account before any receipt lookup or new submission. confirmed must be boolean true. expectedProfileVersions contains exactly basic, workExperience, and education, each a nonnegative integer captured from the review's source reads. Missing optional sections use revision 0; basic must be a saved section with a desired position for a new application.

No target-account selector, applicant contact values, profile payload, application status, public-profile ID, attachment, employer address, job title, or redirect target may be supplied. jobId is the UC-03 job UUID in the path; it is not the public candidate-profile UUID.

Malformed body/types/extra fields use VALIDATION_ERROR. The account/job pair itself provides duplicate prevention; this single-application-per-job workflow does not need a separate client request ID.

Successful Response:

```json
{
  "success": true,
  "message": "Application recorded.",
  "data": {
    "application": {
      "id": "bd9dcb22-653e-4453-8dca-c814e3565652",
      "job": {
        "id": "c6e6e207-0c96-49fd-8ffc-2f43550c254a",
        "reference": "J017249",
        "title": "General Dentist"
      },
      "status": "SUBMITTED",
      "submittedAt": "2026-09-23T19:00:00.000Z",
      "deliveryStatus": "NOT_IMPLEMENTED"
    }
  }
}
```

POST returns HTTP 201 for a new application and HTTP 200 for an existing one. Both return message Application recorded. and exactly data.application. The ApplicationReceipt has exactly id (server UUID), job (exactly id, reference, title captured at submission), status (always SUBMITTED), submittedAt (original UTC ISO 8601), and deliveryStatus (always NOT_IMPLEMENTED).

GET returns HTTP 200 with message `Application state loaded.` and the same data shape: application is the owned receipt or null. null is returned only if no owned application exists and the job is currently visible. A no-longer-visible job with no owned receipt returns JOB_NOT_AVAILABLE. A receipt remains readable when the job is closed/removed; it uses its stored summary rather than exposing the hidden job.

The receipt does not contain the private applicant snapshot. Existing-record responses always preserve original ID, time, and job summary; they do not rebind to current profile data.

The backend stores this exact applicantSnapshot shape with a new application (illustrative values):

```json
{
  "firstName": "Alex",
  "lastName": "Morgan",
  "email": "alex.morgan@example.com",
  "mobileNumber": "+12025550123",
  "desiredPosition": "GENERAL_DENTIST",
  "fluentLanguages": [
    "en"
  ],
  "availableStart": {
    "mode": "IMMEDIATELY",
    "month": null
  },
  "experienceBand": "ONE_TO_THREE",
  "boardCertification": "NOT_APPLICABLE",
  "ratings": {
    "endodontics": 4,
    "orthodontics": 2,
    "prostheticsRestorative": 2,
    "oralSurgeryImplants": 1
  },
  "education": [
    {
      "programCode": "DDS_DMD",
      "otherProgramName": null,
      "completionYear": 2009
    }
  ]
}
```

Snapshot field rules come from UC-01/05/08/09. ratings has all four keys, each nullable; education is the canonical entries array and may be empty. experienceBand and boardCertification may be null when never saved. Contact values are canonical Account values; name/basic values come from the reviewed basic revision. The server captures these values, not client input.

Store the three source revision values internally alongside the snapshot. Do not store photo/resume/video bytes or their private URLs, public-profile snapshot, health-benefit/job-preference settings, passwords, or session credentials in an application. This snapshot is not returned by a public endpoint or exposed to an employer UI in this scope.

Error Response:

All errors contain exactly success false, statusCode, code, message, timestamp (server UTC ISO 8601), and path (actual request pathname without query). Only VALIDATION_ERROR additionally contains errors mapping field paths to nonempty message arrays. No data: null is added and no endpoint-specific rate budget is introduced here.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 404 | JOB_NOT_AVAILABLE | This job is not available. |
| 409 | ACCOUNT_CONTEXT_CHANGED | The signed-in account changed. Review the application again. |
| 409 | APPLICATION_PROFILE_NOT_READY | Complete your basic profile before applying. |
| 409 | APPLICATION_PROFILE_CHANGED | Your profile changed. Review the latest information before applying. |
| 503 | APPLICATION_UNAVAILABLE | Applications are temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

APPLICATION_PROFILE_NOT_READY and APPLICATION_PROFILE_CHANGED apply only to new POST submissions. ACCOUNT_CONTEXT_CHANGED applies to any POST whose identity guard does not match, including a potential receipt replay. Existing receipt replay is 200, not a duplicate-error response. Wrong request content type and unsupported query/body keys use VALIDATION_ERROR.

```json
{
  "success": false,
  "statusCode": 409,
  "code": "APPLICATION_PROFILE_CHANGED",
  "message": "Your profile changed. Review the latest information before applying.",
  "timestamp": "2026-09-23T19:00:00.000Z",
  "path": "/api/v1/job-seeker/jobs/c6e6e207-0c96-49fd-8ffc-2f43550c254a/application"
}
```

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T19:00:00.000Z",
  "path": "/api/v1/job-seeker/jobs/c6e6e207-0c96-49fd-8ffc-2f43550c254a/application",
  "errors": {
    "confirmed": [
      "Confirm this application before submitting."
    ]
  }
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Use NestJS/TypeScript and an Application record uniquely associated with the current Account and job UUID. Persist the receipt fields, immutable job summary, applicantSnapshot, and source versions. No employer foreign-key workflow or message-delivery adapter is required to record it.

After session/input validation and expectedAccountId comparison, look for an existing owned account/job application first. Return its original receipt if present, even when the job later closes or the profile no longer meets new-submission readiness. For a new application, evaluate UC-03 job visibility and applicant source versions/desiredPosition and capture the snapshot coherently through commit.

Job visibility and account eligibility must still hold when a new application commits. If job closure wins first, the new write returns JOB_NOT_AVAILABLE; if application commits first, preserve its receipt. Concurrent valid submits for one account/job yield one committed record; the other returns its receipt. Do not allow a duplicate-row failure to become a spurious 500 or silently overwrite the winner's snapshot.

Explicit integration extension to UC-14: delete all owned Application records, applicant snapshots, job summaries, and receipt associations in the account-closure transaction. Existing jobs and other applicants' records remain intact. A late application write must not recreate data after closure. There are no application file copies requiring another media lifecycle.

Persist applications until account closure in this research release, even when a job closes; no application-history retention or employer archive is implied. Public-profile privacy changes do not delete applications, and applications do not make profiles public.

There is no automatic email/text, hiring-manager inbox, interview request, selection status, or account-profile completion calculation. SUBMITTED is the local recorded state defined by this contract, not evidence of employer receipt.

### Frontend UI Context

Use React/TypeScript/Tailwind and UC-04's existing Apply placement. Add a review panel styled consistently with profile cards; its fields are read-only. Show enough information to understand the submitted snapshot, including contact details and the attachment exclusion, before Confirm.

Applied state uses the actual server receipt, not a local flag remembered after a button click. Show the stored job reference/time and a concise no-delivery notice. Do not imply the candidate has been shortlisted or that an employer will reply.

If the job has closed but an owned receipt is available, render the receipt as a compact state within the existing route without revealing old member-office data. Direct-entry users always have a working Back to jobs link. Do not add an unsupported application-history dashboard solely as a success destination.

### Frontend Logic and API Context

On authenticated job detail, read the application state independently of the current public job result. Never treat a failed application read as application null. Load review source sections only for a deliberate new application; retain their revisions with the shown draft.

The application preview belongs to the current session identity. If the account changes, close the panel and discard the review; never send another account's revisions or imply the same applicant remains active. The server compares expectedAccountId before using any profile versions and captures only that matching session account's source values; coincidentally equal revisions in another account do not authorize submission.

Submit exactly expectedAccountId, expectedProfileVersions, and confirmed true. On ACCOUNT_CONTEXT_CHANGED close the stale review, reload identity, and require a new deliberate review. On 201/200 use the canonical receipt and refresh Applied state. On source change reload all displayed sources and require a fresh confirmation. On 404 discard new-submission controls and reconcile any receipt. On 401 clear private review/receipt state and use existing sign-in navigation.

For unknown outcomes, GET the owned state before offering a deliberate retry. A receipt can reflect a concurrent submission and is still the one authoritative application. Ignore late responses after route/account changes and do not automatically submit after login, profile save, or timer expiry.

### Validation and Error-Handling Context

Validate UUID path, expectedAccountId guard, exact JSON types/keys, integer source versions, confirmed true, and shared account eligibility. Use expectedAccountId, expectedProfileVersions.<section>, confirmed, or request field paths. A malformed job UUID follows the uniform JOB_NOT_AVAILABLE response.

New applications require saved basic information with desiredPosition, not public visibility, verified contacts, completed work/education, a resume/video, or a percentage threshold. A preference mismatch is never a hidden application block. The account's desired position need not equal the target job's specialism; applying is an explicit choice, not proof of qualification.

Distinguish optional initial sections from source-read failure; the latter returns APPLICATION_UNAVAILABLE. Store applicant snapshot/receipt together or not at all. Handle duplicate replay before new-readiness/visibility checks after eligibility/input validation and expected identity comparison.

Do not return private snapshot fields in the receipt or public job response, and do not equate local storage with employer delivery. Preserve the explicit account-closure integration so this new data category does not outlive the closed account contrary to UC-14.
