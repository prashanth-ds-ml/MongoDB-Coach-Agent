> Source: https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/
> Fetch method: direct_markdown

# $group (aggregation stage)

## Definition

`$group`
The $group stage combines multiple documents with the same field, fields, or expression into a single document according to a group key. The result is one document per unique group key.

A group key is often a field, or group of fields. The group key can also be the result of an expression. Use the `_id` field in the `$group` pipeline stage to set the group key. See below for [usage examples](https://www.mongodb.com/docs/reference/operator/aggregation/group/#std-label-ex-agg-group-stage).

In the `$group` stage output, the `_id` field is set to the group key for that document.

The output documents can also contain additional fields that are set using [accumulator expressions](https://www.mongodb.com/docs/reference/operator/aggregation/group/#std-label-accumulators-group).

[`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) does *not* order its output documents.

## Compatibility

`$group`You can use `$group` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

The [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stage has the following prototype form:

```javascript
{
 $group:
   {
     _id: <expression>, // Group key
     <field1>: { <accumulator1> : <expression1> },
     ...
   }
 }
```

<table>
<tr>
<th id="Field">
Field

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Field">
`_id`

</td>
<td headers="Description">
*Required.* The `_id` expression specifies the group key. If you specify an `_id` value of null, or any other constant value, the `$group` stage returns a single document that aggregates values across all of the input documents. [See the Group by Null example](https://www.mongodb.com/docs/reference/operator/aggregation/group/#std-label-null-example).

</td>
</tr>
<tr>
<td headers="Field">
`field`

</td>
<td headers="Description">
*Optional.* Computed using the [accumulator operators](https://www.mongodb.com/docs/reference/operator/aggregation/group/#std-label-accumulators-group).

</td>
</tr>
</table>The `_id` and the [accumulator operators](https://www.mongodb.com/docs/reference/operator/aggregation/group/#std-label-accumulators-group) can accept any valid `expression`. For more information on expressions, see [Expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions).

## Considerations

### Performance

`$group``$group` is a blocking stage, which causes the pipeline to wait for all input data to be retrieved for the blocking stage before processing the data. A blocking stage may reduce performance because it reduces parallel processing for a pipeline with multiple stages. A blocking stage may also use substantial amounts of memory for large data sets.

### Accumulator Operator

The `<accumulator>` operator must be one of the following accumulator operators:

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
[`$accumulator`](https://www.mongodb.com/docs/reference/operator/aggregation/accumulator/#mongodb-group-grp.-accumulator)

</td>
<td headers="Description">
Returns the result of a user-defined accumulator function.

</td>
</tr>
<tr>
<td headers="Name">
[`$addToSet`](https://www.mongodb.com/docs/reference/operator/aggregation/addToSet/#mongodb-group-grp.-addToSet)

</td>
<td headers="Description">
Returns an array of *unique* expression values for each group. Order of the array elements is undefined.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$avg`](https://www.mongodb.com/docs/reference/operator/aggregation/avg/#mongodb-group-grp.-avg)

</td>
<td headers="Description">
Returns an average of numerical values. Ignores non-numeric values.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$bottom`](https://www.mongodb.com/docs/reference/operator/aggregation/bottom/#mongodb-group-grp.-bottom)

</td>
<td headers="Description">
Returns the bottom element within a group according to the specified sort order.

Available in the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) and [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stages.

</td>
</tr>
<tr>
<td headers="Name">
[`$bottomN`](https://www.mongodb.com/docs/reference/operator/aggregation/bottomN/#mongodb-group-grp.-bottomN)

</td>
<td headers="Description">
Returns an aggregation of the bottom `n` fields within a group, according to the specified sort order.

Available in the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) and [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stages.

</td>
</tr>
<tr>
<td headers="Name">
[`$concatArrays`](https://www.mongodb.com/docs/reference/operator/aggregation/concatArrays/#mongodb-group-grp.-concatArrays)

</td>
<td headers="Description">
Returns a single array that combines the elements of two or more arrays.

</td>
</tr>
<tr>
<td headers="Name">
[`$count`](https://www.mongodb.com/docs/reference/operator/aggregation/count-accumulator/#mongodb-group-grp.-count)

</td>
<td headers="Description">
Returns the number of documents in a group.

Distinct from the [`$count`](https://www.mongodb.com/docs/reference/operator/aggregation/count/#mongodb-pipeline-pipe.-count) pipeline stage.

Available in the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) and [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stages.

</td>
</tr>
<tr>
<td headers="Name">
[`$first`](https://www.mongodb.com/docs/reference/operator/aggregation/first/#mongodb-group-grp.-first)

</td>
<td headers="Description">
Returns the result of an [expression](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) for the first document in a group.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$firstN`](https://www.mongodb.com/docs/reference/operator/aggregation/firstN/#mongodb-group-grp.-firstN)

</td>
<td headers="Description">
Returns an aggregation of the first `n` elements within a group. Only meaningful when documents are in a defined order. Distinct from the [`$firstN`](https://www.mongodb.com/docs/reference/operator/aggregation/firstN/#mongodb-expression-exp.-firstN) array operator.

Available in the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group), [expression](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) and [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stages.

</td>
</tr>
<tr>
<td headers="Name">
[`$last`](https://www.mongodb.com/docs/reference/operator/aggregation/last/#mongodb-group-grp.-last)

</td>
<td headers="Description">
Returns the result of an [expression](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) for the last document in a group.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$lastN`](https://www.mongodb.com/docs/reference/operator/aggregation/lastN/#mongodb-group-grp.-lastN)

</td>
<td headers="Description">
Returns an aggregation of the last `n` elements within a group. Only meaningful when documents are in a defined order. Distinct from the [`$lastN`](https://www.mongodb.com/docs/reference/operator/aggregation/lastN/#mongodb-expression-exp.-lastN) array operator.

Available in the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group), [expression](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) and [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stages.

</td>
</tr>
<tr>
<td headers="Name">
[`$max`](https://www.mongodb.com/docs/reference/operator/aggregation/max/#mongodb-group-grp.-max)

</td>
<td headers="Description">
Returns the highest expression value for each group.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$maxN`](https://www.mongodb.com/docs/reference/operator/aggregation/maxN/#mongodb-group-grp.-maxN)

</td>
<td headers="Description">
Returns an aggregation of the `n` maximum valued elements in a group. Distinct from the [`$maxN`](https://www.mongodb.com/docs/reference/operator/aggregation/maxN-array-element/#mongodb-expression-exp.-maxN) array operator.

Available in [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group), [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) and as an [expression](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions).

</td>
</tr>
<tr>
<td headers="Name">
[`$median`](https://www.mongodb.com/docs/reference/operator/aggregation/median/#mongodb-group-grp.-median)

</td>
<td headers="Description">
Returns an approximation of the [median](https://www.mongodb.com/docs/reference/glossary/#std-term-median), the 50th [percentile](https://www.mongodb.com/docs/reference/glossary/#std-term-percentile), as a scalar value.

This operator is available as an accumulator in these stages:

- [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)

- [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)

It is also available as an [aggregation expression](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions).

</td>
</tr>
<tr>
<td headers="Name">
[`$mergeObjects`](https://www.mongodb.com/docs/reference/operator/aggregation/mergeObjects/#mongodb-expression-exp.-mergeObjects)

</td>
<td headers="Description">
Returns a document created by combining the input documents for each group.

</td>
</tr>
<tr>
<td headers="Name">
[`$min`](https://www.mongodb.com/docs/reference/operator/aggregation/min/#mongodb-group-grp.-min)

</td>
<td headers="Description">
Returns the lowest expression value for each group.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$minN`](https://www.mongodb.com/docs/reference/operator/aggregation/minN/#mongodb-group-grp.-minN)

</td>
<td headers="Description">
Returns an aggregation of the `n` minimum valued elements in a group. Distinct from the [`$minN`](https://www.mongodb.com/docs/reference/operator/aggregation/minN-array-element/#mongodb-expression-exp.-minN) array operator.

Available in [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group), [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) and as an [expression](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions).

</td>
</tr>
<tr>
<td headers="Name">
[`$percentile`](https://www.mongodb.com/docs/reference/operator/aggregation/percentile/#mongodb-group-grp.-percentile)

</td>
<td headers="Description">
Returns an array of scalar values that correspond to specified [percentile](https://www.mongodb.com/docs/reference/glossary/#std-term-percentile) values.

This operator is available as an accumulator in these stages:

- [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)

- [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)

It is also available as an [aggregation expression](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions).

</td>
</tr>
<tr>
<td headers="Name">
[`$push`](https://www.mongodb.com/docs/reference/operator/aggregation/push/#mongodb-group-grp.-push)

</td>
<td headers="Description">
Returns an array of expression values for documents in each group.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$setUnion`](https://www.mongodb.com/docs/reference/operator/aggregation/setUnion/#mongodb-group-grp.-setUnion)

</td>
<td headers="Description">
Takes two or more arrays and returns an array containing the elements that appear in any input array.

</td>
</tr>
<tr>
<td headers="Name">
[`$stdDevPop`](https://www.mongodb.com/docs/reference/operator/aggregation/stdDevPop/#mongodb-group-grp.-stdDevPop)

</td>
<td headers="Description">
Returns the population standard deviation of the input values.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$stdDevSamp`](https://www.mongodb.com/docs/reference/operator/aggregation/stdDevSamp/#mongodb-group-grp.-stdDevSamp)

</td>
<td headers="Description">
Returns the sample standard deviation of the input values.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$sum`](https://www.mongodb.com/docs/reference/operator/aggregation/sum/#mongodb-group-grp.-sum)

</td>
<td headers="Description">
Returns a sum of numerical values. Ignores non-numeric values.

Available in the [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stage.

</td>
</tr>
<tr>
<td headers="Name">
[`$top`](https://www.mongodb.com/docs/reference/operator/aggregation/top/#mongodb-group-grp.-top)

</td>
<td headers="Description">
Returns the top element within a group according to the specified sort order.

Available in the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) and [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stages.

</td>
</tr>
<tr>
<td headers="Name">
[`$topN`](https://www.mongodb.com/docs/reference/operator/aggregation/topN/#mongodb-group-grp.-topN)

</td>
<td headers="Description">
Returns an aggregation of the top `n` fields within a group, according to the specified sort order.

Available in the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) and [`$setWindowFields`](https://www.mongodb.com/docs/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields) stages.

</td>
</tr>
</table>

### `$group` and Memory Restrictions

If the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stage exceeds 100 megabytes of RAM, MongoDB writes data to temporary files. However, if the [allowDiskUse](https://www.mongodb.com/docs/reference/command/aggregate/#std-label-aggregate-cmd-allowDiskUse) option is set to `false`, `$group` returns an error. For more information, refer to [Aggregation Pipeline Limits](https://www.mongodb.com/docs/core/aggregation-pipeline-limits/).

### `$group` Performance Optimizations

This section describes optimizations to improve the performance of [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group). There are optimizations that you can make manually and optimizations MongoDB makes internally.

#### Optimization to Return the First or Last Document of Each Group

If a pipeline [`sorts`](https://www.mongodb.com/docs/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort) and [`groups`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) by the same field and the `$group` stage only uses the [`$first`](https://www.mongodb.com/docs/reference/operator/aggregation/first/#mongodb-group-grp.-first) or [`$last`](https://www.mongodb.com/docs/reference/operator/aggregation/last/#mongodb-group-grp.-last) accumulator operator, consider adding an [index](https://www.mongodb.com/docs/indexes/#std-label-indexes) on the grouped field which matches the sort order. In some cases, the `$group` stage can use the index to quickly find the first or last document of each group.

If the `movies` collection contains an index `{ year: 1, title: 1 }`, the following pipeline can use that index to find the first document of each group:

```javascript
db.movies.aggregate([
   {
      $sort: { year: 1, title: 1 }
   },
   {
      $group: {
         _id: { year: "$year" },
         title: { $first: "$title" }
      }
   }
])

```

#### Slot-Based Query Execution Engine

Starting in version 5.2, MongoDB uses the [slot-based execution query engine](https://www.mongodb.com/docs/reference/sbe/#std-label-sbe-landing) to execute [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stages if either:

- `$group` is the first stage in the pipeline.

- All preceding stages in the pipeline can also be executed by the slot-based execution engine.

For more information, see [`$group` Optimization](https://www.mongodb.com/docs/core/aggregation-pipeline-optimization/#std-label-agg-group-optimization-sbe).

## Examples

<Tabs>

<Tab name="MongoDB Shell">

### Count the Number of Documents in a Collection

The examples on this page use data from the [sample_mflix sample dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](https://www.mongodb.com/docs/atlas/sample-data/load-sample-data-local/#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

The following aggregation operation uses the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stage to count the number of documents in the `movies` collection:

```javascript
db.movies.aggregate([
   {
      $group: {
         _id: null,
         count: { $count: {} }
      }
   }
])

```

```javascript
[
  {
    _id: null,
    count: 21349
  }
]

```

This aggregation operation is equivalent to the following SQL statement:

```sql
SELECT COUNT(*) AS count FROM movies
```

- [`$count`](https://www.mongodb.com/docs/reference/operator/aggregation/count/#mongodb-pipeline-pipe.-count)

- [`$count (aggregation accumulator)`](https://www.mongodb.com/docs/reference/operator/aggregation/count-accumulator/#mongodb-group-grp.-count)

### Retrieve Distinct Values

The following aggregation operation uses the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stage to retrieve the distinct `rated` values from the `movies` collection:

```javascript
db.movies.aggregate( [ { $group : { _id : "$rated" } } ] )

```

```javascript
[
  {
    _id: 'TV-PG'
  },
  {
    _id: 'PG'
  },
  {
    _id: 'TV-14'
  },
  {
    _id: 'OPEN'
  },
  {
    _id: 'Not Rated'
  },
  {
    _id: 'GP'
  },
  {
    _id: 'TV-Y7'
  },
  {
    _id: 'G'
  },
  {
    _id: 'PG-13'
  },
  {
    _id: null
  },
  {
    _id: 'M'
  },
  {
    _id: 'R'
  },
  {
    _id: 'TV-MA'
  },
  {
    _id: 'APPROVED'
  },
  {
    _id: 'PASSED'
  },
  {
    _id: 'Approved'
  },
  {
    _id: 'AO'
  },
  {
    _id: 'TV-G'
  }
]

```

For example, `$group` operations of the following form can result in a `DISTINCT_SCAN`:

```javascript
{ $group : { _id : "$<field>" } }
```

For more information on behavior for retrieving distinct values, see the [distinct command behavior](https://www.mongodb.com/docs/reference/command/distinct/#std-label-distinct-command-behavior).

To see whether your operation results in a `DISTINCT_SCAN`, check your operation's [explain results](https://www.mongodb.com/docs/reference/explain-results/#std-label-explain-results).

### Group by Rating

The following aggregation operation groups documents by the `rated` field, calculating the total runtime per rating and returning only the ratings with a total runtime greater than or equal to 100000:

```javascript
db.movies.aggregate(
   [
      // First Stage
      {
         $group: {
            _id: "$rated",
            totalRuntime: { $sum: "$runtime" }
         }
      },
      // Second Stage
      {
         $match: { "totalRuntime": { $gte: 100000 } }
      }
   ]
)

```

```javascript
[
  {
    _id: 'PG-13',
    totalRuntime: 250843
  },
  {
    _id: 'R',
    totalRuntime: 582318
  },
  {
    _id: null,
    totalRuntime: 967127
  },
  {
    _id: 'PG',
    totalRuntime: 191204
  }
]

```

First Stage: - The [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stage groups the documents by `rated` to retrieve the distinct rating values. This stage returns the `totalRuntime` for each rating group.

Second Stage: - The [`$match`](https://www.mongodb.com/docs/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match) stage filters the resulting documents to return only ratings with a `totalRuntime` greater than or equal to 100000.

This aggregation operation is equivalent to the following SQL statement:

```sql
SELECT rated,
   Sum(runtime) AS totalRuntime
FROM   movies
GROUP  BY rated
HAVING totalRuntime >= 100000
```

[`$match`](https://www.mongodb.com/docs/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match)

### Calculate Count, Sum, and Average

#### Group by Year

The following pipeline calculates the total runtime, average runtime, and movie count for each year before 1910:

```javascript
db.movies.aggregate([
   { $match: { "year": { $lt: 1910 } } },
   {
      $group: {
         _id: "$year",
         totalRuntime: { $sum: "$runtime" },
         averageRuntime: { $avg: "$runtime" },
         count: { $sum: 1 }
      }
   },
   { $sort: { totalRuntime: -1 } }
])

```

```javascript
[
  { _id: 1909, totalRuntime: 14, averageRuntime: 14, count: 1 },
  { _id: 1903, totalRuntime: 11, averageRuntime: 11, count: 1 },
  { _id: 1896, totalRuntime: 2, averageRuntime: 1, count: 2 }
]

```

First Stage: - The [`$match`](https://www.mongodb.com/docs/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match) stage filters the documents to only pass movies released before 1910 to the next stage.

Second Stage: - The [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stage groups the documents by year and calculates the total runtime, average runtime, and total count of the documents in each group.

Third Stage: - The [`$sort`](https://www.mongodb.com/docs/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort) stage sorts the results by the total runtime for each group in descending order.

This aggregation operation is equivalent to the following SQL statement:

```sql
SELECT year,
       Sum(runtime) AS totalRuntime,
       Avg(runtime) AS averageRuntime,
       Count(*)     AS count
FROM   movies
WHERE  year < 1910
GROUP  BY year
ORDER  BY totalRuntime DESC
```

- [`$match`](https://www.mongodb.com/docs/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match)

- [`$sort`](https://www.mongodb.com/docs/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort)

- [`db.collection.countDocuments()`](https://www.mongodb.com/docs/reference/method/db.collection.countDocuments/#mongodb-method-db.collection.countDocuments) which wraps the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) aggregation stage with a [`$sum`](https://www.mongodb.com/docs/reference/operator/aggregation/sum/#mongodb-group-grp.-sum) expression.

#### Group by `null`

The following aggregation operation specifies a group `_id` of `null`, calculating the total runtime, average runtime, and count of all documents in the collection.

```javascript
db.movies.aggregate([
   {
      $group: {
         _id: null,
         totalRuntime: { $sum: "$runtime" },
         averageRuntime: { $avg: "$runtime" },
         count: { $sum: 1 }
      }
   }
])

```

```javascript
[
  {
    _id: null,
    totalRuntime: 2167458,
    averageRuntime: 103.65652797704448,
    count: 21349
  }
]

```

This aggregation operation is equivalent to the following SQL statement:

```sql
SELECT Sum(runtime) AS totalRuntime,
       Avg(runtime) AS averageRuntime,
       Count(*)     AS count
FROM   movies
```

- [`$count`](https://www.mongodb.com/docs/reference/operator/aggregation/count/#mongodb-pipeline-pipe.-count)

- [`db.collection.countDocuments()`](https://www.mongodb.com/docs/reference/method/db.collection.countDocuments/#mongodb-method-db.collection.countDocuments) which wraps the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) aggregation stage with a [`$sum`](https://www.mongodb.com/docs/reference/operator/aggregation/sum/#mongodb-group-grp.-sum) expression.

### Pivot Data

#### Group Titles by Year

The following aggregation operation pivots the data in the `movies` collection to group titles by year:

```javascript
db.movies.aggregate([
   { $match: { year: { $lt: 1910 } } },
   { $group: { _id: "$year", titles: { $push: "$title" } } },
   { $sort: { _id: 1 } }
])

```

```javascript
[
  { _id: 1896, titles: [ 'The Kiss', 'The Kiss' ] },
  { _id: 1903, titles: [ 'The Great Train Robbery' ] },
  { _id: 1909, titles: [ 'A Corner in Wheat' ] }
]

```

#### Group Documents by Year

The following aggregation operation groups documents by year:

```javascript
db.movies.aggregate([
   { $match: { year: { $lt: 1910 } } },
   { $group: { _id: "$year", movies: { $push: "$$ROOT" } } },
   {
      $addFields: {
         totalRuntime: { $sum: "$movies.runtime" }
      }
   },
   { $sort: { _id: 1 } }
])

```

```javascript
[
  { _id: 1896, movies: '...', totalRuntime: 2 },
  { _id: 1903, movies: '...', totalRuntime: 11 },
  { _id: 1909, movies: '...', totalRuntime: 14 }
]

```

First Stage: - [`$match`](https://www.mongodb.com/docs/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match) filters the documents to only pass movies released before 1910 to the next stage.

Second Stage: - [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) uses the [`$$ROOT`](https://www.mongodb.com/docs/reference/aggregation-variables/#mongodb-variable-variable.ROOT) system variable to group the entire documents by year.

Third Stage: - [`$addFields`](https://www.mongodb.com/docs/reference/operator/aggregation/addFields/#mongodb-pipeline-pipe.-addFields) adds a field to the output containing the total runtime of movies for each year.

The resulting documents must not exceed the [BSON Document Size](https://www.mongodb.com/docs/reference/limits/#mongodb-limit-BSON-Document-Size) limit of 16 mebibytes.

Fourth Stage: - [`$sort`](https://www.mongodb.com/docs/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort) sorts the resulting documents by `_id` in ascending order.

</Tab>

<Tab name="C#">

The C# examples on this page use the `sample_mflix` database from the [Atlas sample datasets](https://www.mongodb.com/docs/atlas/sample-data/). To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see [Get Started](https://www.mongodb.com/docs/drivers/csharp/current/quick-start/) in the MongoDB .NET/C# Driver documentation.

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

`$group`

[Group()](https://mongodb.github.io/mongo-csharp-driver/3.7.0/api/MongoDB.Driver/MongoDB.Driver.PipelineStageDefinitionBuilder.Group.html)

groups documents by the value of their `Rated` field. Each group's rating is shown in a field named `Rating` in each output document. Each output document also contains fields named `TotalRuntime`, `MedianRuntime`, and `NinetiethPercentileRuntime`, which store the total, median, and 90th percentile runtime values for movies in each group.

To use the MongoDB .NET/C# driver to add a `$group` stage to an aggregation pipeline, call the [Group()](https://mongodb.github.io/mongo-csharp-driver/3.7.0/api/MongoDB.Driver/MongoDB.Driver.PipelineStageDefinitionBuilder.Group.html) method on a `PipelineDefinition` object.

The following example creates a pipeline stage that groups documents by the value of their `Rated` field. Each group's rating is shown in a field named `Rating` in each output document. Each output document also contains fields named `TotalRuntime`, `MedianRuntime`, and `NinetiethPercentileRuntime`, which store the total, median, and 90th percentile runtime values for movies in each group.

```csharp
var pipeline = new EmptyPipelineDefinition<Movie>()
    .Group(
        id: m => m.Rated,
        group: g => new
        {
            Rating = g.Key,
            TotalRuntime = g.Sum(m => m.Runtime),
            MedianRuntime = g.Select(m => m.Runtime).Median(),
            NinetiethPercentileRuntime = g.Select(m => m.Runtime).Percentile(new[] { 0.9 })
        }
    );
```

</Tab>

<Tab name="Node.js">

The Node.js examples on this page use the `sample_mflix` database from the [Atlas sample datasets](https://www.mongodb.com/docs/atlas/sample-data/). To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see [Get Started](https://www.mongodb.com/docs/drivers/node/current/get-started/) in the MongoDB Node.js driver documentation.

`$group`

groups documents by the value of their `rated` field. Each output document contains a `rating` field that stores each group's rating. Each output document also contains a field named `totalRuntime` that stores the total runtime of all movies in the group

To use the MongoDB Node.js driver to add a `$group` stage to an aggregation pipeline, use the `$group` operator in a pipeline object.

The following example creates a pipeline stage that groups documents by the value of their `rated` field. Each output document contains a `rating` field that stores each group's rating. Each output document also contains a field named `totalRuntime` that stores the total runtime of all movies in the group. The example then runs the aggregation pipeline:

```javascript
const pipeline = [
  {
    $group: {
      _id: "$rated",
      rating: { $first: "$rated" },
      totalRuntime: { $sum: "$runtime" }
    }
  }
];

const cursor = collection.aggregate(pipeline);
return cursor;
```

</Tab>

</Tabs>

## Learn More

The [Group and Total Data](https://www.mongodb.com/docs/tutorial/aggregation-examples/group-and-total/#std-label-agg-example-group-data) tutorial provides an extensive example of the [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) operator in a common use case.

To learn more about related pipeline stages, see the [`$addFields`](https://www.mongodb.com/docs/reference/operator/aggregation/addFields/#mongodb-pipeline-pipe.-addFields) guide.
