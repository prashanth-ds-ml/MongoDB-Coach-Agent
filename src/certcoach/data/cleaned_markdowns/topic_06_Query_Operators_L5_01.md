# Logical Query Predicate Operators

Logical operators return data based on boolean logic (and, or, and nor).

| Name | Description |
| --- | --- |
| `$and` | Joins query clauses with a logical `AND` and returns documents that match the conditions of all clauses. |
| `$nor` | Joins query clauses with a logical `NOR` and returns all documents that fail to match all clauses. |
| `$not` | Inverts the effect of a query predicate and returns documents that do *not* match the query predicate. |
| `$or` | Joins query clauses with a logical `OR` and returns all documents that match at least one clause. |

# $and (query predicate operator)

`$and`
`$and` performs a logical `AND` operation on an array of one or more expressions and selects the documents that satisfy all the expressions.

MongoDB provides an implicit `AND` operation when you specify a comma separated list of expressions.

## Syntax

The `$and` has the following syntax:

```javascript
{ $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
```

## Behavior

`$and``false`When evaluating the clauses in the `$and` expression, MongoDB's query optimizer considers which indexes are available that could help satisfy clauses of the `$and` expression when selecting the best plan to execute.

To allow the query engine to optimize queries, `$and` handles errors as follows:

- If any expression supplied to `$and` would cause an error when evaluated alone, the `$and` containing the expression may cause an error but an error is not guaranteed.

- An expression supplied after the first expression supplied to `$and` may cause an error even if the first expression evaluates to `false`.

Most programming languages and drivers, including the MongoDB Shell (`mongosh`), do not allow the construction of objects with duplicate keys at the same object level. For example:

```javascript
db.inventory.find( { price: { $in: [ 7.99, 3.99 ], $in: [ 4.99, 1.99 ] } } )
```

The previous query is invalid because the field name `price` has duplicate operators at the same object level. The query sent to the server differs from the intent. To make the query work, use an explicit `AND`:

```javascript
db.inventory.find( {
   $and: [
      { price: { $in: [ 7.99, 3.99 ] } },
      { price: { $in: [ 4.99, 1.99 ] } }
   ]
} )
```

The previous query explicitly checks that both conditions are satisfied: the `price` array must include at least one value from each `$in` set. For more information, see Examples.

## Examples

The examples match multiple expressions on the same field.

Consider this query:

```javascript
db.inventory.find( { $and: [ { price: { $ne: 1.99 } }, { price: { $exists: true } } ] } )
```

The query selects all documents in the `inventory` collection where:

- the `price` field value is not equal to `1.99` **and**

- the `price` field exists.

You can simplify this query by combining the operator expressions for the `price` field into a single query object with a nested implicit `AND`:

```javascript
db.inventory.find( { price: { $ne: 1.99, $exists: true } } )
```

Rewrites are not always possible, particularly when duplicate conditions exist on the same field. For example:

```javascript
db.inventory.find( { status: { $ne: "closed", $ne: "archived" } } )
```

The previous query is invalid because it uses `$ne` more than once on the `status` field at the same object level. Use `$nin` instead:

```javascript
db.inventory.find( { status: { $nin: [ "closed", "archived" ] } } )
```

Rewrite the query based on your intent. Consider this query:

```javascript
db.inventory.find( {
   $and: [
      { status: "new" },
      { status: "processing" }
   ]
} )
```

To find documents where `status` is either `new` or `processing`, use `$in`:

```javascript
db.inventory.find( { status: { $in: [ "new", "processing" ] } } )
```

If your `status` field is an array `[ "new", "processing" ]` and you want to check if the document contains both `new` and `processing`, use `$all`:

```javascript
db.inventory.find( { status: { $all: [ "new", "processing" ] } } )
```

The previous query is semantically equivalent to `AND`, but `$all` is clearer when querying array fields.

Similar to duplicate field names, the same considerations apply for duplicate operators used in the query.

# $nor (query predicate operator)

## Definition

`$nor`
`$nor` performs a logical `NOR` operation on an array of one or more query predicates and selects the documents that **fail** all the query predicates in the array. The `$nor` has the following syntax:

```javascript
{ $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
```

## Examples

### `$nor` Query with Two Expressions

Consider the following query which uses only the `$nor` operator:

```javascript
db.inventory.find( { $nor: [ { price: 1.99 }, { sale: true } ]  } )
```

This query will return all documents that:

- contain the `price` field whose value is *not* equal to `1.99` and contain the `sale` field whose value *is not* equal to `true` **or**

- contain the `price` field whose value is *not* equal to `1.99`
  *but* do *not* contain the `sale` field **or**

- do *not* contain the `price` field *but* contain the `sale` field whose value *is not* equal to `true` **or**

- do *not* contain the `price` field *and* do *not* contain the `sale` field

### `$nor` and Additional Comparisons

Consider the following query:

```javascript
db.inventory.find( { $nor: [ { price: 1.99 }, { qty: { $lt: 20 } }, { sale: true } ] } )
```

This query will select all documents in the `inventory` collection where:

- the `price` field value does *not* equal `1.99` **and**

- the `qty` field value is *not* less than `20` **and**

- the `sale` field value is *not* equal to `true`

including those documents that do not contain these field(s).

The exception in returning documents that do not contain the field in the `$nor` expression is when the `$nor` operator is used with the `$exists` operator.

### `$nor` and `$exists`

Compare that with the following query which uses the `$nor` operator with the `$exists` operator:

```javascript
db.inventory.find( { $nor: [ { price: 1.99 }, { price: { $exists: false } },
                             { sale: true }, { sale: { $exists: false } } ] } )
```

This query will return all documents that:

- contain the `price` field whose value is *not* equal to `1.99` and contain the `sale` field whose value *is not* equal to `true`

# $not (query predicate operator)

## Definition

`$not`
`$not` performs a logical `NOT` operation on the specified `<operator-expression>` and selects the documents that do *not* match the `<operator-expression>`. This includes documents that do not contain the `field`.

## Syntax

The `$not` operator has the following form:

```javascript
{ field: { $not: { <operator-expression> } } }
```

Consider the following example:

```javascript
db.movies.find( { runtime: { $not: { $gt: 180 } } } )
```

The example selects all documents in the `movies` collection where:

- the `runtime` field value is less than or equal to `180` **or**

- the `runtime` field does not exist

`{ $not: { $gt: 180 } }` differs from the `$lte` operator. `{ $lte: 180 }` returns *only* the documents where the `runtime` field exists and its value is less than or equal to `180`.

Use the `$not` operator with another operator expression. To use `$not` for an inequality check, use:

```javascript
{ runtime: { $not: { $eq: 120 } } }
```

The preceding query is equivalent to:

```javascript
{ runtime: { $ne: 120 } }
```

The following query is invalid because it compares a field without an operator:

```javascript
{ runtime: { $not: 120 } }
```

## Behavior

### Arrays

The `$not` operator can yield unexpected results when used with an array. To match documents based on multiple false conditions, use `$nor`.

### Regular Expressions

The examples on this page use data from the sample_mflix sample dataset. For details on how to load this dataset into your self-managed MongoDB deployment, see Load the sample dataset. If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

`$not` supports logical `NOT` operations on:

- Regular expression objects, such as `/pattern/`.

  The following example returns movies where `runtime` is greater than `1000` minutes and `title` does not start with the letter `T`. Because `$not` also matches documents that don't contain the `title` field, the query returns movies even when title data is unavailable:

  ```javascript
  db.movies.find(
     { title: { $not: /^T/ }, runtime: { $gt: 1000 } },
     { _id: 0, title: 1, runtime: 1 }
  )
  ```

  ```javascript
  [
    { title: 'Centennial', runtime: 1256 },
    { title: 'Baseball', runtime: 1140 }
  ]
  ```

- `$regex` operator expressions.

  The following two queries return movies where `runtime` is greater than `1000` minutes and `title` does not start with the letter `T`. The first query passes a string to `$regex`:

  ```javascript
  db.movies.find(
     { title: { $not: { $regex: "^T" } }, runtime: { $gt: 1000 } },
     { _id: 0, title: 1, runtime: 1 }
  )
  ```

  ```javascript
  [
    { title: 'Centennial', runtime: 1256 },
    { title: 'Baseball', runtime: 1140 }
  ]
  ```

  The second query passes a regex literal to `$regex`:

  ```javascript
  db.movies.find(
     { title: { $not: { $regex: /^T/ } }, runtime: { $gt: 1000 } },
     { _id: 0, title: 1, runtime: 1 }
  )
  ```

  ```javascript
  [
    { title: 'Centennial', runtime: 1256 },
    { title: 'Baseball', runtime: 1140 }
  ]
  ```

- Driver language regular expression objects.

  For example, the following PyMongo query uses Python's `re.compile()` method to compile a regular expression:

  ```python
  import re
  for noMatch in db.inventory.find( { "item": { "$not": re.compile("^p.*") } } ):
      print noMatch
  ```

# $or (query predicate operator)

`$or`
`$or` performs a logical `OR` operation on an array of one or more expressions and selects documents that satisfy at least one of the expressions.

## Syntax

The `$or` operator has the following syntax:

```javascript
{ $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
```

The examples on this page use data from the sample_mflix sample dataset. For details on how to load this dataset into your self-managed MongoDB deployment, see Load the sample dataset. If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

Consider the following example:

```javascript
db.movies.find(
   { $or: [ { runtime: { $gt: 1000 } }, { year: { $lt: 1910 } } ] },
   { _id: 0, title: 1, year: 1, runtime: 1 }
)
```

```javascript
[
  {
    runtime: 11,
    title: 'The Great Train Robbery',
    year: 1903
  },
  {
    runtime: 14,
    title: 'A Corner in Wheat',
    year: 1909
  },
  {
    runtime: 1256,
    title: 'Centennial',
    year: 1978
  },
  {
    runtime: 1140,
    title: 'Baseball',
    year: 1994
  },
  {
    runtime: 1,
    title: 'The Kiss',
    year: 1896
  },
  {
    runtime: 1,
    title: 'The Kiss',
    year: 1896
  }
]
```

This query selects all documents in the `movies` collection that meet either of the following conditions:

- The `runtime` field value is greater than `1000`.

- The `year` field value is earlier than `1910`.

## Behaviors

### `$or` Clauses and Indexes

When evaluating the clauses in the `$or` expression, MongoDB performs a collection scan or an index scan. If all clauses are supported by indexes, MongoDB performs index scans. To use indexes to evaluate an `$or` expression, all the clauses in the `$or` expression must be supported by indexes. Otherwise, MongoDB performs a collection scan.

When using indexes with `$or` queries, each clause of an `$or` can use its own index. Consider this query:

```javascript
db.movies.find(
   { $or: [ { runtime: { $gt: 1000 } }, { year: { $lt: 1910 } } ] }
)
```

To support this query, create one index on `runtime` and another index on `year`, rather than a compound index:

```javascript
db.movies.createIndex( { runtime: 1 } ),
db.movies.createIndex( { year: 1 } ),
```

### `$or` and `text` Queries

If `$or` includes a `$text` query, all clauses in the `$or` array must be supported by an index. This is because a `$text` query *must* use an index, and `$or` can only use indexes if all its clauses are supported by indexes. If the `$text` query cannot use an index, the query returns an error.

`$text` provides text query capabilities for self-managed (non-Atlas) deployments. For data hosted on MongoDB, MongoDB also offers an improved full-text query solution, MongoDB Search.

### `$or` and Geospatial Queries

`$or` supports geospatial clauses. However, if you use a near clause (`$near` or `$nearSphere`), `$or` cannot contain any other clauses. Using `$or` with a single clause has the same effect as omitting the `$or` operator.

The following query is valid because `$or` uses a non-near geospatial clause (`$geoIntersects`):

```javascript
db.theaters.find( {
   $or: [
      {
         "location.geo": {
            $geoIntersects: {
               $geometry: {
                  type: "Polygon",
                  coordinates: [
                     [ [ -74.5, 40.5 ], [ -73.5, 40.5 ],
                       [ -73.5, 41.0 ], [ -74.5, 40.5 ] ]
                  ]
               }
            }
         }
      },
      { "location.address.state": "NY" }
   ]
} )
```

```javascript
[
  {
    _id: ObjectId('59a47287cfa9a3a73e51e92f'),
    theaterId: 200,
    location: {
      address: {
        street1: '3124 Jericho Tpke',
        city: 'East Northport',
        state: 'NY',
        zipcode: '11731'
      },
      geo: {
        type: 'Point',
        coordinates: [
          -73.319092,
          40.838463
        ]
      }
    }
  },
  {
    _id: ObjectId('59a47287cfa9a3a73e51ead6'),
    theaterId: 345,
    location: {
      address: {
        street1: '148 Walt Whitman Rd',
        city: 'Huntington Station',
        state: 'NY',
        zipcode: '11746'
      },
      geo: {
        type: 'Point',
        coordinates: [
          -73.410637,
          40.825775
        ]
      }
    }
  },
  {
    _id: ObjectId('59a47287cfa9a3a73e51eae8'),
    theaterId: 374,
    location: {
      address: {
        street1: '2478 Central Park Ave',
        city: 'Yonkers',
        state: 'NY',
        zipcode: '10710'
      },
      geo: {
        type: 'Point',
        coordinates: [
          -73.826805,
          40.983246
        ]
      }
    }
  },
  {
    _id: ObjectId('59a47287cfa9a3a73e51eafd'),
    theaterId: 384,
    location: {
      address: {
        street1: '40 Catherwood Road',
        city: 'Ithaca',
        state: 'NY',
        zipcode: '14850'
      },
      geo: {
        type: 'Point',
        coordinates: [
          -76.492142,
          42.481991
        ]
      }
    }
  },
  {
    _id: ObjectId('59a47287cfa9a3a73e51eb2c'),
    theaterId: 428,
    location: {
      address: {
        street1: '1 Crossgates Mall Rd',
        city: 'Albany',
        state: 'NY',
        zipcode: '12203'
      },
      geo: {
        type: 'Point',
        coordinates: [
          -73.848686,
          42.690285
        ]
      }
    }
  }
]
```

### `$or` and Sort Operations

When executing `$or` queries with a `sort()`, MongoDB can use indexes that support the `$or` clauses.

### `$or` and Partial Indexes

You can create partial indexes with `$or`. Use the `partialFilterExpression` of the db.collection.createIndex() method to create a partial index.

### `$or` Compared to `$in`

If you use `$or` with `<expressions>` that are equality checks for the value of the same field, use `$in` instead of `$or`.

This query selects documents in the `movies` collection where `year` is `1903` or `1909`:

```javascript
db.movies.find( { year: { $in: [1903, 1909] } },
   { _id: 0, title: 1, year: 1 }
)
```

```javascript
[
  { title: 'The Great Train Robbery', year: 1903 },
  { title: 'A Corner in Wheat', year: 1909 }
]
```

### Nested `$or` Clauses

You can nest `$or` operations.

### Error Handling

`$or``true`To allow the query engine to optimize queries, `$or` handles errors as follows:

- If any expression supplied to `$or` would cause an error when evaluated alone, the `$or` containing the expression may cause an error but an error is not guaranteed.

- An expression supplied after the first expression supplied to `$or` may cause an error even if the first expression evaluates to `true`.
