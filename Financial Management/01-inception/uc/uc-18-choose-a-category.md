---
artifact_type: business-use-case-specification
status: "Draft"
uc_id: UC-18
uc_name: "Choose a Category"
---

# UC-18: Choose a Category

## Functional Use-Case Specification

### Use Case ID

UC-18

### Use Case Name

Choose a Category

### Description

Inspect category choices and select a category for a transaction or financial goal.

### Actor(s)

Primary: Account holder. Supporting: application client and application service.

### Priority

High.

### Trigger

The user opens the category selector in a form.

### Pre-Condition(s)

PRE-1: The application view is open in the client.

### Post-Condition(s)

POST-1: On success, the client displays the selected category in the requesting form.
POST-2: On failure, the client displays a recovery message in the current view.

### Basic Flow

1. The user opens the category selector in a form.
2. The client requests categories.
3. The system returns category choices.
4. The user selects a category.
5. The client requests category details.
6. The system returns the selection.
7. The client displays the selected category in the form.

### Alternative Flow

AF-1:

1. The user clears the category selector.
2. The client shows the form with no selected category.

### Exception Flow

EF-1:

1. The system returns an operation error.
2. The client displays the error message and keeps the current view open.
3. The actor revises the interaction or retries the request.

EF-2:

1. The system returns a rejected authentication context.
2. The client presents the login entry point.

### Related UI

- Product-source UI descriptions: [Use cases rows 64-81](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A64:B81). No Figma node identifier was supplied.

- Category detail presentation is a proposed extension grounded in the supplied category-detail endpoint, not a verified design screen.

- Goal category selector: [Use cases rows 299-316](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=0&range=A299:B316). Category endpoint evidence: [API rows 173-205](https://docs.google.com/spreadsheets/d/1b6nG8slHLf2CtXZwVHHsNrogvhHNg3lceK6f3B7mKIM/edit#gid=439687549&range=A173:B205).

### Related API IDs

- [API-CATEGORY-LIST](../api/api-category-list.md)
- [API-CATEGORY-DETAIL](../api/api-category-detail.md)

### Notes

See [source mapping](../../coverage-report.md), [review decisions](../../consistency-review.md), and [assumptions](../../ASSUMPTIONS.md). The supplied spreadsheet is specification evidence; no running application or Figma interaction was verified.

## UML Model

~~~plantuml
@startuml
hide empty members

class Category {
  +id: Integer
  +name: String
}

class CategoryQuery {
  +selectedId: Integer [0..1]
}

class CategoryResult {
  +success: Boolean
  +categories: Sequence(Category)
  +selected: Category [0..1]
}

class CategoryService {
  +choose(ctx: RequestContext, cmd: CategoryQuery): CategoryResult
}

class RequestContext {
  +userId: Integer
  +authenticated: Boolean
}

class User {
  +id: Integer
}

CategoryResult --> Category : categories
CategoryResult --> Category : selected

@enduml
~~~

## Business Rules

~~~ocl
-- BR-UC-18-01
-- Source: Product source
context CategoryService::choose(ctx: RequestContext, cmd: CategoryQuery): CategoryResult
pre BR_UC_18_01_AuthenticatedContext:
  ctx.authenticated and User.allInstances()->exists(u | u.id = ctx.userId)
~~~

~~~ocl
-- BR-UC-18-02
-- Source: Assumption
context CategoryService::choose(ctx: RequestContext, cmd: CategoryQuery): CategoryResult
post BR_UC_18_02_ExactList:
  result.success implies result.categories->collect(id)->asSet() = Category.allInstances()->collect(id)->asSet()
~~~

~~~ocl
-- BR-UC-18-03
-- Source: Assumption
context Category
inv BR_UC_18_03_CategoryIdentity:
  Category.allInstances()->isUnique(id)
~~~

~~~ocl
-- BR-UC-18-04
-- Source: Assumption
context CategoryService::choose(ctx: RequestContext, cmd: CategoryQuery): CategoryResult
post BR_UC_18_04_NoDuplicateChoices:
  result.categories->isUnique(id)
~~~

~~~ocl
-- BR-UC-18-05
-- Source: Assumption
context CategoryService::choose(ctx: RequestContext, cmd: CategoryQuery): CategoryResult
post BR_UC_18_05_ChoiceMapping:
  result.categories->forAll(v | Category.allInstances()->exists(c | c.id = v.id and c.name = v.name))
~~~

~~~ocl
-- BR-UC-18-06
-- Source: Assumption
context CategoryService::choose(ctx: RequestContext, cmd: CategoryQuery): CategoryResult
post BR_UC_18_06_DeterministicOrder:
  result.categories->size() <= 1 or Sequence{1..result.categories->size()-1}->forAll(i | result.categories->at(i).id < result.categories->at(i+1).id)
~~~

~~~ocl
-- BR-UC-18-07
-- Source: Assumption
context CategoryService::choose(ctx: RequestContext, cmd: CategoryQuery): CategoryResult
post BR_UC_18_07_SelectedIdentity:
  result.success implies (if cmd.selectedId.oclIsUndefined() then result.selected.oclIsUndefined() else Category.allInstances()->one(c | c.id = cmd.selectedId and result.selected.id = c.id and result.selected.name = c.name) endif)
~~~

~~~ocl
-- BR-UC-18-08
-- Source: Product source
-- Equality denotes the complete persistent value snapshot, including every property, not object identity alone.
context CategoryService::choose(ctx: RequestContext, cmd: CategoryQuery): CategoryResult
post BR_UC_18_08_CategoryUnchanged:
  Category.allInstances()->collect(e | Tuple{id = e.id, name = e.name})->asSet() = Category.allInstances()@pre->collect(e | Tuple{id = e.id@pre, name = e.name@pre})->asSet()
~~~
