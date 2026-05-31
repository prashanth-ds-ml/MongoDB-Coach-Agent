> Source: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
> Fetch method: direct_markdown

# Aggregation Pipeline

An aggregation pipeline consists of one or more stages that process documents. These documents can come from a collection, a view, or a specially designed stage.

Each stage performs an operation on the input documents. For example, a stage can `$filter` documents, `$group` documents, and calculate values. The documents that a stage outputs are then passed to the next stage in the pipeline.

An aggregation pipeline can return results for groups of documents. You can also update documents with an aggregation pipeline using the stages shown in Updates with Aggregation Pipeline.

Aggregation pipelines run with the `db.collection.aggregate()` method do not modify documents in a collection, unless the pipeline contains a `$merge` or `$out` stage.

run aggregation pipelines in the UIYou can run aggregation pipelines in the UI for deployments hosted in MongoDB Atlas.

When you run aggregation pipelines on MongoDB Atlas deployments in the MongoDB Atlas UI, you can preview the results at each stage.

## Complete Aggregation Pipeline Examples

The Complete Aggregation Pipeline Tutorials section contains complete tutorials that provide detailed explanations of common aggregation tasks in a step-by-step format. The tutorials include examples for MongoDB Shell and each of the official MongoDB drivers.

## Additional Aggregation Pipeline Stage Details

An aggregation pipeline consists of one or more stages that process documents:

- A stage does not have to output one document for every input document. For example, some stages may produce new documents or filter out documents.

- The same stage can appear multiple times in the pipeline with these stage exceptions: `$out`, `$merge`, and `$geoNear`.

For all aggregation stages, see Aggregation Stages.

### Expressions and Operators

Some aggregation pipeline stages accept expressions. Operators calculate values based on input expressions.

In the MongoDB Query Language, you can build expressions from the following components:

| Component | Example |
| --- | --- |
| Constants | `3` |
| Operators | `$add` |
| Field path expressions | `"$<path.to.field>"` |
For example, `{ $add: [ 3, "$inventory.total" ] }` is an expression that consists of the `$add` operator and two operands:

- The constant `3`

- The field path expression
  `"$inventory.total"`

The expression returns the result of adding 3 to the value at path `inventory.total` of the input document.

### Field Paths

Field path expressions are used to access fields in input documents. To specify a field path, prefix the field name or the dotted field path (if the field is in an embedded document) with a dollar sign `$`. For example, `"$user"` to specify the field path for the `user` field or `"$user.name"` to specify the field path to the embedded `"user.name"` field.

`"$<field>"` is equivalent to `"$$CURRENT.<field>"` where the `CURRENT` is a system variable that defaults to the root of the current object, unless stated otherwise in specific stages.

For more information and examples, see Field Paths.

## Run an Aggregation Pipeline

To run an aggregation pipeline, use:

- `db.collection.aggregate()` or

- `aggregate`

## Update Documents Using an Aggregation Pipeline

To update documents with an aggregation pipeline, use:

| Command | `mongosh` Methods |
| --- | --- |
| `findAndModify` | db.collection.findOneAndUpdate()db.collection.findAndModify() |
| `update` | db.collection.updateOne()db.collection.updateMany() Bulk.find.update() Bulk.find.updateOne() Bulk.find.upsert() |

## Other Considerations

### Aggregation Pipeline Limitations

An aggregation pipeline has limitations on the value types and the result size. See Aggregation Pipeline Limits.

### Aggregation Pipelines and Sharded Collections

An aggregation pipeline supports operations on sharded collections. See Aggregation Pipeline and Sharded Collections.

### Aggregation Pipelines as an Alternative to Map-Reduce

Starting in MongoDB 5.0, map-reduce is deprecated:

- Instead of map-reduce, you should use an aggregation pipeline. Aggregation pipelines provide better performance and usability than map-reduce.

- You can rewrite map-reduce operations using aggregation pipeline stages, such as `$group`, `$merge`, and others.

- For map-reduce operations that require custom functionality, you can use the `$accumulator` and `$function` aggregation operators. You can use those operators to define custom aggregation expressions in JavaScript.

For examples of aggregation pipeline alternatives to map-reduce, see:

- Map-Reduce to Aggregation Pipeline

- Map-Reduce Examples

### Accessing Array Element Indexes in $map, $filter, and $reduce

MongoDB 8.3 improves access to array element indexes in `$map`, `$filter`, and `$reduce` aggregation expressions. You can use the new `arrayIndexAs` field to set a variable to store the index of an array element. You can also use the new `$$IDX` aggregation system variable to access the index of the current array element if you omit `arrayIndexAs`.
