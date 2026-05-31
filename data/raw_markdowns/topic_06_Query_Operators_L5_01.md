# Logical Query Predicate Operators

Logical operators return data based on boolean logic (and, or, and nor).

<table>
<tr>
<th id="Name">
Name

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Name">
[`$and`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/and/#mongodb-query-op.-and)

</td>
<td headers="Description">
Joins query clauses with a logical `AND` and returns documents that match the conditions of all clauses.

</td>
</tr>
<tr>
<td headers="Name">
[`$nor`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nor/#mongodb-query-op.-nor)

</td>
<td headers="Description">
Joins query clauses with a logical `NOR` and returns all documents that fail to match all clauses.

</td>
</tr>
<tr>
<td headers="Name">
[`$not`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/not/#mongodb-query-op.-not)

</td>
<td headers="Description">
Inverts the effect of a query predicate and returns documents that do *not* match the query predicate.

</td>
</tr>
<tr>
<td headers="Name">
[`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or)

</td>
<td headers="Description">
Joins query clauses with a logical `OR` and returns all documents that match at least one clause.

</td>
</tr>
</table>

# $and (query predicate operator)

`$and`
[`$and`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/and/#mongodb-query-op.-and) performs a logical `AND` operation on an array of one or more expressions and selects the documents that satisfy all the expressions.

MongoDB provides an implicit `AND` operation when you specify a comma separated list of expressions.

## Compatibility

`$and`You can use `$and` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

The [`$and`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/and/#mongodb-query-op.-and) has the following syntax:

```javascript
{ $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
```

## Behavior

`$and``false`When evaluating the clauses in the [`$and`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/and/#mongodb-query-op.-and) expression, MongoDB's query optimizer considers which indexes are available that could help satisfy clauses of the [`$and`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/and/#mongodb-query-op.-and) expression when [selecting the best plan to execute](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/query-plans/#std-label-read-operations-query-optimization).

To allow the query engine to optimize queries, `$and` handles errors as follows:

- If any expression supplied to `$and` would cause an error when evaluated alone, the `$and` containing the expression may cause an error but an error is not guaranteed.

- An expression supplied after the first expression supplied to `$and` may cause an error even if the first expression evaluates to `false`.

Most programming languages and drivers, including the [MongoDB Shell](https://www.mongodb.com/docs/mongodb-shell/#std-label-mdb-shell-overview) (`mongosh`), do not allow the construction of objects with duplicate keys at the same object level. For example:

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

The previous query explicitly checks that both conditions are satisfied: the `price` array must include at least one value from each [`$in`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/in/#mongodb-query-op.-in) set. For more information, see [Examples](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/and/#std-label-query-and-examples).

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

The previous query is invalid because it uses [`$ne`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/ne/#mongodb-query-op.-ne) more than once on the `status` field at the same object level. Use [`$nin`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nin/#mongodb-query-op.-nin) instead:

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

To find documents where `status` is either `new` or `processing`, use [`$in`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/in/#mongodb-query-op.-in):

```javascript
db.inventory.find( { status: { $in: [ "new", "processing" ] } } )
```

If your `status` field is an array `[ "new", "processing" ]` and you want to check if the document contains both `new` and `processing`, use [`$all`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/all/#mongodb-query-op.-all):

```javascript
db.inventory.find( { status: { $all: [ "new", "processing" ] } } )
```

The previous query is semantically equivalent to `AND`, but [`$all`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/all/#mongodb-query-op.-all) is clearer when querying array fields.

Similar to duplicate field names, the same considerations apply for duplicate operators used in the query.

## Learn More

- [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find)

- [`$ne`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/ne/#mongodb-query-op.-ne)

- [`$exists`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/exists/#mongodb-query-op.-exists)

- [`$in`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/in/#mongodb-query-op.-in)

- [`$all`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/all/#mongodb-query-op.-all)

# $nor (query predicate operator)

## Definition

`$nor`
[`$nor`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nor/#mongodb-query-op.-nor) performs a logical `NOR` operation on an array of one or more query predicates and selects the documents that **fail** all the query predicates in the array. The [`$nor`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nor/#mongodb-query-op.-nor) has the following syntax:

```javascript
{ $nor: [ { <expression1> }, { <expression2> }, ...  { <expressionN> } ] }
```

## Examples

### `$nor` Query with Two Expressions

Consider the following query which uses only the [`$nor`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nor/#mongodb-query-op.-nor) operator:

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

The exception in returning documents that do not contain the field in the [`$nor`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nor/#mongodb-query-op.-nor) expression is when the [`$nor`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nor/#mongodb-query-op.-nor) operator is used with the [`$exists`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/exists/#mongodb-query-op.-exists) operator.

### `$nor` and `$exists`

Compare that with the following query which uses the [`$nor`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nor/#mongodb-query-op.-nor) operator with the [`$exists`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/exists/#mongodb-query-op.-exists) operator:

```javascript
db.inventory.find( { $nor: [ { price: 1.99 }, { price: { $exists: false } },
                             { sale: true }, { sale: { $exists: false } } ] } )
```

This query will return all documents that:

- contain the `price` field whose value is *not* equal to `1.99` and contain the `sale` field whose value *is not* equal to `true`

- [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find)

- [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or)

- [`$set`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/update/set/#mongodb-update-up.-set)

- [`$exists`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/exists/#mongodb-query-op.-exists)

# $not (query predicate operator)

## Definition

`$not`
[`$not`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/not/#mongodb-query-op.-not) performs a logical `NOT` operation on the specified `<operator-expression>` and selects the documents that do *not* match the `<operator-expression>`. This includes documents that do not contain the `field`.

## Compatibility

`$not`You can use `$not` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

The [`$not`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/not/#mongodb-query-op.-not) operator has the following form:

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

`{ $not: { $gt: 180 } }` differs from the [`$lte`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/lte/#mongodb-query-op.-lte) operator. `{ $lte: 180 }` returns *only* the documents where the `runtime` field exists and its value is less than or equal to `180`.

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

The `$not` operator can yield unexpected results when used with an array. To match documents based on multiple false conditions, use [`$nor`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nor/#mongodb-query-op.-nor).

### Regular Expressions

The examples on this page use data from the [sample_mflix sample dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](https://www.mongodb.com/docs/atlas/sample-data/load-sample-data-local/#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

[`$not`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/not/#mongodb-query-op.-not) supports logical `NOT` operations on:

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

- [`$regex`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/regex/#mongodb-query-op.-regex) operator expressions.

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

  For example, the following [PyMongo](https://pymongo.readthedocs.io/en/stable/index.html) query uses Python's `re.compile()` method to compile a regular expression:

  ```python
  import re
  for noMatch in db.inventory.find( { "item": { "$not": re.compile("^p.*") } } ):
      print noMatch
  ```

## Learn More

- [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find)

- [`$set`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/update/set/#mongodb-update-up.-set)

- [`$gt`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/gt/#mongodb-query-op.-gt)

- [`$regex`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/regex/#mongodb-query-op.-regex)

- [`$eq`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/eq/#mongodb-query-op.-eq)

# $or (query predicate operator)

`$or`
[`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) performs a logical `OR` operation on an array of one or more expressions and selects documents that satisfy at least one of the expressions.

## Compatibility

`$or`You can use `$or` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

The [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) operator has the following syntax:

```javascript
{ $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
```

The examples on this page use data from the [sample_mflix sample dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](https://www.mongodb.com/docs/atlas/sample-data/load-sample-data-local/#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

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

When evaluating the clauses in the [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) expression, MongoDB performs a collection scan or an index scan. If all clauses are supported by indexes, MongoDB performs index scans. To use indexes to evaluate an [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) expression, all the clauses in the [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) expression must be supported by indexes. Otherwise, MongoDB performs a collection scan.

When using indexes with [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) queries, each clause of an [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) can use its own index. Consider this query:

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

If [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) includes a [`$text`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/text/#mongodb-query-op.-text) query, all clauses in the [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) array must be supported by an index. This is because a `$text` query *must* use an index, and [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) can only use indexes if all its clauses are supported by indexes. If the `$text` query cannot use an index, the query returns an error.

`$text` provides text query capabilities for self-managed (non-Atlas) deployments. For data hosted on MongoDB, MongoDB also offers an improved full-text query solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/).

### `$or` and Geospatial Queries

`$or` supports [geospatial clauses](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/geospatial/#std-label-geospatial-query-operators). However, if you use a near clause ([`$near`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/near/#mongodb-query-op.-near) or [`$nearSphere`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/nearSphere/#mongodb-query-op.-nearSphere)), `$or` cannot contain any other clauses. Using `$or` with a single clause has the same effect as omitting the `$or` operator.

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

When executing [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) queries with a [`sort()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort), MongoDB can use indexes that support the [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) clauses.

### `$or` and Partial Indexes

You can create [partial indexes](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/index-partial/#std-label-index-type-partial) with [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or). Use the `partialFilterExpression` of the [db.collection.createIndex()](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.createIndex/#std-label-method-createIndex) method to create a partial index.

### `$or` Compared to `$in`

If you use [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) with `<expressions>` that are equality checks for the value of the same field, use [`$in`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/in/#mongodb-query-op.-in) instead of [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or).

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

You can nest [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) operations.

- [`$and`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/and/#mongodb-query-op.-and)

- [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find)

- [`sort()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort)

- [`$in`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/in/#mongodb-query-op.-in)

### Error Handling

`$or``true`To allow the query engine to optimize queries, `$or` handles errors as follows:

- If any expression supplied to `$or` would cause an error when evaluated alone, the `$or` containing the expression may cause an error but an error is not guaranteed.

- An expression supplied after the first expression supplied to `$or` may cause an error even if the first expression evaluates to `true`.

