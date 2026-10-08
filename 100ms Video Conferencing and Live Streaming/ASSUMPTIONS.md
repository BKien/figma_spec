# Assumptions

These explicit assumptions complete the existing supported Figma scope. They are implementation decisions, not additional claims about the design or the 100ms provider. Rule blocks cite the stable IDs below.

## A-01 — Preview and names

Display names are trimmed and contain 1–50 characters after trimming; preview and join use the same rule. Permissions, hardware and requested track state govern local preview. Viewer preview starts muted. These are assumptions, not asserted hidden Figma facts.

Rule references: `BR-JOIN-PREVIEW-01`, `BR-JOIN-PREVIEW-02`, `BR-JOIN-PREVIEW-03`, `BR-JOIN-PREVIEW-04`, `BR-JOIN-PREVIEW-05`, `BR-JOIN-PREVIEW-06`, `BR-JOIN-PREVIEW-07`, `BR-JOIN-SESSION-04`.

## A-02 — Join and session lifecycle

Provisioning supplies a designated host principal before join. Host identity takes precedence over role defaults. The host joins as HOST; other live-stream participants join as VIEWER and conference participants as BROADCASTER. Host join opens LOBBY to LIVE. Non-hosts can wait in LOBBY. Duplicate joined membership for a principal is rejected. Capacities are 100 conference members, 1,000 stream members and 10 on-stage members, including the host.

Rule references: `BR-JOIN-SESSION-05`, `BR-JOIN-SESSION-06`, `BR-JOIN-SESSION-07`, `BR-JOIN-SESSION-08`, `BR-JOIN-SESSION-09`, `BR-JOIN-SESSION-10`, `BR-JOIN-SESSION-11`.

## A-03 — Stream start and completion

Only the joined host starts a READY stream in a LIVE session. START produces STARTING; a trusted provider completion produces LIVE or resets to READY on failure. A completion is conditional on its resource version, so a stale completion cannot undo STOP/END.

Rule references: `BR-START-STREAM-04`, `BR-START-STREAM-05`, `BR-START-STREAM-06`, `BR-START-STREAM-07`, `BR-START-STREAM-08`, `BR-START-STREAM-09`.

## A-04 — Stream stop and restart

Only the joined host stops STARTING/LIVE. STOP produces ENDED but preserves the session status. A stopped stream cannot restart in that session. A new provisioned session is required. The stop operation also applies the cascade rules.

Rule references: `BR-STOP-STREAM-04`, `BR-STOP-STREAM-05`, `BR-STOP-STREAM-06`, `BR-STOP-STREAM-07`.

## A-05 — Viewer representation

Viewer playback uses LIVE stream state; viewer publishing is disabled. Stage participants may publish while the stream is live. Autoplay starts muted.

Rule references: `BR-WATCH-STREAM-02`, `BR-WATCH-STREAM-03`, `BR-WATCH-STREAM-04`, `BR-WATCH-STREAM-05`, `BR-WATCH-STREAM-06`, `BR-WATCH-STREAM-07`.

## A-06 — Stage requests

Joined viewers create one pending request while the stream is live. CREATE has no request/version target. A viewer cancels only its own pending request with the observed request version.

Rule references: `BR-REQUEST-STAGE-04`, `BR-REQUEST-STAGE-05`, `BR-REQUEST-STAGE-06`, `BR-REQUEST-STAGE-07`, `BR-REQUEST-STAGE-08`.

## A-07 — Stage decisions

Only the joined host decides a pending request belonging to the same live stream session. ACCEPT changes the viewer role to STAGE_PARTICIPANT; REJECT preserves it. ACCEPT enforces the 10-person stage limit. Version comparison makes decisions atomic.

Rule references: `BR-RESPOND-STAGE-04`, `BR-RESPOND-STAGE-05`, `BR-RESPOND-STAGE-06`, `BR-RESPOND-STAGE-07`, `BR-RESPOND-STAGE-08`.

## A-08 — Participant reads

Joined members read their session roster. Page size defaults to 50 and must be 1–50. The roster uses stable ascending joinedAt/id keyset order, without inferred host-first ranking. Cursors are scoped to the session and collection.

Rule references: `BR-SESSION-PARTICIPANTS-02`, `BR-SESSION-PARTICIPANTS-03`, `BR-SESSION-PARTICIPANTS-07`.

## A-09 — Chat

Joined members send nonempty trimmed messages of at most 1,000 characters. The stored normalized body is returned. Server timestamps and session revision sequences identify messages. Chat is rendered as plain text; trimming is not an HTML sanitizer.

Rule references: `BR-SEND-CHAT-04`, `BR-SEND-CHAT-05`, `BR-SEND-CHAT-06`.

## A-10 — Reactions

Canonical values are LIKE, CLAP, HEART, CELEBRATE, HAND and SURPRISE. Clients map these to the six emoji appearances. Reaction HAND is visual feedback, not an implicit stage request.

Rule references: `BR-SEND-REACTION-04`, `BR-SEND-REACTION-05`, `BR-SEND-REACTION-06`, `BR-SEND-REACTION-07`.

## A-11 — Sharing

Only one share is active in a session. A live-stream viewer cannot start sharing. START requires a selected SCREEN/PDF kind and a source reference supplied by the media/content adapter, and has no expected share version. The owner or joined host stops the current share with its observed version.

Rule references: `BR-SHARE-CONTENT-04`, `BR-SHARE-CONTENT-05`, `BR-SHARE-CONTENT-06`.

## A-12 — Preview drafts and media preferences

Before join, device choices are local draft state. Join transfers them and creates the participant preference rows. Device availability is checked by the client adapter. Server PATCH stores opaque references. All server preference operations are self-only; omitted fields are preserved and explicit null clears nullable fields.

Rule references: `BR-JOIN-SESSION-13`, `BR-CONFIGURE-DEVICES-03`, `BR-CONFIGURE-DEVICES-04`, `BR-CONFIGURE-DEVICES-05`, `BR-CONFIGURE-DEVICES-06`, `BR-CONFIGURE-DEVICES-07`, `BR-CONFIGURE-DEVICES-08`, `BR-CONFIGURE-DEVICES-09`, `BR-CONFIGURE-DEVICES-10`, `BR-CONFIGURE-DEVICES-11`, `BR-CONFIGURE-DEVICES-12`, `BR-CONFIGURE-DEVICES-13`.

## A-13 — Virtual backgrounds

The catalog lists enabled background assets. The no-background choice is null. A local preview selection becomes a draft until join; joined selections use the same preference PATCH.

Rule references: `BR-JOIN-SESSION-12`, `BR-SELECT-BACKGROUND-01`, `BR-SELECT-BACKGROUND-02`, `BR-SELECT-BACKGROUND-03`, `BR-SELECT-BACKGROUND-04`, `BR-SELECT-BACKGROUND-06`, `BR-SELECT-BACKGROUND-07`.

## A-14 — Layout and panels

Layout and pictureInPicture cannot be null. PiP clears the side panel; otherwise the panel is null, CHAT, PARTICIPANTS or SETTINGS. PRESENTER can be selected only with an active content share. Updates are personal.

Rule references: `BR-SESSION-LAYOUT-01`, `BR-SESSION-LAYOUT-02`, `BR-SESSION-LAYOUT-03`, `BR-SESSION-LAYOUT-04`, `BR-SESSION-LAYOUT-05`, `BR-SESSION-LAYOUT-06`, `BR-SESSION-LAYOUT-07`.

## A-15 — Pin and spotlight

Pin is a personal view preference, matching `Pin Tile for Myself` in the Figma tile menu. Spotlight is session-scoped, matching `Spotlight Tile for Everyone`; the session state exposes one nullable spotlight target to every client. Pin and spotlight targets must be joined in the same session. The design shows spotlight to publishing participants, so HOST, BROADCASTER and STAGE_PARTICIPANT may set or clear it; VIEWER may not. Personal pins remain unchanged when the shared spotlight changes.

Rule references: `BR-PIN-SPOTLIGHT-01`, `BR-PIN-SPOTLIGHT-02`, `BR-PIN-SPOTLIGHT-03`, `BR-PIN-SPOTLIGHT-06`, `BR-PIN-SPOTLIGHT-07`, `BR-PIN-SPOTLIGHT-08`, `BR-PIN-SPOTLIGHT-09`, `BR-PIN-SPOTLIGHT-10`.

## A-16 — Recording

Only the joined host controls recording. START in a LIVE session creates a STARTING record with a creation timestamp at version 1 with no expected recording version. One STARTING/RECORDING instance is permitted. Provider completion changes it to RECORDING or FAILED. STOP compares the current recording version. Provider references remain internal.

Rule references: `BR-RECORD-SESSION-04`, `BR-RECORD-SESSION-05`, `BR-RECORD-SESSION-06`, `BR-RECORD-SESSION-07`, `BR-RECORD-SESSION-08`.

## A-17 — Leave

A non-host leaves independently and the session status is preserved. The host uses End for everyone; host transfer is not introduced. Leave disables media, stops owned content and cancels pending requests. Rejoin creates a new participant ID for the same principal.

Rule references: `BR-LEAVE-SESSION-04`, `BR-LEAVE-SESSION-05`, `BR-LEAVE-SESSION-06`, `BR-LEAVE-SESSION-07`.

## A-18 — End for everyone

The joined host ends a non-ended session with its observed session version. The session becomes ENDED, joined participants become LEFT, media is disabled, and the stream, recording, share and pending-request cascades run atomically.

Rule references: `BR-END-SESSION-04`, `BR-END-SESSION-05`, `BR-END-SESSION-06`, `BR-END-SESSION-07`, `BR-END-SESSION-08`.

## A-19 — Trust and identity

Both registered and anonymous users receive an externally provisioned bearer session access token with a stable principal ID and session scope. The token remains usable across the documented endpoints; join does not exchange it. Command actor IDs come from trusted membership resolution. Provider callbacks use separate authentication. UUID text is used consistently at wire and database boundaries. Raw tokens are not persisted.

Rule references: `BR-JOIN-SESSION-01`, `BR-JOIN-SESSION-02`, `BR-START-STREAM-01`, `BR-START-STREAM-02`, `BR-STOP-STREAM-01`, `BR-STOP-STREAM-02`, `BR-WATCH-STREAM-01`, `BR-REQUEST-STAGE-01`, `BR-REQUEST-STAGE-02`, `BR-RESPOND-STAGE-01`, `BR-RESPOND-STAGE-02`, `BR-SESSION-PARTICIPANTS-01`, `BR-SEND-CHAT-01`, `BR-SEND-CHAT-02`, `BR-SEND-CHAT-07`, `BR-SEND-REACTION-01`, `BR-SEND-REACTION-02`, `BR-SHARE-CONTENT-01`, `BR-SHARE-CONTENT-02`, `BR-CONFIGURE-DEVICES-01`, `BR-SELECT-BACKGROUND-05`, `BR-PIN-SPOTLIGHT-04`, `BR-RECORD-SESSION-01`, `BR-RECORD-SESSION-02`, `BR-LEAVE-SESSION-01`, `BR-LEAVE-SESSION-02`, `BR-END-SESSION-01`, `BR-END-SESSION-02`.

## A-20 — Mutation execution and retry

Every public server mutation, including join and preferences, uses MutationGateway. A serializable transaction locks the session row before lookup and dispatch. Deduplication key scope is principal/session/operation/key and uses a canonical payload hash. Same-key same-payload replay returns the immutable original HTTP response without dispatch. A changed payload is a conflict. Successful receipts are retained for 24 hours; an expired record is atomically replaced on a fresh command; infrastructure failures roll back. Fresh successful commands and provider completions advance session.version once. Replays do not rerun domain preconditions, including after leave/end. All effects, result serialization and the receipt commit atomically; no raw bearer/provider token is stored.

Rule references: `BR-JOIN-SESSION-03`, `BR-JOIN-SESSION-14`, `BR-JOIN-SESSION-15`, `BR-JOIN-SESSION-16`, `BR-JOIN-SESSION-17`, `BR-START-STREAM-03`, `BR-STOP-STREAM-03`, `BR-REQUEST-STAGE-03`, `BR-RESPOND-STAGE-03`, `BR-SEND-CHAT-03`, `BR-SEND-REACTION-03`, `BR-SHARE-CONTENT-03`, `BR-CONFIGURE-DEVICES-02`, `BR-PIN-SPOTLIGHT-05`, `BR-RECORD-SESSION-03`, `BR-LEAVE-SESSION-03`, `BR-END-SESSION-03`.

## A-21 — Cascades

Stream stop demotes former stage participants, disables their publication, stops shares and recordings, and cancels pending stage requests. Leave applies owned-share and own-request cleanup. End applies all cleanup and closes even a READY stream. Cleanup uses pre-state membership and advances each changed resource version.

Rule references: `BR-STOP-STREAM-08`, `BR-STOP-STREAM-09`, `BR-STOP-STREAM-10`, `BR-STOP-STREAM-11`, `BR-LEAVE-SESSION-08`, `BR-LEAVE-SESSION-09`, `BR-LEAVE-SESSION-10`, `BR-END-SESSION-09`, `BR-END-SESSION-10`, `BR-END-SESSION-11`.

## A-22 — Persistence and concurrent constraints

Conditional unique expression indexes enforce one joined membership per principal/session, one joined host, one pending request per viewer, one active share and one active recording. Historical terminal rows remain repeatable. Session-row serialization enforces aggregate capacities and orders state changes with callbacks. Composite foreign keys bind actors/resources to the same session.

Rule references: `BR-JOIN-SESSION-18`, `BR-JOIN-SESSION-19`, `BR-REQUEST-STAGE-09`, `BR-SHARE-CONTENT-07`, `BR-RECORD-SESSION-09`.

## A-23 — Read and adapter boundaries

Session-state polling supplies session/resource versions, self media/view preferences, host-visible stage requests (or only the caller requests), and reaction events. A departed member may retrieve final state only after the session has ended. Chat has a separate ascending-sequence read API. Message/reaction cursors retain a high-water mark for polling; reaction pages contain at most 50 events. Session-state reads use a consistent database snapshot. Media bytes, PDF upload/source registration, session provisioning and credential issuance belong to named external adapters; their internals are outside this product package.

Rule references: `BR-SESSION-PARTICIPANTS-04`, `BR-SESSION-PARTICIPANTS-05`, `BR-SESSION-PARTICIPANTS-06`, `BR-SEND-CHAT-08`, `BR-SEND-CHAT-09`.
