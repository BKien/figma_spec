# Common API Contract

All paths are relative to the service origin and return JSON. Success responses use `success: true` and a `data` object. Error responses use an `error` object with stable `code` and human-readable `message`. IDs are opaque strings. Calendar dates use ISO 8601 `YYYY-MM-DD`; timestamps use RFC 3339. Lists can include `nextCursor` for continuation. A missing cursor means no further page. The endpoint files describe transport shape only; domain policy is in the linked use cases.
