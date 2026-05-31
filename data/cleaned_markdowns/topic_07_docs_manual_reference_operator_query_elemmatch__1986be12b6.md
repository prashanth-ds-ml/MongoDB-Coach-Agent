> Source: https://www.mongodb.com/docs/manual/reference/operator/query/elemMatch/
> Fetch method: direct_markdown

# $elemMatch (query predicate operator)

$elemMatch (projection operator)

## Definition

`$elemMatch`
The `$elemMatch` operator matches documents that contain an array field with at least one element that matches all the specified query criteria.

## Syntax

```javascript
{ <field>: { $elemMatch: { <query1>, <query2>, ... } } }
```

## Behavior

- You cannot specify a `$where` operator in an `$elemMatch`.

- You cannot specify a `$text` query operator in an `$elemMatch`.

## Examples

### Element Match

Given the following documents in the `scores` collection:

```javascript
{ _id: 1, results: [ 82, 85, 88 ] }
{ _id: 2, results: [ 75, 88, 89 ] }
```

The following query matches only those documents where the `results` array contains at least one element that is both greater than or equal to `80` and is less than `85`:

```javascript
db.scores.find(
   { results: { $elemMatch: { $gte: 80, $lt: 85 } } }
)
```

The query returns the following document because the element `82` is both greater than or equal to `80` and is less than `85`:

```javascript
{ "_id" : 1, "results" : [ 82, 85, 88 ] }
```

For more information on specifying multiple criteria on array elements, see Specify Multiple Conditions for Array Elements.

### Array of Embedded Documents

This statement inserts documents into the `survey` collection:

```javascript
db.survey.insertMany( [
   { "_id": 1, "results": [ { "product": "abc", "score": 10 },
                            { "product": "xyz", "score": 5 } ] },
   { "_id": 2, "results": [ { "product": "abc", "score": 8 },
                            { "product": "xyz", "score": 7 } ] },
   { "_id": 3, "results": [ { "product": "abc", "score": 7 },
                            { "product": "xyz", "score": 8 } ] },
   { "_id": 4, "results": [ { "product": "abc", "score": 7 },
                            { "product": "def", "score": 8 } ] },
   { "_id": 5, "results": { "product": "xyz", "score": 7 } }
] )
```

The document with an `_id` of `5` doesn't contain an array. That document is included to show that `$elemMatch` only matches array elements, which you will see in the following examples.

The following query matches documents where `results` contains at least one element where `product` is `"xyz"` and `score` is greater than or equal to `8`:

```javascript
db.survey.find(
   { results: { $elemMatch: { product: "xyz", score: { $gte: 8 } } } }
)
```

Specifically, the query matches the following document:

```javascript
{ "_id" : 3, "results" : [ { "product" : "abc", "score" : 7 },
                           { "product" : "xyz", "score" : 8 } ] }
```

### Single Query Condition

The following sections show the output differences when you use `$elemMatch` with a single query condition, and omit `$elemMatch`.

#### Example 1

Query with `$elemMatch`:

```javascript
db.survey.find(
   { results: { $elemMatch: { product: "xyz" } } }
)
```

The query returns documents where any `product` in `results` is `"xyz"`:

```javascript
[
   {
      _id: 1,
      results: [ { product: 'abc', score: 10 }, { product: 'xyz', score: 5 } ]
   },
   {
      _id: 2,
      results: [ { product: 'abc', score: 8 }, { product: 'xyz', score: 7 } ]
   },
   {
      _id: 3,
      results: [ { product: 'abc', score: 7 }, { product: 'xyz', score: 8 } ]
   }
]
```

Query without `$elemMatch`:

```javascript
db.survey.find(
   { "results.product": "xyz" }
)
```

In the following output, notice that the document with an `_id` of `5` (which doesn't contain an array) is also included:

```javascript
[
   {
      _id: 1,
      results: [ { product: 'abc', score: 10 }, { product: 'xyz', score: 5 } ]
   },
   {
      _id: 2,
      results: [ { product: 'abc', score: 8 }, { product: 'xyz', score: 7 } ]
   },
   {
      _id: 3,
      results: [ { product: 'abc', score: 7 }, { product: 'xyz', score: 8 } ]
   },
   { _id: 5, results: { product: 'xyz', score: 7 } }
]
```

#### Example 2

Consider the following queries:

- First query has a single `<query>` condition in `$elemMatch`.

- Second query omits `$elemMatch`.

First query with `$elemMatch`:

```javascript
db.survey.find(
   { "results": { $elemMatch: { product: { $ne: "xyz" } } } }
)
```

The query returns documents that has a `product` with value other than `"xyz"`:

```javascript
{ "_id" : 1, "results" : [ { "product" : "abc", "score" : 10 },
                           { "product" : "xyz", "score" : 5 } ] }
{ "_id" : 2, "results" : [ { "product" : "abc", "score" : 8 },
                           { "product" : "xyz", "score" : 7 } ] }
{ "_id" : 3, "results" : [ { "product" : "abc", "score" : 7 },
                           { "product" : "xyz", "score" : 8 } ] }
{ "_id" : 4, "results" : [ { "product" : "abc", "score" : 7 },
                           { "product" : "def", "score" : 8 } ] }
```

Second query without `$elemMatch`:

```javascript
db.survey.find(
   { "results.product": { $ne: "xyz" } }
)
```

The query returns documents where none of the `product` `results` are `"xyz"`:

```javascript
{ "_id" : 4, "results" : [ { "product" : "abc", "score" : 7 },
                           { "product" : "def", "score" : 8 } ] }
```

Both queries include the document with an `_id` of `4`, and omit the document with an `_id` of `5` because the `product` is `"xyz"`.
