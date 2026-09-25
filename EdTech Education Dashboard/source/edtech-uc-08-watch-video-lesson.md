# UC-08: Watch a Video Lesson and Save Progress

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Watch a Video Lesson and Save Progress

Description:

- Lets an enrolled Student play a course video, resume its saved position, and record completed playback coverage for unit-level progress.
- Completes UC-07 VIDEO navigation and supplies actual video-unit completion to UC-05/06. The experiment records player-reported playback coverage; it does not claim verified attendance, attention, or proctoring.
- The 90% completion threshold, progress contract, and concurrency rules are project decisions. The Figma frame supports the player layout and controls.

Primary Actor:

Authenticated, onboarded Student enrolled in the video course.

Preconditions:

- UC-07 resolves the requested VIDEO unit and renders the course sidebar at `/student/courses/:courseId/units/:unitId`.
- A playable experiment video with matching duration is configured. Use a real bundled fixture asset; the blank source player is not a working video.
- The fixed unit curriculum and shared progress aggregation are available. No online streaming provider or external account is required.

Postconditions:

- Success: The Student can view the lesson. Confirmed playback ranges and resume position persist for this account/unit. A first accepted nonempty coverage report starts the unit.
- Once unique covered content reaches at least 90% of video duration, the unit is completed once. Module/course counts update under UC-05/06; completion never increments twice.
- Failure: Rejected updates change no saved progress. Unsaved viewing is not shown as confirmed completion. Merely opening the player, seeking, or pressing Next earns no completion.

Main Flow:

1. The unit page requests video details and current saved progress after the UC-07 access check.
2. Load the configured asset; offer playback from resumePositionSeconds. A completed video defaults to replay from zero with a visible Completed state; the stored position is not reset by the read.
3. The Student presses Play. The player records continuous actually played intervals; a seek jump does not cover the skipped interval.
4. Send accumulated whole-second intervals and current position every 15 seconds while playback advances, and on pause/end or explicit Save progress. Serialize saves within the tab.
5. The backend validates the update, combines new coverage with already confirmed coverage, saves the position, and returns authoritative unit progress.
6. Reaching ceil(0.90 * durationSeconds) covered seconds marks the unit completed, preserves its first completedAt, and makes the updated progress available to UC-05–07.
7. Next navigates through UC-07 ordering. If unsaved coverage exists, attempt a save first; if it fails, let the Student retry or explicitly leave without that unsaved progress.

Alternative Flow:

A.1 — Player controls

- Enable Play/Pause, seek bar, elapsed/total time, volume/mute, fullscreen, and playback speed 0.5x, 1x, 1.5x, 2x. Playback speed changes wall-clock time, not content coverage.
- Captions are enabled only when the response supplies a track. Download is disabled in this baseline with an explanation; no unimplemented transcript or settings destination is linked.
- Preference changes remain local to this player; later Learning Preferences may provide defaults. No measured learning-time/streak metric is inferred from media position or coverage.

A.2 — Coverage and completion

- Store the union of accepted half-open intervals [startSeconds,endSeconds). Overlapping/replayed sections count once. coveredSeconds is the union length; coveragePercent=floor(100 * coveredSeconds / durationSeconds).
- Seeking to the end, reopening the page, or rewatching the same segment cannot substitute for covering missing content. All reporting is an experiment playback record, not a guarantee the person watched attentively.
- Completion is monotonic; replaying or moving backward cannot uncomplete a unit. startedAt/completedAt are server times of first qualifying accepted writes, not client-reported timestamps.
- Example duration 420 seconds requires 378 unique seconds. A [0,380) report meets the threshold; source sample timestamps are not hardcoded.

A.3 — Reload, concurrent devices, and repeats

- GET restores the last confirmed position/coverage. Buffered but unsaved playback may be lost on abrupt closure; do not promise background delivery.
- Each save includes updateId and expectedRevision. An accepted updateId with identical normalized payload returns HTTP 200 with current progress without applying it again; changed payload under that ID returns REQUEST_CONFLICT.
- Different new updates with stale revision return PROGRESS_CONFLICT. Fetch current progress, retain this tab's unsaved intervals, and allow a deliberate new save with the latest revision/new ID. Coverage unions naturally avoid double counting; do not silently overwrite another device's resume position during conflict recovery.
- Accepted-update associations remain while the enrollment's progress record exists. A replay does not change activity time or revision.

A.4 — Activity propagation

- A first start or newly covered seconds advances enrollment lastActivityAt to the accepted server time. A position-only save or duplicate replay does not count as new learning activity.
- On first unit completion, recompute shared module/course state coherently. Set course completedAt only on its first transition to all required units complete. Other units retain their outcomes.
- learningSeconds, streakDays, and weeklyGoalPercent remain null when their measurement/goal sources are absent, per UC-05. Coverage seconds are not measured study time.

Exception Flow:

E.1 — Asset failure

- If media cannot load/play, show Retry video. Do not send fabricated playback ranges. If its actual duration differs materially from the configured integer duration (more than one second), show a content-configuration error and stop progress reporting until corrected.

E.2 — Save uncertainty or conflict

- A timed-out/malformed save response leaves this update unresolved. Pause periodic writes, retain its ID/payload, and offer Retry save with that same update. Do not generate fresh IDs automatically for an unknown result.
- A successful replay resolves the pending update. A definite conflict follows A.3; service failure offers retry without reporting unsaved completion.
- The player may continue playing with a visible Progress not saved notice, buffering ranges for a later serialized save. A page/account change discards another account's buffered state.

E.3 — Session loss

- A 401 pauses reporting, clears private content, and opens Sign in. Previously confirmed progress remains; unconfirmed playback is not guaranteed. Onboarding/content errors follow the shared envelope.

UI Integration:

- `15 Courses Detail Video`, node `222:912`.
  https://www.figma.com/design/JDzl2rsSdGcA8tgcDG4kgy/EdTech?node-id=222-912
- Live context/screenshot inspected on 2026-09-20. Preserve sidebar, lesson heading, large player, play/volume/progress/time/fullscreen controls, and Next.
- Real playback behavior, coverage threshold, speed-menu choices, Save progress/retry feedback, disabled download, and leave-with-unsaved-progress notice are supplements. No mobile or frozen dataset claim. Render actual duration and current position, not source 2:00/7:00 sample values.

API Endpoint:

- `GET /api/v1/student/courses/:courseId/units/:unitId/video`
- `PUT /api/v1/student/courses/:courseId/units/:unitId/video/progress`
- `GET /api/v1/student/courses/:courseId/units/:unitId/video/media` (playable asset response; supports byte ranges)

Request Body:

GET accepts no body/query. PUT accepts exactly:
```json
{
  "updateId": "9a7de0e1-0197-4524-8534-b75217b14fa0",
  "expectedRevision": 0,
  "resumePositionSeconds": 380,
  "playedRanges": [
    {
      "startSeconds": 0,
      "endSeconds": 380
    }
  ]
}
```

IDs are UUIDs. expectedRevision is a nonnegative safe integer. Position and range endpoints are whole seconds within [0,durationSeconds]; start < end. playedRanges accepts 0–100 elements with exactly the two keys shown; an empty array saves only position and cannot start/complete a new unit. Merge adjacent/overlapping intervals and sort them for repeat comparison. Preserve any remaining buffered intervals for a later save if a payload exceeds 100 disjoint ranges. Reject unknown keys/query, wrong types, nonfinite/fractional numbers, and client status/completion timestamps.

Successful Response:

```json
{
  "success": true,
  "message": "Video lesson retrieved.",
  "data": {
    "courseId": "ba22825a-9acf-4d85-af5f-5c77f83d6ac7",
    "unitId": "af79a45f-d04a-4c78-b5be-30cac0e3d161",
    "title": "Installing Python & VS Code",
    "durationSeconds": 420,
    "mediaUrl": "/api/v1/student/courses/ba22825a-9acf-4d85-af5f-5c77f83d6ac7/units/af79a45f-d04a-4c78-b5be-30cac0e3d161/video/media",
    "captions": [],
    "progress": {
      "revision": 0,
      "status": "NOT_STARTED",
      "resumePositionSeconds": 0,
      "coveredSeconds": 0,
      "coveragePercent": 0,
      "startedAt": null,
      "completedAt": null
    }
  }
}
```

```json
{
  "success": true,
  "message": "Video progress saved.",
  "data": {
    "unitId": "af79a45f-d04a-4c78-b5be-30cac0e3d161",
    "progress": {
      "revision": 1,
      "status": "COMPLETED",
      "resumePositionSeconds": 380,
      "coveredSeconds": 380,
      "coveragePercent": 90,
      "startedAt": "2026-09-20T10:06:20.000Z",
      "completedAt": "2026-09-20T10:06:20.000Z"
    }
  }
}
```

- HTTP 200. IDs UUIDs; title nonempty; durationSeconds positive integer; captions is an array of {language: BCP-47 string, label: nonempty string, url: string}. Empty means no caption track. The fixture may omit captions entirely by returning [].
- mediaUrl/caption URLs are playable resource URLs restricted to this enrollment through the same account integration. The media handler must support byte-range playback (200/206) and unavailable-access responses; it is an asset response, not a JSON-success envelope. JSON API errors use the envelope below. A 416 range response follows the media protocol. No unrestricted public fixture URL is returned as if it enforced enrollment.
- All progress fields required: revision nonnegative integer; status NOT_STARTED|IN_PROGRESS|COMPLETED; resumePositionSeconds integer 0..duration; coveredSeconds integer 0..duration; coveragePercent integer 0..100; startedAt/completedAt nullable ISO UTC. completedAt exists only after completion; startedAt exists once coverage >0.
- Every accepted new update increments revision by one, including position-only updates. Replays do not increment. Completed progress may retain coverage below 100% if it passed 90%; its state remains COMPLETED.
- GET returns current authoritative progress; the first and second examples illustrate a transition from no coverage to a qualifying accepted batch. A real client normally sends smaller periodic batches. The course curriculum and aggregation from UC-06 are unchanged.

Error Response:

```json
{
  "success": false,
  "statusCode": 503,
  "code": "VIDEO_UNAVAILABLE",
  "message": "Video learning is temporarily unavailable. Please try again later.",
  "timestamp": "2026-09-20T10:00:00.000Z",
  "path": "/api/v1/student/courses/ba22825a-9acf-4d85-af5f-5c77f83d6ac7/units/af79a45f-d04a-4c78-b5be-30cac0e3d161/video/progress"
}
```

Use the shared envelope from UC-01–06: success=false, statusCode matching HTTP status, code, message, server ISO UTC timestamp, and actual pathname without query. Omit data. Only VALIDATION_ERROR may add errors mapping input paths to nonempty arrays of strings. All shown success keys are required; dates and IDs are examples, not fixed response values.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 401 | UNAUTHENTICATED | You must sign in to continue. |
| 403 | ONBOARDING_REQUIRED | Complete your learning profile to continue. |
| 404 | LEARNING_CONTENT_NOT_AVAILABLE | This learning content is not available. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

Every endpoint requires an ACTIVE, verified STUDENT session, completed onboarding, and current account enrollment in the requested course. The unit/module must belong to that course. Use the same generic 404 for missing content, wrong nesting/type, or missing enrollment. Malformed UUIDs are 400. 401 clears private state and opens `/sign-in`; 403 opens `/student/onboarding`; service failure is not logout. No query/body field may select another account. These UCs add no new rate-limit policy.

| HTTP | Code | Exact message |
| --- | --- | --- |
| 409 | PROGRESS_CONFLICT | Video progress changed. Load the latest progress before saving. |
| 409 | REQUEST_CONFLICT | This request identifier was already used for different content. |
| 503 | VIDEO_UNAVAILABLE | Video learning is temporarily unavailable. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement enrolled video reads, media delivery, and progress writes in NestJS/TypeScript. Validate unit type and account/course nesting on the actual write and asset access, not only initial page load. Maintain one coverage/position/revision record per enrollment/unit and the repeat association. Combine ranges, apply the threshold, and update shared unit/module/course outcomes coherently. This UC specifies outcomes without prescribing cryptography, limiter algorithms, or session internals.

### Frontend UI Context

Implement the real player in React/TypeScript/Tailwind inside UC-07's shell. Preserve visible source controls where supported, explain disabled download/captions, and render saved versus unsaved feedback. Player imagery is not a substitute for a playable media fixture.

### Frontend Logic and API Context

Record continuous playback intervals without bridging seek gaps; flush whole-second ranges periodically and on pause/end. Serialize requests, retain unresolved ID/payload, and distinguish accepted ranges from unsaved buffered intervals. Restore the saved position after metadata loads. Confirm completion from the response, then invalidate UC-05–07 progress reads. Navigation uses UC-07's ordering and the declared unsaved-progress behavior.

### Validation and Error-Handling Context

Validate IDs, enrollment, media duration, finite bounds, interval cardinality, revision, and repeat identity. Never trust client-provided status or award completion on page entry. Keep failures visible without fabricating progress and distinguish player-reported coverage from attendance or measured study duration.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
