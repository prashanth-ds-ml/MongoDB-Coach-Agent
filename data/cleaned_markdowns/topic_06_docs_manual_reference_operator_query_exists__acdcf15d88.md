> Source: https://www.mongodb.com/docs/manual/reference/operator/query/exists/
> Fetch method: direct_markdown

# $exists (query predicate operator)

## Definition

`$exists`
The `$exists` operator matches documents that contain or do not contain a specified field, including documents where the field value is `null`.

MongoDB `$exists` does **not** correspond to SQL operator `exists`. For SQL `exists`, see `$in`.

For MongoDB Search `exists`, see exists (MongoDB Search Operator) in the Atlas documentation.

## Syntax

To specify an `$exists` expression, use the following prototype:

```javascript
{ field: { $exists: <boolean> } }
```

When `<boolean>` is true, `$exists` matches the documents that contain the field, including documents where the field value is `null`. If `<boolean>` is false, the query returns only the documents that do not contain the field.

## Query Data on Atlas by Using MongoDB Search

exists (MongoDB Search Operator)`$exists`For data stored in MongoDB Atlas, you can use the MongoDB Search exists (MongoDB Search Operator) operator when running `$search` queries. Running `$exists` after `$search` is less performant than running `$search` with the exists (MongoDB Search Operator) operator.

To learn more about the MongoDB Search version of this operator, see the exists (MongoDB Search Operator) operator in the Atlas documentation.

## Examples

The examples on this page use data from the sample_mflix sample dataset. For details on how to load this dataset into your self-managed MongoDB deployment, see Load the sample dataset. If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

### Exists and Not Equal To

Consider the following example:

```javascript
db.movies.find( { rated: { $exists: true, $nin: [ "R", "PG-13" ] } } ).limit(5)

```

This query selects 5 documents in the `movies` collection where the `rated` field exists *and* its value does not equal `"R"` or `"PG-13"`.

### Null Values

The `movies` collection in the `sample_mflix` database contains documents where some fields are present and others are missing. For example, the `rated` field exists in 11,455 documents and is absent from the remaining 9,894 documents.

#### `$exists: true`

The following query specifies the query predicate `rated: { $exists: true }`:

```javascript
db.movies.find( { rated: { $exists: true } }, { _id: 0, title: 1, rated: 1 } ).limit( 3 )

```

The results consist of three documents that contain the field `rated`:

```javascript
[
  { title: 'The Great Train Robbery', rated: 'TV-G' },
  { title: 'A Corner in Wheat', rated: 'G' },
  { title: 'Traffic in Souls', rated: 'TV-PG' }
]
```

#### `$exists: false`

The following query specifies the query predicate `rated: { $exists: false }`:

```javascript
db.movies.find( { rated: { $exists: false } }, { _id: 0, title: 1, year: 1 } ).limit( 3 )

```

The results consist of three documents that do not contain the field `rated`:

```javascript
[
  {
    title: 'Winsor McCay, the Famous Cartoonist of the N.Y. Herald and His Moving Comics',
    year: 1911
  },
  { title: 'Gertie the Dinosaur', year: 1914 },
  { title: 'In the Land of the Head Hunters', year: 1914 }
]
```

### Use a Sparse Index to Improve `$exists` Performance

The following table compares `$exists` query performance using sparse and non-sparse indexes:

| `$exists` Query | Using a Sparse Index | Using a Non-Sparse Index |
| --- | --- | --- |
| `{ $exists: true }` | Most efficient. MongoDB can make an exact match and does not require a `FETCH`. | More efficient than queries without an index, but still requires a `FETCH`. |
| `{ $exists: false }` | Cannot use the index and requires a `COLLSCAN`. | Requires a `FETCH`. |
Queries that use `{ $exists: true }` on fields that use a non-sparse index or that use `{ $exists: true }` on fields that are not indexed examine all documents in a collection. To improve performance, create a sparse index on the `field` as shown in the following scenario:

1. The `movies` collection contains documents where the `metacritic` field is present in some documents and absent from others. Of the 21,349 documents, 6,964 have the `metacritic` field and 14,385 do not.

2. Create a sparse index on the `metacritic` field:

   ```javascript
   db.movies.createIndex(
      { metacritic: 1 },
      { name: "metacriticSparseIndex", sparse: true }
   )

   ```

3. The following example counts the documents where the `metacritic` field has a value (including null) and uses the sparse index:

   ```javascript
   db.movies.countDocuments( { metacritic: { $exists: true } } )

   ```

   The example returns 6964. The operation does not count the documents that are missing the `metacritic` field.

If you only need documents where the `field` has a non-null value, you:

- Can use `$ne: null` instead of `$exists: true`.

- Do not need a sparse index on the `field`.

For example, using the `movies` collection:

```javascript
db.movies.countDocuments( { metacritic: { $ne: null } } )

```

The example returns 6964. Documents that are missing the `metacritic` value or have a null `metacritic` value are not counted.
