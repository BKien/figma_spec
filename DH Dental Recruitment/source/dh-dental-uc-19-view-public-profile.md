# UC-19: View a Public Candidate Profile

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

View a Public Candidate Profile

Description:

- Allows visitors to inspect one explicitly published candidate snapshot, see its declared experience/self-ratings and preferred work details, open related public profiles, and copy the public link.
- Uses the source public profile composition with explicit data-alignment changes: UC-05–08 do not collect a biography, free-text skill tags, or employer-by-employer history, so this UC does not invent those records from lorem ipsum.
- Public fields come only from UC-17's approved snapshot. Detail/related ordering, photo delivery, missing-data behavior, routes, and error contract are research decisions.

Primary Actor:

Visitor or signed-in user.

Preconditions:

- UC-17 supplies publication data and UC-18 supplies the directory and PublicProfileCard schema.
- Implement public, reloadable `/candidate-profiles/:profileId` with the same ID used by directory cards.
- No login, employer role, complete profile, or verified contact is required to read an available public snapshot. Public reading does not grant access to the owner's private profile endpoints.

Postconditions:

- Success: Display the one current public snapshot and up to four related currently public candidate cards.
- Failure: Show a uniform profile-unavailable or service-error state without leaking a private/closed profile's identity or previously cached content.
- No application, hiring contact, follow action, message, notification, profile edit, or private-media access occurs.

Main Flow:

1. Open View Profile from UC-18 or a direct public profile URL.
2. GET the public detail and render name, desired position, optional published photo, preferred cities/availability, generated summary, languages/start availability, experience band, and four self-ratings.
3. Display missing optional values as Not provided/Not rated, with no fabricated completion score or verification badge.
4. Optionally open one of the related profiles, copy the current canonical public URL, or return to the directory.
5. If the optional source login form is used, follow UC-02 and return to this same public page; successful login unlocks no additional candidate data in this UC.

Alternative Flow:

A.1 — Missing public photo or optional experience

- photoUrl null uses neutral initials. Null experienceBand displays Not provided; null ratings display Not rated rather than zero skill.
- preferredLocations [] displays Any preferred location. availableStart retains its published month/immediate semantics, and a past month means availability already began rather than an expired candidate.
- Never borrow the private owner's photo, resume, introduction video, email, or phone to complete the public screen.

A.2 — Related profiles

- Select at most four other visible public snapshots, excluding the current ID and duplicates. Sort by same desiredPosition first, then publishedAt descending, then public UUID ascending.
- Use the same returned relatedProfiles array for the sidebar and lower card section. Normalize their headings to Related candidates / Other candidates, avoiding the source's Dentist label for Office Manager/Assistant profiles.
- A short/empty result is valid; do not fill gaps with private or repeated source people.

A.3 — Sign-in and sharing

- Reuse UC-02's exact login/session form for the source's guest sign-in panel. Add `/candidate-profiles/<valid UUID>` without query/fragment to its accepted local next destinations. An inline login rechecks the current detail after session confirmation.
- Signed-in users see the same public fields; no employer-contact or hidden private candidate section is implied. Keep source Sign up routed to UC-01 without promising automatic return or publication.
- Enable only Copy link among share controls. Copy the application-origin public detail URL without account/session data. Report success only after clipboard success; otherwise present selectable URL text. Other external share destinations remain unavailable.

Exception Flow:

E.1 — Unknown, private, inactive, or closed profile

- Malformed/unknown UUID, PRIVATE publication, missing snapshot, or non-ACTIVE/non-JOB_SEEKER owner all return the same PROFILE_NOT_AVAILABLE result. Authentication does not bypass visibility.
- Clear an old displayed snapshot/photo/related list when the current detail reports unavailable. Offer Back to candidates; the detail endpoint is not an owner preview.

E.2 — Public-photo or service failure

- Reevaluate publication visibility for each photo request. Null/unavailable photo returns PROFILE_PHOTO_NOT_AVAILABLE; a current reference with inaccessible storage returns PUBLIC_PROFILE_UNAVAILABLE.
- A failed optional image can show neutral initials with an image error, but must not cause the UI to fetch the private photo endpoint. A failed main detail read is not replaced with another person's data.

E.3 — Visibility changes after initial load

- Refresh detail on route entry/reentry and browser Back. If the snapshot becomes private or its owner closes the account, subsequent detail/media reads fail uniformly.
- A previously downloaded image/text copy cannot be retracted by this UI. Do not promise instant deletion from every external reader's device.

UI Integration:

- [Public profile detail, frame `2:1478`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-1478), DH Dental Recruitment (Community), Pages / Job Seeker (`1:2`), inspected with context/screenshot on 2026-09-23.
- Preserve its main card, identity/photo summary, side login/related panels, copy-link affordance, and lower related cards. This is a desktop reference, not a frozen dataset or verified prototype interaction.
- Replace About with Profile summary using UC-17's deterministic summary and published language/start/preference values. Replace free-text Skills chips with the four declared UC-08 self-ratings, explicitly labeled Self-assessed.
- Replace Work History with Experience summary showing the published experienceBand. No individual employer names, date intervals, or work-history prose is invented because those fields are not collected by UC-08.
- Omit source Profile Completion 90% entirely; the existing project defines no calculation. Label locations Preferred work locations and the position Desired position, avoiding claims about residence or verified occupation.
- These section adaptations and all unavailable/loading/error/responsive states are explicit supplements. On narrow screens place main profile content before the login/related sections. Preserve meaningful labels and numeric rating text alongside visual stars.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/candidate-profiles/:profileId` | Public snapshot and related cards |
| GET | `/api/v1/candidate-profiles/:profileId/photo` | Current publication photo bytes |

Both are public, accept no query parameters/body, and must check current publication eligibility. They do not accept Account.id or an owner-access override. UC-02 login/session endpoints remain unchanged when the optional login panel is used.

Request Body:

None. profileId is the stable public UUID assigned by UC-17. A malformed path UUID uses the same 404 unavailable response as an unknown/private profile; extra query/body input uses VALIDATION_ERROR.

The photo endpoint serves a whole-file JPEG/PNG. A Range header is ignored and a valid photo is returned as HTTP 200 in full; no partial-file API is introduced.

Successful Response:

```json
{
  "success": true,
  "message": "Candidate profile loaded.",
  "data": {
    "asOf": "2026-09-23T18:00:00.000Z",
    "profile": {
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
    },
    "relatedProfiles": []
  }
}
```

HTTP 200 with exactly data.asOf, profile, and relatedProfiles. profile is UC-17's exact PublicProfile schema; it contains the snapshot publishedAt, not an invented live private updatedAt. relatedProfiles contains 0–4 UC-18 PublicProfileCard objects with no additional fields.

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

Main snapshot and related visibility are evaluated coherently for the response. Related cards need not share the same publication date or optional values.

GET photo returns HTTP 200 binary bytes, Content-Type image/jpeg or image/png matching the copied photo, and actual Content-Length, without a success JSON envelope. It serves only the currently referenced publication photo and no original filename or arbitrary storage path. New photo requests after privacy/closure must not return a previously cached public image without reevaluating eligibility.

Error Response:

All JSON errors contain exactly success false, statusCode, code, message, timestamp (server UTC ISO 8601), and path (actual pathname without query). Only VALIDATION_ERROR additionally contains errors, mapping field paths to nonempty message arrays. Other errors omit errors. Do not add data: null. No endpoint-specific rate budget is introduced in this UC.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 404 | PROFILE_NOT_AVAILABLE | This profile is not available. |
| 404 | PROFILE_PHOTO_NOT_AVAILABLE | This profile photo is not available. |
| 503 | PUBLIC_PROFILE_UNAVAILABLE | This profile is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Detail uses PROFILE_NOT_AVAILABLE for all unavailable IDs/owners/visibility states. Photo uses PROFILE_PHOTO_NOT_AVAILABLE for those same states or no selected public photo, so its response does not reveal the reason. A known-current stored photo that cannot be read is 503. No 401/403 is caused by absence of a session.

```json
{
  "success": false,
  "statusCode": 404,
  "code": "PROFILE_NOT_AVAILABLE",
  "message": "This profile is not available.",
  "timestamp": "2026-09-23T18:00:00.000Z",
  "path": "/api/v1/candidate-profiles/2d6b20d6-3297-4457-866e-302cae08074d"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Read UC-17's current snapshot only when its publication is PUBLIC and its owner is an ACTIVE JOB_SEEKER. No private-profile joins should enrich the returned representation beyond the visibility check. Pending private edits do not change a public detail response until republished.

Build related cards from the same eligible public pool with the declared deterministic order. Do not expose owner IDs, contact values, private media, or internal source revisions through related cards, photo paths, or diagnostics. Self-ratings remain declarations, not computed qualifications.

Photo reads use the publication copy and current eligibility. Making private, account closure, and republish retirement follow UC-17/14. A transfer already started may finish; subsequent reads must resolve current visibility and the current photo reference rather than serve an inaccessible old publication.

The endpoints are public for both visitors and signed-in users. Logging in does not grant private candidate data or enable an employer contact endpoint; those workflows require separate specifications.

### Frontend UI Context

Implement the adapted Figma composition in React/TypeScript/Tailwind and reuse UC-18 cards plus UC-02's guest login form. Use actual returned values; no lorem ipsum biography, source sample work dates, duplicated Manual dexterity tags, or fixed progress percentage is rendered.

Explain self-assessed ratings without adding a qualification score. Show neutral fallback for no public photo and explicit missing-value labels. Keep public and private owner routes distinct; the author uses `/profile/publication` to review visibility, not this endpoint as a hidden private preview.

### Frontend Logic and API Context

Load detail by public profile UUID and cancel/ignore earlier requests after route changes. The optional session request affects only the shell/login panel, not which candidate fields are returned.

Use relatedProfiles once for both source related sections and bind every View Profile to its returned ID. Copy only the canonical browser detail URL. A current 404 clears the snapshot and media before showing unavailable; browser reentry triggers a fresh read rather than trusting a previously public cache.

After optional login, confirm UC-02 session and refetch the public profile. Never call owner-only basic/photo/resume/video endpoints for the viewed candidate. Extend only the declared local next destination pattern; all other UC-02 validation behavior remains.

Back to candidates works for direct-entry readers, while browser Back restores a prior filtered directory URL when present.

### Validation and Error-Handling Context

Use uniform unavailable behavior for malformed/unknown/private/closed IDs, including when the requester owns a private profile. Extra query/body input uses errors.request. Public GET requests never require contact verification or an employer session.

Keep a main detail outage distinct from a missing optional photo. Do not downgrade a 503 to a fabricated empty successful profile, invent unavailable biography/work-history data, or continue showing a previous candidate after route failure.

No app state may interpret a public link as approval to contact, hire, publish further private data, or verify a candidate. Match the exact snapshot allowlist and the declared source-driven UI adaptations.
