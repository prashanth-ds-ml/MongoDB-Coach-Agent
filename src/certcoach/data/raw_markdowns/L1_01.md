# db.collection.insertOne() (mongosh method)

This page documents a [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) method. To see the equivalent method in a MongoDB driver, see the corresponding page for your programming language:

## Definition

`db.collection.insertOne()`
[`insert`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/command/insert/#mongodb-dbcommand-dbcmd.insert) commandInserts a single document into a collection.

A document containing:

- A boolean `acknowledged` as `true` if the operation ran with [write concern](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/glossary/#std-term-write-concern) or `false` if write concern was disabled.

- A field `insertedId` with the `_id` value of the inserted document.

## Compatibility

`insertOne()`This method is available in deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

This command is supported in all MongoDB Atlas clusters. For information on Atlas support for all commands, see [Unsupported Commands](https://www.mongodb.com/docs/atlas/unsupported-commands/).

- [MongoDB Enterprise](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

`db.collection.insertOne()` has the following form:

```javascript
db.collection.insertOne(
    <document>,
    {
      writeConcern: <document>
    }
)
```

### Parameters

`insertOne()` takes the following parameters:

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
`document`

</td>
<td headers="Type">
document

</td>
<td headers="Description">
A document to insert into the collection.

</td>
</tr>
<tr>
<td headers="Parameter">
`writeConcern`

</td>
<td headers="Type">
document

</td>
<td headers="Description">
Optional. A document expressing the [write concern](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/write-concern/). Omit to use the default write concern.

Do not explicitly set the write concern for the operation if run in a transaction. To use write concern with transactions, see [Transactions and Write Concern](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/transactions/#std-label-transactions-write-concern).

</td>
</tr>
</table>

## Behaviors

### Collection and `_id` Field Creation

`insertOne()`If the collection does not exist, then `insertOne()` creates the collection.

If the document to insert does not specify an [_id](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/glossary/#std-term-_id) field, then [`mongod`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/program/mongod/#mongodb-binary-bin.mongod) adds the `_id` field and assigns a unique [`ObjectId()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/ObjectId/#mongodb-method-ObjectId) for the document. Most drivers create an ObjectId and insert the `_id` field, but the [`mongod`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/program/mongod/#mongodb-binary-bin.mongod) will create and populate the `_id` if the driver or application does not.

If the document contains an `_id` field, the `_id` value must be unique within the collection to avoid duplicate key error.

### Explainability

`insertOne()` is not compatible with [`db.collection.explain()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/db.collection.explain/#mongodb-method-db.collection.explain).

### Error Handling

On error, `insertOne()` throws either a `writeError` or `writeConcernError` exception.

#### Schema Validation Errors

If your collection uses [schema validation](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/schema-validation/#std-label-schema-validation-overview) and has `validationAction` set to `error`, inserting an invalid document throws a `MongoServerError` and `insertOne()` fails.

### Transactions

`insertOne()` can be used inside [distributed transactions](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/transactions/#std-label-transactions).

In most cases, a distributed transaction incurs a greater performance cost over single document writes, and the availability of distributed transactions should not be a replacement for effective schema design. For many scenarios, the [denormalized data model (embedded documents and arrays)](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/data-modeling/embedding/#std-label-data-modeling-embedding) will continue to be optimal for your data and use cases. That is, for many scenarios, modeling your data appropriately will minimize the need for distributed transactions.

For additional transactions usage considerations (such as runtime limit and oplog size limit), see also [Production Considerations](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/transactions-production-consideration/#std-label-production-considerations).

#### Collection Creation in Transactions

You can create collections and indexes inside a [distributed transaction](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/transactions/#std-label-transactions-create-collections-indexes) if the transaction is not a cross-shard write transaction.

If you specify an insert on a non-existing collection in a transaction, MongoDB creates the collection implicitly.

#### Write Concerns and Transactions

Do not explicitly set the write concern for the operation if run in a transaction. To use write concern with transactions, see [Transactions and Write Concern](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/core/transactions/#std-label-transactions-write-concern).

`insertOne()`

### Oplog Entries

If an `insertOne()` operation successfully inserts a document, the operation adds an entry on the [oplog](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/glossary/#std-term-oplog) (operations log). If the operation fails, the operation does not add an entry on the oplog.

## Examples

### Insert a Document without Specifying an `_id` Field

In the following example, the document passed to `insertOne()` does not contain the `_id` field:

```javascript
try {
   db.products.insertOne( { item: "card", qty: 15 } );
} catch (e) {
   print (e);
};
```

The operation returns the following document:

```javascript
{
   "acknowledged" : true,
   "insertedId" : ObjectId("56fc40f9d735c28df206d078")
}
```

Because the documents did not include `_id`, [`mongod`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/program/mongod/#mongodb-binary-bin.mongod) creates and adds the `_id` field and assigns it a unique [`ObjectId()`](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/method/ObjectId/#mongodb-method-ObjectId) value.

The `ObjectId` values are specific to the machine and time when the operation is run. As such, your values may differ from those in the example.

### Insert a Document Specifying an `_id` Field

In the following example, the document passed to `insertOne()` includes the `_id` field. The value of `_id` must be unique within the collection to avoid duplicate key error.

```javascript
try {
   db.products.insertOne( { _id: 10, item: "box", qty: 20 } );
} catch (e) {
   print (e);
}
```

The operation returns the following:

```javascript
{ "acknowledged" : true, "insertedId" : 10 }
```

Inserting an duplicate value for any key that is part of a [unique index](https://mongodbcom-cdn.staging.corp.mongodb.com/docs/reference/glossary/#std-term-unique-index), such as `_id`, throws an exception. The following attempts to insert a document with a `_id` value that already exists:

```javascript
try {
   db.products.insertOne( { _id: 10, "item" : "packing peanuts", "qty" : 200 } );
} catch (e) {
   print (e);
}
```

Since `_id: 10` already exists, the following exception is thrown:

```javascript
WriteError({
   "index" : 0,
   "code" : 11000,
   "errmsg" : "E11000 duplicate key error collection: inventory.products index: _id_ dup key: { : 10.0 }",
   "op" : {
      "_id" : 10,
      "item" : "packing peanuts",
      "qty" : 200
   }
})
```

### Increase Write Concern

Given a three member replica set, the following operation specifies a `w` of `majority`, `wtimeout` of `100`:

```javascript
try {
   db.products.insertOne(
       { "item": "envelopes", "qty": 100, type: "Self-Sealing" },
       { writeConcern: { w: "majority", wtimeout: 100 } }
   );
} catch (e) {
   print (e);
}
```

If the acknowledgment takes longer than the `wtimeout` limit, the following exception is thrown:

```javascript
WriteConcernError({
   "code" : 64,
   "errmsg" : "waiting for replication timed out",
   "errInfo" : {
     "wtimeout" : true,
     "writeConcern" : {
       "w" : "majority",
       "wtimeout" : 100,
       "provenance" : "getLastErrorDefaults"
     }
   }
})
```

