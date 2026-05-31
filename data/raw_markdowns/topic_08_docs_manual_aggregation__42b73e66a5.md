> Source: https://www.mongodb.com/docs/manual/aggregation/
> Fetch method: direct_markdown

# Aggregation Operations

Aggregation operations process multiple documents and return computed results. You can use aggregation operations to:

- Group values from multiple documents together.

- Perform operations on the grouped data to return a single result.

- Analyze data changes over time.

- Query the most up-to-date version of your data.

By using the built-in aggregation operators in MongoDB, you can perform analytics on your cluster without having to move your data to another platform.

## Get Started

To perform aggregation operations, you can use:

- [Aggregation pipelines](https://www.mongodb.com/docs/aggregation/#std-label-aggregation-pipeline-intro), which are the preferred method for performing aggregations.

- [Single purpose aggregation methods](https://www.mongodb.com/docs/aggregation/#std-label-single-purpose-agg-methods), which are simple but lack the capabilities of an aggregation pipeline.

[run aggregation pipelines in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/agg-pipeline/)You can [run aggregation pipelines in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/agg-pipeline/) for deployments hosted in [MongoDB Atlas](https://www.mongodb.com/docs/atlas).

## Aggregation Pipelines

An aggregation pipeline consists of one or more [stages](https://www.mongodb.com/docs/reference/mql/aggregation-stages/#std-label-aggregation-pipeline-operator-reference) that process documents. These documents can come from a collection, a view, or a specially designed stage.

Each stage performs an operation on the input documents. For example, a stage can [`$filter`](https://www.mongodb.com/docs/reference/operator/aggregation/filter/#mongodb-expression-exp.-filter) documents, [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) documents, and calculate values. The documents that a stage outputs are then passed to the next stage in the pipeline.

An aggregation pipeline can return results for groups of documents. You can also update documents with an aggregation pipeline using the stages shown in [Updates with Aggregation Pipeline](https://www.mongodb.com/docs/tutorial/update-documents-with-aggregation-pipeline/#std-label-updates-agg-pipeline).

Aggregation pipelines run with the [`db.collection.aggregate()`](https://www.mongodb.com/docs/reference/method/db.collection.aggregate/#mongodb-method-db.collection.aggregate) method do not modify documents in a collection, unless the pipeline contains a [`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge) or [`$out`](https://www.mongodb.com/docs/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out) stage.

### Aggregation Pipeline Example

The examples on this page use data from the [sample_mflix sample dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](https://www.mongodb.com/docs/atlas/sample-data/load-sample-data-local/#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

This pipeline finds the top three directors who have directed the most movies in the database.

First, add a [`$match`](https://www.mongodb.com/docs/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match) stage to filter the documents to movies that have directors listed (excluding documents where directors field is null or empty):

```javascript
{
    $match : {
        "directors" : { $exists: true, $ne: null, $not: {$size: 0} }
    }
},

```

The `$match` stage reduces the number of documents in our pipeline by filtering out movies without director information. Next, use [`$unwind`](https://www.mongodb.com/docs/reference/operator/aggregation/unwind/#mongodb-pipeline-pipe.-unwind) to deconstruct the directors array so we can count movies per individual director:

```javascript
{
    $unwind : "$directors"
},

```

Then, [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) the documents by director name and count the number of movies each director has made:

```javascript
{
    $group : {
    _id : "$directors",
    movieCount : {
        $sum: 1
        }
    }
},

```

To find the directors with the most movies, use the [`$sort`](https://www.mongodb.com/docs/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort) stage to sort the remaining documents in descending order by movie count:

```javascript
{
    $sort : {
        movieCount : -1
    }
},

```

After you sort your documents, use the [`$limit`](https://www.mongodb.com/docs/reference/operator/aggregation/limit/#mongodb-pipeline-pipe.-limit) stage to return the top three directors who have directed the most movies:

```javascript
{
    $limit : 3
}

```

The full pipeline is given in this example:

```javascript
db.movies.aggregate(
  [
    {
        $match : {
            "directors" : { $exists: true, $ne: null, $not: {$size: 0} }
        }
    },
    {
        $unwind : "$directors"
    },
    {
        $group : {
        _id : "$directors",
        movieCount : {
            $sum: 1
            }
        }
    },
    {
        $sort : {
            movieCount : -1
        }
    },
    {
        $limit : 3
    }
  ]
)

```

This pipeline returns these results:

```javascript
[
  { _id: 'Woody Allen', movieCount: 40 },
  { _id: 'Martin Scorsese', movieCount: 32 },
  { _id: 'Takashi Miike', movieCount: 31 }
]

```

For runnable examples containing sample input documents, see [Complete Aggregation Pipeline Examples](https://www.mongodb.com/docs/core/aggregation-pipeline/#std-label-aggregation-pipeline-examples).

### Learn More About Aggregation Pipelines

To learn more about aggregation pipelines, see [Aggregation Pipeline](https://www.mongodb.com/docs/core/aggregation-pipeline/#std-label-aggregation-pipeline).

## Single Purpose Aggregation Methods

The single purpose aggregation methods aggregate documents from a single collection. The methods are simple but lack the capabilities of an aggregation pipeline.

<table>
<tr>
<th id="Method">
Method

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Method">
[`db.collection.estimatedDocumentCount()`](https://www.mongodb.com/docs/reference/method/db.collection.estimatedDocumentCount/#mongodb-method-db.collection.estimatedDocumentCount)

</td>
<td headers="Description">
Returns an approximate count of the documents in a collection or a view.

</td>
</tr>
<tr>
<td headers="Method">
[`db.collection.count()`](https://www.mongodb.com/docs/reference/method/db.collection.count/#mongodb-method-db.collection.count)

</td>
<td headers="Description">
Returns a count of the number of documents in a collection or a view.

</td>
</tr>
<tr>
<td headers="Method">
[`db.collection.distinct()`](https://www.mongodb.com/docs/reference/method/db.collection.distinct/#mongodb-method-db.collection.distinct)

</td>
<td headers="Description">
Returns an array of documents that have distinct values for the specified field.

</td>
</tr>
</table>
