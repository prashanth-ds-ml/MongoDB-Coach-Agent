# $in (query predicate operator)

`$in`
The `$in` operator selects the documents where the value of a field equals any value in the specified array.

## Compatibility

`$in`You can use `$in` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

The `$in` operator has the following form:

```javascript
{ field: { $in: [ <value1>, <value2>, ... <valueN> ] } }
```

For comparison of different BSON type values, see the [specified BSON comparison order](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bson-type-comparison-order/#std-label-bson-types-comparison-order).

If `field` has an array, the `$in` operator selects the documents whose `field` has an array that contains at least one element that matches a value in the specified array. For example, `<value1>`, `<value2>`, and so on.

`$in` compares each parameter to each document in the collection, which can cause performance issues. To improve performance, create an index on the `field` you want to query. An index allows MongoDB to create bounds for each `$in` element and search more efficiently.

This document describes the `$in` query operator. For the `$in` aggregation operator, see [$in (expression operator)](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/aggregation/in/).

## Query Data on Atlas by Using MongoDB Search

[in Operator](https://www.mongodb.com/docs/atlas/atlas-search/operators-collectors/in/#std-label-in-ref)`$in`For data stored in [MongoDB Atlas](https://www.mongodb.com/docs/atlas/), you can use the [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) [in Operator](https://www.mongodb.com/docs/atlas/atlas-search/operators-collectors/in/#std-label-in-ref) operator when running [`$search`](https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search) queries. Running `$in` after [`$search`](https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search) is less performant than running [`$search`](https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/#mongodb-pipeline-pipe.-search) with the [in Operator](https://www.mongodb.com/docs/atlas/atlas-search/operators-collectors/in/#std-label-in-ref) operator.

To learn more about the MongoDB Search version of this operator, see the [in Operator](https://www.mongodb.com/docs/atlas/atlas-search/operators-collectors/in/#std-label-in-ref) operator in the Atlas documentation.

## Examples

The examples on this page use data from the [sample_mflix sample dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](https://www.mongodb.com/docs/atlas/sample-data/load-sample-data-local/#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

### Match Values

This query selects documents in the `movies` collection where the value of the `rated` field is `"G"` or `"TV-G"`:

```javascript
db.movies.find(
   { rated: { $in: ["G", "TV-G"] } },
   { _id: 0, title: 1 }
)

```

```
[
  { title: 'The Great Train Robbery' },
  { title: 'A Corner in Wheat' },
  { title: 'From Hand to Mouth' },
  { title: 'One Week' },
  { title: 'The Devil to Pay!' },
  { title: 'Footlight Parade' },
  { title: 'Gold Diggers of 1935' },
  { title: 'Naughty Marietta' },
  { title: 'Modern Times' },
  { title: 'Gone with the Wind' },
  { title: 'Fantasia' },
  { title: 'The Man Who Came to Dinner' },
  { title: 'National Velvet' },
  { title: 'Alice in Wonderland' },
  { title: 'The Member of the Wedding' },
  { title: 'Seven Brides for Seven Brothers' },
  { title: 'Around the World in Eighty Days' },
  { title: 'The King and I' },
  { title: 'A King in New York' },
  { title: 'Ben-Hur' }
]

```

Although you can write the query using the [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) operator, use the `$in` operator rather than the [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or) operator when performing equality checks on the same field.

### Match Values in an Array

The following [`updateMany()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.updateMany/#mongodb-method-db.collection.updateMany) operation sets the `familyFriendly` field to `true` when the `rated` array has at least one element that matches either `"G"` or `"TV-G"`:

```javascript
db.movies.updateMany(
   { rated: { $in: ["G", "TV-G"] } },
   { $set: { familyFriendly: true } }
)

```

```
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 536,
  modifiedCount: 536,
  upsertedCount: 0
}

```

For additional examples on querying arrays, see:

- [Query an Array](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/query-arrays/#std-label-read-operations-arrays)

- [Query an Array of Embedded Documents](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/query-array-of-documents/#std-label-array-match-embedded-documents)

For additional examples on querying, see [Query Documents](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document).

### Use `$in` with a Regular Expression

The `$in` operator can select documents using regular expressions of the form `/pattern/`.

This query selects documents in the `movies` collection where the `plot` field either starts with `Alien` or contains `sci-fi`:

```javascript
db.movies.find(
   { plot: { $in: [ /^Alien/ , /sci-fi/ ] } },
   { _id: 0, title: 1, plot: 1 }
)

```

```
[
  {
    plot: 'Aliens come to Earth seeking scientists to help them in their war.',
    title: 'This Island Earth'
  },
  {
    plot: 'Censored by the Polish authorities, this film was reedited and new footage added. It begins with a sci-fi motif: abstract images and electronic music take the viewer from ruins of Lebanon ...',
    title: 'Rece do gèry'
  },
  {
    plot: 'An idyllic sci-fi future has one major drawback: life must end at 30.',
    title: "Logan's Run"
  },
  {
    plot: "Four horror/sci-fi segments directed by four famous directors which are their own versions of classic stories from Rod Serling's landmark television series.",
    title: 'Twilight Zone: The Movie'
  },
  {
    plot: 'Aliens who look like clowns come from outer space and terrorize a small town.',
    title: 'Killer Klowns from Outer Space'
  },
  ...
]

```

## Learn More

- [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find)

- [`updateMany()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.updateMany/#mongodb-method-db.collection.updateMany)

- [`$or`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/or/#mongodb-query-op.-or)

- [`$set`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/update/set/#mongodb-update-up.-set)

- [`$elemMatch`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch)

