# Coverage Report

## Normalized boundary

UC-01 through UC-20 form the normalized package boundary. Supplied UC-21 and UC-22 remain byte-preserved under `source/` because the repository contract caps a normalized package at 20 use cases.

| Candidate ID | Actor goal | Status | Gap |
| --- | --- | --- | --- |
| UC-01 | Register Account and Verify Email | Supported | None. |
| UC-02 | Sign In | Supported | None. |
| UC-03 | Recover Password | Supported | None. |
| UC-04 | Browse, Search and Filter Products | Supported | None. |
| UC-05 | View Product Details | Supported | None. |
| UC-06 | Manage Shopping Cart | Supported | None. |
| UC-07 | Checkout and Place Order | Supported | None. |
| UC-08 | Track Order | Supported | None. |
| UC-09 | Manage Wishlist | Supported | None. |
| UC-10 | Compare Products | Supported | None. |
| UC-11 | Manage Account Profile | Supported | None. |
| UC-12 | Change Password | Supported | None. |
| UC-13 | Manage Saved Billing and Shipping Addresses | Supported | None. |
| UC-14 | View and Manage Browsing History | Supported | None. |
| UC-15 | View Account Order History | Supported | None. |
| UC-16 | View Order Details | Supported | None. |
| UC-17 | Rate a Delivered Order | Supported | None. |
| UC-18 | Find Help and Read FAQs | Supported | None. |
| UC-19 | Submit a Support Request | Supported | None. |
| UC-20 | Browse and Read Blog Articles | Supported | None. |
| UC-21 | Read and Post Blog Comments | Excluded from normalized boundary | Preserved verbatim under source/ because the repository contract permits no more than 20 normalized use cases per package. |
| UC-22 | Sign Out of the Current Session | Excluded from normalized boundary | Preserved verbatim under source/ because the repository contract permits no more than 20 normalized use cases per package. |

All attached files, including candidates outside the normalized boundary, are retained unchanged under `source/`.
