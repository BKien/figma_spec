# UC-17: Manage Public Profile Visibility

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Manage Public Profile Visibility

Description:

- Allows a Job Seeker to preview a limited public representation of their existing profile, explicitly publish it, replace that published snapshot after later edits, or make it private again.
- This enables the directory/detail goals in UC-18/19. Registration and private-profile editing remain private by default and do not automatically publish anything.
- The source menu's Make Profile Private action and public profile screens establish a visibility concept. The reverse publish action, preview screen, snapshot scope, confirmation, and contracts are explicit research additions; no owner publication editor or complete workflow has been verified in the source.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER.

Preconditions:

- UC-01/02 supply account/session; UC-05/06/08 supply basic information, work preferences, and experience summary. UC-03 defines the canonical position/location labels.
- Implement `/profile/publication` as a reloadable owner route. The account menu opens this page through Make profile public when private, or Make profile private when public; selecting the menu item itself performs no mutation.
- UC-18/19 public read routes are integrated before enabling Publish. Publication-photo storage and removal are available if the actor chooses to include a photo.

Postconditions:

- Success: Visibility and a limited approved snapshot are committed together with a new publication revision. PUBLIC appears in UC-18/19; PRIVATE is absent from directory counts, detail, related profiles, and subsequent public photo requests.
- Failure: The preceding publication remains intact; invalid/conflicting requests do not partly change public content.
- Editing UC-05/06/08 alone changes only the private source. The published snapshot remains unchanged until an explicit Publish latest profile confirmation.
- Existing sessions, private profile fields, UC-07 ranking, and global completion status remain unchanged. Public disclosure is limited to the previewed projection.

Main Flow:

1. Open the owner publication page and load current visibility plus a preview of the latest source profile.
2. Review the exact public fields and the full-name disclosure. Choose whether to include the current profile photo; the default for each publish review is off.
3. If desiredPosition is missing, open UC-05 to complete basic information before publishing.
4. Select Publish profile, or Publish latest profile when already public. Confirm that anyone, including signed-out visitors, can read the shown snapshot.
5. Submit the publication revision, preview source revisions, visibility PUBLIC, and the photo choice.
6. The backend confirms eligibility and unchanged source/publication versions, captures the approved snapshot and optional photo copy, and commits it.
7. Show `Profile publication updated.` and a working View public profile link to `/candidate-profiles/<profileId>`.

Alternative Flow:

A.1 — Initial private profile

- Without a publication record, GET returns publication revision 0, visibility PRIVATE, profileId null, and publishedProfile null. GET creates no record and no public ID.
- Preview reads current private sections; absent UC-06/08 sections use their documented initial values. Missing desiredPosition prevents publishing but does not prevent using the owner page or making an existing publication private.

A.2 — Make private

- Show which current publication will be removed from public access and ask for confirmation. Submit visibility PRIVATE with sourceVersions null and includePhoto false.
- Clear the published snapshot, end access to its photo, and advance the publication revision. Keep a previously assigned public profileId reserved for this account so old links return unavailable rather than pointing to someone else.
- Repeated PRIVATE with the current revision is valid and advances revision once, even when already private. A never-published account keeps profileId null. This does not delete the private source profile.

A.3 — Private edits and republishing

- Preview and currently published values may differ. Show them distinctly so a private name, preference, rating, or photo edit is not mistaken for already-public content.
- Republishing replaces the whole approved snapshot, including a fresh publishedAt. The public ID remains stable. An unchecked includePhoto removes any previously published photo from the new snapshot.

A.4 — Cancel and sign-in

- Cancel confirmation makes no request. Add exactly `/profile/publication` to UC-02's accepted local next destinations, without query/fragment, encoded as next.
- Explain that making a profile private stops future application responses but cannot retract copies already downloaded by readers.

Exception Flow:

E.1 — Source or publication changed

- A stale publication revision returns PUBLICATION_VERSION_CONFLICT. A changed source revision during publishing returns PROFILE_SOURCE_CHANGED. Both preserve the last committed public state.
- Reload the preview and current publication and require another deliberate confirmation; do not silently publish newer private data the actor has not reviewed.

E.2 — Not ready, closed account, or photo failure

- Publishing without desiredPosition returns PROFILE_NOT_READY. No complete education, verified contact, resume, video, or overall completion percentage is required.
- Missing/ineligible sessions return UNAUTHENTICATED; an otherwise valid unsupported role returns ROLE_NOT_ALLOWED. Recheck account eligibility at commit so closure cannot be followed by a late publication.
- If includePhoto true but no source photo exists, return VALIDATION_ERROR. Failed photo copying returns PUBLICATION_UNAVAILABLE and leaves the previous publication intact.

E.3 — Lost response

- GET the owner publication state and preview without automatically repeating PUT. Show the actual current visibility/snapshot for review. A revision increment alone does not prove which concurrent request won.
- If the state read fails, retain an unknown-outcome message with Retry read. Never display PUBLIC or PRIVATE success based solely on a local toggle.

UI Integration:

- File DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`). [Account menu `2:4121`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4121) provides Make Profile Private; its context was inspected during UC-13. [Public profile `2:1478`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1478) and [directory `2:1700`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1700) were inspected on 2026-09-23 for this batch.
- The owner preview/confirmation route is a declared UI supplement, assembled using UC-05's existing profile shell. No exact source owner-publishing frame or frozen dataset is claimed.
- Show full name, desired position, preferred work locations, availability, languages, start availability, experience band, and self-ratings exactly as they would appear publicly. Include current profile photo is an explicit checkbox, initially unchecked.
- State before confirmation: `Anyone can view the published fields, including your full name and the photo if selected. Email, phone, resume and introduction video stay private. Later edits remain private until you publish again.`
- Use visible PUBLIC/PRIVATE labels and distinct current-publication/latest-preview panels. Neutral initials are used when no public photo is selected. Do not show a fabricated 90% progress bar or an unverified professional badge.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/profile/publication` | Read current publication and latest owner preview |
| PUT | `/api/v1/job-seeker/profile/publication` | Publish a snapshot or make it private |

Owner endpoints require UC-02 sessions, accept no query parameters, and resolve ownership from the session. GET has no body. PUT accepts application/json. Public reads/photo delivery are defined by UC-18/19.

Request Body:

```json
{
  "expectedRevision": 0,
  "visibility": "PUBLIC",
  "sourceVersions": {
    "basic": 1,
    "jobPreferences": 1,
    "workExperience": 1
  },
  "includePhoto": false
}
```

All four keys are required. expectedRevision is an integer >= 0. visibility is PUBLIC or PRIVATE. For PUBLIC, sourceVersions contains exactly basic, jobPreferences, workExperience, each a nonnegative integer matching the owner preview; includePhoto is boolean. For PRIVATE, sourceVersions must be null and includePhoto must be false. No body-supplied public fields, account ID, public ID, photo URL, or publishedAt is accepted.

Making private does not require the source profile to remain complete or unchanged. Publishing checks all three source versions even if a particular change would not alter a public field, so the preview and publication correspond to one reviewed source state.

Successful Response:

```json
{
  "success": true,
  "message": "Profile publication updated.",
  "data": {
    "asOf": "2026-09-23T18:00:00.000Z",
    "publication": {
      "revision": 1,
      "visibility": "PUBLIC",
      "profileId": "2d6b20d6-3297-4457-866e-302cae08074d",
      "publishedProfile": {
        "id": "2d6b20d6-3297-4457-866e-302cae08074d",
        "displayName": "Alex Morgan",
        "desiredPosition": "GENERAL_DENTIST",
        "summary": "Seeking General Dentist.",
        "preferredLocations": [
          {
            "id": "sugar-land-tx-us",
            "label": "Sugar Land, Texas"
          }
        ],
        "availability": "PART_TIME",
        "fluentLanguages": [
          "en"
        ],
        "availableStart": {
          "mode": "IMMEDIATELY",
          "month": null
        },
        "experienceBand": "ONE_TO_THREE",
        "ratings": {
          "endodontics": 4,
          "orthodontics": 2,
          "prostheticsRestorative": 2,
          "oralSurgeryImplants": 1
        },
        "photoUrl": null,
        "publishedAt": "2026-09-23T18:00:00.000Z"
      }
    },
    "preview": {
      "sourceVersions": {
        "basic": 1,
        "jobPreferences": 1,
        "workExperience": 1
      },
      "photoAvailable": false,
      "content": {
        "displayName": "Alex Morgan",
        "desiredPosition": "GENERAL_DENTIST",
        "summary": "Seeking General Dentist.",
        "preferredLocations": [
          {
            "id": "sugar-land-tx-us",
            "label": "Sugar Land, Texas"
          }
        ],
        "availability": "PART_TIME",
        "fluentLanguages": [
          "en"
        ],
        "availableStart": {
          "mode": "IMMEDIATELY",
          "month": null
        },
        "experienceBand": "ONE_TO_THREE",
        "ratings": {
          "endodontics": 4,
          "orthodontics": 2,
          "prostheticsRestorative": 2,
          "oralSurgeryImplants": 1
        }
      }
    }
  }
}
```

GET uses message `Profile publication loaded.` Both return HTTP 200 and exactly data.asOf, publication, and preview. publication has exactly revision, visibility, profileId, and publishedProfile. revision advances once for every successful PUT; profileId is null only before any publication; publishedProfile is null when PRIVATE and a PublicProfile when PUBLIC.

preview contains exactly sourceVersions, photoAvailable (boolean), and content. content contains exactly the nine content keys shown; desiredPosition and summary may be null when setup is incomplete. The other initial values follow UC-05/06/08. Preview never contains a public photo URL; the owner's existing UC-05 photo can be shown privately when photoAvailable is true.

PublicProfile contains exactly the keys in the example: id, displayName, desiredPosition, summary, preferredLocations, availability, fluentLanguages, availableStart, experienceBand, ratings, photoUrl, and publishedAt. id is a server-issued public-profile UUID distinct from Account.id; publishedAt is UTC ISO 8601. The remaining content is a publication snapshot, not a live read of private profile edits.

- displayName is UC-05's canonical firstName + one space + lastName; the preview explicitly discloses that the full name will be public.
- desiredPosition is the UC-03/05 enum: GENERAL_DENTIST, DENTIST_SPECIALIST, DENTAL_HYGIENIST, DENTAL_ASSISTANT, OFFICE_STAFF, or OFFICE_MANAGER. Labels follow UC-03; a published profile never has null here.
- summary is exactly `Seeking <desired-position label>.`, generated from the declared enum label, not free text or an inferred biography.
- preferredLocations is the UC-06 locationIds mapped to {id,label} using UC-03 options, in lexicographic ID order. [] means Any preferred location. These are desired work cities, not residence, current location, or geolocation.
- availability is UC-06 ANY, FULL_TIME, or PART_TIME. ANY means open to either mode, not a third job type.
- fluentLanguages and availableStart preserve UC-05's exact shapes/values. The preview may show the initial [] and {mode:NOT_SPECIFIED,month:null}; a publishable saved basic section has its validated values.
- experienceBand and the four-key ratings object follow UC-08 exactly, including null values for unprovided experience/ratings.
- photoUrl is null or `/api/v1/candidate-profiles/<id>/photo`, served only while that publication is current, PUBLIC, and owned by an ACTIVE JOB_SEEKER. It references a copied publication photo, never UC-05's owner-only photo endpoint.

No account ID, email, phone, password, resume, introduction video, education, board-certification declaration, health-benefit preference, practice-interest preference, notification settings, source revision, or overall completion percentage appears in a public representation.

Error Response:

All JSON errors contain exactly success false, statusCode, code, message, timestamp (server UTC ISO 8601), and path (actual pathname without query). Only VALIDATION_ERROR additionally contains errors, mapping field paths to nonempty message arrays. Other errors omit errors. Do not add data: null. No endpoint-specific rate budget is introduced in this UC.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 409 | PUBLICATION_VERSION_CONFLICT | Your publication changed. Reload it before confirming. |
| 409 | PROFILE_SOURCE_CHANGED | Your profile changed. Review the latest preview before publishing. |
| 409 | PROFILE_NOT_READY | Choose a desired position before publishing your profile. |
| 503 | PUBLICATION_UNAVAILABLE | Profile publication is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

409 applies to PUT only. Wrong media type, extra keys/query/body on GET use VALIDATION_ERROR. Example:

```json
{
  "success": false,
  "statusCode": 409,
  "code": "PROFILE_SOURCE_CHANGED",
  "message": "Your profile changed. Review the latest preview before publishing.",
  "timestamp": "2026-09-23T18:00:00.000Z",
  "path": "/api/v1/job-seeker/profile/publication"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Persist an independent owner Publication with revision, visibility, stable optional public UUID, optional public snapshot, and optional copied-photo reference. Use NestJS/TypeScript and the existing Account/source sections. The first publication assigns a public UUID; private GET does not assign one.

Capture the public projection from the declared source revisions, not from client-supplied profile content. Snapshot values and optional copied photo become visible together. Source/private updates do not change a published snapshot or its public photo bytes. Store a separate publication photo so a subsequent private photo replacement cannot alter the public image without confirmation.

At every public read, require PUBLIC and an ACTIVE JOB_SEEKER owner. Making private removes the snapshot and public photo reference at commit, and retires the unused photo copy within 24 hours. Republish similarly retires the superseded copy. A preexisting download may finish; new requests must not return an old private/closed publication.

Explicit integration extension to UC-14: remove Publication and snapshot in the closure transaction, invalidate its public reads immediately, and include copied publication photos in the existing 24-hour media cleanup. Publishing and account-owned updates must not recreate a closed account's data. Public IDs from closed accounts are never assigned to new accounts, even if the email is reused.

Private profile APIs remain owner-only. This limited, confirmed projection is the sole new public disclosure path; it does not change their response schema or expose their media URLs.

### Frontend UI Context

Use React/TypeScript/Tailwind and the profile shell. Label previewed location as Preferred work locations, never the candidate's residence. Ratings remain Self-assessed; null values are Not provided/Not rated. Show the source-backed position labels without claiming a verified occupation.

Publication is a separate action from saving profile sections. Display a working edit-basic link when desiredPosition is missing, and keep Make private available for a current publication even when the latest source would not pass publish validation. The photo checkbox defaults off each time a new publish review starts.

### Frontend Logic and API Context

Read current state before opening a confirmation. Submit only the revision, visibility, source versions, and photo choice. On conflict/source change reload and require review; never adopt a new source revision and resend automatically.

After success use the returned publication as authoritative and refresh any visible directory/detail. Preserve private profile edits separately. On an ambiguous outcome refetch and show actual saved state without claiming which request produced it. Clear owner preview on session/account change and ignore superseded responses.

The menu action navigates to the preview page rather than mutating immediately. Enable public directory/detail links only with UC-18/19 implemented, so publishing never ends in a 404 caused by an absent route.

### Validation and Error-Handling Context

Reject unknown object keys, invalid enum/boolean/revision types, and inconsistent PUBLIC/PRIVATE combinations. Use expectedRevision, sourceVersions.<section>, visibility, includePhoto, and request paths in validation errors.

Compare versions and account eligibility through commit. Photo-read/copy failure must not publish text with a falsely promised photo. Initial missing optional sections are valid defaults; an unavailable source service is not a missing section.

Public opt-in must not leak fields outside the exact projection, and private/source edits must not silently update it. Externally observable unavailable behavior is shared across unknown, private, inactive-owner, and closed-owner public IDs as defined in UC-19.
