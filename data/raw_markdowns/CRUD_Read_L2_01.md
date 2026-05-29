# db.collection.find() (mongosh method)

This page documents a [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) method. To see the equivalent method in a MongoDB driver, see the corresponding page for your programming language:

## Definition

`db.collection.find(query, projection, options)`
[`find`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/find/#mongodb-dbcommand-dbcmd.find) commandSelects documents in a collection or view and returns a [cursor](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/cursors/#std-label-cursors) to the selected documents.

A [cursor](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/cursors/#std-label-cursors) to the documents that match the `query` criteria. When the [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method "returns documents," the method is actually returning a cursor to the documents.

## Compatibility

methodThis method is available in deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

This command is supported in all MongoDB Atlas clusters. For information on Atlas support for all commands, see [Unsupported Commands](https://www.mongodb.com/docs/atlas/unsupported-commands/).

- [MongoDB Enterprise](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

The [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method has the following form:

```javascript
db.collection.find( <query>, <projection>, <options> )
```

### Parameters

The [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method takes the following parameters:

<table>
<tr>
<th id="Parameter">
Parameter

</th>
<th id="Type">
Type

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Parameter">
[query](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-method-find-query)

</td>
<td headers="Type">
document

</td>
<td headers="Description">
Optional. Specifies selection filter using [query operators](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-projection-operators-top). To return all documents in a collection, omit this parameter or pass an empty document (`{}`).

</td>
</tr>
<tr>
<td headers="Parameter">
[projection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-method-find-projection)

</td>
<td headers="Type">
document

</td>
<td headers="Description">
Optional. Specifies the fields to return in the documents that match the query filter. To return all fields in the matching documents, omit this parameter.  For details, see [Projection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-find-projection).

</td>
</tr>
<tr>
<td headers="Parameter">
[options](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-method-find-options)

</td>
<td headers="Type">
document

</td>
<td headers="Description">
Optional. Specifies additional options for the query. These options modify query behavior and how results are returned. For details, see [Options](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-find-options).

</td>
</tr>
</table>

## Behavior

### Projection

As part of making [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) and [`findAndModify()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.findAndModify/#mongodb-method-db.collection.findAndModify) projection consistent with aggregation's [`$project`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project) stage,

- The [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) and [`findAndModify()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.findAndModify/#mongodb-method-db.collection.findAndModify) projection can accept [aggregation expressions and syntax](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions).

- MongoDB enforces additional restrictions with regards to projections. See [Projection Restrictions](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/limits/#mongodb-limit-Projection-Restrictions) for details.

The `projection` parameter determines which fields are returned in the matching documents. The `projection` parameter takes a document of the following form:

```javascript
{ <field1>: <value>, <field2>: <value> ... }
```

<table>
<tr>
<th id="Projection">
Projection

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Projection">
`<field>: <1 or true>`

</td>
<td headers="Description">
Specifies the inclusion of a field. If you specify a non-zero integer for the projection value, the operation treats the value as `true`.

</td>
</tr>
<tr>
<td headers="Projection">
`<field>: <0 or false>`

</td>
<td headers="Description">
Specifies the exclusion of a field.

</td>
</tr>
<tr>
<td headers="Projection">
`"<field>.$": <1 or true>`

</td>
<td headers="Description">
Uses the [`$`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) array projection operator to return the first element that matches the query condition on the array field. If you specify a non-zero integer for the projection value, the operation treats the value as `true`.

Not available for [views](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/views/#std-label-views-landing-page).

</td>
</tr>
<tr>
<td headers="Projection">
`<field>: <array projection>`

</td>
<td headers="Description">
Uses the array projection operators ([`$elemMatch`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice)) to specify the array elements to include.

Not available for [views](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/views/#std-label-views-landing-page).

</td>
</tr>
<tr>
<td headers="Projection">
`<field>: <$meta expression>`

</td>
<td headers="Description">
Uses the [`$meta`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/aggregation/meta/#mongodb-expression-exp.-meta) operator expression to specify the inclusion of available [`per-document metadata`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/aggregation/meta/#mongodb-expression-exp.-meta).

Not available for [views](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/views/#std-label-views-landing-page).

</td>
</tr>
<tr>
<td headers="Projection">
`<field>: <aggregation expression>`

</td>
<td headers="Description">
Specifies the value of the projected field.

With the use of [aggregation expressions and syntax](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions), including the use of literals and aggregation variables, you can project new fields or project existing fields with new values.

- If you specify a non-numeric, non-boolean literal (such as a literal string or an array or an operator expression) for the projection value, the field is projected with the new value, for example:

  - `{ field: [ 1, 2, 3, "$someExistingField" ] }`

  - `{ field: "New String Value" }`

  - `{ field: { status: "Active", total: { $sum: "$existingArray" } } }`

- To project a literal value for a field, use the [`$literal`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/aggregation/literal/#mongodb-expression-exp.-literal) aggregation expression; for example:

  - `{ field: { $literal: 5 } }`

  - `{ field: { $literal: true } }`

  - `{ field: { $literal: { fieldWithValue0: 0, fieldWithValue1: 1 } } }`

</td>
</tr>
</table>

### Options

<table>
<tr>
<th id="Option">
Option

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Option">
allowDiskUse

</td>
<td headers="Description">
Whether or not pipelines that require more than 100 megabytes of memory to execute write to temporary files on disk. For details, see [`cursor.allowDiskUse()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.allowDiskUse/#mongodb-method-cursor.allowDiskUse).

</td>
</tr>
<tr>
<td headers="Option">
allowPartialResults

</td>
<td headers="Description">
For queries against a sharded collection, allows the command (or subsequent getMore commands) to return partial results, rather than an error, if one or more queried shards are unavailable.

</td>
</tr>
<tr>
<td headers="Option">
awaitData

</td>
<td headers="Description">
If the cursor is a a tailable-await cursor. Requires `tailable` to be `true`.

</td>
</tr>
<tr>
<td headers="Option">
collation

</td>
<td headers="Description">
Collation settings for update operation.

</td>
</tr>
<tr>
<td headers="Option">
comment

</td>
<td headers="Description">
Adds a `$comment` to the query that shows in the [profiler](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/database-profiler/#std-label-profiler) logs.

</td>
</tr>
<tr>
<td headers="Option">
explain

</td>
<td headers="Description">
Adds explain output based on the verbosity mode provided.

</td>
</tr>
<tr>
<td headers="Option">
hint

</td>
<td headers="Description">
Forces the query optimizer to use specific indexes in the query.

</td>
</tr>
<tr>
<td headers="Option">
limit

</td>
<td headers="Description">
Sets a limit of documents returned in the result set.

</td>
</tr>
<tr>
<td headers="Option">
max

</td>
<td headers="Description">
The exclusive upper bound for a specific index.

</td>
</tr>
<tr>
<td headers="Option">
maxAwaitTimeMS

</td>
<td headers="Description">
The maximum amount of time for the server to wait on new documents to satisfy a tailable cursor query. Requires `tailable` and `awaitData` to be `true`.

</td>
</tr>
<tr>
<td headers="Option">
maxTimeMS

</td>
<td headers="Description">
The maximum amount of time (in milliseconds) the server should allow the query to run.

</td>
</tr>
<tr>
<td headers="Option">
min

</td>
<td headers="Description">
The inclusive lower bound for a specific index.

</td>
</tr>
<tr>
<td headers="Option">
noCursorTimeout

</td>
<td headers="Description">
Whether the server should timeout the cursor after a period of inactivity (by default 10 minutes).

</td>
</tr>
<tr>
<td headers="Option">
projection

</td>
<td headers="Description">
Specifies the fields to return in the documents that match the query filter.

You can specify projection in two ways for [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) and [`findOne()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.findOne/#mongodb-method-db.collection.findOne):

- Setting the `projection` parameter

- Setting the `options` parameter to `projection`

If you specify both parameters, the `projection` parameter takes precedence. To use `options.projection`, set the `projection` parameter to `null` or `undefined`.

</td>
</tr>
<tr>
<td headers="Option">
readConcern

</td>
<td headers="Description">
Specifies the read concern level for the query.

</td>
</tr>
<tr>
<td headers="Option">
readPreference

</td>
<td headers="Description">
Specifies the read preference level for the query.

</td>
</tr>
<tr>
<td headers="Option">
returnKey

</td>
<td headers="Description">
Whether only the index keys are returned for a query.

</td>
</tr>
<tr>
<td headers="Option">
showRecordId

</td>
<td headers="Description">
If the `$recordId` field is added to the returned documents. The `$recordId` indicates the position of the document in the result set.

</td>
</tr>
<tr>
<td headers="Option">
skip

</td>
<td headers="Description">
How many documents to skip before returning the first document in the result set.

</td>
</tr>
<tr>
<td headers="Option">
sort

</td>
<td headers="Description">
The order of the documents returned in the result set. Fields specified in the sort, must have an index.

</td>
</tr>
<tr>
<td headers="Option">
tailable

</td>
<td headers="Description">
Indicates if the cursor is tailable. Tailable cursors remain open after the intial results of the query are exhausted. Tailable cursors are only available on [Capped Collections](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/capped-collections/#std-label-manual-capped-collection).

</td>
</tr>
</table>#### Embedded Field Specification

For fields in an embedded documents, you can specify the field using either:

- [dot notation](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/document/#std-label-document-dot-notation-embedded-fields), for example `"field.nestedfield": <value>`

- nested form, for example `{ field: { nestedfield: <value> } }`

#### `_id` Field Projection

The `_id` field is included in the returned documents by default unless you explicitly specify `_id: 0` in the projection to suppress the field.

#### Inclusion or Exclusion

A `projection` *cannot* contain *both* include and exclude specifications, with the exception of the `_id` field:

- In projections that *explicitly include* fields, the `_id` field is the only field that you can *explicitly exclude*.

- In projections that *explicitly excludes* fields, the `_id` field is the only field that you can *explicitly include*; however, the `_id` field is included by default.

See [Projection Examples](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-find-projection-examples).

#### Sorting

When an operation both sorts *and* [projects](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/glossary/#std-term-projection) with the same fields, MongoDB sorts on the original field values before applying the projection. For more information about operation order, see [find() Order of Operations](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/find/#std-label-find-order-of-operations).

### Cursor Handling

Executing [`db.collection.find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) automatically iterates the cursor to display up to the first 20 documents. Type `it` to continue iteration.

To access the returned documents with a driver, use the appropriate cursor handling mechanism for the [driver language](https://www.mongodb.com/docs/drivers/).

- [Iterate the Returned Cursor](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-crud-read-cursor)

- [Modify the Cursor Behavior](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-find-modify-cursor)

- [Available `mongosh` Cursor Methods](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-find-cursor-methods)

### Read Concern

To specify the [read concern](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/read-concern/#std-label-read-concern) for [`db.collection.find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find), use the [`cursor.readConcern()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.readConcern/#mongodb-method-cursor.readConcern) method.

### Type Bracketing

MongoDB treats some data types as equivalent for comparison purposes. For instance, numeric types undergo conversion before comparison. For most data types, however, [comparison operators](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/comparison/#std-label-query-selectors-comparison) only perform comparisons on documents where the [BSON type](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bson-type-comparison-order/#std-label-bson-types-comparison-order) of the target field matches the type of the query operand. Consider the following collection:

```javascript
{ "_id": "apples", "qty": 5 }
{ "_id": "bananas", "qty": 7 }
{ "_id": "oranges", "qty": { "in stock": 8, "ordered": 12 } }
{ "_id": "avocados", "qty": "fourteen" }
```

The following query uses [`$gt`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/gt/#mongodb-query-op.-gt) to return documents where the value of `qty` is greater than `4`.

```javascript
db.collection.find( { qty: { $gt: 4 } } )
```

The query returns the following documents:

```javascript
{ "_id": "apples", "qty": 5 }
{ "_id": "bananas", "qty": 7 }
```

The document with `_id` equal to `"avocados"` is not returned because its `qty` value is of type `string` while the [`$gt`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/gt/#mongodb-query-op.-gt) operand is of type `integer`.

The document with `_id` equal to `"oranges"` is not returned because its `qty` value is of type `object`.

To enforce data types in a collection, use [Schema Validation](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/schema-validation/).

### Sessions

For cursors created inside a session, you cannot call [`getMore`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/getMore/#mongodb-dbcommand-dbcmd.getMore) outside the session.

Similarly, for cursors created outside of a session, you cannot call [`getMore`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/getMore/#mongodb-dbcommand-dbcmd.getMore) inside a session.

#### Session Idle Timeout

MongoDB drivers and [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) associate all operations with a [server session](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/server-sessions/), with the exception of unacknowledged write operations. For operations not explicitly associated with a session (i.e. using [`Mongo.startSession()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/Mongo.startSession/#mongodb-method-Mongo.startSession)), MongoDB drivers and `mongosh` create an implicit session and associate it with the operation.

If a session is idle for longer than 30 minutes, the MongoDB server marks that session as expired and may close it at any time. When the MongoDB server closes the session, it also kills any in-progress operations and open cursors associated with the session. This includes cursors configured with [`noCursorTimeout()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.noCursorTimeout/#mongodb-method-cursor.noCursorTimeout) or a [`maxTimeMS()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.maxTimeMS/#mongodb-method-cursor.maxTimeMS) greater than 30 minutes.

For operations that may be idle for longer than 30 minutes, associate the operation with an explicit session using [`Mongo.startSession()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/Mongo.startSession/#mongodb-method-Mongo.startSession) and periodically refresh the session using the [`refreshSessions`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/refreshSessions/#mongodb-dbcommand-dbcmd.refreshSessions) command. See [Session Idle Timeout](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/limits/#mongodb-limit-Session-Idle-Timeout) for more information.

### Transactions

[`db.collection.find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) can be used inside [distributed transactions](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/transactions/#std-label-transactions).

- For cursors created outside of a transaction, you cannot call [`getMore`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/getMore/#mongodb-dbcommand-dbcmd.getMore) inside the transaction.

- For cursors created in a transaction, you cannot call [`getMore`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/getMore/#mongodb-dbcommand-dbcmd.getMore) outside the transaction.

In most cases, a distributed transaction incurs a greater performance cost over single document writes, and the availability of distributed transactions should not be a replacement for effective schema design. For many scenarios, the [denormalized data model (embedded documents and arrays)](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/data-modeling/embedding/#std-label-data-modeling-embedding) will continue to be optimal for your data and use cases. That is, for many scenarios, modeling your data appropriately will minimize the need for distributed transactions.

For additional transactions usage considerations (such as runtime limit and oplog size limit), see also [Production Considerations](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/transactions-production-consideration/#std-label-production-considerations).

[`db.collection.find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find)

### Client Disconnection

If the client that issued [`db.collection.find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) disconnects before the operation completes, MongoDB marks [`db.collection.find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) for termination using [`killOp`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/killOp/#mongodb-dbcommand-dbcmd.killOp).

### Query Settings

You can use query settings to set index hints, set [operation rejection filters](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/operation-rejection-filters/#std-label-operation-rejection-filters), and other fields. The settings apply to the [query shape](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/aggregation/queryStats/#std-label-queryStats-queryShape) on the entire cluster. The cluster retains the settings after shutdown.

The [query optimizer](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/glossary/#std-term-query-optimizer) uses the query settings as an additional input during query planning, which affects the plan selected to run the query. You can also use query settings to block a query shape.

To add query settings and explore examples, see [`setQuerySettings`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/setQuerySettings/#mongodb-dbcommand-dbcmd.setQuerySettings).

You can add query settings for [`find`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/find/#mongodb-dbcommand-dbcmd.find), [`distinct`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/distinct/#mongodb-dbcommand-dbcmd.distinct), and [`aggregate`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/aggregate/#mongodb-dbcommand-dbcmd.aggregate) commands.

Query settings have more functionality and are preferred over deprecated [index filters](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/query-plans/#std-label-index-filters).

To remove query settings, use [`removeQuerySettings`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/removeQuerySettings/#mongodb-dbcommand-dbcmd.removeQuerySettings). To obtain the query settings, use a [`$querySettings`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/aggregation/querySettings/#mongodb-pipeline-pipe.-querySettings) stage in an aggregation pipeline.

## Examples

The examples in this section use documents from the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/#std-label-bios-example-collection) where the documents generally have the form:

```javascript
{
    "_id" : <value>,
    "name" : { "first" : <string>, "last" : <string> },       // embedded document
    "birth" : <ISODate>,
    "death" : <ISODate>,
    "contribs" : [ <string>, ... ],                           // Array of Strings
    "awards" : [
        { "award" : <string>, year: <number>, by: <string> }  // Array of embedded documents
        ...
    ]
}
```

To create and populate the `bios` collection, see [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/#std-label-bios-example-collection).

### Find All Documents in a Collection

The [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method with no parameters returns all documents from a collection and returns all fields for the documents. For example, the following operation returns all documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/#std-label-bios-example-collection):

```javascript
db.bios.find()
```

### Find Documents that Match Query Criteria

#### Query for Equality

- The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where `_id` equals `5`:

  ```javascript
  db.bios.find( { _id: 5 } )
  ```

- The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the field `last` in the `name` embedded document equals `"Hopper"`:

  ```javascript
  db.bios.find( { "name.last": "Hopper" } )
  ```

  To access fields in an embedded document, use [dot notation](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/document/#std-label-document-dot-notation-embedded-fields) (`"<embedded document>.<field>"`).

#### Query Using Operators

To find documents that match a set of selection criteria, call [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) with the `<criteria>` parameter.

MongoDB provides various [query operators](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify the criteria.

- The following operation uses the [`$in`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/in/#mongodb-query-op.-in) operator to return documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where `_id` equals either `5` or `ObjectId("507c35dd8fada716c89d0013")`:

  ```javascript
  db.bios.find(
     { _id: { $in: [ 5, ObjectId("507c35dd8fada716c89d0013") ] } }
  )
  ```

- The following operation uses the [`$gt`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/gt/#mongodb-query-op.-gt) operator returns all the documents from the `bios` collection where `birth` is greater than `new Date('1950-01-01')`:

  ```javascript
  db.bios.find( { birth: { $gt: new Date('1950-01-01') } } )
  ```

- The following operation uses the [`$regex`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/regex/#mongodb-query-op.-regex) operator to return documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where `name.last` field starts with the letter `N` (or is `"LIKE N%"`)

  ```javascript
  db.bios.find(
     { "name.last": { $regex: /^N/ } }
  )
  ```

For a list of the query operators, see [Query Predicates](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors).

#### Query for Ranges

Combine comparison operators to specify ranges for a field. The following operation returns from the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) documents where `birth` is between `new Date('1940-01-01')` and `new Date('1960-01-01')` (exclusive):

```javascript
db.bios.find( { birth: { $gt: new Date('1940-01-01'), $lt: new Date('1960-01-01') } } )
```

For a list of the query operators, see [Query Predicates](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors).

#### Query for Multiple Conditions

The following operation returns all the documents from the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where `birth` field is [`greater than`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/gt/#mongodb-query-op.-gt) `new Date('1950-01-01')` and `death` field does not exists:

```javascript
db.bios.find( {
   birth: { $gt: new Date('1920-01-01') },
   death: { $exists: false }
} )
```

For a list of the query operators, see [Query Predicates](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors).

### Compare Two Fields from A Single Document

`$expr` can contain expressions that compare fields from the same document.

The following operation uses [`$expr`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/expr/#mongodb-query-op.-expr) to find documents in the `movies` collection where the Rotten Tomatoes viewer rating exceeds the critic rating:

```javascript
db.movies.find(
   { $expr: { $gt: [ "$tomatoes.viewer.rating", "$tomatoes.critic.rating" ] } },
   { _id: 0, title: 1, "tomatoes.viewer.rating": 1, "tomatoes.critic.rating": 1 }
).sort( { "tomatoes.viewer.rating": -1 } ).limit( 3 )

```

```javascript
[
  { title: 'I Am Maria', tomatoes: { viewer: { rating: 5 } } },
  { title: 'Kadin Hamlet', tomatoes: { viewer: { rating: 5 } } },
  { title: 'The Seine Meets Paris', tomatoes: { viewer: { rating: 5 } } }
]
```

### Query Embedded Documents

The following examples query the `name` embedded field in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/#std-label-bios-example-collection).

#### Query Exact Matches on Embedded Documents

The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the embedded document `name` is *exactly* `{ first: "Yukihiro", last: "Matsumoto" }`, including the order:

```javascript
db.bios.find(
    { name: { first: "Yukihiro", last: "Matsumoto" } }
)
```

The `name` field must match the embedded document exactly. The query does **not** match documents with the following `name` fields:

```javascript
{
   first: "Yukihiro",
   aka: "Matz",
   last: "Matsumoto"
}

{
   last: "Matsumoto",
   first: "Yukihiro"
}
```

#### Query Fields of an Embedded Document

The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the embedded document `name` contains a field `first` with the value `"Yukihiro"` and a field `last` with the value `"Matsumoto"`. The query uses [dot notation](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/glossary/#std-term-dot-notation) to access fields in an embedded document:

```javascript
db.bios.find(
   {
     "name.first": "Yukihiro",
     "name.last": "Matsumoto"
   }
)
```

The query matches the document where the `name` field contains an embedded document with the field `first` with the value `"Yukihiro"` and a field `last` with the value `"Matsumoto"`. For instance, the query would match documents with `name` fields that held either of the following values:

```javascript
{
  first: "Yukihiro",
  aka: "Matz",
  last: "Matsumoto"
}

{
  last: "Matsumoto",
  first: "Yukihiro"
}
```

For more information and examples, see also [Query on Embedded/Nested Documents](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/query-embedded-documents/).

### Query Arrays

#### Query for an Array Element

The following examples query the `contribs` array in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/).

- The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the array field `contribs` contains the element `"UNIX"`:

  ```javascript
  db.bios.find( { contribs: "UNIX" } )
  ```

- The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the array field `contribs` contains the element `"ALGOL"` or `"Lisp"`:

  ```javascript
  db.bios.find( { contribs: { $in: [ "ALGOL", "Lisp" ]} } )
  ```

- The following operation use the [`$all`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/all/#mongodb-query-op.-all) query operator to return documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the array field `contribs` contains both the elements `"ALGOL"` and `"Lisp"`:

  ```javascript
  db.bios.find( { contribs: { $all: [ "ALGOL", "Lisp" ] } } )
  ```

  For more examples, see [`$all`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/all/#mongodb-query-op.-all).  See also [`$elemMatch`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch).

- The following operation uses the [`$size`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/size/#mongodb-query-op.-size) operator to return documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the array size of `contribs` is 4:

  ```javascript
  db.bios.find( { contribs: { $size: 4 } } )
  ```

For more information and examples of querying an array, see:

- [Query an Array](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/query-arrays/)

- [Query an Array of Embedded Documents](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/query-array-of-documents/)

For a list of array specific query operators, see [Array Query Predicate Operators](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/arrays/#std-label-operator-query-array).

#### Query an Array of Documents

The following examples query the `awards` array in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/).

- The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the `awards` array contains an element with `award` field equals `"Turing Award"`:

  ```javascript
  db.bios.find(
     { "awards.award": "Turing Award" }
  )
  ```

- The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) where the `awards` array contains at least one element with both the `award` field equals `"Turing Award"` and the `year` field greater than 1980:

  ```javascript
  db.bios.find(
     { awards: { $elemMatch: { award: "Turing Award", year: { $gt: 1980 } } } }
  )
  ```

  Use the [`$elemMatch`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch) operator to specify multiple criteria on an array element.

For more information and examples of querying an array, see:

- [Query an Array](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/query-arrays/)

- [Query an Array of Embedded Documents](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/query-array-of-documents/)

For a list of array specific query operators, see [Array Query Predicate Operators](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/query-predicates/arrays/#std-label-operator-query-array).

### Query for BSON Regular Expressions

To find documents that contain BSON regular expressions as values, call [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) with the `bsonRegExp` option set to `true`. The `bsonRegExp` option allows you to return regular expressions that can't be represented as JavaScript regular expressions.

The following operation returns documents in a collection named `testbson` where the value of a field named `foo` is a `BSONRegExp` type:

```javascript
db.testbson.find( {}, {}, { bsonRegExp: true } )
```

```javascript
[
  {
    _id: ObjectId('65e8ba8a4b3c33a76e6cacca'),
    foo: BSONRegExp('(?-i)AA_', 'i')
  }
]
```

### Projections

The [projection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#std-label-find-projection) parameter specifies which fields to return. The parameter contains either include or exclude specifications, not both, unless the exclude is for the `_id` field.

Unless the `_id` field is explicitly excluded in the projection document `_id: 0`, the `_id` field is returned.

#### Specify the Fields to Return

The following operation finds all documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) and returns only the `name` field, `contribs` field and `_id` field:

```javascript
db.bios.find( { }, { name: 1, contribs: 1 } )
```

Unless the `_id` field is explicitly excluded in the projection document `_id: 0`, the `_id` field is returned.

#### Explicitly Excluded Fields

The following operation queries the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) and returns all fields *except* the `first` field in the `name` embedded document and the `birth` field:

```javascript
db.bios.find(
   { contribs: 'OOP' },
   { 'name.first': 0, birth: 0 }
)
```

#### Explicitly Exclude the `_id` Field

Unless the `_id` field is explicitly excluded in the projection document `_id: 0`, the `_id` field is returned.

The following operation finds documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) and returns only the `name` field and the `contribs` field:

```javascript
db.bios.find(
   { },
   { name: 1, contribs: 1, _id: 0 }
)
```

#### On Arrays and Embedded Documents

The following operation queries the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) and returns the `last` field in the `name` embedded document and the first two elements in the `contribs` array:

```javascript
db.bios.find(
   { },
   { _id: 0, 'name.last': 1, contribs: { $slice: 2 } } )
```

You can also specify embedded fields using the nested form. For example:

```javascript
db.bios.find(
   { },
   { _id: 0, name: { last: 1 }, contribs: { $slice: 2 } }
)
```

#### Use Aggregation Expression

[`db.collection.find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) projection can accept [aggregation expressions and syntax](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions).

With the use of aggregation expressions and syntax, you can project new fields or project existing fields with new values. For example, the following operation uses aggregation expressions to override the value of the `name` and `awards` fields as well as to include new fields `reportDate`, `reportBy`, and `reportNumber`.

```javascript
db.bios.find(
   { },
   {
     _id: 0,
     name: {
        $concat: [
           { $ifNull: [ "$name.aka", "$name.first" ] },
           " ",
           "$name.last"
        ]
     },
     birth: 1,
     contribs: 1,
     awards: { $cond: { if: { $isArray: "$awards" }, then: { $size: "$awards" }, else: 0 } },
     reportDate: { $dateToString: {  date: new Date(), format: "%Y-%m-%d" } },
     reportBy: "hellouser123",
     reportNumber: { $literal: 1 }
   }
)
```

To set the `reportRun` field to the value `1` The operation returns the following documents:

```javascript
{ "birth" : ISODate("1924-12-03T05:00:00Z"), "contribs" : [ "Fortran", "ALGOL", "Backus-Naur Form", "FP" ], "name" : "John Backus", "awards" : 4, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "birth" : ISODate("1927-09-04T04:00:00Z"), "contribs" : [ "Lisp", "Artificial Intelligence", "ALGOL" ], "name" : "John McCarthy", "awards" : 3, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "birth" : ISODate("1906-12-09T05:00:00Z"), "contribs" : [ "UNIVAC", "compiler", "FLOW-MATIC", "COBOL" ], "name" : "Grace Hopper", "awards" : 4, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "birth" : ISODate("1926-08-27T04:00:00Z"), "contribs" : [ "OOP", "Simula" ], "name" : "Kristen Nygaard", "awards" : 3, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "birth" : ISODate("1931-10-12T04:00:00Z"), "contribs" : [ "OOP", "Simula" ], "name" : "Ole-Johan Dahl", "awards" : 3, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "birth" : ISODate("1956-01-31T05:00:00Z"), "contribs" : [ "Python" ], "name" : "Guido van Rossum", "awards" : 2, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "birth" : ISODate("1941-09-09T04:00:00Z"), "contribs" : [ "UNIX", "C" ], "name" : "Dennis Ritchie", "awards" : 3, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "birth" : ISODate("1965-04-14T04:00:00Z"), "contribs" : [ "Ruby" ], "name" : "Matz Matsumoto", "awards" : 1, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "birth" : ISODate("1955-05-19T04:00:00Z"), "contribs" : [ "Java" ], "name" : "James Gosling", "awards" : 2, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
{ "contribs" : [ "Scala" ], "name" : "Martin Odersky", "awards" : 0, "reportDate" : "2020-06-05", "reportBy" : "hellouser123", "reportNumber" : 1 }
```

[Project Fields to Return from Query](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/tutorial/project-fields-from-query-results/)

### Iterate the Returned Cursor

The [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns a [cursor](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/cursors/#std-label-cursors) to the results.

In [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), if the returned cursor is not assigned to a variable using the `var` keyword, the cursor is automatically iterated to access up to the first 20 documents that match the query. You can update the `displayBatchSize` variable to change the number of automatically iterated documents.

The following example sets the batch size to 3. Future `db.collection.find()` operations will only return 3 documents per cursor iteration.

```javascript
config.set( "displayBatchSize", 3 )
```

To manually iterate over the results, assign the returned cursor to a variable with the `var` keyword, as shown in the following sections.

#### With Variable Name

The following example uses the variable `myCursor` to iterate over the cursor and print the matching documents:

```javascript
var myCursor = db.bios.find( );

myCursor
```

#### With `next()` Method

The following example uses the cursor method [`next()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.next/#mongodb-method-cursor.next) to access the documents:

```javascript
var myCursor = db.bios.find( );

var myDocument = myCursor.hasNext() ? myCursor.next() : null;

if (myDocument) {
    var myName = myDocument.name;
    print (tojson(myName));
}
```

To print, you can also use the `printjson()` method instead of `print(tojson())`:

```javascript
if (myDocument) {
   var myName = myDocument.name;
   printjson(myName);
}
```

#### With `forEach()` Method

The following example uses the cursor method [`forEach()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.forEach/#mongodb-method-cursor.forEach) to iterate the cursor and access the documents:

```javascript
var myCursor = db.bios.find( );

myCursor.forEach(printjson);
```

### Modify the Cursor Behavior

[`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) and the [drivers](https://www.mongodb.com/docs/drivers/) provide several cursor methods that call on the *cursor* returned by the [`find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method to modify its behavior.

#### Order Documents in the Result Set

The [`sort()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) method orders the documents in the result set. The following operation returns documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/) sorted in ascending order by the `name` field:

```javascript
db.bios.find().sort( { name: 1 } )
```

[`sort()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) corresponds to the `ORDER BY` statement in SQL.

#### Limit the Number of Documents to Return

The [`limit()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) method limits the number of documents in the result set. The following operation returns at most `5` documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/#std-label-bios-example-collection):

```javascript
db.bios.find().limit( 5 )
```

[`limit()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) corresponds to the `LIMIT` statement in SQL.

#### Set the Starting Point of the Result Set

The [`skip()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) method controls the starting point of the results set. The following operation skips the first `5` documents in the [bios collection](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/bios-example-collection/#std-label-bios-example-collection) and returns all remaining documents:

```javascript
db.bios.find().skip( 5 )
```

#### Specify Collation

[Collation](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/collation/#std-label-collation) allows users to specify language-specific rules for string comparison, such as rules for lettercase and accent marks.

The [`collation()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.collation/#mongodb-method-cursor.collation) method specifies the [collation](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/collation/#std-label-collation) for the [`db.collection.find()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) operation.

```javascript
db.bios.find( { "name.last": "hopper" } ).collation( { locale: "en_US", strength: 1 } )
```

#### Combine Cursor Methods

The following statements chain cursor methods [`limit()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) and [`sort()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort):

```javascript
db.bios.find().sort( { name: 1 } ).limit( 5 )
db.bios.find().limit( 5 ).sort( { name: 1 } )
```

The two statements are equivalent; i.e. the order in which you chain the [`limit()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) and the [`sort()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) methods is not significant. Both statements return the first five documents, as determined by the ascending sort order on 'name'.

#### Available `mongosh` Cursor Methods

- [`cursor.allowDiskUse()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.allowDiskUse/#mongodb-method-cursor.allowDiskUse)

- [`cursor.batchSize()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.batchSize/#mongodb-method-cursor.batchSize)

- [`cursor.close()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.close/#mongodb-method-cursor.close)

- [`cursor.isClosed()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.isClosed/#mongodb-method-cursor.isClosed)

- [`cursor.collation()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.collation/#mongodb-method-cursor.collation)

- [`cursor.comment()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.comment/#mongodb-method-cursor.comment)

- [`cursor.count()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.count/#mongodb-method-cursor.count)

- [`cursor.explain()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.explain/#mongodb-method-cursor.explain)

- [`cursor.forEach()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.forEach/#mongodb-method-cursor.forEach)

- [`cursor.hasNext()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.hasNext/#mongodb-method-cursor.hasNext)

- [`cursor.hint()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.hint/#mongodb-method-cursor.hint)

- [`cursor.isExhausted()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.isExhausted/#mongodb-method-cursor.isExhausted)

- [`cursor.itcount()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.itcount/#mongodb-method-cursor.itcount)

- [`cursor.limit()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit)

- [`cursor.map()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.map/#mongodb-method-cursor.map)

- [`cursor.max()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.max/#mongodb-method-cursor.max)

- [`cursor.maxTimeMS()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.maxTimeMS/#mongodb-method-cursor.maxTimeMS)

- [`cursor.min()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.min/#mongodb-method-cursor.min)

- [`cursor.next()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.next/#mongodb-method-cursor.next)

- [`cursor.noCursorTimeout()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.noCursorTimeout/#mongodb-method-cursor.noCursorTimeout)

- [`cursor.objsLeftInBatch()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.objsLeftInBatch/#mongodb-method-cursor.objsLeftInBatch)

- [`cursor.pretty()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.pretty/#mongodb-method-cursor.pretty)

- [`cursor.readConcern()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.readConcern/#mongodb-method-cursor.readConcern)

- [`cursor.readPref()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.readPref/#mongodb-method-cursor.readPref)

- [`cursor.returnKey()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.returnKey/#mongodb-method-cursor.returnKey)

- [`cursor.showRecordId()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.showRecordId/#mongodb-method-cursor.showRecordId)

- [`cursor.size()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.size/#mongodb-method-cursor.size)

- [`cursor.skip()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip)

- [`cursor.sort()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort)

- [`cursor.tailable()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.tailable/#mongodb-method-cursor.tailable)

- [`cursor.toArray()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/cursor.toArray/#mongodb-method-cursor.toArray)

### Use Variables in `let` Option

You can specify query options to modify query behavior and indicate how results are returned.

For example, to define variables that you can access elsewhere in the `find` method, use the `let` option. To filter results using a variable, you must access the variable within the [`$expr`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/query/expr/#mongodb-query-op.-expr) operator.

Create a collection `cakeFlavors`:

```javascript
db.cakeFlavors.insertMany( [
   { _id: 1, flavor: "chocolate" },
   { _id: 2, flavor: "strawberry" },
   { _id: 3, flavor: "cherry" }
] )
```

The following example defines a `targetFlavor` variable in `let` and uses the variable to retrieve the chocolate cake flavor:

```javascript
db.cakeFlavors.find(
   { $expr: { $eq: [ "$flavor", "$$targetFlavor" ] } },
   { _id: 0 },
   { let : { targetFlavor: "chocolate" }
} )
```

Output:

```javascript
[ { flavor: 'chocolate' } ]
```

### Retrieve Documents for Roles Granted to the Current User

Starting in MongoDB 7.0, you can use the new [`USER_ROLES`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/aggregation-variables/#mongodb-variable-variable.USER_ROLES) system variable to return user [roles](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/authorization/#std-label-roles).

The scenario in this section shows users with various roles who have limited access to documents in a collection containing budget information.

The scenario shows one possible use of `USER_ROLES`. The `budget` collection contains documents with a field named `allowedRoles`. As you'll see in the following scenario, you can write queries that compare the user roles found in the `allowedRoles` field with the roles returned by the `USER_ROLES` system variable.

For another `USER_ROLES` example scenario, see [Retrieve Medical Information for Roles Granted to the Current User](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/views/create-view/#std-label-create-view-user-roles-system-variable-medical-example). That example doesn't store the user roles in the document fields, as is done in the following example.

For the budget scenario in this section, perform the following steps to create the roles, users, and `budget` collection:

#### Create the roles

Run:

```javascript
db.createRole( { role: "Marketing", roles: [], privileges: [] } )
db.createRole( { role: "Sales", roles: [], privileges: [] } )
db.createRole( { role: "Development", roles: [], privileges: [] } )
db.createRole( { role: "Operations", roles: [], privileges: [] } )
```

#### Create the users

Create users named `John` and `Jane` with the required roles. Replace the `test` database with your database name.

```javascript
db.createUser( {
   user: "John",
   pwd: "jn008",
   roles: [
      { role: "Marketing", db: "test" },
      { role: "Development", db: "test" },
      { role: "Operations", db: "test" },
      { role: "read", db: "test" }
   ]
} )

db.createUser( {
   user: "Jane",
   pwd: "je009",
   roles: [
      { role: "Sales", db: "test" },
      { role: "Operations", db: "test" },
      { role: "read", db: "test" }
   ]
} )
```

#### Create the collection

Run:

```javascript
db.budget.insertMany( [
   {
      _id: 0,
      allowedRoles: [ "Marketing" ],
      comment: "For marketing team",
      yearlyBudget: 15000
   },
   {
      _id: 1,
      allowedRoles: [ "Sales" ],
      comment: "For sales team",
      yearlyBudget: 17000,
      salesEventsBudget: 1000
   },
   {
      _id: 2,
      allowedRoles: [ "Operations" ],
      comment: "For operations team",
      yearlyBudget: 19000,
      cloudBudget: 12000
   },
   {
      _id: 3,
      allowedRoles: [ "Development" ],
      comment: "For development team",
      yearlyBudget: 27000
   }
] )
```

Perform the following steps to retrieve the documents accessible to `John`:

#### Log in as John

Run:

```javascript
db.auth( "John", "jn008" )
```

#### Retrieve the documents

To use a system variable, add `$$` to the start of the variable name. Specify the `USER_ROLES` system variable as `$$USER_ROLES`.

Run:

```javascript
db.budget.find( {
   $expr: {
      $not: {
         $eq: [ { $setIntersection: [ "$allowedRoles", "$$USER_ROLES.role" ] }, [] ]
      }
   }
} )
```

The previous example returns the documents from the `budget` collection that match at least one of the roles that the user who runs the example has. To do that, the example uses [`$setIntersection`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/operator/aggregation/setIntersection/#mongodb-expression-exp.-setIntersection) to return documents where the intersection between the `budget` document `allowedRoles` field and the set of user roles from `$$USER_ROLES` is not empty.

#### Examine the documents

`John` has the `Marketing`, `Operations`, and `Development` roles, and sees these documents:

```javascript
[
   {
      _id: 0,
      allowedRoles: [ 'Marketing' ],
      comment: 'For marketing team',
      yearlyBudget: 15000
   },
   {
      _id: 2,
      allowedRoles: [ 'Operations' ],
      comment: 'For operations team',
      yearlyBudget: 19000,
      cloudBudget: 12000
   },
   {
      _id: 3,
      allowedRoles: [ 'Development' ],
      comment: 'For development team',
      yearlyBudget: 27000
   }
]
```

Perform the following steps to retrieve the documents accessible to `Jane`:

#### Log in as Jane

Run:

```javascript
db.auth( "Jane", "je009" )
```

#### Retrieve the documents

Run:

```javascript
db.budget.find( {
   $expr: {
      $not: {
         $eq: [ { $setIntersection: [ "$allowedRoles", "$$USER_ROLES.role" ] }, [] ]
      }
   }
} )
```

#### Examine the documents

`Jane` has the `Sales` and `Operations` roles, and sees these documents:

```javascript
[
   {
      _id: 1,
      allowedRoles: [ 'Sales' ],
      comment: 'For sales team',
      yearlyBudget: 17000,
      salesEventsBudget: 1000
   },
   {
      _id: 2,
      allowedRoles: [ 'Operations' ],
      comment: 'For operations team',
      yearlyBudget: 19000,
      cloudBudget: 12000
   }
]
```

On a sharded cluster, a query can be run on a shard by another server node on behalf of the user. In those queries, `USER_ROLES` is still populated with the roles for the user.

### Modify a Query with options

The following examples show how you can use the `options` field in a `find()` query. Use the following [`insertMany()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.insertMany/#mongodb-method-db.collection.insertMany) to setup the `users` collection:

```javascript
db.users.insertMany( [
   { username: "david", age: 27 },
   { username: "amanda", age: 25 },
   { username: "rajiv", age: 32 },
   { username: "rajiv", age: 90 }
] )
```

#### limit with options

The following query limits the number of documents in the result set with the `limit` options parameter:

```javascript
db.users.find(
   { username : "rajiv"}, // query
   { age : 1 }, // projection
   { limit : 1 } // options
)
```

#### allowDiskUse with options

The following query uses the `options` parameter to enable `allowDiskUse`:

```javascript
db.users.find(
   { username : "david" },
   { age : 1 },
   { allowDiskUse : true }
)
```

#### explain with options

The following query uses the `options` parameter to get the `executionStats` explain output:

```javascript
var cursor = db.users.find(
   { username: "amanda" },
   { age : 1 },
   { explain : "executionStats" }
)
cursor.next()
```

#### Specify Multiple options in a query

The following query uses multiple `options` in a single query. This query uses `limit` set to `2` to return only two documents, and `showRecordId` set to `true` to return the position of the document in the result set:

```javascript
db.users.find(
   {},
   { username: 1, age: 1 },
   {
     limit: 2,
     showRecordId: true
   }
)
```

## Learn More

- [`findOne()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.findOne/#mongodb-method-db.collection.findOne)

- [`findAndModify()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.findAndModify/#mongodb-method-db.collection.findAndModify)

- [`findOneAndDelete()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.findOneAndDelete/#mongodb-method-db.collection.findOneAndDelete)

- [`findOneAndReplace()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.findOneAndReplace/#mongodb-method-db.collection.findOneAndReplace)

