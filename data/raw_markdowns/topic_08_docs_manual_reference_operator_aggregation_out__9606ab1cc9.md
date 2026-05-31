> Source: https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/
> Fetch method: direct_markdown

# $out (aggregation stage)

## Definition

`$out`
Takes the documents returned by the aggregation pipeline and writes them to a specified collection. You can specify the output database.

The `$out` stage must be *the last stage* in the pipeline. The `$out` operator lets the aggregation framework return result sets of any size.

If the collection specified by the `$out` operation already exists, then the `$out` stage atomically replaces the existing collection with the new results collection upon completion of the aggregation. See [Replace Existing Collection](https://www.mongodb.com/docs/reference/operator/aggregation/out/#std-label-replace-existing-collection) for details.

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

- Starting in MongoDB 7.0.3 and 7.1, `$out` can take a document to output to a [time series collection](https://www.mongodb.com/docs/core/timeseries-collections/#std-label-manual-timeseries-landing):

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

  After creating a time series collection, you can modify its granularity using the [`collMod`](https://www.mongodb.com/docs/reference/command/collMod/#mongodb-dbcommand-dbcmd.collMod) method. However, you can only increase the timespan covered by each bucket. You cannot decrease it.

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
  `db`

  </td>
  <td headers="Description">
  The output database name.

  - For a [replica set](https://www.mongodb.com/docs/replication/#std-label-replica-set) or a standalone, if the output database does not exist, `$out` also creates the database.

  </td>
  </tr>
  <tr>
  <td headers="Field">
  `coll`

  </td>
  <td headers="Description">
  The output collection name.

  </td>
  </tr>
  <tr>
  <td headers="Field">
  `timeseries`

  </td>
  <td headers="Description">
  A document that specifies the configuration to use when writing to a time series collection. The `timeField` is required. All other fields are optional.

  </td>
  </tr>
  <tr>
  <td headers="Field">
  `timeField`

  </td>
  <td headers="Description">
  Required when writing to a time series collection. The name of the field which contains the date in each time series document. Documents in a time series collection must have a valid BSON date as the value for the `timeField`.

  </td>
  </tr>
  <tr>
  <td headers="Field">
  `metaField`

  </td>
  <td headers="Description">
  Optional. The name of the field which contains metadata in each time series document. The metadata in the specified field should be data that is used to label a unique series of documents. The metadata should rarely, if ever, change The name of the specified field may not be `_id` or the same as the `timeseries.timeField`. The field can be of any data type.

  Although the `metaField` field is optional, using metadata can improve query optimization. For example, MongoDB automatically [creates a compound index](https://www.mongodb.com/docs/core/timeseries/timeseries-secondary-index/#std-label-timeseries-add-secondary-index) on the `metaField` and `timeField` fields for new collections. If you do not provide a value for this field, the data is bucketed solely based on time.

  </td>
  </tr>
  <tr>
  <td headers="Field">
  `granularity`

  </td>
  <td headers="Description">
  Optional. Do not use if setting `bucketRoundingSeconds` and `bucketMaxSpanSeconds`.

  Possible values are `seconds` (default), `minutes`, and `hours`.

  Set `granularity` to the value that most closely matches the time between consecutive incoming timestamps. This improves performance by optimizing how MongoDB stores data in the collection.

  For more information on granularity and bucket intervals, see [Set Granularity for Time Series Data](https://www.mongodb.com/docs/core/timeseries/timeseries-granularity/#std-label-timeseries-granularity).

  </td>
  </tr>
  <tr>
  <td headers="Field">
  `bucketMaxSpanSeconds`

  </td>
  <td headers="Description">
  Optional. Use with `bucketRoundingSeconds` as an alternative to `granularity`. Sets the maximum time between timestamps in the same bucket.

  Possible values are 1-31536000.

  </td>
  </tr>
  <tr>
  <td headers="Field">
  `bucketRoundingSeconds`

  </td>
  <td headers="Description">
  Optional. Use with `bucketMaxSpanSeconds` as an alternative to `granularity`. Must be equal to `bucketMaxSpanSeconds`.

  When a document requires a new bucket, MongoDB rounds down the document's timestamp value by this interval to set the minimum time for the bucket.

  </td>
  </tr>
  </table>
- You cannot specify a sharded collection as the output collection. The input collection for a pipeline can be sharded. To output to a sharded collection, see [`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge).

- The `$out` operator cannot write results to a [capped collection](https://www.mongodb.com/docs/core/capped-collections/#std-label-manual-capped-collection).

- If you modify a collection with a [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) index, you must first delete and then re-create the search index. Consider using [`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge) instead.

### Comparison with `$merge`

MongoDB provides two stages, [`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge) and `$out`, for writing the results of the aggregation pipeline to a collection. The following summarizes the capabilities of the two stages:

<table>
<tr>
<th id="$out">
`$out`

</th>
<th id="$merge">
[`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge)

</th>
</tr>
<tr>
<td headers="$out">
- Can output to a collection in the same or different database.

</td>
<td headers="$merge">
- Can output to a collection in the same or different database.

</td>
</tr>
<tr>
<td headers="$out">
- Creates a new collection if the output collection does not already exist.

</td>
<td headers="$merge">
- Creates a new collection if the output collection does not already exist.

</td>
</tr>
<tr>
<td headers="$out">
- Replaces the output collection completely if it already exists.

</td>
<td headers="$merge">
- Can incorporate results (insert new documents, merge documents, replace documents, keep existing documents, fail the operation, process documents with a custom update pipeline) into an existing collection.

  Can replace the content of the collection but only if the aggregation results contain a match for all existing documents in the collection.

</td>
</tr>
<tr>
<td headers="$out">
- Cannot output to a sharded collection. Input collection, however, can be sharded.

</td>
<td headers="$merge">
- Can output to a sharded collection. Input collection can also be sharded.

</td>
</tr>
<tr>
<td headers="$out">
- Starting in MongoDB 7.0.3 and 7.1, can output to a time series collection.

</td>
<td headers="$merge">
- Cannot output to a time series collection.

</td>
</tr>
<tr>
<td headers="$out">
- Corresponds to the SQL statements:

  - ```sql
    INSERT INTO T2 SELECT * FROM T1
    ```

  - ```sql
    SELECT * INTO T2 FROM T1
    ```

</td>
<td headers="$merge">
- Corresponds to the SQL statement:

  - ```sql
    MERGE T2 AS TARGET
    USING (SELECT * FROM T1) AS SOURCE
    ON MATCH (T2.ID = SOURCE.ID)
    WHEN MATCHED THEN
      UPDATE SET TARGET.FIELDX = SOURCE.FIELDY
    WHEN NOT MATCHED THEN
      INSERT (FIELDX)
      VALUES (SOURCE.FIELDY)
    ```

  - Create/Refresh Materialized Views

</td>
</tr>
</table>

## Behaviors

### $out Read Operations Run on Secondary Replica Set Members

Starting in MongoDB 5.0, `$out` can run on replica set secondary nodes if all the nodes in cluster have [featureCompatibilityVersion](https://www.mongodb.com/docs/reference/command/setFeatureCompatibilityVersion/#std-label-view-fcv) set to `5.0` or higher and the [Read Preference](https://www.mongodb.com/docs/core/read-preference/) is set to secondary.

Read operations of the `$out` statement occur on the secondary nodes, while the write operations occur only on the primary nodes.

Not all driver versions support targeting of `$out` operations to replica set secondary nodes. Check your [driver](https://www.mongodb.com/docs/drivers/) documentation to see when your driver added support for `$out` running on a secondary.

### Create New Collection

The `$out` operation creates a new collection if one does not already exist.

The collection is not visible until the aggregation completes. If the aggregation fails, MongoDB does not create the collection.

### Replace Existing Collection

If the collection specified by the `$out` operation already exists, then upon completion of the aggregation, the `$out` stage atomically replaces the existing collection with the new results collection. Specifically, the `$out` operation:

1. Creates a temp collection.

2. Copies the indexes from the existing collection to the temp collection.

3. Inserts the documents into the temp collection.

4. Calls the [`renameCollection`](https://www.mongodb.com/docs/reference/command/renameCollection/#mongodb-dbcommand-dbcmd.renameCollection) command with `dropTarget: true` to rename the temp collection to the destination collection.

If specified collection exists and the `$out` operation specifies `timeseries` options, then the following restrictions apply:

1. The existing collection must be a time series collection.

2. The existing collection must not be a view.

3. The `timeseries` options included in the `$out` stage must exactly match those on the existing collection.

The `$out` operation does not change any indexes that existed on the previous collection. If the aggregation fails, the `$out` operation makes no changes to the pre-existing collection.

#### Schema Validation Errors

If your `coll` collection uses [schema validation](https://www.mongodb.com/docs/core/schema-validation/#std-label-schema-validation-overview) and has `validationAction` set to `error`, inserting an invalid document with `$out` throws an error. The `$out` operation makes no changes to the pre-existing collection and documents returned by the aggregation pipeline are not added to the `coll` collection.

### Index Constraints

The pipeline will fail to complete if the documents produced by the pipeline would violate any unique indexes, including the index on the `_id` field of the original output collection.

If the `$out` operation modifies a collection with a [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) index, you must delete and re-create the search index. Consider using [`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge) instead.

### `majority` Read Concern

You can specify [read concern](https://www.mongodb.com/docs/reference/read-concern/#std-label-read-concern) level [`"majority"`](https://www.mongodb.com/docs/reference/read-concern-majority/#mongodb-readconcern-readconcern.-majority-) for an aggregation that includes an [`$out`](https://www.mongodb.com/docs/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out) stage.

### Interaction with `mongodump`

A [`mongodump`](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump) started with [`--oplog`](https://www.mongodb.com/docs/database-tools/mongodump/#std-option-mongodump.--oplog) fails if a client issues an aggregation pipeline that includes `$out` during the dump process. See [`mongodump --oplog`](https://www.mongodb.com/docs/database-tools/mongodump/#std-option-mongodump.--oplog) for more information.

### Restrictions

<table>
<tr>
<th id="Restrictions">
Restrictions

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Restrictions">
[transactions](https://www.mongodb.com/docs/core/transactions/#std-label-transactions)

</td>
<td headers="Description">
An aggregation pipeline cannot use `$out` inside [transactions](https://www.mongodb.com/docs/core/transactions/#std-label-transactions).

</td>
</tr>
<tr>
<td headers="Restrictions">
[view definition](https://www.mongodb.com/docs/core/views/#std-label-views-landing-page)

</td>
<td headers="Description">
The `$out` stage is not allowed as part of a view definition. If the view definition includes nested pipeline (e.g. the view definition includes [`$lookup`](https://www.mongodb.com/docs/reference/operator/aggregation/lookup/#mongodb-pipeline-pipe.-lookup) or [`$facet`](https://www.mongodb.com/docs/reference/operator/aggregation/facet/#mongodb-pipeline-pipe.-facet) stage), this `$out` stage restriction applies to the nested pipelines as well.

</td>
</tr>
<tr>
<td headers="Restrictions">
[`$lookup`](https://www.mongodb.com/docs/reference/operator/aggregation/lookup/#mongodb-pipeline-pipe.-lookup) stage

</td>
<td headers="Description">
You can't include the `$out` stage in the [`$lookup`](https://www.mongodb.com/docs/reference/operator/aggregation/lookup/#mongodb-pipeline-pipe.-lookup) stage's [nested pipeline](https://www.mongodb.com/docs/reference/operator/aggregation/lookup/#std-label-lookup-syntax-let-pipeline).

</td>
</tr>
<tr>
<td headers="Restrictions">
[`$facet`](https://www.mongodb.com/docs/reference/operator/aggregation/facet/#mongodb-pipeline-pipe.-facet) stage

</td>
<td headers="Description">
[`$facet`](https://www.mongodb.com/docs/reference/operator/aggregation/facet/#mongodb-pipeline-pipe.-facet) stage's [nested pipeline](https://www.mongodb.com/docs/reference/operator/aggregation/lookup/#std-label-lookup-syntax-let-pipeline) cannot include the `$out` stage.

</td>
</tr>
<tr>
<td headers="Restrictions">
[`$unionWith`](https://www.mongodb.com/docs/reference/operator/aggregation/unionWith/#mongodb-pipeline-pipe.-unionWith) stage

</td>
<td headers="Description">
[`$unionWith`](https://www.mongodb.com/docs/reference/operator/aggregation/unionWith/#mongodb-pipeline-pipe.-unionWith) stage's [nested pipeline](https://www.mongodb.com/docs/reference/operator/aggregation/unionWith/#std-label-unionWith-pipeline) cannot include the `$out` stage.

</td>
</tr>
<tr>
<td headers="Restrictions">
[`"linearizable"`](https://www.mongodb.com/docs/reference/read-concern-linearizable/#mongodb-readconcern-readconcern.-linearizable-) read concern

</td>
<td headers="Description">
The [`$out`](https://www.mongodb.com/docs/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out) stage cannot be used in conjunction with read concern [`"linearizable"`](https://www.mongodb.com/docs/reference/read-concern-linearizable/#mongodb-readconcern-readconcern.-linearizable-). If you specify [`"linearizable"`](https://www.mongodb.com/docs/reference/read-concern-linearizable/#mongodb-readconcern-readconcern.-linearizable-) read concern for [`db.collection.aggregate()`](https://www.mongodb.com/docs/reference/method/db.collection.aggregate/#mongodb-method-db.collection.aggregate), you cannot include the [`$out`](https://www.mongodb.com/docs/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out) stage in the pipeline.

</td>
</tr>
</table>

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

First Stage (`$group`): - The [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stage groups by the `authors` and uses [`$push`](https://www.mongodb.com/docs/reference/operator/aggregation/push/#mongodb-group-grp.-push) to add the titles to a `books` array field:

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

For a [replica set](https://www.mongodb.com/docs/replication/#std-label-replica-set) or a standalone, if the output database does not exist, `$out` also creates the database.

`$out` can output to a collection in a database different from where the aggregation is run.

The following aggregation operation pivots the data in the `books` collection to have titles grouped by authors and then writes the results to the `authors` collection in the `reporting` database:

```javascript
db.getSiblingDB("test").books.aggregate( [
    { $group : { _id : "$author", books: { $push: "$title" } } },
    { $out : { db: "reporting", coll: "authors" } }
] )
```

First Stage (`$group`): - The [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) stage groups by the `authors` and uses [`$push`](https://www.mongodb.com/docs/reference/operator/aggregation/push/#mongodb-group-grp.-push) to add the titles to a `books` array field:

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

`$out`

[Out()](https://mongodb.github.io/mongo-csharp-driver/3.7.0/api/MongoDB.Driver/MongoDB.Driver.PipelineStageDefinitionBuilder.Out.html)

writes the results of the pipeline into the `movies` collection:

To use the MongoDB .NET/C# driver to add a `$out` stage to an aggregation pipeline, call the [Out()](https://mongodb.github.io/mongo-csharp-driver/3.7.0/api/MongoDB.Driver/MongoDB.Driver.PipelineStageDefinitionBuilder.Out.html) method on a `PipelineDefinition` object.

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

The Node.js examples on this page use the `sample_mflix` database from the [Atlas sample datasets](https://www.mongodb.com/docs/atlas/sample-data/). To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see [Get Started](https://www.mongodb.com/docs/drivers/node/current/get-started/) in the MongoDB Node.js driver documentation.

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
