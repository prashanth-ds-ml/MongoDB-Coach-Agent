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

- Aggregation pipelines, which are the preferred method for performing aggregations.

- Single purpose aggregation methods, which are simple but lack the capabilities of an aggregation pipeline.

run aggregation pipelines in the UIYou can run aggregation pipelines in the UI for deployments hosted in MongoDB Atlas.

## Aggregation Pipelines

An aggregation pipeline consists of one or more stages that process documents. These documents can come from a collection, a view, or a specially designed stage.

Each stage performs an operation on the input documents. For example, a stage can `$filter` documents, `$group` documents, and calculate values. The documents that a stage outputs are then passed to the next stage in the pipeline.

An aggregation pipeline can return results for groups of documents. You can also update documents with an aggregation pipeline using the stages shown in Updates with Aggregation Pipeline.

Aggregation pipelines run with the `db.collection.aggregate()` method do not modify documents in a collection, unless the pipeline contains a `$merge` or `$out` stage.

### Aggregation Pipeline Example

The examples on this page use data from the sample_mflix sample dataset. For details on how to load this dataset into your self-managed MongoDB deployment, see Load the sample dataset. If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

This pipeline finds the top three directors who have directed the most movies in the database.

First, add a `$match` stage to filter the documents to movies that have directors listed (excluding documents where directors field is null or empty):

```javascript
{
    $match : {
        "directors" : { $exists: true, $ne: null, $not: {$size: 0} }
    }
},

```

The `$match` stage reduces the number of documents in our pipeline by filtering out movies without director information. Next, use `$unwind` to deconstruct the directors array so we can count movies per individual director:

```javascript
{
    $unwind : "$directors"
},

```

Then, `$group` the documents by director name and count the number of movies each director has made:

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

To find the directors with the most movies, use the `$sort` stage to sort the remaining documents in descending order by movie count:

```javascript
{
    $sort : {
        movieCount : -1
    }
},

```

After you sort your documents, use the `$limit` stage to return the top three directors who have directed the most movies:

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

For runnable examples containing sample input documents, see Complete Aggregation Pipeline Examples.

#
