> Source: https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/
> Fetch method: direct_markdown

# $out (aggregation stage)

## Definition

`$out`
Takes the documents returned by the aggregation pipeline and writes them to a specified collection. You can specify the output database.

The `$out` stage must be *the last stage* in the pipeline. The `$out` operator lets the aggregation framework return result sets of any size.

If the collection specified by the `$out` operation already exists, then the `$out` stage atomically replaces the existing collection with the new results collection upon completion of the aggregation. See Replace Existing Collection for details.

## Syntax

The `$out` stage has the following syntax:

- `$out` can take a string to specify only the output collection (i.e. output to a collection in the same database):

  ```javascript
  { $out: "<output-collection>" } // Output collection is in the same database
  ```

- `$out` can take a document to specify the output database as well as the output collection:

  ```javascript
  { $out: { db: "<output-db>", coll: "<output-collection>" } }
  ```

- Starting in MongoDB 7.0.3 and 7.1, `$out` can take a document to output to a time series collection:

  ```javascript
  { $out:
    { db: "<output-db>", coll: "<output-collection>",
      timeseries: {
        timeField: "<field-name>",
        metaField: "<field-name>",
        granularity:  "seconds" || "minutes" || "hours" ,
      }
    }
  }
  ```

  After creating a time series collection, you can modify its granularity using the `collMod` method. However, you can only increase the timespan covered by each bucket. You cannot decrease it.

  | Field | Description |
| --- | --- |
| `db` | The output database name. - For a replica set or a standalone, if the output database does not exist, `$out` also creates the database. |
| `coll` | The output collection name. |
| `timeseries` | A document that specifies the configuration to use when writing to a time series collection. The `timeField` is required. All other fields are optional. |
| `timeField` | Required when writing to a time series collection. The name of the field which contains the date in each time series document. Documents in a time series collection must have a valid BSON date as the value for the `timeField`. |
| `metaField` | Optional. The name of the field which contains metadata in each time series document. The metadata in the specified field should be data that is used to label a unique series of documents. The metadata should rarely, if ever, change The name of the specified field may not be `_id` or the same as the `timeseries.timeField`. The field can be of any data type. Although the `metaField` field is optional, using metadata can improve query optimization. For example, MongoDB automatically creates a compound index on the `metaField` and `timeField` fields for new collections. If you do not provide a value for this field, the data is bucketed solely based on time. |
| `granularity` | Optional. Do not use if setting `bucketRoundingSeconds` and `bucketMaxSpanSeconds`. Possible values are `seconds` (default), `minutes`, and `hours`. Set `granularity` to the value that most closely matches the time between consecutive incoming timestamps. This improves performance by optimizing how MongoDB stores data in the collection. For more information on granularity and bucket intervals, see Set Granularity for Time Series Data. |
| `bucketMaxSpanSeconds` | Optional. Use with `bucketRoundingSeconds` as an alternative to `granularity`. Sets the maximum time between timestamps in the same bucket. Possible values are 1-31536000. |
| `bucketRoundingSeconds` | Optional. Use with `bucketMaxSpanSeconds` as an alternative to `granularity`. Must be equal to `bucketMaxSpanSeconds`. When a document requires a new bucket, MongoDB rounds down the document's timestamp value by this interval to set the minimum time for the bucket. |

- You cannot specify a sharded collection as the output collection. The input collection for a pipeline can be sharded. To output to a sharded collection, see `$merge`.

- The `$out` operator cannot write results to a capped collection.

- If you modify a collection with a MongoDB Search index, you must first delete and then re-create the search index. Consider using `$merge` instead.

### Comparison with `$merge`

MongoDB provides two stages, `$merge` and `$out`, for writing the results of the aggregation pipeline to a collection. The following summarizes the capabilities of the two stages:

| `$out` | `$merge` |
| --- | --- |
| - Can output to a collection in the same or different database. | - Can output to a collection in the same or different database. |
| - Creates a new collection if the output collection does not already exist. | - Creates a new collection if the output collection does not already exist. |
| - Replaces the output collection completely if it already exists. | - Can incorporate results (insert new documents, merge documents, replace documents, keep existing documents, fail the operation, process documents with a custom update pipeline) into an existing collection. Can replace the content of the collection but only if the aggregation results contain a match for all existing documents in the collection. |
| - Cannot output to a sharded collection. Input collection, however, can be sharded. | - Can output to a sharded collection. Input collection can also be sharded. |
| - Starting in MongoDB 7.0.3 and 7.1, can output to a time series collection. | - Cannot output to a time series collection. |
| - Corresponds to the SQL statements: - ```sql INSERT INTO T2 SELECT * FROM T1 ``` - ```sql SELECT * INTO T2 FROM T1 ``` | - Corresponds to the SQL statement: - ```sql MERGE T2 AS TARGET USING (SELECT * FROM T1) AS SOURCE ON MATCH (T2.ID = SOURCE.ID) WHEN MATCHED THEN UPDATE SET TARGET.FIELDX = SOURCE.FIELDY WHEN NOT MATCHED THEN INSERT (FIELDX) VALUES (SOURCE.FIELDY) ``` - Create/Refresh Materialized Views |

## Behaviors

### $out Read Operations Run on Secondary Replica Set Members

Starting in MongoDB 5.0, `$out` can run on replica set secondary nodes if all the nodes in cluster have featureCompatibilityVersion set to `5.0` or higher and the Read Preference is set to secondary.

Read operations of the `$out` statement occur on the secondary nodes, while the write operations occur only on the primary nodes.

Not all driver versions support targeting of `$out` operations to replica set secondary nodes. Check your driver documentation to see when your driver added support for `$out` running on a secondary.

### Create New Collection

The `$out` operation creates a new collection if one does not already exist.

The collection is not visible until the aggregation completes. If the aggregation fails, MongoDB does not create the collection.

### Replace Existing Collection

If the collection specified by the `$out` operation already exists, then upon completion of the aggregation, the `$out` stage atomically replaces the existing collection with the new results collection. Specifically, the `$out` operation:

1. Creates a temp collection.

2. Copies the indexes from the existing collection to the temp collection.

3. Inserts the documents into the temp collection.

4. Calls the `renameCollection` command with `dropTarget: true` to rename the temp collection to the destination collection.

If specified collection exists and the `$out` operation specifies `timeseries` options, then the following restrictions apply:

1. The existing collection must be a time series collection.

2. The existing collection must not be a view.

3. The `timeseries` options included in the `$out` stage must exactly match those on the existing collection.

The `$out` operation does not change any indexes that existed on the previous collection. If the aggregation fails, the `$out` operation makes no changes to the pre-existing collection.

#### Schema Validation Errors

If your `coll` collection uses schema validation and has `validationAction` set to `error`, inserting an invalid document with `$out` throws an error. The `$out` operation makes no changes to the pre-existing collection and documents returned by the aggregation pipeline are not added to the `coll` collection.

### Index Constraints

The pipeline will fail to complete if the documents produced by the pipeline would violate any unique indexes, including the index on the `_id` field of the original output collection.

If the `$out` operation modifies a collection with a MongoDB Search index, you must delete and re-create the search index. Consider using `$merge` instead.

### `majority` Read Concern

You can specify read concern level `"majority"` for an aggregation that includes an `$out` stage.

### Interaction with `mongodump`

A `mongodump` started with `--oplog` fails if a client issues an aggregation pipeline that includes `$out` during the dump process. See `mongodump --oplog` for more information.

### Restrictions

| Restrictions | Description |
| --- | --- |
| transactions | An aggregation pipeline cannot use `$out` inside transactions. |
| view definition | The `$out` stage is not allowed as part of a view definition. If the view definition includes nested pipeline (e.g. the view definition includes `$lookup` or `$facet` stage), this `$out` stage restriction applies to the nested pipelines as well. |
| `$lookup` stage | You can't include the `$out` stage in the `$lookup` stage's nested pipeline. |
| `$facet` stage | `$facet` stage's nested pipeline cannot include the `$out` stage. |
| `$unionWith` stage | `$unionWith` stage's nested pipeline cannot include the `$out` stage. |
| `"linearizable"` read concern | The `$out` stage cannot be used in conjunction with read concern `"linearizable"`. If you specify `"linearizable"` read concern for `db.collection.aggregate()`, you cannot include the `$out` stage in the pipeline. |

## Examples

<Tabs>

<Tab name="MongoDB Shell">

In the `test` database, create a collection `books` with the following documents:

```javascript
db.getSiblingDB("test").books.insertMany([
   { "_id" : 8751, "title" : "The Banquet", "author" : "Dante", "copies" : 2 },
   { "_id" : 8752, "title" : "Divine Comedy", "author" : "Dante", "copies" : 1 },
   { "_id" : 8645, "title" : "Eclogues", "author" : "Dante", "copies" : 2 },
   { "_id" : 7000, "title" : "The Odyssey", "author" : "Homer", "copies" : 10 },
   { "_id" : 7020, "title" : "Iliad", "author" : "Homer", "copies" : 10 }
])
```

If the `test` database does not already exist, the insert operation creates the database as well as the `books` collection.

### Output to Same Database

The following aggregation operation pivots the data in the `books` collection in the `test` database to have titles grouped by authors and then writes the results to the `authors` collection, also in the `test` database.

```javascript
db.getSiblingDB("test").books.aggregate( [
    { $group : { _id : "$author", books: { $push: "$title" } } },
    { $out : "authors" }
] )
```

First Stage (`$group`): - The `$group` stage groups by the `authors` and uses `$push` to add the titles to a `books` array field:

```javascript
{ "_id" : "Dante", "books" : [ "The Banquet", "Divine Comedy", "Eclogues" ] }
{ "_id" : "Homer", "books" : [ "The Odyssey", "Iliad" ] }
```

Second Stage (`$out`): - The `$out` stage outputs the documents to the `authors` collection in the `test` database.

To view the documents in the output collection, run the following operation:

```javascript
db.getSiblingDB("test").authors.find()
```

The collection contains the following documents:

```javascript
{ "_id" : "Homer", "books" : [ "The Odyssey", "Iliad" ] }
{ "_id" : "Dante", "books" : [ "The Banquet", "Divine Comedy", "Eclogues" ] }
```

### Output to a Different Database

For a replica set or a standalone, if the output database does not exist, `$out` also creates the database.

`$out` can output to a collection in a database different from where the aggregation is run.

The following aggregation operation pivots the data in the `books` collection to have titles grouped by authors and then writes the results to the `authors` collection in the `reporting` database:

```javascript
db.getSiblingDB("test").books.aggregate( [
    { $group : { _id : "$author", books: { $push: "$title" } } },
    { $out : { db: "reporting", coll: "authors" } }
] )
```

First Stage (`$group`): - The `$group` stage groups by the `authors` and uses `$push` to add the titles to a `books` array field:

```javascript
{ "_id" : "Dante", "books" : [ "The Banquet", "Divine Comedy", "Eclogues" ] }
{ "_id" : "Homer", "books" : [ "The Odyssey", "Iliad" ] }
```

Second Stage (`$out`): - The `$out` stage outputs the documents to the `authors` collection in the `reporting` database.

To view the documents in the output collection, run the following operation:

```javascript
db.getSiblingDB("reporting").authors.find()
```

The collection contains the following documents:

```javascript
{ "_id" : "Homer", "books" : [ "The Odyssey", "Iliad" ] }
{ "_id" : "Dante", "books" : [ "The Banquet", "Divine Comedy", "Eclogues" ] }
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

`$out`

Out()

writes the results of the pipeline into the `movies` collection:

To use the MongoDB .NET/C# driver to add a `$out` stage to an aggregation pipeline, call the Out() method on a `PipelineDefinition` object.

The following example creates a pipeline stage that writes the results of the pipeline into the `movies` collection:

```csharp
var movieCollection = client
    .GetDatabase("sample_mflix")
    .GetCollection<Movie>("movies");

var pipeline = new EmptyPipelineDefinition<Movie>()
    .Out(movieCollection);
```

</Tab>

<Tab name="Node.js">

The Node.js examples on this page use the `sample_mflix` database from the Atlas sample datasets. To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see Get Started in the MongoDB Node.js driver documentation.

`$out`

writes the results of the pipeline into the `movies` collection

To use the MongoDB Node.js driver to add a `$out` stage to an aggregation pipeline, use the `$out` operator in a pipeline object.

The following example creates a pipeline stage that writes the results of the pipeline into the `movies` collection. The example then runs the aggregation pipeline:

```javascript
const pipeline = [{ $out: { db: "sample_mflix", coll: "movies" } }];

const cursor = collection.aggregate(pipeline);
return cursor;
```

</Tab>

</Tabs>
