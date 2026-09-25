# Coverage Report

## Normalized boundary

UC-01 through UC-20 form the normalized package boundary. Supplied UC-21 remains byte-preserved under `source/` because the repository contract caps a normalized package at 20 use cases.

| Candidate ID | Actor goal | Status | Gap |
| --- | --- | --- | --- |
| UC-01 | Register a Student Account and Verify Email | Supported | None. |
| UC-02 | Sign In to a Student Account | Supported | None. |
| UC-03 | Set Up a Student Learning Profile | Supported | None. |
| UC-04 | Discover Courses | Supported | None. |
| UC-05 | View the Learning Dashboard | Supported | None. |
| UC-06 | View Assigned Courses and Module Progress | Supported | None. |
| UC-07 | View Course Modules and Learning Content | Supported | None. |
| UC-08 | Watch a Video Lesson and Save Progress | Supported | None. |
| UC-09 | Take a Course Quiz and View the Result | Supported | None. |
| UC-10 | View and Update Student Contact Profile | Supported | None. |
| UC-11 | Manage Learning Preferences | Supported | None. |
| UC-12 | Manage Notification Preferences | Supported | None. |
| UC-13 | Change the Current Account Password | Supported | None. |
| UC-14 | Recover a Forgotten Password | Supported | None. |
| UC-15 | Sign Out of the Current Browser Session | Supported | None. |
| UC-16 | Register an Instructor Account | Supported | None. |
| UC-17 | Create and Edit a Course Draft | Supported | None. |
| UC-18 | Publish a Course and Assign Learners | Supported | None. |
| UC-19 | Inspect an Enrolled Learner’s Progress | Supported | None. |
| UC-20 | Manage Course Learning Deadlines | Supported | None. |
| UC-21 | Rate a Completed Course | Excluded from normalized boundary | Preserved verbatim under source/ because the repository contract permits no more than 20 normalized use cases per package. |

All attached files, including candidates outside the normalized boundary, are retained unchanged under `source/`.
