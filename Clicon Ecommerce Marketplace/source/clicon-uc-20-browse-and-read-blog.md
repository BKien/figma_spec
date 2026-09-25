# UC-20: Browse and Read Blog Articles

## Functional Use-Case Specification

USE CASE SPECIFICATION

Use Case Name:

Browse and Read Blog Articles

Description:

- Lets visitors find published editorial articles through keyword, category, tag, sort, and pagination, then read a complete article and navigate related sidebar content.
- Combines list and reading as one content-discovery goal. Comment reading/posting is UC-21; no article-authoring CMS, advertising service, or external social posting is included.
- Search/sort rules, article schema, and content fixtures are project decisions; Figma supplies the list/detail desktop composition.

Primary Actor:

Visitor or signed-in Customer.

Preconditions:

Public `/blog` and `/blog/:slug` routes exist with reload support. The content store supplies coherent published articles and their assets. No login is required.

Postconditions:

- Success: The visitor finds matching published articles and reads the requested article, or sees an explicit no-results state.
- Failure: Missing/unpublished articles show not-found; service failure is distinct. Reads do not post comments, increment fabricated view counters, or alter shopping/account state.

Main Flow:

1. The visitor opens `/blog` through a project navigation link added to the shared footer.
2. The frontend requests metadata and the first list page, rendering categories, article cards, search/sort, sidebar, and pagination.
3. The visitor changes keyword/category/tag/sort; the URL records those filters and the list resets to page 1.
4. Read more, a card title/image, or a Latest Blog link opens `/blog/:slug`.
5. The detail endpoint returns the article body; the frontend renders the cover, coherent author/category/date, body blocks, and sidebar.
6. Browser Back restores the prior list filters/page. Article comments are loaded independently through UC-21.

Alternative Flow:

A.1 — Filters and sort

- q is a case-insensitive literal substring in title/excerpt. Category and tag are exact published metadata slugs; all supplied filters combine with AND. Only one category and one tag may be active; All clears category.
- Sort newest uses publishedAt descending/id descending. Oldest uses both ascending. Most Popular uses public commentCount descending, then publishedAt/id descending. These rules are project decisions, not hidden analytics.
- Search submits on Enter/button; selector/tag changes apply immediately. Changing any filter/sort resets page 1. No results offers Clear filters.

A.2 — Sidebar and content

- Latest Blog lists the three newest published articles (excluding the current article on detail). Gallery is up to eight configured images for visual context; images are not invented navigation destinations. Tags navigate to `/blog?tag=<slug>`.
- Clicking the comment count moves to the detail comments anchor. UC-21 owns its content; a missing comment service does not block article reading.
- Share icons remain disabled with a scope explanation. There is no automated social post, unsupported copy-success claim, or newsletter integration.

A.3 — No content and removed article

- An empty published collection returns a successful empty list. A removed/unpublished direct slug returns ARTICLE_NOT_FOUND with Back to blog.
- Optional gallery/latest groups may be empty. Missing image assets use labelled placeholders; no unrelated filler article is substituted.

Exception Flow:

E.1 — Invalid filters or slug

- Malformed/unknown category/tag, duplicate query keys, unsupported sort, or invalid page returns VALIDATION_ERROR. Show recovery to unfiltered blog rather than silently changing the request.

E.2 — Service or navigation failure

- BLOG_UNAVAILABLE gives a retry for the current list/article. Ignore older responses after navigation so a different article cannot appear under the failed slug.
- Pagination is a live list: new publications/comments may shift later pages. Replace page contents, do not append them into a claimed frozen dataset.

UI Integration:

- Sources: `25_Blog List`, node `494:17620`, and `26_Blog Detail`, node `494:18663`.
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=494-17620
  https://www.figma.com/design/LEzMSML2K1XeZAxmvNvEYm/Clicon---eCommerce-Marketplace-Website-Figma-Template--Community---Community---Copy-?node-id=494-18663
- Live detail screenshot/context inspected on 2026-09-19. The list was too large; focused contexts/screenshots verified search/sort `494:18186`, card `494:18036`, sidebar `494:18404`, and pagination `494:18637` against its frame metadata.
- Preserve two-column article-card grid, category sidebar, Latest Blog/Gallery/Popular Tag sections, orange Read more/pagination, and article cover/body composition with Public Sans. Error/no-results and sort menu options beyond visible Most Popular are project supplements.
- Correct sample author inconsistencies by using one authorName. Body imagery/text must form coherent article fixtures, not the source's unrelated filler. No complete frozen dataset or mobile detail frame is claimed.
- UC-21 replaces the detail comments integration area. Until integrated, its form is disabled; no comment-count example such as 738 is hardcoded.

API Endpoint:

`GET /api/v1/blog/metadata`

`GET /api/v1/blog/articles`

`GET /api/v1/blog/articles/:slug`

Request Body:

No bodies. Metadata/detail accept no query parameters. slug is 1–160 lowercase alphanumeric words separated by single hyphens.

List accepts q (optional trimmed text max 100 code points; blank omitted), category/tag (optional known metadata slug), sort (newest, oldest, popular; default popular), page (decimal integer 1–1000000, default 1). Fixed pageSize=8. Reject unknown/repeated fields. Browser filters use the same names; an anchor is not sent to the API.

Successful Response:

```json
{
  "success": true,
  "message": "Blog metadata retrieved.",
  "data": {
    "categories": [
      {
        "slug": "computer-laptop",
        "name": "Computer & Laptop"
      }
    ],
    "tags": [
      {
        "slug": "laptops",
        "name": "Laptops"
      }
    ],
    "latest": [
      {
        "id": "554df919-d792-4db8-8d15-898854c38f81",
        "slug": "choosing-a-laptop",
        "title": "Choosing a laptop for everyday work",
        "excerpt": "A guide to matching laptop features to everyday tasks.",
        "imageUrl": "/images/blog/laptop-guide.jpg",
        "imageAlt": "Laptop on a desk",
        "authorName": "Clicon Editorial",
        "category": {
          "slug": "computer-laptop",
          "name": "Computer & Laptop"
        },
        "tags": [
          {
            "slug": "laptops",
            "name": "Laptops"
          }
        ],
        "publishedAt": "2026-09-19T09:00:00.000Z",
        "commentCount": 0
      }
    ],
    "gallery": [
      {
        "url": "/images/blog/laptop-guide.jpg",
        "alt": "Laptop on a desk"
      }
    ]
  }
}
```

```json
{
  "success": true,
  "message": "Blog articles retrieved.",
  "data": {
    "items": [
      {
        "id": "554df919-d792-4db8-8d15-898854c38f81",
        "slug": "choosing-a-laptop",
        "title": "Choosing a laptop for everyday work",
        "excerpt": "A guide to matching laptop features to everyday tasks.",
        "imageUrl": "/images/blog/laptop-guide.jpg",
        "imageAlt": "Laptop on a desk",
        "authorName": "Clicon Editorial",
        "category": {
          "slug": "computer-laptop",
          "name": "Computer & Laptop"
        },
        "tags": [
          {
            "slug": "laptops",
            "name": "Laptops"
          }
        ],
        "publishedAt": "2026-09-19T09:00:00.000Z",
        "commentCount": 0
      }
    ],
    "page": 1,
    "pageSize": 8,
    "totalItems": 1,
    "totalPages": 1
  }
}
```

```json
{
  "success": true,
  "message": "Blog article retrieved.",
  "data": {
    "article": {
      "id": "554df919-d792-4db8-8d15-898854c38f81",
      "slug": "choosing-a-laptop",
      "title": "Choosing a laptop for everyday work",
      "excerpt": "A guide to matching laptop features to everyday tasks.",
      "imageUrl": "/images/blog/laptop-guide.jpg",
      "imageAlt": "Laptop on a desk",
      "authorName": "Clicon Editorial",
      "category": {
        "slug": "computer-laptop",
        "name": "Computer & Laptop"
      },
      "tags": [
        {
          "slug": "laptops",
          "name": "Laptops"
        }
      ],
      "publishedAt": "2026-09-19T09:00:00.000Z",
      "commentCount": 0,
      "body": [
        {
          "type": "paragraph",
          "text": "Choose features that match the work you do most often."
        },
        {
          "type": "heading",
          "text": "Compare practical needs"
        },
        {
          "type": "list",
          "items": [
            "Screen size",
            "Memory",
            "Storage"
          ]
        },
        {
          "type": "quote",
          "text": "Start with your tasks rather than a product label.",
          "attribution": null
        },
        {
          "type": "image",
          "url": "/images/blog/laptop-guide.jpg",
          "alt": "Laptop on a desk",
          "caption": null
        }
      ]
    }
  }
}
```
- HTTP 200. Summary keys are exactly those shown; IDs UUIDs; slugs unique; title/excerpt/authorName/imageAlt nonempty strings; imageUrl nullable; category {slug,name}; tags array of {slug,name}; publishedAt ISO UTC; commentCount nonnegative integer from UC-21.
- Detail adds ordered body blocks. Allowed exact block schemas: paragraph/heading {type,text}; list {type,items} with nonempty text array; quote {type,text,attribution} nullable attribution; image {type,url,alt,caption} nullable caption. Text is plain text. At least one text block is required; no arbitrary HTML field or script-bearing content format is introduced.
- Metadata arrays preserve configured order; latest reuses the same summary shape. Only published content appears. Return the four newest published summaries, or all available when fewer than four exist, using publishedAt/id descending. On list, display the first three; on detail, exclude its own ID first and then display the first three.
- totalPages=ceil(totalItems/8), zero if empty; out-of-range page returns empty items with current counts. Page rows/count are a consistent read. No query-created filter facets are fabricated.

Error Response:

Use the shared error envelope: success=false, statusCode matching HTTP status, code, message, server-generated ISO 8601 UTC timestamp, and actual request pathname without query string. Omit data. Optional errors is only for VALIDATION_ERROR and maps input paths to nonempty arrays of strings. All shown success keys are required; examples illustrate contracts rather than fixed data.

```json
{
  "success": false,
  "statusCode": 404,
  "code": "ARTICLE_NOT_FOUND",
  "message": "This article is not available.",
  "timestamp": "2026-09-19T10:00:00.000Z",
  "path": "/api/v1/blog/articles/choosing-a-laptop"
}
```

| HTTP | Code | Exact message |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Please correct the highlighted fields. |
| 404 | ARTICLE_NOT_FOUND | This article is not available. |
| 503 | BLOG_UNAVAILABLE | Blog content is temporarily unavailable. Please try again later. |
| 500 | INTERNAL_ERROR | Unable to complete your request. Please try again later. |

## Project-Specific Implementation Context

### Backend Implementation Context

Implement the three public NestJS endpoints with stable article identity, published visibility, metadata relations, exact filters/sorts, and structured content blocks. Reuse UC-21's visible comment count instead of a fixed sample number. No editing CMS, tracking beacon, view-counter write, or ranking algorithm beyond the declared sort is required.

### Frontend UI Context

Build BlogListPage/BlogDetailPage in React/TypeScript/Tailwind from the inspected components. Reuse common shell and pagination; render body blocks as defined components, with accessible heading order and meaningful image alt text. Preserve the comments region for UC-21.

### Frontend Logic and API Context

Keep list filters/page in URL and reset page after filter changes. Load metadata independently of primary content; a metadata failure can show sidebar retry while readable article content remains. Guard stale responses; on article change reset scroll/body/comment state. Browser Back restores list query. Format dates consistently in UTC with a visible timezone note where timestamps are shown.

### Validation and Error-Handling Context

Validate query/slug shapes and metadata membership. Distinguish empty matches, missing article, broken image, and unavailable content service. No raw error becomes a fake article or hardcoded count. Network/malformed responses offer manual retry for the current URL; comment failures do not erase a loaded article.

<!-- Preserve Technical Report content when supplied. Do not add Prompt E/Security Requirements here. -->
