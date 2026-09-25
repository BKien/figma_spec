# UC-10: Record and Manage an Introduction Video

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Record and Manage an Introduction Video

Description:

- Allows a Job Seeker to record a short introduction in the browser, review it, and explicitly save it to their account. A compatible local video can be selected as an alternative; a saved video can be played, replaced, or removed.
- The source supports a camera/recording area, Record Your Answers, a policy link, and a sample-video/mobile-app panel. Review, save, replacement, deletion, and upload-fallback states are project supplements needed to define an end-to-end feature.
- This UC stores one account-level introduction, not a job-specific application answer. It sends nothing to a recruiter and does not submit an application. Duration/format limits, routes, state transitions, and backend contracts are declared research decisions.

Primary Actor:

Authenticated ACTIVE JOB_SEEKER.

Preconditions:

- UC-01/02 supply the shared account/session. `/introduction-video` is implemented as a reloadable route and activates the previously unavailable Introduction Video navigation.
- Browser recording is used only where camera/microphone permissions and a supported recording format are available. The development deployment must support those browser capabilities; otherwise the actor may choose the declared file-upload alternative.
- The backend can inspect, store, and serve one supported video per account. It returns a successful save only after the complete video is ready for playback; this UC defines no asynchronous processing job or third-party video service.
- The profile does not have to be complete, and contact verification is not required. A real camera, prerecorded personal video, or truthful empty state is used; the source's sample poster is never saved as the actor's introduction.

Postconditions:

- Success: The reviewed video is committed as the account's one current introduction, or removal is confirmed; the video's section revision advances once and the page reflects the current saved state.
- Failure/cancel: A rejected or abandoned draft leaves the previous saved video intact. A lost write response is treated as unknown until reconciled.
- Camera/microphone capture ends when recording stops, is canceled, the account becomes ineligible, or the page is left. Nothing is uploaded before the actor selects Save video.
- No public profile, application, notification, transcript, AI score, or recruiter sharing is created. UC-07 ranking and global profileCompletionStatus remain unchanged.

Main Flow:

1. Open Introduction Video, confirm the session, and load the current video section.
2. Select Record Your Answers. Request camera/microphone access and, if available, show a live preview with Start recording.
3. Select Start recording. Capture the introduction and show elapsed time; Stop recording ends capture, and reaching 120 seconds stops it automatically.
4. Show the resulting local playback preview with Record again, Discard, and Save video. Stop all camera/microphone tracks once recording ends.
5. Review the draft and select Save video. If a saved video already exists, the action is labeled Replace saved video so its effect is clear.
6. Submit the recorded file and loaded expectedRevision. The backend validates the media and revision and commits it only when storage and metadata are usable.
7. Show `Introduction video saved.` and render the saved video with playback, Record again/Choose video file, and Remove video actions.

Alternative Flow:

A.1 — No saved introduction

- GET returns revision 0, video null, updatedAt null for a never-saved section. Show `No introduction video saved yet.` with recording/file-selection actions.
- A saved-but-later-removed section also has video null, but retains its newer revision and updatedAt. Neither state requires a default clip.

A.2 — Choose an existing file

- Choose video file is an explicit supplement to the source. It accepts the formats and limits below and enters the same review/save flow; selection does not upload immediately.
- Use this path when the actor declines camera access, lacks devices, or the browser cannot record a supported format. If the selected file cannot play in this browser, explain that limitation and require a compatible preview before enabling Save; do not claim every browser plays every accepted codec.

A.3 — Record again, discard, or leave

- Record again discards the current unsaved recording and starts a new preview/capture flow after the actor confirms that the draft may be replaced. The previously saved server video remains intact until another save succeeds.
- Discard removes only the local draft and returns to the saved/empty state. If navigating away with an unsaved draft, offer Stay or Discard and leave; stopping capture and removing local media does not delete the saved video.
- Recording controls do not automatically submit an answer for any job. The prompt is normalized to a general profile introduction rather than implying a selected opportunity.

A.4 — Remove the saved video

- Remove video opens a small confirmation identifying the current saved introduction. Confirm sends the section revision in the DELETE request; Cancel leaves it unchanged.
- A confirmed removal returns video null with an advanced revision and `Introduction video removed.` The old media URL no longer serves that video.
- Removal is unavailable during recording, draft review, saving, reconciliation, or an existing removal request; first discard or resolve the local draft. No other profile content is removed.

A.5 — Sign-in and policy information

- Add exactly `/introduction-video` to UC-02's local next destinations, with no query/fragment, preserving the default `/jobs` route. Encode it as the next parameter for sign-in.
- Photo/Video Policy opens the real local `/photo-video-policy` informational route. It states the research behavior: recording starts only on action, capture remains local until Save, only the signed-in owner can retrieve these profile media in the current scope, replacement/removal changes the current saved media, and recording does not apply for jobs or send content to recruiters.
- This route is an integration supplement within this UC, not a separate document deliverable or a claim about an existing production privacy policy.

Exception Flow:

E.1 — Recording cannot start or is interrupted

- Permission denied, missing/busy devices, unsupported recording capability, or device loss shows a specific local explanation with Retry or Choose video file. No backend success/error envelope is invented for a browser-only failure.
- Device loss or a recorder failure stops capture and marks the draft incomplete; do not enable Save for that draft. A regular manual stop or duration-limit stop can produce a reviewable draft if the final file meets the media rules.
- No hidden camera/microphone capture continues after Stop, Discard, account change, or navigation.

E.2 — Unsupported or invalid media

- Reject unsupported container/codec, corrupt/empty content, missing audio or video track, duration outside the range, or an oversized file using the declared API errors. A filename/MIME label alone is not sufficient evidence of a playable introduction.
- The existing saved video remains available after a failed replacement. Show errors beside the draft, and let the actor discard it or explicitly retry when appropriate.

E.3 — Concurrent save/removal or unknown result

- Stale expectedRevision returns INTRODUCTION_VIDEO_VERSION_CONFLICT. Load the current section and let the actor review before explicitly replacing/removing it with the new revision.
- After a lost PUT/DELETE response, GET the section and show the current saved state for confirmation. A changed revision, duration, or byte size alone does not prove that this exact draft won a concurrent update; play the current video for review. Do not automatically repeat a write against the newest revision.
- If the session ends, stop capture, clear local/private media state, and require sign-in. If the section cannot be read, show a service error instead of assuming no video exists.

E.4 — Playback failure

- A replaced/removed/unknown media ID returns INTRODUCTION_VIDEO_NOT_FOUND. Refresh metadata and show the current video, or the empty state if it was removed.
- Browser decoding/playback failure shows `This video could not be played in this browser.` with Retry or a compatible-file replacement path. Do not substitute the source sample clip and label it as the user's video.

UI Integration:

- File DH Dental Recruitment (Community), page Pages / Job Seeker (`1:2`).
- [Job Seeker / Introduction Video, frame `2:4160`](https://www.figma.com/design/5PvZvQ4E6DepIhbL8D35cV/DH-Dental-Recruitment--Community-?node-id=2-4160): question/prompt, policy link, recording viewport, camera/microphone/record controls, timer, Record Your Answers, and lower sample/mobile-app panel.
- Context and screenshot inspected on 2026-09-23. Only this desktop base state is evidenced; the source does not establish save/delete contracts, permission flows, final media assets, or a frozen dataset.
- Normalize the source opportunity-specific sentence to `Introduce yourself and explain what you would bring to a dental team.` This account-level page has no selected job context.
- Add explicit preview, Start recording, Stop recording, review, Save/Replace, Discard, remove-confirmation, and file-selection states. Retain the source viewport and teal primary action style; show a clear state label and elapsed time rather than treating the camera icon as proof that capture is active.
- The lower sample poster is illustrative. In this research release, disable its play affordance with `Sample video unavailable` because no playable sample asset has been supplied. App Store/Google Play badges are noninteractive illustrative content; no verified app destinations are supplied.
- The real policy route, responsive layout, accessible control names, loading/progress, errors, and empty/saved views are implementation supplements. Saved/draft playback uses browser playback controls and does not autoplay.

API Endpoint:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/v1/job-seeker/introduction-video` | Load the current introduction-video section |
| PUT | `/api/v1/job-seeker/introduction-video` | Save or replace the current video |
| DELETE | `/api/v1/job-seeker/introduction-video` | Remove the current video |
| GET | `/api/v1/job-seeker/introduction-video/media/:videoId` | Play current owner media, with optional single byte range |

All require the UC-02 session and reject query parameters. Both GET endpoints have no body. PUT uses multipart/form-data. DELETE accepts application/json. `/photo-video-policy` is a static browser route and needs no API.

Request Body:

PUT consists of exactly one metadata text part containing JSON and exactly one binary video part:

```json
{
  "expectedRevision": 0
}
```

metadata contains only expectedRevision, a required integer >= 0 equal to the last loaded introduction-video revision. Its maximum size is 16,384 UTF-8 bytes. video must satisfy all of the following:

| Property | Accepted value |
| --- | --- |
| Size | > 0 and <= 52,428,800 bytes (50 MiB) |
| Duration | From 1.000 through 120.000 seconds, inclusive, measured from the saved media |
| WebM | video/webm containing VP8 or VP9 video and Opus audio |
| MP4 | video/mp4 containing H.264 video and AAC audio |
| Tracks | Exactly one video track and one audio track; no additional tracks |
| Content | A readable, complete video file; audio may include silence, but an audio track must exist |

These are finite research delivery choices, not claims that Figma specifies codecs. No transcoding, remote video URL, or resumable/chunk upload contract is provided. Browser recording must select a format it actually supports from the accepted set; otherwise use the file alternative. The complete multipart body, including framing, is at most 53,477,376 bytes (51 MiB).

File/body/metadata byte-limit failures return 413 UPLOAD_TOO_LARGE. Wrong request media type or unsupported media container/codec returns 415 UNSUPPORTED_MEDIA_TYPE. Empty/corrupt supported media, wrong tracks, invalid duration, missing parts, duplicate parts, malformed metadata, or unexpected fields returns 400 VALIDATION_ERROR. The server derives contentType, byteSize, and duration; client declarations do not replace inspection.

DELETE body, with no additional fields:

```json
{
  "expectedRevision": 1
}
```

For GET media, videoId is the current video's UUID. Missing, malformed, unknown, replaced, removed, or another account's ID yields the same 404 INTRODUCTION_VIDEO_NOT_FOUND after session eligibility is evaluated.

GET media optionally accepts one Range header in bytes units: bytes=start-end, bytes=start-, or bytes=-suffixLength, with decimal nonnegative offsets and a positive suffix length. A malformed, multi-range, or unsatisfiable request returns 416 RANGE_NOT_SATISFIABLE. Clamp an end beyond the last byte to the file end; a suffix longer than the file selects the whole file. Without Range, return the complete file.

Successful Response:

Metadata GET, PUT, and DELETE return HTTP 200 with data containing exactly asOf and introductionVideo. PUT example:

```json
{
  "success": true,
  "message": "Introduction video saved.",
  "data": {
    "asOf": "2026-09-23T15:00:00.000Z",
    "introductionVideo": {
      "revision": 1,
      "video": {
        "id": "8d01b628-6c4b-43b2-ae24-e733998932a8",
        "url": "/api/v1/job-seeker/introduction-video/media/8d01b628-6c4b-43b2-ae24-e733998932a8",
        "contentType": "video/webm",
        "byteSize": 6291456,
        "durationSeconds": 45.2,
        "createdAt": "2026-09-23T15:00:00.000Z"
      },
      "updatedAt": "2026-09-23T15:00:00.000Z"
    }
  }
}
```

GET uses message `Introduction video loaded.` introductionVideo contains exactly revision, video, and updatedAt. video is null or the exact object shown: id (server-issued UUID), url (same-origin current-owner media route), contentType (video/webm or video/mp4), byteSize (actual integer bytes), durationSeconds (server-measured seconds rounded to three decimal places), and createdAt (UTC ISO 8601). Validate the duration range before rounding.

Each successful PUT creates a new video ID and increments the section revision once; the previous ID stops resolving to media. The initial GET returns revision 0, video null, updatedAt null. Each accepted DELETE with the current revision increments once, even if video is already null; its success is removal of any current video, not proof one existed. Example after removing the video above:

```json
{
  "success": true,
  "message": "Introduction video removed.",
  "data": {
    "asOf": "2026-09-23T15:05:00.000Z",
    "introductionVideo": {
      "revision": 2,
      "video": null,
      "updatedAt": "2026-09-23T15:05:00.000Z"
    }
  }
}
```

GET media returns binary content, without a success JSON envelope:

- No Range: 200, Content-Type matching the saved video, Content-Length equal to total bytes, and Accept-Ranges: bytes.
- Valid single range: 206 with those applicable headers, Content-Range: bytes start-end/total, and Content-Length equal to the selected inclusive byte count. Even a range selecting the whole file returns 206.
- Unsatisfiable/invalid range: 416 JSON error plus Content-Range: bytes */<total byte count>. Resolve eligibility and the current video before range evaluation; unavailable media remains 404.

No original filename, public playback link, upload token, account ID, transcript, or recognition result is returned.

Error Response:

All JSON errors contain exactly success false, statusCode, code, message, timestamp (UTC ISO 8601), and path (actual pathname without query). VALIDATION_ERROR additionally contains errors, an object mapping field paths to nonempty arrays of messages. Other codes omit errors. Do not add data: null. Binary download/playback successes are explicitly identified; their errors still use this JSON envelope.

| HTTP | code | message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | Please sign in to continue. |
| 403 | ROLE_NOT_ALLOWED | This action is not available for your account role. |
| 404 | INTRODUCTION_VIDEO_NOT_FOUND | No introduction video is available. |
| 409 | INTRODUCTION_VIDEO_VERSION_CONFLICT | Your introduction video changed in another session. Reload the latest version before saving. |
| 413 | UPLOAD_TOO_LARGE | The video upload exceeds the allowed size. |
| 415 | UNSUPPORTED_MEDIA_TYPE | Use an accepted WebM or MP4 video in multipart form data. |
| 416 | RANGE_NOT_SATISFIABLE | This media range is not available. |
| 503 | INTRODUCTION_VIDEO_UNAVAILABLE | Introduction video is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

404/416 apply only to GET media. 409 applies to PUT/DELETE. 413/415 apply to PUT. Invalid DELETE content type uses 400 VALIDATION_ERROR with errors.request. A current video reference whose storage cannot be read is a 503 service failure; a genuinely no-longer-current ID is 404.

```json
{
  "success": false,
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Please correct the highlighted fields.",
  "timestamp": "2026-09-23T15:00:00.000Z",
  "path": "/api/v1/job-seeker/introduction-video",
  "errors": {
    "video": [
      "Video duration must be between 1 and 120 seconds."
    ]
  }
}
```

```json
{
  "success": false,
  "statusCode": 409,
  "code": "INTRODUCTION_VIDEO_VERSION_CONFLICT",
  "message": "Your introduction video changed in another session. Reload the latest version before saving.",
  "timestamp": "2026-09-23T15:00:00.000Z",
  "path": "/api/v1/job-seeker/introduction-video"
}
```

```json
{
  "success": false,
  "statusCode": 416,
  "code": "RANGE_NOT_SATISFIABLE",
  "message": "This media range is not available.",
  "timestamp": "2026-09-23T15:00:00.000Z",
  "path": "/api/v1/job-seeker/introduction-video/media/8d01b628-6c4b-43b2-ae24-e733998932a8"
}
```

## Project-Specific Implementation Context

### Backend Implementation Context

Use the UC-02 cookie-based browser session. All feature endpoints require the account resolved from that session to be an ACTIVE JOB_SEEKER. Unverified email/mobile, an incomplete basic profile, and global profileCompletionStatus INCOMPLETE do not block this feature. A missing, expired, or account-ineligible session returns 401 UNAUTHENTICATED; an otherwise valid unsupported-role session returns 403 ROLE_NOT_ALLOWED. No endpoint accepts a caller-supplied account ID.

Implement one IntroductionVideo section per Account in the proposed NestJS/TypeScript backend, with independent revision, optional current video reference, and updatedAt. Persist the declared video metadata and usable file content. No job ID is stored in this section, and recording/saving it does not call an application endpoint.

The server checks the complete media against format, tracks, duration, and byte limits before committing it. PUT returns success only when the committed media can be served; no intermediate PROCESSING success state is defined. In particular, recordings whose container lacks a simple duration header must be inspected from their actual media timeline rather than rejected solely because one metadata header is absent.

Use the expected section revision for both replacement and removal. First save creates revision 1; concurrent writes against the same revision cannot both succeed. Failed/conflicting replacement leaves the old video current. Store the new usable media before committing its reference, and clean up unreferenced files from rejected attempts. Retire replaced/removed media after the reference changes; a later GET of an old ID must not continue exposing it as current media.

Every media read checks the current owner's section and requested video ID, including range reads. A transfer already in progress when replacement/removal commits may finish, but subsequent requests must use current state. Do not let deletion of the physical old file corrupt a different current video or its metadata.

Metadata GET of an absent section returns the initial representation without mutation. A known current reference with unavailable storage is a service error; do not erase it as though the user removed their video. Section revisions remain separate from UC-05/06/08/09, and saving a video changes none of those contracts or overall profile completion.

### Frontend UI Context

Use React, TypeScript, and Tailwind CSS with the existing authenticated shell. The source viewport is reused for idle, live preview, recording, draft playback, and saved playback, with distinct labels/actions. A red indicator and elapsed timer are present only while recording; a poster or local preview is not described as a saved video.

Expose readable limits before capture/file selection: 1–120 seconds, maximum 50 MiB, and accepted WebM/MP4 formats. Start recording only after an explicit action and available device permission. A live preview can be muted to prevent audio feedback while capture still includes microphone audio. The saved/draft player uses ordinary controls and no autoplay.

The review state shows Save video or Replace saved video, Record again, and Discard. Removal has its own confirmation. On a narrow viewport, size the video proportionally and keep the timer/action buttons usable. If a selected video cannot be previewed, disable Save and explain the compatibility issue.

Keep the sample-video panel clearly illustrative and its unavailable actions labeled. The policy link opens its implemented informational route; it must not navigate to an absent page or an invented external production policy.

### Frontend Logic and API Context

Load session and metadata, capturing the current section revision. Maintain explicit local states: loading, idle/saved, requesting devices, preview, recording, reviewing draft, saving, confirming removal, removing, reconciling, and error. A saved video can remain the confirmed server state while a local draft exists; keep their metadata separate.

Detect actual recording support before choosing an accepted format. Finalize recorded media before review/save. Stop at the duration limit and finalize the resulting file; if the final container exceeds the server's duration/size limits, mark it invalid and request a shorter recording rather than lying about its duration. Browser validation is an early convenience; the server remains authoritative.

Stop capture tracks and release local preview resources after Stop, Discard, session loss, or navigation. A local recording/file stays in this editor until explicitly saved or discarded; it is not restored after account changes. No automatic upload occurs when recording stops.

Send PUT multipart with metadata and the chosen complete file; do not send client duration, public URL, or original profile data. While saving/removing/reconciling, prevent duplicate writes and navigation that falsely implies cancellation of a server mutation. Show measured upload progress when available, then a separate saving indicator until the server returns.

On success, use the canonical response, discard the local draft, and fetch the new media URL. On conflict or uncertain outcome, reload metadata and let the actor review the actual saved clip before any new mutation. After confirmed removal, stop playback, clear media state, and show video null. A 404 while playing triggers metadata refresh rather than an endless media retry loop.

Integrate the declared next destination into UC-02, preserve its session lifetimes, and ignore responses belonging to an earlier account/video. Browser recording failures are local UI errors, separate from the API envelope.

### Validation and Error-Handling Context

Reject unknown/duplicate multipart parts, missing expectedRevision, noninteger/negative revisions, unsupported queries or GET bodies, and extra DELETE keys. API validation errors use expectedRevision, metadata, video, or request. Size limits are byte counts and duration validation uses actual media time, not the local elapsed display.

Differentiate unsupported container/codec (415), corrupt or invalid track/duration content (400), excessive size (413), stale section revision (409), no current requested video (404), invalid range (416), and storage/service failure (503). Keep response envelopes consistent with UC-01–09; only documented media successes are binary.

A recording permission failure never creates a server video or an account error. Unverified contact data is not a reason to block recording/upload. A self-introduction is not proof of identity, licensing, professional competence, application submission, or agreement to recruiter sharing.

Never replace a valid saved video with an incomplete upload, show an unavailable sample as the user's clip, or claim an unknown write succeeded because the timer ended. Preserve the prior committed state on rejected replacements and allow explicit recovery through the recorded flows.
