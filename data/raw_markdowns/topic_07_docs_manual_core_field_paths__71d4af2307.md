> Source: https://www.mongodb.com/docs/manual/core/field-paths/
> Fetch method: direct_markdown

# Field Paths

You can use [field path](https://www.mongodb.com/docs/reference/glossary/#std-term-field-path) expressions to access fields in input documents. To specify a field path, prefix the field name or the [dotted field path](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) (if the field is in an embedded document) with a dollar sign `$`.

## Use Cases

You can use field paths for the following use cases:

- [Nested Fields](https://www.mongodb.com/docs/core/field-paths/#std-label-agg-nested-fields)

- [Array of Nested Fields](https://www.mongodb.com/docs/core/field-paths/#std-label-agg-array-of-nested-fields)

- [Array of Nested Arrays](https://www.mongodb.com/docs/core/field-paths/#std-label-agg-nested-array-of-arrays)

### Nested Fields

The examples on this page use data from the [sample_mflix sample dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](https://www.mongodb.com/docs/atlas/sample-data/load-sample-data-local/#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

The following example uses the `movies` collection from the `sample_mflix` database. Each document in this collection has the following structure:

```javascript
{
   _id: ObjectId("573a1390f29313caabcd42e8"),
   title: "The Great Train Robbery",
   year: 1903,
   imdb: { rating: 7.4, votes: 9847, id: 439 },
   ...
}
```

Documents in the `movies` collection contain additional fields not shown here.

To specify the nested field `rating` within the `imdb` field, use [dot notation](https://www.mongodb.com/docs/reference/glossary/#std-term-dot-notation) (`"field.nestedField"`) with a dollar sign `$`. The following aggregation pipeline projects only the `imdb_rating` nested field value for the matching document:

```javascript
db.movies.aggregate( [
   { $match: { title: "The Godfather" } },
   {
      $project: {
         _id: 0,
         imdb_rating: "$imdb.rating"
      }
   }
] )

```

Below is an example returned document:

```javascript
[ { imdb_rating: 9.2 } ]
```

### Array of Nested Fields

You can use [dot notation](https://www.mongodb.com/docs/reference/glossary/#std-term-dot-notation) in a field path to access a field that is nested within an array.

For example, consider a `products` collection that contains an `instock` field. The `instock` field contains an array of nested `warehouse` fields.

```javascript
db.products.insertMany( [
   { item: "journal", instock: [ { warehouse: "A"}, { warehouse: "C" } ] },
   { item: "notebook", instock: [ { warehouse: "C" } ] },
   { item: "paper", instock: [ { warehouse: "A" }, { warehouse: "B" } ] },
   { item: "planner", instock: [ { warehouse: "A" }, { warehouse: "B" } ] },
   { item: "postcard", instock: [ { warehouse: "B" }, { warehouse: "C" } ] }
] )
```

The following aggregation pipeline uses `$instock.warehouse` to access the nested `warehouse` fields.

```javascript
db.products.aggregate( [
   {
      $project: {
         _id: 0,
         item: 1,
         warehouses: "$instock.warehouse"
      }
   }
] )

```

In this example, `$instock.warehouse` outputs an array of values that are in the nested `warehouse` field for each document. The pipeline returns the following documents:

```javascript
[
   {
      _id: ObjectId('6740b55e33b29cf6b1d884f7'),
      item: "journal",
      warehouses: [ "A", "C" ]
   },
   {
      _id: ObjectId('6740b55e33b29cf6b1d884f8'),
      item: "notebook",
      warehouses: [ "C" ]
   },
   {
      _id: ObjectId('6740b55e33b29cf6b1d884f9'),
      item: "paper",
      warehouses: [ "A", "B" ]
   },
   {
      _id: ObjectId('6740b55e33b29cf6b1d884fa'),
      item: "planner",
      warehouses: [ "A", "B" ]
   },
   {
      _id: ObjectId('6740b55e33b29cf6b1d884fb'),
      item: "postcard",
      warehouses: [ "B", "C" ]
   }
]
```

### Array of Nested Arrays

You can also use [dot notation](https://www.mongodb.com/docs/reference/glossary/#std-term-dot-notation) with a dollar sign `$` in a field path to access an array within a nested array.

This example uses a `fruits` collection that contains the following document:

```javascript
db.fruits.insertOne(
   {
      _id: ObjectId("5ba53172ce6fa2fcfc58e0ac"),
      inventory: [
         {
            apples: [
               "macintosh",
               "golden delicious",
            ]
         },
         {
            oranges: [
               "mandarin",
            ]
         },
         {
            apples: [
               "braeburn",
               "honeycrisp",
            ]
         }
      ]
   }
)
```

The document in the collection contains an `inventory` array where each element in the array is an object that contains a nested array field.

Consider the following aggregation pipeline:

```javascript
db.fruits.aggregate( [
   {
      $project: {
         all_apples: "$inventory.apples"
      }
   }
] )

```

In this pipeline, `$inventory.apples` resolves to an array of nested arrays. The pipeline returns the following document:

```javascript
{
   _id: ObjectId('5ba53172ce6fa2fcfc58e0ac'),
   all_apples: [
      [ "macintosh", "golden delicious" ],
      [ "braeburn", "honeycrisp" ]
   ]
}
```

## Learn More

For more information on accessing and interacting with nested elements, see [Dot Notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) and [Query an Array of Embedded Documents](https://www.mongodb.com/docs/tutorial/query-array-of-documents/#std-label-array-match-embedded-documents).
