> Source: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
> Fetch method: direct_markdown

# Aggregation Pipeline

An aggregation pipeline consists of one or more [stages](https://www.mongodb.com/docs/reference/mql/aggregation-stages/#std-label-aggregation-pipeline-operator-reference) that process documents. These documents can come from a collection, a view, or a specially designed stage.

Each stage performs an operation on the input documents. For example, a stage can [`$filter`](https://www.mongodb.com/docs/reference/operator/aggregation/filter/#mongodb-expression-exp.-filter) documents, [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group) documents, and calculate values. The documents that a stage outputs are then passed to the next stage in the pipeline.

An aggregation pipeline can return results for groups of documents. You can also update documents with an aggregation pipeline using the stages shown in [Updates with Aggregation Pipeline](https://www.mongodb.com/docs/tutorial/update-documents-with-aggregation-pipeline/#std-label-updates-agg-pipeline).

Aggregation pipelines run with the [`db.collection.aggregate()`](https://www.mongodb.com/docs/reference/method/db.collection.aggregate/#mongodb-method-db.collection.aggregate) method do not modify documents in a collection, unless the pipeline contains a [`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge) or [`$out`](https://www.mongodb.com/docs/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out) stage.

[run aggregation pipelines in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/agg-pipeline/)You can [run aggregation pipelines in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/agg-pipeline/) for deployments hosted in [MongoDB Atlas](https://www.mongodb.com/docs/atlas).

When you run aggregation pipelines on MongoDB Atlas deployments in the MongoDB Atlas UI, you can preview the results at each stage.

## Complete Aggregation Pipeline Examples

The [Complete Aggregation Pipeline Tutorials](https://www.mongodb.com/docs/tutorial/aggregation-complete-examples/#std-label-aggregation-complete-examples) section contains complete tutorials that provide detailed explanations of common aggregation tasks in a step-by-step format. The tutorials include examples for MongoDB Shell and each of the [official MongoDB drivers](https://www.mongodb.com/docs/drivers/).

## Additional Aggregation Pipeline Stage Details

An aggregation pipeline consists of one or more [stages](https://www.mongodb.com/docs/reference/mql/aggregation-stages/#std-label-aggregation-pipeline-operator-reference) that process documents:

- A stage does not have to output one document for every input document. For example, some stages may produce new documents or filter out documents.

- The same stage can appear multiple times in the pipeline with these stage exceptions: [`$out`](https://www.mongodb.com/docs/reference/operator/aggregation/out/#mongodb-pipeline-pipe.-out), [`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge), and [`$geoNear`](https://www.mongodb.com/docs/reference/operator/aggregation/geoNear/#mongodb-pipeline-pipe.-geoNear).

For all aggregation stages, see [Aggregation Stages](https://www.mongodb.com/docs/reference/mql/aggregation-stages/#std-label-aggregation-pipeline-operator-reference).

### Expressions and Operators

Some aggregation pipeline stages accept [expressions](https://www.mongodb.com/docs/reference/glossary/#std-term-expression). Operators calculate values based on input expressions.

In the MongoDB Query Language, you can build expressions from the following components:

<table>
<tr>
<th id="Component">
Component

</th>
<th id="Example">
Example

</th>
</tr>
<tr>
<td headers="Component">
Constants

</td>
<td headers="Example">
`3`

</td>
</tr>
<tr>
<td headers="Component">
Operators

</td>
<td headers="Example">
[`$add`](https://www.mongodb.com/docs/reference/operator/aggregation/add/#mongodb-expression-exp.-add)

</td>
</tr>
<tr>
<td headers="Component">
Field path expressions

</td>
<td headers="Example">
`"$<path.to.field>"`

</td>
</tr>
</table>For example, `{ $add: [ 3, "$inventory.total" ] }` is an expression that consists of the `$add` operator and two operands:

- The constant `3`

- The [field path expression](https://www.mongodb.com/docs/core/aggregation-pipeline/#std-label-agg-quick-ref-field-paths)
  `"$inventory.total"`

The expression returns the result of adding 3 to the value at path `inventory.total` of the input document.

### Field Paths

[Field path](https://www.mongodb.com/docs/reference/glossary/#std-term-field-path) expressions are used to access fields in input documents. To specify a field path, prefix the field name or the [dotted field path](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) (if the field is in an embedded document) with a dollar sign `$`. For example, `"$user"` to specify the field path for the `user` field or `"$user.name"` to specify the field path to the embedded `"user.name"` field.

`"$<field>"` is equivalent to `"$$CURRENT.<field>"` where the [`CURRENT`](https://www.mongodb.com/docs/reference/aggregation-variables/#mongodb-variable-variable.CURRENT) is a system variable that defaults to the root of the current object, unless stated otherwise in specific stages.

For more information and examples, see [Field Paths](https://www.mongodb.com/docs/core/field-paths/#std-label-agg-field-paths).

## Run an Aggregation Pipeline

To run an aggregation pipeline, use:

- [`db.collection.aggregate()`](https://www.mongodb.com/docs/reference/method/db.collection.aggregate/#mongodb-method-db.collection.aggregate) or

- [`aggregate`](https://www.mongodb.com/docs/reference/command/aggregate/#mongodb-dbcommand-dbcmd.aggregate)

## Update Documents Using an Aggregation Pipeline

To update documents with an aggregation pipeline, use:

<table>
<tr>
<th id="Command">
Command

</th>
<th id="mongosh%20Methods">
`mongosh` Methods

</th>
</tr>
<tr>
<td headers="Command">
[`findAndModify`](https://www.mongodb.com/docs/reference/command/findAndModify/#mongodb-dbcommand-dbcmd.findAndModify)

</td>
<td headers="mongosh%20Methods">
[db.collection.findOneAndUpdate()](https://www.mongodb.com/docs/reference/method/db.collection.findOneAndUpdate/#std-label-findOneAndUpdate-agg-pipeline)[db.collection.findAndModify()](https://www.mongodb.com/docs/reference/method/db.collection.findAndModify/#std-label-findAndModify-agg-pipeline)

</td>
</tr>
<tr>
<td headers="Command">
[`update`](https://www.mongodb.com/docs/reference/command/update/#mongodb-dbcommand-dbcmd.update)

</td>
<td headers="mongosh%20Methods">
[db.collection.updateOne()](https://www.mongodb.com/docs/reference/method/db.collection.updateOne/#std-label-updateOne-example-agg)[db.collection.updateMany()](https://www.mongodb.com/docs/reference/method/db.collection.updateMany/#std-label-updateMany-example-agg)[Bulk.find.update()](https://www.mongodb.com/docs/reference/method/Bulk.find.update/#std-label-example-bulk-find-update-agg)[Bulk.find.updateOne()](https://www.mongodb.com/docs/reference/method/Bulk.find.updateOne/#std-label-example-bulk-find-update-one-agg)[Bulk.find.upsert()](https://www.mongodb.com/docs/reference/method/Bulk.find.upsert/#std-label-bulk-find-upsert-update-agg-example)

</td>
</tr>
</table>

## Other Considerations

### Aggregation Pipeline Limitations

An aggregation pipeline has limitations on the value types and the result size. See [Aggregation Pipeline Limits](https://www.mongodb.com/docs/core/aggregation-pipeline-limits/).

### Aggregation Pipelines and Sharded Collections

An aggregation pipeline supports operations on sharded collections. See [Aggregation Pipeline and Sharded Collections](https://www.mongodb.com/docs/core/aggregation-pipeline-sharded-collections/#std-label-aggregation-pipeline-sharded-collection).

### Aggregation Pipelines as an Alternative to Map-Reduce

Starting in MongoDB 5.0, [map-reduce](https://www.mongodb.com/docs/core/map-reduce/#std-label-map-reduce) is deprecated:

- Instead of [map-reduce](https://www.mongodb.com/docs/core/map-reduce/#std-label-map-reduce), you should use an [aggregation pipeline](https://www.mongodb.com/docs/core/aggregation-pipeline/#std-label-aggregation-pipeline). Aggregation pipelines provide better performance and usability than map-reduce.

- You can rewrite map-reduce operations using [aggregation pipeline stages](https://www.mongodb.com/docs/reference/mql/aggregation-stages/#std-label-aggregation-pipeline-operator-reference), such as [`$group`](https://www.mongodb.com/docs/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group), [`$merge`](https://www.mongodb.com/docs/reference/operator/aggregation/merge/#mongodb-pipeline-pipe.-merge), and others.

- For map-reduce operations that require custom functionality, you can use the [`$accumulator`](https://www.mongodb.com/docs/reference/operator/aggregation/accumulator/#mongodb-group-grp.-accumulator) and [`$function`](https://www.mongodb.com/docs/reference/operator/aggregation/function/#mongodb-expression-exp.-function) aggregation operators. You can use those operators to define custom aggregation expressions in JavaScript.

For examples of aggregation pipeline alternatives to map-reduce, see:

- [Map-Reduce to Aggregation Pipeline](https://www.mongodb.com/docs/reference/map-reduce-to-aggregation-pipeline/#std-label-map-reduce-to-agg-pipeline)

- [Map-Reduce Examples](https://www.mongodb.com/docs/tutorial/map-reduce-examples/#std-label-map-reduce-examples)

### Accessing Array Element Indexes in $map, $filter, and $reduce

MongoDB 8.3 improves access to array element indexes in [`$map`](https://www.mongodb.com/docs/reference/operator/aggregation/map/#mongodb-expression-exp.-map), [`$filter`](https://www.mongodb.com/docs/reference/operator/aggregation/filter/#mongodb-expression-exp.-filter), and [`$reduce`](https://www.mongodb.com/docs/reference/operator/aggregation/reduce/#mongodb-expression-exp.-reduce) aggregation expressions. You can use the new `arrayIndexAs` field to set a variable to store the index of an array element. You can also use the new [`$$IDX`](https://www.mongodb.com/docs/reference/aggregation-variables/#mongodb-variable-variable.IDX) aggregation system variable to access the index of the current array element if you omit `arrayIndexAs`.

## Learn More

To learn more about aggregation pipelines, see:

- [Expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expression-operators)

- [Aggregation Stages](https://www.mongodb.com/docs/reference/mql/aggregation-stages/#std-label-aggregation-pipeline-operator-reference)
