> Source: https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/
> Fetch method: direct_markdown

# $lookup (aggregation stage)

## Definition

`$lookup`
Performs a left outer join to a collection in the *same* database to filter in documents from the foreign collection for processing. The `$lookup` stage adds a new array field to each input document. The new array field contains the matching documents from the foreign collection. The `$lookup` stage passes these reshaped documents to the next stage.

Starting in MongoDB 5.1, you can use `$lookup` with sharded collections.

To combine elements from two different collections, use the `$unionWith` pipeline stage.

Excessive use of `$lookup` may slow down query performance. To reduce reliance on `$lookup`, consider an embedded data model to store related data in a single collection.

For details on `$lookup` performance, see Performance Considerations.

## Syntax

The `$lookup` stage syntax:

```none
{
   $lookup:
     {
       from: <collection to join>,
       localField: <field from the input documents>,
       foreignField: <field from the documents of the "from" collection>,
       let: { <var_1>: <expression>, …, <var_n>: <expression> },
       pipeline: [ <pipeline to run> ],
       as: <output array field>
     }
}
```

The `$lookup` accepts a document with these fields:

| Field | Necessity | Description |
| --- | --- | --- |
| from | Required | Specifies the foreign collection in the *same* database to join to the local collection. It is possible in some edge cases to subsitute `from` with `pipeline` with `$documents` as the first stage. For an example, see Use a $documents Stage in a $lookup Stage. Starting in MongoDB 5.1, the `from` collection can be sharded. |
| localField | Optional if `pipeline` is specified | Specifies the field from the documents input to the `$lookup` stage. `$lookup` performs an equality match on the `localField` to the `foreignField` from the documents of the `from` collection. If an input document does not contain the `localField`, the `$lookup` treats the field as having a value of `null` for matching purposes. |
| foreignField | Optional if `pipeline` is specified | Specifies the foreign documents' `foreignField` to perform an equality match with the local documents' `localField`. If a foreign document does not contain a `foreignField` value, the `$lookup` uses a `null` value for the match. |
| let | Optional | Specifies variables to use in the pipeline stages. Use the variable expressions to access the fields from the local collection's documents that are input to the `pipeline`. To reference variables in pipeline stages, use the `"$$<variable>"` syntax. The let variables can be accessed by the stages in the pipeline, including additional `$lookup` stages nested in the `pipeline`. - A `$match` stage requires the use of an `$expr` operator to access the variables. The `$expr` operator allows the use of aggregation expressions inside of the `$match` syntax. The `$eq`, `$lt`, `$lte`, `$gt`, and `$gte` comparison operators placed in an `$expr` operator can use an index on the `from` collection referenced in a `$lookup` stage. Limitations: - Indexes can only be used for comparisons between fields and constants, so the `let` operand must resolve to a constant. For example, a comparison between `$a` and a constant value can use an index, but a comparison between `$a` and `$b` cannot. - Indexes are not used for comparisons where the `let` operand resolves to an empty or missing value. - Multikey, partial, or sparse indexes are not used. - Other (non-`$match`) stages in the pipeline do not require an `$expr` operator to access the variables. |
| pipeline | Optional if `localField` and `foreignField` are specified | Specifies the `pipeline` to run on the foreign collection. The `pipeline` returns documents from the foreign collection. To return all documents, specify an empty `pipeline: []`. The `pipeline` cannot include the `$out` or `$merge` stages. Starting in v6.0, the `pipeline` can contain the MongoDB Search `$search` stage as the first stage inside the pipeline. To learn more, see MongoDB Search Support. The `pipeline` cannot access fields from input documents. Instead, define variables for the document fields using the let option and then reference the variables in the `pipeline` stages. To reference variables in pipeline stages, use the `"$$<variable>"` syntax. The let variables can be accessed by the stages in the pipeline, including additional `$lookup` stages nested in the `pipeline`. - A `$match` stage requires the use of an `$expr` operator to access the variables. The `$expr` operator allows the use of aggregation expressions inside of the `$match` syntax. The `$eq`, `$lt`, `$lte`, `$gt`, and `$gte` comparison operators placed in an `$expr` operator can use an index on the `from` collection referenced in a `$lookup` stage. Limitations: - Indexes can only be used for comparisons between fields and constants, so the `let` operand must resolve to a constant. For example, a comparison between `$a` and a constant value can use an index, but a comparison between `$a` and `$b` cannot. - Indexes are not used for comparisons where the `let` operand resolves to an empty or missing value. - Multikey, partial, or sparse indexes are not used. - Other (non-`$match`) stages in the pipeline do not require an `$expr` operator to access the variables. |
| as | Required | Specifies the name of the new array field to add to the input documents. The new array field contains the matching documents from the `from` collection. If the specified name already exists in the input document, the existing field is *overwritten*. |

### Equality Match with a Single Join Condition

To perform an equality match between a field from the input documents with a field from the documents of the foreign collection, the `$lookup` stage has this syntax:

```none
{
   $lookup:
     {
       from: <collection to join>,
       localField: <field from the input documents>,
       foreignField: <field from the documents of the "from" collection>,
       pipeline: [ <pipeline to run> ],
       as: <output array field>
     }
}
```

In this example, `pipeline` is optional and runs after the local and foreign equality stage.

The operation corresponds to this pseudo-SQL statement:

```sql
SELECT *, (
   SELECT ARRAY_AGG(*)
   FROM <collection to join>
   WHERE <foreignField> = <collection.localField>
) AS <output array field>
FROM collection;
```

The SQL statements on this page are included for comparison to the MongoDB aggregation pipeline syntax. The SQL statements aren't runnable.

For MongoDB examples, see these pages:

- Perform a Single Equality Join with `$lookup`

- Use `$lookup` with an Array

- Use `$lookup` with `$mergeObjects`

### Join Conditions and Subqueries on a Foreign Collection

MongoDB supports:

- Executing a pipeline on a foreign collection.

- Multiple join conditions.

- Correlated and uncorrelated subqueries.

In MongoDB, an uncorrelated subquery means that every input document will return the same result. A correlated subquery is a pipeline in a `$lookup` stage that uses the local or `input` collection's fields to return results correlated to each incoming document.

Starting in MongoDB 5.0, for an uncorrelated subquery in a `$lookup` pipeline stage containing a `$sample` stage, the `$sampleRate` operator, or the `$rand` operator, the subquery is always run again if repeated. Previously, depending on the subquery output size, either the subquery output was cached or the subquery was run again.

MongoDB correlated subqueries are comparable to SQL correlated subqueries, where the inner query references outer query values. An SQL uncorrelated subquery does not reference outer query values.

MongoDB 5.0 also supports concise correlated subqueries.

To perform correlated and uncorrelated subqueries with two collections, and perform other join conditions besides a single equality match, use this `$lookup` syntax:

```javascript
{
   $lookup:
      {
         from: <foreign collection>,
         let: { <var_1>: <expression>, …, <var_n>: <expression> },
         pipeline: [ <pipeline to run on foreign collection> ],
         as: <output array field>
      }
}
```

The operation corresponds to this pseudo-SQL statement:

```sql
SELECT *, <output array field>
FROM collection
WHERE <output array field> IN (
   SELECT <documents as determined from the pipeline>
   FROM <collection to join>
   WHERE <pipeline>
);
```

See the following examples:

- Use Multiple Join Conditions and a Correlated Subquery

- Perform an Uncorrelated Subquery with `$lookup`

### Correlated Subqueries Using Concise Syntax

Starting in MongoDB 5.0, you can use a concise syntax for a correlated subquery. Correlated subqueries reference document fields from a foreign collection  *and* the "local" collection on which the `aggregate()` method was run.

The following new concise syntax removes the requirement for an equality match on the foreign and local fields inside of an `$expr` operator:

```javascript
{
   $lookup:
      {
         from: <foreign collection>,
         localField: <field from local collection's documents>,
         foreignField: <field from foreign collection's documents>,
         let: { <var_1>: <expression>, …, <var_n>: <expression> },
         pipeline: [ <pipeline to run> ],
         as: <output array field>
      }
}
```

The operation corresponds to this pseudo-SQL statement:

```sql
SELECT *, <output array field>
FROM localCollection
WHERE <output array field> IN (
   SELECT <documents as determined from the pipeline>
   FROM <foreignCollection>
   WHERE <foreignCollection.foreignField> = <localCollection.localField>
   AND <pipeline match condition>
);
```

See this example:

- Perform a Concise Correlated Subquery with `$lookup`

## Behavior

### Encrypted Collections

Starting in MongoDB 8.1, you can reference multiple encrypted collections in a `$lookup` stage. However, `$lookup` does not support:

- Using an encrypted field as the join field in the `localField` or `foreignField`.

  For drivers using Client-Side Field Level Encryption, you can use an encrypted field as a join field only if you are performing a self-join operation.

- Using any field in an encrypted array. An array is considered as encrypted if it contains any encrypted elements.

  - For example, you can't use any field within the resulting as array of the `$lookup` operation, unless you're using Client-Side Field Level Encryption and `$unwind` the `as` field.

### Views and Collation

If performing an aggregation that involves multiple views, such as with `$lookup` or `$graphLookup`, the views must have the same collation.

### Restrictions

You cannot include the `$out` or the `$merge` stage in the `$lookup` stage. That is, when specifying a pipeline for the foreign collection, you cannot include either stage in the `pipeline` field.

```javascript
{
   $lookup:
   {
      from: <collection to join>,
      let: { <var_1>: <expression>, …, <var_n>: <expression> },
      pipeline: [ <pipeline to execute on the foreign collection> ],  // Cannot include $out or $merge
      as: <output array field>
   }
}
```

### MongoDB Search Support

Starting in MongoDB 6.0, you can specify the MongoDB Search `$search` or `$searchMeta` stage in the `$lookup` pipeline to search collections on the Atlas cluster. The `$search` or the `$searchMeta` stage must be the first stage inside the `$lookup` pipeline.

For example, when you Join Conditions and Subqueries on a Foreign Collection or run Correlated Subqueries Using Concise Syntax, you can specify `$search` or `$searchMeta` inside the pipeline as shown below:

<Tabs>

<Tab name="$search">

```
[{
  "$lookup": {
    "from": <foreign collection>,
    localField: <field from the input documents>,
    foreignField: <field from the documents of the "from" collection>,
    "as": <output array field>,
    "pipeline": [{
      "$search": {
        "<operator>": {
          <operator-specification>
        }
      },
      ...
    }]
  }
}]
```

</Tab>

<Tab name="$searchMeta">

```
[{
  "$lookup": {
    "from": <foreign collection>,
    localField: <field from the input documents>,
    foreignField: <field from the documents of the "from" collection>,
    "as": <output array field>,
    "pipeline": [{
      "$searchMeta": {
        "<collector>": {
          <collector-specification>
        }
      },
      ...
    }]
  }
}]
```

</Tab>

</Tabs>

To see an example of `$lookup` with `$search`, see the MongoDB Search tutorial Run a MongoDB Search $search Query Using $lookup.

### Sharded Collections

Starting in MongoDB 5.1, you can specify sharded collections in the `from` parameter of `$lookup` stages.

Starting in MongoDB 8.0, you can use the `$lookup` stage within a transaction while targeting a sharded collection.

### Slot-Based Query Execution Engine

Starting in version 6.0, MongoDB can use the slot-based execution query engine to execute `$lookup` stages if *all* preceding stages in the pipeline can also be executed by the slot-based execution engine and none of the following conditions are true:

- The `$lookup` operation executes a pipeline on a foreign collection. To see an example of this kind of operation, see Join Conditions and Subqueries on a Foreign Collection.

- The `$lookup`'s `localField` or `foreignField` specify numeric components. For example: `{ localField: "restaurant.0.review" }`.

- The `from` field of any `$lookup` in the pipeline specifies a view or sharded collection.

For more information, see `$lookup` Optimization.

### Performance Considerations

`$lookup` performance depends on the type of operation performed. Refer to the following table for performance considerations for different `$lookup` operations.

| `$lookup` Operation | Performance Considerations |
| --- | --- |
| Equality Match with a Single Join | - `$lookup` operations that perform equality matches with a single join perform better when the foreign collection contains an index on the `foreignField`. IMPORTANT: If a supporting index on the `foreignField` does not exist, a `$lookup` operation that performs an equality match with a single join will likely have poor performance. |
| Uncorrelated Subqueries | - `$lookup` operations that contain uncorrelated subqueries perform better when the inner pipeline can reference an index of the foreign collection. - MongoDB only needs to run the `$lookup` subquery once before caching the query because there is no relationship between the source and foreign collections. The subquery is not based on any value in the source collection. This behavior improves performance for subsequent executions of the `$lookup` operation. |
| Correlated Subqueries | - `$lookup` operations that contain correlated subqueries perform better when the following conditions apply: - The foreign collection contains an index on the `foreignField`. - The foreign collection contains an index that references the inner pipeline. - If your pipeline passes a large number of documents to the `$lookup` query, the following strategies may improve performance: - Reduce the number of documents that MongoDB passes to the `$lookup` query. For example, set a stricter filter during the `$match` stage. - Run the inner pipeline of the `$lookup` subquery as a separate query and use `$out` to create a temporary collection. Then, run an equality match with a single join. - Reconsider the data's schema to ensure it is optimal for the use case. |
For general performance strategies, see Indexing Strategies and Query Optimization.

## Examples

<Tabs>

<Tab name="MongoDB Shell">

The examples on this page use data from the sample_mflix sample dataset. For details on how to load this dataset into your self-managed MongoDB deployment, see Load the sample dataset. If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

### Perform a Single Equality Join with `$lookup`

The following aggregation operation first filters the `movies` collection to movies with a `runtime` greater than `1000`, then joins with the `comments` collection on the `_id` and `movie_id` fields:

```javascript
db.movies.aggregate( [
   { $match: { runtime: { $gt: 1000 } } },
   {
      $lookup: {
         from: "comments",
         localField: "_id",
         foreignField: "movie_id",
         as: "movie_comments"
      }
   },
   {
      $project: {
         _id: 0,
         title: 1,
         year: 1,
         "movie_comments.name": 1,
         "movie_comments.text": 1,
         "movie_comments.date": 1
      }
   }
] )

```

```javascript
[
  {
    title: 'Centennial',
    year: 1978,
    movie_comments: [
      {
        name: 'Ellaria Sand',
        text: 'Excepturi nam nam eum possimus aspernatur autem. Quis nulla optio praesentium ut distinctio explicabo.',
        date: ISODate('1995-08-18T03:01:50.000Z')
      }
    ]
  },
  { title: 'Baseball', year: 1994, movie_comments: [] }
]

```

The operation corresponds to this pseudo-SQL statement:

```sql
SELECT *, movie_comments
FROM movies
WHERE movie_comments IN (
   SELECT *
   FROM comments
   WHERE movie_id = movies._id
);
```

For more information, see Equality Match Performance Considerations.

### Use `$lookup` with an Array

If the `localField` is an array, you can match the array elements against a scalar `foreignField` without an `$unwind` stage.

The following aggregation operation joins the `movies` collection with the `users` collection, matching the `cast` array field from `movies` against the scalar `name` field from `users`:

```javascript
db.movies.aggregate( [
   {
      $match: {
         title: {
            $in: [ "Roger & Me", "The Sum of Us",
               "Centennial" ]
         }
      }
   },
   {
      $lookup: {
         from: "users",
         localField: "cast",
         foreignField: "name",
         as: "cast_users"
      }
   },
   {
      $project: {
         _id: 0,
         title: 1,
         year: 1,
         cast: 1,
         "cast_users.name": 1,
         "cast_users.email": 1
      }
   },
   { $sort: { year: 1 } }
] )

```

```javascript
[
  {
    cast: [
      'Raymond Burr',
      'Barbara Carrera',
      'Richard Chamberlain',
      'Robert Conrad'
    ],
    title: 'Centennial',
    year: 1978,
    cast_users: []
  },
  {
    cast: [
      'Michael Moore',
      'Roger B. Smith',
      'Rhonda Britton',
      'Fred Ross'
    ],
    title: 'Roger & Me',
    year: 1989,
    cast_users: [ { name: 'Michael Moore', email: 'michael_moore@fakegmail.com' } ]
  },
  {
    cast: [
      'Jack Thompson',
      'Russell Crowe',
      'John Polson',
      'Deborah Kennedy'
    ],
    title: 'The Sum of Us',
    year: 1994,
    cast_users: [
      {
        name: 'Deborah Kennedy',
        email: 'deborah_kennedy@fakegmail.com'
      }
    ]
  }
]

```

### Use `$lookup` with `$mergeObjects`

The `$mergeObjects` operator combines multiple documents into a single document.

The following operation uses `$lookup` to join the `movies` collection with the `comments` collection, then uses `$mergeObjects` in `$replaceRoot` to merge the first comment document with the movie document:

```javascript
db.movies.aggregate( [
   { $match: { runtime: { $gt: 1000 } } },
   {
      $lookup: {
         from: "comments",
         localField: "_id",
         foreignField: "movie_id",
         as: "movie_comments"
      }
   },
   {
      $replaceRoot: {
         newRoot: {
            $mergeObjects: [
               { $arrayElemAt: [ "$movie_comments", 0 ] },
               "$$ROOT"
            ]
         }
      }
   },
   {
      $project: {
         _id: 0,
         title: 1,
         year: 1,
         genres: 1,
         name: 1,
         email: 1,
         text: 1,
         date: 1
      }
   }
] )

```

```javascript
[
  {
    name: 'Ellaria Sand',
    email: 'indira_varma@gameofthron.es',
    text: 'Excepturi nam nam eum possimus aspernatur autem. Quis nulla optio praesentium ut distinctio explicabo.',
    date: ISODate('1995-08-18T03:01:50.000Z'),
    genres: [ 'Action', 'Adventure', 'Drama' ],
    title: 'Centennial',
    year: 1978
  },
  {
    genres: [ 'Documentary', 'History', 'Sport' ],
    title: 'Baseball',
    year: 1994
  }
]

```

### Use Multiple Join Conditions and a Correlated Subquery

Pipelines can execute on a foreign collection and include multiple join conditions. The `$expr` operator enables more complex join conditions including conjunctions and non-equality matches.

A join condition can reference a field in the local collection on which the `aggregate()` method was run and reference a field in the foreign collection. This allows a correlated subquery between the two collections.

MongoDB 5.0 supports concise correlated subqueries.

The following example:

- Joins the `movies` and `comments` collections using the `_id` and `movie_id` fields.

- Filters comments to include only those posted after the movie's release year.

```javascript
db.movies.aggregate( [
   {
      $match: {
         title: {
            $in: [ "Class Action", "Kafka", "Corpse Bride" ]
         }
      }
   },
   {
      $lookup: {
         from: "comments",
         localField: "_id",
         foreignField: "movie_id",
         let: { movie_year: "$year" },
         pipeline: [
            {
               $match: {
                  $expr: {
                     $gt: [
                        { $year: "$date" }, "$$movie_year"
                     ]
                  }
               }
            },
            { $project: { _id: 0, name: 1, date: 1 } }
         ],
         as: "post_release_comments"
      }
   },
   {
      $project: {
         _id: 0,
         title: 1,
         year: 1,
         post_release_comments: 1
      }
   }
] )

```

```javascript
[
  {
    year: 1991,
    title: 'Class Action',
    post_release_comments: [
      { name: 'Khal Drogo', date: ISODate('2016-12-06T07:17:03.000Z') }
    ]
  },
  {
    year: 1991,
    title: 'Kafka',
    post_release_comments: [
      { name: 'Khal Drogo', date: ISODate('1998-05-10T03:10:20.000Z') }
    ]
  },
  { year: 2005, title: 'Corpse Bride', post_release_comments: [] }
]

```

The operation corresponds to this pseudo-SQL statement:

```sql
SELECT *, post_release_comments
FROM movies
WHERE post_release_comments IN (
   SELECT name, date
   FROM comments
   WHERE movie_id = movies._id
   AND YEAR(date) > movies.year
);
```

The `$eq`, `$lt`, `$lte`, `$gt`, and `$gte` comparison operators placed in an `$expr` operator can use an index on the `from` collection referenced in a `$lookup` stage. Limitations:

- Indexes can only be used for comparisons between fields and constants, so the `let` operand must resolve to a constant.

  For example, a comparison between `$a` and a constant value can use an index, but a comparison between `$a` and `$b` cannot.

- Indexes are not used for comparisons where the `let` operand resolves to an empty or missing value.

- Multikey, partial, or sparse indexes are not used.

For example, if the index `{ movie_id: 1 }` exists on the `comments` collection:

- The equality match on the `comments.movie_id` field uses the index.

- `$expr`

- Variables in Aggregation Expressions

### Perform an Uncorrelated Subquery with `$lookup`

An aggregation pipeline `$lookup` stage can execute a pipeline on the foreign collection, which allows uncorrelated subqueries. An uncorrelated subquery does not reference the local document fields.

Starting in MongoDB 5.0, for an uncorrelated subquery in a `$lookup` pipeline stage containing a `$sample` stage, the `$sampleRate` operator, or the `$rand` operator, the subquery is always run again if repeated. Previously, depending on the subquery output size, either the subquery output was cached or the subquery was run again.

The following operation joins the `users` collection with movies that have a runtime greater than 1000 minutes from the `movies` collection:

```javascript
db.users.aggregate( [
   {
      $match: {
         email: { $in: [
            "mark_addy@gameofthron.es",
            "lena_headey@gameofthron.es"
         ] }
      }
   },
   {
      $lookup: {
         from: "movies",
         pipeline: [
            { $match: { runtime: { $gt: 1000 } } },
            { $project: { _id: 0, title: 1, year: 1 } }
         ],
         as: "long_movies"
      }
   },
   {
      $project: {
         _id: 0, name: 1, email: 1, long_movies: 1
      }
   }
] )

```

```javascript
[
  {
    name: 'Robert Baratheon',
    email: 'mark_addy@gameofthron.es',
    long_movies: [
      { title: 'Centennial', year: 1978 },
      { title: 'Baseball', year: 1994 }
    ]
  },
  {
    name: 'Cersei Lannister',
    email: 'lena_headey@gameofthron.es',
    long_movies: [
      { title: 'Centennial', year: 1978 },
      { title: 'Baseball', year: 1994 }
    ]
  }
]

```

The operation corresponds to this pseudo-SQL statement:

```sql
SELECT *, long_movies
FROM users
WHERE long_movies IN (
   SELECT title, year
   FROM movies
   WHERE runtime > 1000
);
```

For more information, see Uncorrelated Subquery Performance Considerations.

### Perform a Concise Correlated Subquery with `$lookup`

Starting in MongoDB 5.0, an aggregation pipeline `$lookup` stage supports a concise correlated subquery syntax that improves joins between collections. The new concise syntax removes the requirement for an equality match on the foreign and local fields inside of an `$expr` operator in a `$match` stage.

The following example:

- Joins the `movies` and `comments` collections by matching the localField `_id` with the foreignField
  `movie_id`. The match is performed before the `pipeline` is run.

- Filters comments to include only those posted after the movie's release year, accessed using `$$movie_year` and `$date` respectively.

```javascript
db.movies.aggregate( [
   {
      $match: {
         title: { $in: [
            "I Don't Kiss",
            "Lucky Luke",
            "Mississippi Masala"
         ] }
      }
   },
   {
      $lookup: {
         from: "comments",
         localField: "_id",
         foreignField: "movie_id",
         let: { movie_year: "$year" },
         pipeline: [
            {
               $match: {
                  $expr: {
                     $gt: [
                        { $year: "$date" }, "$$movie_year"
                     ]
                  }
               }
            },
            { $project: { _id: 0, name: 1, date: 1 } }
         ],
         as: "post_release_comments"
      }
   },
   {
      $project: {
         _id: 0,
         title: 1,
         year: 1,
         post_release_comments: 1
      }
   }
] )

```

```javascript
[
  {
    title: "I Don't Kiss",
    year: 1991,
    post_release_comments: [
      {
        name: 'Brandon Hardy',
        date: ISODate('2016-09-18T11:11:34.000Z')
      }
    ]
  },
  {
    title: 'Lucky Luke',
    year: 1991,
    post_release_comments: [
      {
        name: 'Kelsey Smith',
        date: ISODate('2010-01-13T17:55:01.000Z')
      }
    ]
  },
  {
    title: 'Mississippi Masala',
    year: 1991,
    post_release_comments: [
      {
        name: 'Phillip Collins',
        date: ISODate('2010-05-13T08:04:22.000Z')
      }
    ]
  }
]

```

This example uses the older verbose syntax from MongoDB versions before 5.0 and returns the same results as the previous concise example:

```javascript
db.movies.aggregate( [
   {
      $match: {
         title: { $in: [
            "I Don't Kiss",
            "Lucky Luke",
            "Mississippi Masala"
         ] }
      }
   },
   {
      $lookup: {
         from: "comments",
         let: { movie_id: "$_id", movie_year: "$year" },
         pipeline: [
            {
               $match: {
                  $expr: {
                     $and: [
                        { $eq: [ "$movie_id", "$$movie_id" ] },
                        { $gt: [
                           { $year: "$date" }, "$$movie_year"
                        ] }
                     ]
                  }
               }
            },
            { $project: { _id: 0, name: 1, date: 1 } }
         ],
         as: "post_release_comments"
      }
   },
   {
      $project: {
         _id: 0,
         title: 1,
         year: 1,
         post_release_comments: 1
      }
   }
] )

```

```javascript
[
  {
    title: "I Don't Kiss",
    year: 1991,
    post_release_comments: [
      {
        name: 'Brandon Hardy',
        date: ISODate('2016-09-18T11:11:34.000Z')
      }
    ]
  },
  {
    title: 'Lucky Luke',
    year: 1991,
    post_release_comments: [
      {
        name: 'Kelsey Smith',
        date: ISODate('2010-01-13T17:55:01.000Z')
      }
    ]
  },
  {
    title: 'Mississippi Masala',
    year: 1991,
    post_release_comments: [
      {
        name: 'Phillip Collins',
        date: ISODate('2010-05-13T08:04:22.000Z')
      }
    ]
  }
]

```

The previous examples correspond to this pseudo-SQL statement:

```sql
SELECT *, post_release_comments
FROM movies
WHERE post_release_comments IN (
   SELECT *
   FROM comments
   WHERE comments.movie_id = movies._id
   AND YEAR(comments.date) > movies.year
);
```

For more information, see Correlated Subquery Performance Considerations.

### Namespaces in Subpipelines

Starting in MongoDB 8.0, namespaces in subpipelines within `$lookup` and `$unionWith` are validated to ensure the correct use of `from` and `coll` fields:

- For `$lookup`, omit the `from` field if you use a subpipeline with a stage which doesn't require a specified collection. For example, a `$documents` stage.

- Similarly, for `$unionWith`, omit the `coll` field.

Unchanged behavior:

- For a `$lookup` that starts with a stage for a collection, for example a `$match` or `$collStats` subpipeline, you must include the `from` field and specify the collection.

- Similarly, for `$unionWith`, include the `coll` field and specify the collection.

The following scenario shows an example.

Create a collection `cakeFlavors`:

```javascript
db.cakeFlavors.insertMany( [
   { _id: 1, flavor: "chocolate" },
   { _id: 2, flavor: "strawberry" },
   { _id: 3, flavor: "cherry" }
] )
```

</Tab>

<Tab name="C#">

The C# examples on this page use the `sample_mflix` database from the Atlas sample datasets. To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see Get Started in the MongoDB .NET/C# Driver documentation.

The following `Movie` class models the documents in the `sample_mflix.movies` collection:

```csharp
public class Movie
{
    public ObjectId Id { get; set; }

    public int Runtime { get; set; }

    public string Title { get; set; }

    public string Rated { get; set; }

    public List<string> Genres { get; set; }

    public string Plot { get; set; }

    public ImdbData Imdb { get; set; }

    public int Year { get; set; }

    public int Index { get; set; }

    public string[] Comments { get; set; }

    [BsonElement("lastupdated")]
    public DateTime LastUpdated { get; set; }
}
```

The C# classes on this page use Pascal case for their property names, but the field names in the MongoDB collection use camel case. To account for this difference, you can use the following code to register a `ConventionPack` when your application starts:

```csharp
var camelCaseConvention = new ConventionPack { new CamelCaseElementNameConvention() };
ConventionRegistry.Register("CamelCase", camelCaseConvention, type => true);
```

The following `Comment` class models the documents in the `sample_mflix.comments` collection:

```csharp
public class Comment
{
    public Guid Id { get; set; }

    [BsonElement("movie_id")]
    public Guid MovieId { get; set; }

    public string Text { get; set; }
}
```

`$lookup`

Lookup()

performs a left outer join between the `movies` and `comments` collections. The code joins the `Id` field from each `Movie` document to the `MovieId` field in the `Comment` documents. The comments for each movie are stored in a field named `Comments` in each `Movie` document.

To use the MongoDB .NET/C# driver to add a `$lookup` stage to an aggregation pipeline, call the Lookup() method on a `PipelineDefinition` object.

The following example creates a pipeline stage that performs a left outer join between the `movies` and `comments` collections. The code joins the `Id` field from each `Movie` document to the `MovieId` field in the `Comment` documents. The comments for each movie are stored in a field named `Comments` in each `Movie` document.

```csharp
var commentCollection = client
    .GetDatabase("aggregation_examples")
    .GetCollection<Comment>("comments");

var pipeline = new EmptyPipelineDefinition<Movie>()
    .Lookup<Movie, Movie, Comment, Movie>(
        foreignCollection: commentCollection,
        localField: m => m.Id,
        foreignField: c => c.MovieId,
        @as: m => m.Comments);
```

</Tab>

<Tab name="Node.js">

The Node.js examples on this page use the `sample_mflix` database from the Atlas sample datasets. To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see Get Started in the MongoDB Node.js driver documentation.

`$lookup`

performs a left outer join between the `movies` and `comments` collections. The code joins the `_id` field from each `movie` document to the `movie_id` field in the `comment` documents. The `comments` field stores the comments for each movie in each `movie` document

To use the MongoDB Node.js driver to add a `$lookup` stage to an aggregation pipeline, use the `$lookup` operator in a pipeline object.

The following example creates a pipeline stage that performs a left outer join between the `movies` and `comments` collections. The code joins the `_id` field from each `movie` document to the `movie_id` field in the `comment` documents. The `comments` field stores the comments for each movie in each `movie` document. The example then runs the aggregation pipeline:

```javascript
const pipeline = [
  {
    $lookup: {
      from: "comments",
      localField: "_id",
      foreignField: "movie_id",
      as: "comments"
    }
  }
];

const cursor = collection.aggregate(pipeline);
return cursor;
```

</Tab>

</Tabs>
