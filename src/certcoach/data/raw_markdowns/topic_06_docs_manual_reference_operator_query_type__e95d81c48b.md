> Source: https://www.mongodb.com/docs/manual/reference/operator/query/type/
> Fetch method: direct_markdown

# $type (query predicate operator)

## Definition

`$type`
[`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) selects documents where the *value* of the `field` is an instance of the specified [BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) type(s). Querying by data type is useful for unstructured data where data types aren't predictable.

## Compatibility

`$type`You can use `$type` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

A [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) expression for a single [BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) type has the following syntax:

```javascript
{ field: { $type: <BSON type> } }
```

You can specify either the number or alias for the [BSON type](https://www.mongodb.com/docs/reference/operator/query/type/#std-label-document-type-available-types).

The [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) expression can also accept an array of [BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) types and has the following syntax:

```javascript
{ field: { $type: [ <BSON type1> , <BSON type2>, ... ] } }
```

The above query matches documents where the `field` value is any of the listed types. The types specified in the array can be either numeric or string aliases.

For an example, see [Querying by Multiple Data Types](https://www.mongodb.com/docs/reference/operator/query/type/#std-label-document-querying-by-multiple-data-types).

[Available Types](https://www.mongodb.com/docs/reference/operator/query/type/#std-label-document-type-available-types) describes the BSON types and their corresponding numeric and string aliases.

- [`$isNumber`](https://www.mongodb.com/docs/reference/operator/aggregation/isNumber/#mongodb-expression-exp.-isNumber) - checks if the argument is a number.

- [`$type (Aggregation)`](https://www.mongodb.com/docs/reference/operator/aggregation/type/#mongodb-expression-exp.-type) - returns the BSON type of the argument.

## Behavior

[`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) returns documents where the BSON type of the `field` matches the BSON type passed to [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type).

### Arrays

For documents where `field` is an array, [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) returns documents in which at least one array element matches a type passed to [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type).

Queries for `$type: "array"` return documents where the field itself is an array.

### Available Types

The [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) operator accepts string aliases for the BSON types in addition to the numbers corresponding to the BSON types.

[`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) supports the `number` alias, which matches against the following [BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) types:

- [`double`](https://www.mongodb.com/docs/reference/mongodb-extended-json/#mongodb-bsontype-Double)

- [`32-bit integer`](https://www.mongodb.com/docs/reference/mongodb-extended-json/#mongodb-bsontype-Int32)

- [`64-bit integer`](https://www.mongodb.com/docs/reference/mongodb-extended-json/#mongodb-bsontype-Int64)

- [`decimal`](https://www.mongodb.com/docs/reference/mongodb-extended-json/#mongodb-bsontype-Decimal128)

For examples, see [Examples](https://www.mongodb.com/docs/reference/operator/query/type/#std-label-query-type-examples).

[`$isNumber`](https://www.mongodb.com/docs/reference/operator/aggregation/isNumber/#mongodb-expression-exp.-isNumber)

### MinKey and MaxKey

[`MinKey`](https://www.mongodb.com/docs/reference/mongodb-extended-json/#mongodb-bsontype-MinKey) and [`MaxKey`](https://www.mongodb.com/docs/reference/mongodb-extended-json/#mongodb-bsontype-MaxKey) are used in comparison operations and exist primarily for internal use. For all possible [BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) element values, `MinKey` is always the smallest value, and `MaxKey` is always the greatest value.

Querying for `minKey` or `maxKey` with [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) only returns fields that match the special `MinKey` or `MaxKey` values.

For example, the following `data` collection has these documents with `MinKey` and `MaxKey`:

```javascript
db.data.insertMany( [
   { _id: 1, x: MinKey() },
   { _id: 2, y: MaxKey() }
] )

```

The following query returns the document with `_id: 1`:

```javascript
db.data.find( { x: { $type: "minKey" } } )

```

```javascript
[
  {
    _id: 1,
    x: MinKey()
  }
]

```

The following query returns the document with `_id: 2`:

```javascript
db.data.find( { y: { $type: "maxKey" } } )

```

```javascript
[
  {
    _id: 2,
    y: MaxKey()
  }
]

```

## Examples

### Querying by Data Type

The examples on this page use data from the [sample_mflix sample dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](https://www.mongodb.com/docs/atlas/sample-data/load-sample-data-local/#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

The `movies` collection stores IMDb ratings in the `imdb.rating` field. Most documents store `imdb.rating` as a `double`, but some documents store it as an empty `string` (`""`).

The following queries return documents from 2013 where `imdb.rating` is the [BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) type `string`.

This query specifies the type with the number of the [BSON type](https://www.mongodb.com/docs/reference/operator/query/type/#std-label-document-type-available-types).

```javascript
db.movies.find(
   { "imdb.rating": { $type: 2 }, year: 2013 },
   { _id: 0, title: 1, year: 1, "imdb.rating": 1 }
)

```

```javascript
[
  { title: 'Coming to Terms', year: 2013, imdb: { rating: '' } },
  { title: 'Absent Minded', year: 2013, imdb: { rating: '' } }
]

```

This query specifies the type with the alias of the BSON type:

```javascript
db.movies.find(
   { "imdb.rating": { $type: "string" }, year: 2013 },
   { _id: 0, title: 1, year: 1, "imdb.rating": 1 }
)

```

```javascript
[
  { title: 'Coming to Terms', year: 2013, imdb: { rating: '' } },
  { title: 'Absent Minded', year: 2013, imdb: { rating: '' } }
]

```

The following query uses the `number` alias to return documents where `imdb.rating` is the [BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) type `double`, `int`, or `long`:

```javascript
db.movies.find(
   { "imdb.rating": { $type: "number" }, runtime: { $gt: 1000 } },
   { _id: 0, title: 1, runtime: 1, "imdb.rating": 1 }
)

```

```javascript
[
  { runtime: 1256, title: 'Centennial', imdb: { rating: 8.5 } },
  { runtime: 1140, title: 'Baseball', imdb: { rating: 9.1 } }
]

```

### Querying by Multiple Data Types

The following queries return documents where `imdb.rating` is the [BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) type `string` or `double`. The first query uses numeric aliases and the second query uses string aliases.

```javascript
db.movies.find(
   { "imdb.rating": { $type: [ 2, 1 ] },
     runtime: { $gt: 1000 } },
   { _id: 0, title: 1, runtime: 1, "imdb.rating": 1 }
)

```

```javascript
[
  { runtime: 1256, title: 'Centennial', imdb: { rating: 8.5 } },
  { runtime: 1140, title: 'Baseball', imdb: { rating: 9.1 } }
]

```

```javascript
db.movies.find(
   { "imdb.rating": { $type: [ "string", "double" ] },
     runtime: { $gt: 1000 } },
   { _id: 0, title: 1, runtime: 1, "imdb.rating": 1 }
)

```

```javascript
[
  { runtime: 1256, title: 'Centennial', imdb: { rating: 8.5 } },
  { runtime: 1140, title: 'Baseball', imdb: { rating: 9.1 } }
]

```

### Querying by Array Type

The `movies` collection stores film genres in the `genres` field as an array. The following query returns documents where the `genres` field is an array:

```javascript
db.movies.find(
   { genres: { $type: "array" }, runtime: { $gt: 1000 } },
   { _id: 0, title: 1, genres: 1 }
)

```

```javascript
[
  {
    title: 'Centennial',
    genres: [ 'Action', 'Adventure', 'Drama' ]
  },
  {
    title: 'Baseball',
    genres: [ 'Documentary', 'History', 'Sport' ]
  }
]

```

### Querying by MinKey and MaxKey

The folllowing examples use the `restaurants` collection that uses `minKey` for any grade that is a failing grade:

```javascript
db.restaurants.insertOne( {
   _id: 1,
   address: {
      building: "230",
      coord: [ -73.996089, 40.675018 ],
      street: "Huntington St",
      zipcode: "11231"
   },
   borough: "Brooklyn",
   cuisine: "Bakery",
   grades: [
      { date : new Date(1393804800000), grade : "C", score : 15 },
      { date : new Date(1378857600000), grade : "C", score : 16 },
      { date : new Date(1358985600000), grade : MinKey(), score : 30 },
      { date : new Date(1322006400000), grade : "C", score : 15 }
   ],
   name : "Dan's Donuts",
   restaurant_id : "30075445"
} )

```

And `maxKey` for any grade that is the highest passing grade:

```javascript
db.restaurants.insertOne( {
   _id : 2,
   address : {
      building : "1166",
      coord : [ -73.955184, 40.738589 ],
      street : "Manhattan Ave",
      zipcode : "11222"
   },
   borough: "Brooklyn",
   cuisine: "Bakery",
   grades: [
      { date : new Date(1393804800000), grade : MaxKey(), score : 2 },
      { date : new Date(1378857600000), grade : "B", score : 6 },
      { date : new Date(1358985600000), grade : MaxKey(), score : 3 },
      { date : new Date(1322006400000), grade : "B", score : 5 }
   ],
   name : "Dainty Daisey's Donuts",
   restaurant_id : "30075449"
} )

```

The following query returns any restaurant whose `grades.grade` field contains `minKey` *or* is an array containing an element of the specified type:

```javascript
db.restaurants.find(
   { "grades.grade" : { $type : "minKey" } }
)

```

```javascript
[
  {
    _id: 1,
    address: {
      building: '230',
      coord: [
        -73.996089,
        40.675018
      ],
      street: 'Huntington St',
      zipcode: '11231'
    },
    borough: 'Brooklyn',
    cuisine: 'Bakery',
    grades: [
      {
        date: ISODate('2014-03-03T00:00:00.000Z'),
        grade: 'C',
        score: 15
      },
      {
        date: ISODate('2013-09-11T00:00:00.000Z'),
        grade: 'C',
        score: 16
      },
      {
        date: ISODate('2013-01-24T00:00:00.000Z'),
        grade: MinKey(),
        score: 30
      },
      {
        date: ISODate('2011-11-23T00:00:00.000Z'),
        grade: 'C',
        score: 15
      }
    ],
    name: ...,
    restaurant_id: '30075445'
  }
]

```

The following query returns any restaurant whose `grades.grade` field contains `maxKey` *or* is an array containing an element of the specified type:

```javascript
db.restaurants.find(
   { "grades.grade" : { $type : "maxKey" } }
)

```

```javascript
[
  {
    _id: 2,
    address: {
      building: '1166',
      coord: [
        -73.955184,
        40.738589
      ],
      street: 'Manhattan Ave',
      zipcode: '11222'
    },
    borough: 'Brooklyn',
    cuisine: 'Bakery',
    grades: [
      {
        date: ISODate('2014-03-03T00:00:00.000Z'),
        grade: MaxKey(),
        score: 2
      },
      {
        date: ISODate('2013-09-11T00:00:00.000Z'),
        grade: 'B',
        score: 6
      },
      {
        date: ISODate('2013-01-24T00:00:00.000Z'),
        grade: MaxKey(),
        score: 3
      },
      {
        date: ISODate('2011-11-23T00:00:00.000Z'),
        grade: 'B',
        score: 5
      }
    ],
    name: ...,
    restaurant_id: '30075449'
  }
]

```

## Learn More

- [Query for Null or Missing Fields](https://www.mongodb.com/docs/tutorial/query-for-null-fields/#std-label-faq-developers-query-for-nulls)

- [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find)

- [BSON Types](https://www.mongodb.com/docs/reference/bson-types/#std-label-bson-types)
