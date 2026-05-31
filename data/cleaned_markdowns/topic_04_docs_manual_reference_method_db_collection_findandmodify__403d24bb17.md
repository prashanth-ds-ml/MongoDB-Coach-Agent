> Source: https://www.mongodb.com/docs/manual/reference/method/db.collection.findAndModify/
> Fetch method: direct_markdown

# db.collection.findAndModify() (mongosh method)

Use `findOneAndUpdate()`, `findOneAndDelete()`, or `findOneAndReplace()`   instead.

## Definition

`db.collection.findAndModify(document)`
`findAndModify` commandUpdates and returns a single document. By default, the returned document does not include the modifications made on the update. To return the document with the modifications made on the update, use the `new` option.

## Syntax

The `findAndModify()` method has the following form:

```none
db.collection.findAndModify({
    query: <document>,
    sort: <document>,
    remove: <boolean>,
    update: <document or aggregation pipeline>,
    new: <boolean>,
    fields: <document>,
    upsert: <boolean>,
    bypassDocumentValidation: <boolean>,
    writeConcern: <document>,
    maxTimeMS: <integer>,
    collation: <document>,
    arrayFilters: [ <filterdocument1>, ... ],
    let: <document> // Added in MongoDB 5.0
});
```

### Parameters

The `db.collection.findAndModify()` method takes a document parameter with the following embedded document fields:

`db.collection.findAndModify()`| Parameter | Type | Description |
| --- | --- | --- |
| `query` | document | Optional. The selection criteria for the modification. The `query` field employs the same query selectors as used in the `db.collection.find()` method. Although the query may match multiple documents, `db.collection.findAndModify()` **will only select one document to modify**. If unspecified, defaults to an empty document. If the query argument is not a document, the operation errors. |
| `sort` | document | Optional. Determines which document the operation updates if the query selects multiple documents. `db.collection.findAndModify()` updates the first document in the sort order specified by this argument. If the sort argument is not a document, the operation errors. MongoDB does not store documents in a collection in a particular order. When sorting on a field which contains duplicate values, documents containing those values may be returned in any order. The `$sort` operation is not a "stable sort," which means that documents with equivalent sort keys are not guaranteed to remain in the same relative order in the output as they were in the input. If the field specified in the sort criteria does not exist in two documents, then the value on which they are sorted is the same. The two documents may be returned in any order. If consistent sort order is desired, include at least one field in your sort that contains unique values. The easiest way to guarantee this is to include the `_id` field in your sort query. See Sort Consistency for more information. |
| `remove` | boolean | Must specify either the `remove` or the `update` field. Removes the document specified in the `query` field. Set this to `true` to remove the selected document . The default is `false`. |
| `update` | document or array | Must specify either the `remove` or the `update` field. Performs an update of the selected document. - If passed a document with update operator expressions, `db.collection.findAndModify()` performs the specified modification. - If passed a replacement document `{ <field1>: <value1>, ...}`, the `db.collection.findAndModify()` performs a replacement. - If passed an aggregation pipeline `[ <stage1>, <stage2>, ... ]`, `db.collection.findAndModify()` updates the document per the pipeline. The pipeline can consist of the following stages: - `$addFields` and its alias `$set` - `$project` and its alias `$unset` - `$replaceRoot` and its alias `$replaceWith` |
| `new` | boolean | Optional. When `true`, returns the updated document rather than the original. The default is `false`. |
| `fields` | document | Optional. A subset of fields to return. The `fields` document specifies an inclusion of a field with `1`, as in: `fields: { <field1>: 1, <field2>: 1, ... }`. If the `fields` argument is not a document, the operation errors. For more information on projection, see `fields` Projection. |
| `upsert` | boolean | Optional. Used in conjunction with the `update` field. When `true`, `findAndModify()` either: - Creates a new document if no documents match the `query`. For more details see upsert behavior. - Updates a single document that matches the `query`. To avoid multiple upserts, ensure that the `query` field(s) are uniquely indexed. See Upsert with Unique Index for an example. Defaults to `false`, which does *not* insert a new document when no match is found. |
| `bypassDocumentValidation` | boolean | Optional. Enables `db.collection.findAndModify()` to bypass schema validation during the operation. This lets you update documents that do not meet the validation requirements. |
| `writeConcern` | document | Optional. A document expressing the write concern. Omit to use the default write concern. Do not explicitly set the write concern for the operation if run in a transaction. To use write concern with transactions, see Transactions and Write Concern. |
| `maxTimeMS` | non-negative integer | Optional. Specifies a time limit in milliseconds. If you do not specify a value for `maxTimeMS`, operations will not time out. A value of `0` explicitly specifies the default unbounded behavior. MongoDB terminates operations that exceed their allotted time limit using the same mechanism as `db.killOp()`. MongoDB only terminates an operation at one of its designated interrupt points. |
| `collation` | document | Optional. Specifies the collation to use for the operation. Collation allows users to specify language-specific rules for string comparison, such as rules for lettercase and accent marks. The collation option has the following syntax: ```javascript collation: { locale: <string>, caseLevel: <boolean>, caseFirst: <string>, strength: <int>, numericOrdering: <boolean>, alternate: <string>, maxVariable: <string>, backwards: <boolean> } ``` When specifying collation, the `locale` field is mandatory; all other collation fields are optional. For descriptions of the fields, see Collation Document. If the collation is unspecified but the collection has a default collation (see `db.createCollection()`), the operation uses the collation specified for the collection. If no collation is specified for the collection or for the operations, MongoDB uses the simple binary comparison used in prior versions for string comparisons. You cannot specify multiple collations for an operation. For example, you cannot specify different collations per field, or if performing a find with a sort, you cannot use one collation for the find and another for the sort. |
| `arrayFilters` | array | Optional. An array of filter documents that determine which array elements to modify for an update operation on an array field. In the update document, use the [`$[<identifier>]`](https://www.mongodb.com/docs/reference/operator/update/positional-filtered/#mongodb-update-up.---identifier--) filtered positional operator to define an identifier, which you then reference in the array filter documents. You cannot have an array filter document for an identifier if the identifier is not included in the update document. The `<identifier>` must begin with a lowercase letter and contain only alphanumeric characters. You can include the same identifier multiple times in the update document; however, for each distinct identifier (`$[identifier]`) in the update document, you must specify **exactly one** corresponding array filter document. That is, you cannot specify multiple array filter documents for the same identifier. For example, if the update statement includes the identifier `x` (possibly multiple times), you cannot specify the following for `arrayFilters` that includes 2 separate filter documents for `x`: ```javascript // INVALID [ { "x.a": { $gt: 85 } }, { "x.b": { $gt: 80 } } ] ``` However, you can specify compound conditions on the same identifier in a single filter document, such as in the following examples: ```javascript // Example 1 [ { $or: [{"x.a": {$gt: 85}}, {"x.b": {$gt: 80}}] } ] // Example 2 [ { $and: [{"x.a": {$gt: 85}}, {"x.b": {$gt: 80}}] } ] // Example 3 [ { "x.a": { $gt: 85 }, "x.b": { $gt: 80 } } ] ``` For examples, see Specify `arrayFilters` for an Array Update Operations. `arrayFilters` is not available for updates that use an aggregation pipeline. |
| let | document | Optional. Specifies a document with a list of variables. This allows you to improve command readability by separating the variables from the query text. The document syntax is: ```javascript { <variable_name_1>: <expression_1>, ..., <variable_name_n>: <expression_n> } ``` The variable is set to the value returned by the expression, and cannot be changed afterwards. To access the value of a variable in the command, use the double dollar sign prefix (`$$`) together with your variable name in the form `$$<variable_name>`. For example: `$$targetTotal`. To use a variable to filter results, you must access the variable within the `$expr` operator. For a complete example using `let` and variables, see Use Variables in `let`. |

## Return Data

For remove operations, if the query matches a document, `findAndModify()` returns the removed document. If the query does not match a document to remove, `findAndModify()` returns `null`.

For update operations, `findAndModify()` returns one of the following:

- If the `new` parameter is not set or is `false`:

  - the pre-modification document if the query matches a document;

  - otherwise, `null`.

- If `new` is `true`:

  - the updated document if the query returns a match;

  - the inserted document if `upsert: true` and no document matches the query;

  - otherwise, `null`.

## Behavior

### Performance

`findAndModify()`Retryable writes require the `findAndModify()` method to copy the entire document into a special side collection for each node in a replica set before it performs the update. This can make `findAndModify()` an expensive operation when dealing with large documents or large replica sets.

To update the first document in a user-defined ordering with better performance, use the `db.collection.updateOne()` method with the `sort` option.

### `fields` Projection

As part of making `find()` and `findAndModify()` projection consistent with aggregation's `$project` stage,

- The `find()` and `findAndModify()` projection can accept aggregation expressions and syntax.

- MongoDB enforces additional restrictions with regards to projections. See Projection Restrictions for details.

The `fields` option takes a document in the following form:

```javascript
{ field1: <value>, field2: <value> ... }
```

| Projection | Description |
| --- | --- |
| `<field>: <1 or true>` | Specifies the inclusion of a field. If you specify a non-zero integer for the projection value, the operation treats the value as `true`. |
| `<field>: <0 or false>` | Specifies the exclusion of a field. |
| `"<field>.$": <1 or true>` | Uses the `$` array projection operator to return the first element that matches the query condition on the array field. If you specify a non-zero integer for the projection value, the operation treats the value as `true`. Not available for views. |
| `<field>: <array projection>` | Uses the array projection operators (`$elemMatch`, `$slice`) to specify the array elements to include. Not available for views. |
| `<field>: <aggregation expression>` | Specifies the value of the projected field. With the use of aggregation expressions and syntax, including the use of literals and aggregation variables, you can project new fields or project existing fields with new values. - If you specify a non-numeric, non-boolean literal (such as a literal string or an array or an operator expression) for the projection value, the field is projected with the new value, for example: - `{ field: [ 1, 2, 3, "$someExistingField" ] }` - `{ field: "New String Value" }` - `{ field: { status: "Active", total: { $sum: "$existingArray" } } }` - To project a literal value for a field, use the `$literal` aggregation expression, for example: - `{ field: { $literal: 5 } }` - `{ field: { $literal: true } }` - `{ field: { $literal: { fieldWithValue0: 0, fieldWithValue1: 1 } } }` |
#### Embedded Field Specification

For fields in an embedded documents, you can specify the field using either:

- dot notation, for example `"field.nestedfield": <value>`

- nested form, for example `{ field: { nestedfield: <value> } }`

#### `_id` Field Projection

The `_id` field is included in the returned documents by default unless you explicitly specify `_id: 0` in the projection to suppress the field.

#### Inclusion or Exclusion

A `projection` *cannot* contain *both* include and exclude specifications, with the exception of the `_id` field:

- In projections that *explicitly include* fields, the `_id` field is the only field that you can *explicitly exclude*.

- In projections that *explicitly excludes* fields, the `_id` field is the only field that you can *explicitly include*; however, the `_id` field is included by default.

For more information on projection, see also:

- Project Fields to Return from Query

### Upsert with Unique Index

Upserts can create duplicate documents, unless there is a unique index to prevent duplicates.

Consider an example where no document with the name `Andy` exists and multiple clients issue the following command at roughly the same time:

```javascript
db.people.findAndModify(
   {
     query: { name: "Andy" },
     update: { $inc: { score: 1 } },
     upsert: true
   }
)
```

If all `findOneAndUpdate()` operations finish the query phase before any client successfully inserts data, **and** there is no unique index on the `name` field, each `findOneAndUpdate()` operation may result in an insert, creating multiple documents with `name: Andy`.

A unique index on the `name` field ensures that only one document is created. With a unique index in place, the multiple `findOneAndUpdate()` operations now exhibit the following behavior:

- Exactly one `findOneAndUpdate()` operation will successfully insert a new document.

- Other `findOneAndUpdate()` operations either update the newly-inserted document or fail due to a unique key collision.

  In order for other `findOneAndUpdate()` operations to update the newly-inserted document, **all** of the following conditions must be met:

  - The target collection has a unique index that would cause a duplicate key error.

  - The update operation is not `updateMany` or `multi` is `false`.

  - The update match condition is either:

    - A single equality predicate. For example `{ "fieldA" : "valueA" }`

    - A logical AND of equality predicates. For example `{ "fieldA" : "valueA", "fieldB" : "valueB" }`

  - The fields in the equality predicate match the fields in the unique index key pattern.

  - The update operation does not modify any fields in the unique index key pattern.

The following table shows examples of `upsert` operations that, when a key collision occurs, either result in an update or fail.

| Unique Index Key Pattern | Update Operation | Result |
| --- | --- | --- |
| ```javascript { name : 1 } ``` | ```javascript db.people.updateOne( { name: "Andy" }, { $inc: { score: 1 } }, { upsert: true } ) ``` | The `score` field of the matched document is incremented by 1. |
| ```javascript { name : 1 } ``` | ```javascript db.people.updateOne( { name: { $ne: "Joe" } }, { $set: { name: "Andy" } }, { upsert: true } ) ``` | The operation fails because it modifies the field in the unique index key pattern (`name`). |
| ```javascript { name : 1 } ``` | ```javascript db.people.updateOne( { name: "Andy", email: "andy@xyz.com" }, { $set: { active: false } }, { upsert: true } ) ``` | The operation fails because the equality predicate fields (`name`, `email`) do not match the index key field (`name`). |

### Sharded Collections

To use `findAndModify` on a sharded collection:

- If you only target one shard, you can use a partial shard key in the `query` field or,

- You can provide an equality condition on a full shard key in the `query` field.

- Starting in version 7.1, you do not need to provide the shard key or `_id` field in the query specification.

Documents in a sharded collection can be missing the shard key fields. To target a document that is missing the shard key, you can use the `null` equality match in conjunction with another filter condition (such as on the `_id` field). For example:

```javascript
{ _id: <value>, <shardkeyfield>: null } // _id of the document missing shard key
```

#### Shard Key Modification

You can update a document's shard key value unless the shard key field is the immutable `_id` field.

Documents in sharded collections can be missing the shard key fields. Take precaution to avoid accidentally removing the shard key when changing a document's shard key value.

To update the **existing** shard key value with `db.collection.findAndModify()`:

- You must run on a `mongos`. Do not issue the operation directly on the shard.

- You must run either in a transaction or as a retryable write.

- You must include an equality filter on the full shard key.

#### Missing Shard Key

Documents in a sharded collection can be missing the shard key fields. To use `db.collection.findAndModify()` to set the document's **missing** shard key:

- You must run on a `mongos`. Do not issue the operation directly on the shard.

- You must run either in a transaction or as a retryable write if the new shard key value is not `null`.

- You must include an equality filter on the full shard key.

Since a missing key value is returned as part of a null equality match, to avoid updating a null-valued key, include additional query conditions (such as on the `_id` field) as appropriate.

See also:

- Set Missing Shard Key Fields

### Schema Validation

The `db.collection.findAndModify()` method adds support for the `bypassDocumentValidation` option, which lets you bypass schema validation when inserting or updating documents in a collection with validation rules.

### Comparisons with the `update` Method

the pre-modified version of the documentWhen updating a document, `db.collection.findAndModify()` and the `updateOne()` method operate differently:

- If multiple documents match the update criteria, for `db.collection.findAndModify()`, you can specify a `sort` to provide some measure of control on which document to update.

  `updateOne()` updates the first document that matches.

- By default, `db.collection.findAndModify()` returns the pre-modified version of the document. To obtain the updated document, use the `new` option.

  The `updateOne()` method returns a `WriteResult()` object that contains the status of the operation.

  To return the updated document, use the `find()` method. However, other updates may have modified the document between your update and the document retrieval. Also, if the update modified only a single document but multiple documents matched, you will need to use additional logic to identify the updated document.

When modifying a *single* document, both `db.collection.findAndModify()` and the `updateOne()` method *atomically* update the document. See Atomicity and Transactions for more details about interactions and order of operations of these methods.

### Transactions

`db.collection.findAndModify()` can be used inside distributed transactions.

In most cases, a distributed transaction incurs a greater performance cost over single document writes, and the availability of distributed transactions should not be a replacement for effective schema design. For many scenarios, the denormalized data model (embedded documents and arrays) will continue to be optimal for your data and use cases. That is, for many scenarios, modeling your data appropriately will minimize the need for distributed transactions.

For additional transactions usage considerations (such as runtime limit and oplog size limit), see also Production Considerations.

#### Upsert within Transactions

You can create collections and indexes inside a distributed transaction if the transaction is not a cross-shard write transaction.

`db.collection.findAndModify()` with `upsert: true` can be run on an existing collection or a non-existing collection. If run on a non-existing collection, the operation creates the collection.

Create Collections and Indexes in a Transaction

#### Write Concerns and Transactions

Do not explicitly set the write concern for the operation if run in a transaction. To use write concern with transactions, see Transactions and Write Concern.

### Oplog Entries

If a `db.collection.findAndModify()` operation successfully finds and modifies a document, the operation adds an entry on the oplog (operations log). If the operation fails or does not find a document to modify, the operation does not add an entry on the oplog.

### Write Concern Errors

In MongoDB versions earlier than 6.0, if the `findAndModify` command is run on a sharded cluster, `mongos` discards the `writeConcernError` document if the shard response contains an error. In MongoDB 6.0 and later, `mongos` returns `writeConcernError`.

## Examples

### Update and Return

The following method updates and returns an existing document in the people collection where the document matches the query criteria:

```javascript
db.people.findAndModify({
    query: { name: "Tom", state: "active", rating: { $gt: 10 } },
    sort: { rating: 1 },
    update: { $inc: { score: 1 } }
})
```

This method performs the following actions:

1. The `query` finds a document in the `people` collection where the `name` field has the value `Tom`, the `state` field has the value `active` and the `rating` field has a value `greater than` 10.

2. The `sort` orders the results of the query in ascending order. If multiple documents meet the `query` condition, the method will select for modification the first document as ordered by this `sort`.

3. The update `increments` the value of the `score` field by 1.

4. The method returns the original (i.e. pre-modification) document selected for this update:

   ```javascript
   {
     "_id" : ObjectId("50f1e2c99beb36a0f45c6453"),
     "name" : "Tom",
     "state" : "active",
     "rating" : 100,
     "score" : 5
   }
   ```

   To return the updated document, add the `new:true` option to the method.

   If no document matched the `query` condition, the method returns `null`.

### Upsert

The following method includes the `upsert: true` option for the `update` operation to either update a matching document or, if no matching document exists, create a new document:

```javascript
db.people.findAndModify({
    query: { name: "Gus", state: "active", rating: 100 },
    sort: { rating: 1 },
    update: { $inc: { score: 1 } },
    upsert: true
})
```

If the method finds a matching document, the method performs an update.

If the method does **not** find a matching document, the method creates a new document. Because the method included the `sort` option, it returns an empty document `{ }` as the original (pre-modification) document:

```javascript
{ }
```

If the method did **not** include a `sort` option, the method returns `null`.

```javascript
null
```

### Return New Document

The following method includes both the `upsert: true` option and the `new:true` option. The method either updates a matching document and returns the updated document or, if no matching document exists, inserts a document and returns the newly inserted document in the `value` field.

In the following example, no document in the `people` collection matches the `query` condition:

```none
db.people.findAndModify({
    query: { name: "Pascal", state: "active", rating: 25 },
    sort: { rating: 1 },
    update: { $inc: { score: 1 } },
    upsert: true,
    new: true
})
```

The method returns the newly inserted document:

```javascript
{
   "_id" : ObjectId("50f49ad6444c11ac2448a5d6"),
   "name" : "Pascal",
   "rating" : 25,
   "score" : 1,
   "state" : "active"
}
```

### Sort and Remove

By including a `sort` specification on the `rating` field, the following example removes from the `people` collection a single document with the `state` value of `active` and the lowest `rating` among the matching documents:

```javascript
db.people.findAndModify(
   {
     query: { state: "active" },
     sort: { rating: 1 },
     remove: true
   }
)
```

The method returns the deleted document:

```javascript
{
   "_id" : ObjectId("52fba867ab5fdca1299674ad"),
   "name" : "XYZ123",
   "score" : 1,
   "state" : "active",
   "rating" : 3
}
```

### Specify Collation

Collation allows users to specify language-specific rules for string comparison, such as rules for lettercase and accent marks.

A collection `myColl` has the following documents:

```javascript
{ _id: 1, category: "café", status: "A" }
{ _id: 2, category: "cafe", status: "a" }
{ _id: 3, category: "cafE", status: "a" }
```

The following operation includes the collation option:

```javascript
db.myColl.findAndModify({
    query: { category: "cafe", status: "a" },
    sort: { category: 1 },
    update: { $set: { status: "Updated" } },
    collation: { locale: "fr", strength: 1 }
});
```

The operation returns the following document:

```javascript
{ "_id" : 1, "category" : "café", "status" : "A" }
```

### Specify `arrayFilters` for an Array Update Operations

`arrayFilters` is not available for updates that use an aggregation pipeline.

When updating an array field, you can specify `arrayFilters` that determine which array elements to update.

#### Update Elements Match `arrayFilters` Criteria

`arrayFilters` is not available for updates that use an aggregation pipeline.

Create a collection `students` with the following documents:

```javascript
db.students.insertMany( [
   { "_id" : 1, "grades" : [ 95, 92, 90 ] },
   { "_id" : 2, "grades" : [ 98, 100, 102 ] },
   { "_id" : 3, "grades" : [ 95, 110, 100 ] }
] )
```

To update all elements that are greater than or equal to `100` in the `grades` array, use the filtered positional operator [`$[<identifier>]`](https://www.mongodb.com/docs/reference/operator/update/positional-filtered/#mongodb-update-up.---identifier--) with the `arrayFilters` option in the `db.collection.findAndModify()` method:

```javascript
db.students.findAndModify({
   query: { grades: { $gte: 100 } },
   update: { $set: { "grades.$[element]" : 100 } },
   arrayFilters: [ { "element": { $gte: 100 } } ]
})
```

The operation updates the `grades` field for a single document, and after the operation, the collection has the following documents:

```javascript
{ "_id" : 1, "grades" : [ 95, 92, 90 ] }
{ "_id" : 2, "grades" : [ 98, 100, 100 ] }
{ "_id" : 3, "grades" : [ 95, 110, 100 ] }
```

#### Update Specific Elements of an Array of Documents

`arrayFilters` is not available for updates that use an aggregation pipeline.

Create a collection `students2` with the following documents:

```javascript
db.students2.insertMany( [
   {
      "_id" : 1,
      "grades" : [
         { "grade" : 80, "mean" : 75, "std" : 6 },
         { "grade" : 85, "mean" : 90, "std" : 4 },
         { "grade" : 85, "mean" : 85, "std" : 6 }
      ]
   },
   {
      "_id" : 2,
      "grades" : [
         { "grade" : 90, "mean" : 75, "std" : 6 },
         { "grade" : 87, "mean" : 90, "std" : 3 },
         { "grade" : 85, "mean" : 85, "std" : 4 }
      ]
   }
] )
```

The following operation finds a document where the `_id` field equals `1` and uses the filtered positional operator [`$[<identifier>]`](https://www.mongodb.com/docs/reference/operator/update/positional-filtered/#mongodb-update-up.---identifier--) with the `arrayFilters` to update the `mean` for all elements in the `grades` array where the grade is greater than or equal to `85`.

```javascript
db.students2.findAndModify({
   query: { _id : 1 },
   update: { $set: { "grades.$[elem].mean" : 100 } },
   arrayFilters: [ { "elem.grade": { $gte: 85 } } ]
})
```

The operation updates the `grades` field for a single document, and after the operation, the collection has the following documents:

```javascript
{
   "_id" : 1,
   "grades" : [
      { "grade" : 80, "mean" : 75, "std" : 6 },
      { "grade" : 85, "mean" : 100, "std" : 4 },
      { "grade" : 85, "mean" : 100, "std" : 6 }
   ]
}
{
   "_id" : 2,
   "grades" : [
      { "grade" : 90, "mean" : 75, "std" : 6 },
      { "grade" : 87, "mean" : 90, "std" : 3 },
      { "grade" : 85, "mean" : 85, "std" : 4 }
   ]
}
```

### Use an Aggregation Pipeline for Updates

`db.collection.findAndModify()` can accept an aggregation pipeline for the update. The pipeline can consist of the following stages:

- `$addFields` and its alias `$set`

- `$project` and its alias `$unset`

- `$replaceRoot` and its alias `$replaceWith`

Using the aggregation pipeline allows for a more expressive update statement, such as expressing conditional updates based on current field values or updating one field using the value of another field(s).

For example, create a collection `students2` with the following documents:

```javascript
db.students2.insertMany( [
   {
      "_id" : 1,
      "grades" : [
         { "grade" : 80, "mean" : 75, "std" : 6 },
         { "grade" : 85, "mean" : 90, "std" : 4 },
         { "grade" : 85, "mean" : 85, "std" : 6 }
      ]
   },
   {
      "_id" : 2,
      "grades" : [
         { "grade" : 90, "mean" : 75, "std" : 6 },
         { "grade" : 87, "mean" : 90, "std" : 3 },
         { "grade" : 85, "mean" : 85, "std" : 4 }
      ]
   }
] )
```

The following operation finds a document where the `_id` field equals `1` and uses an aggregation pipeline to calculate a new field `total` from the `grades` field:

```javascript
db.students2.findAndModify( {
   query: {  "_id" : 1 },
   update: [ { $set: { "total" : { $sum: "$grades.grade" } } } ],  // The $set stage is an alias for ``$addFields`` stage
   new: true
} )
```

The `$set` used in the pipeline refers to the aggregation stage `$set` and not the update operator `$set`.

The operation returns the *updated* document:

```javascript
{
   "_id" : 1,
   "grades" : [ { "grade" : 80, "mean" : 75, "std" : 6 }, { "grade" : 85, "mean" : 90, "std" : 4 }, { "grade" : 85, "mean" : 85, "std" : 6 } ],
   "total" : 250
}
```

### Use Variables in `let`

letTo define variables that you can access elsewhere in the command, use the let option.

To filter results using a variable, you must access the variable within the `$expr` operator.

Create a collection `cakeFlavors`:

```javascript
db.cakeFlavors.insertMany( [
   { _id: 1, flavor: "chocolate" },
   { _id: 2, flavor: "strawberry" },
   { _id: 3, flavor: "cherry" }
] )
```

The following example defines a `targetFlavor` variable in `let` and uses the variable to change the cake flavor from cherry to orange:

```javascript
db.cakeFlavors.findAndModify( {
   query: {
      $expr: { $eq: [ "$flavor", "$$targetFlavor" ] }
   },
   update: { flavor: "orange" },
   let: { targetFlavor: "cherry" }
} )
```

### User Roles and Document Updates

Starting in MongoDB 7.0, you can use the new `USER_ROLES` system variable to return user roles.

The example in this section shows updates to fields in a collection containing medical information. The example reads the current user roles from the `USER_ROLES` system variable and only performs the updates if the user has a specific role.

To use a system variable, add `$$` to the start of the variable name. Specify the `USER_ROLES` system variable as `$$USER_ROLES`.

The example creates these users:

- `James` with a `Billing` role.

- `Michelle` with a `Provider` role.

Perform the following steps to create the roles, users, and collection:

#### Create the roles

Create roles named `Billing` and `Provider` with the required privileges and resources.

Run:

```javascript
db.createRole( { role: "Billing", privileges: [ { resource: { db: "test",
   collection: "medicalView" }, actions: [ "find" ] } ], roles: [ ] } )
db.createRole( { role: "Provider", privileges: [ { resource: { db: "test",
   collection: "medicalView" }, actions: [ "find" ] } ], roles: [ ] } )
```

#### Create the users

Create users named `James` and `Michelle` with the required roles.

```javascript
db.createUser( {
   user: "James",
   pwd: "js008",
   roles: [
      { role: "Billing", db: "test" }
   ]
} )

db.createUser( {
   user: "Michelle",
   pwd: "me009",
   roles: [
      { role: "Provider", db: "test" }
   ]
} )
```

#### Create the collection

Run:

```javascript
db.medical.insertMany( [
   {
      _id: 0,
      patientName: "Jack Jones",
      diagnosisCode: "CAS 17",
      creditCard: "1234-5678-9012-3456"
   },
   {
      _id: 1,
      patientName: "Mary Smith",
      diagnosisCode: "ACH 01",
      creditCard: "6541-7534-9637-3456"
   }
] )
```

Log in as as `Michelle`, who has the `Provider` role, and perform an update:

#### Log in as `Michelle`

Run:

```javascript
db.auth( "Michelle", "me009" )
```

#### Perform update

Run:

```javascript
// Attempt to find and modify document
db.medical.findAndModify( {
   query:
      { $and: [
         {
            // Only update the document for Mary Smith
            patientName: { $eq: "Mary Smith" }
         },
         {
            // User must have the Provider role to perform the update
            $expr: { $ne: [ {
               $setIntersection: [ [ "Provider" ], "$$USER_ROLES.role" ]
            }, [] ] }
         }
      ]
   },
   // Update document
   update: {
      patientName: "Mary Smith",
      diagnosisCode: "ACH 03",
      creditCard: "6541-7534-9637-3456"
   }
} )
```

The previous example uses `$setIntersection` to return documents where the intersection between the `"Provider"` string and the user roles from `$$USER_ROLES.role` is not empty. `Michelle` has the `Provider` role, so the update is performed.

Next, log in as as `James`, who does not have the `Provider` role, and attempt to perform the same update:

#### Log in as `James`

Run:

```javascript
db.auth( "James", "js008" )
```

#### Attempt to perform update

Run:

```javascript
// Attempt to find and modify document
db.medical.findAndModify( {
   query:
      { $and: [
         {
            // Only update the document for Mary Smith
            patientName: { $eq: "Mary Smith" }
         },
         {
            // User must have the Provider role to perform the update
            $expr: { $ne: [ {
               $setIntersection: [ [ "Provider" ], "$$USER_ROLES.role" ]
            }, [] ] }
         }
      ]
   },
   // Update document
   update: {
      patientName: "Mary Smith",
      diagnosisCode: "ACH 03",
      creditCard: "6541-7534-9637-3456"
   }
} )
```

The previous example does not update any documents.
