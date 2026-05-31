# db.collection.insertMany() (mongosh method)

## Definition

`db.collection.insertMany()`
`insert` commandInserts multiple documents into a collection.

A document containing:

- An `acknowledged` boolean, set to `true` if the operation ran with write concern or `false` if write concern was disabled

- An `insertedIds` array, containing `_id` values for each successfully inserted document

## Syntax

`db.collection.insertMany()` has the following syntax:

```javascript
db.collection.insertMany(
   [ <document 1> , <document 2>, ... ],
   {
      writeConcern: <document>,
      ordered: <boolean>
   }
)
```

### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `document` | document | An array of documents to insert into the collection. |
| `writeConcern` | document | Optional. A document expressing the write concern. Omit to use the default write concern. Do not explicitly set the write concern for the operation if run in a transaction. To use write concern with transactions, see Transactions and Write Concern. |
| `ordered` | boolean | Optional. A boolean specifying whether the `mongod` instance should perform an ordered or unordered insert. Defaults to `true`. |

## Behaviors

Given an array of documents, `insertMany()` inserts each document in the array into the collection. There is no limit to the number of documents you can specify in the array.

### Execution of Operations

By default, documents are inserted in the order they are provided.

- If `ordered` is set to `true` and an insert fails, the server does not continue inserting records.

- If `ordered` is set to `false` and an insert fails, the server continues inserting records. Documents may be reordered by `mongod` to increase performance. Applications should not depend on ordering of inserts if using an unordered `insertMany()`.

Executing an `ordered` list of operations on a sharded collection will generally be slower than executing an `unordered` list since with an ordered list, each operation must wait for the previous operation to finish.

### Limits & Batching

The driver batches documents specified in the `insertMany()` array and there is no limit to the amount of documents the database can handle. The driver groups data into batches according to the maxWriteBatchSize, which is 100,000 and cannot be modified. For example, if the `insertMany()` operation contains 250,000 documents, the driver creates three batches: two with 100,000 documents and one with 50,000 documents.

The driver only performs batching when using the high-level API. If you use `db.runCommand()` directly (for example, when writing a driver), MongoDB throws an error when attempting to execute a write batch that exceeds the `maxWriteBatchSize` limit.

If the error report for a single batch grows too large, MongoDB truncates all remaining error messages. If there are at least two error messages with size greater than `1MB`, those messages are truncated.

The sizes and grouping mechanics are internal performance details and are subject to change in future versions.

### Collection and `_id` Field Creation

`insertMany()`If the collection does not exist, then `insertMany()` creates the collection.

If the document to insert does not specify an _id field, then `mongod` adds the `_id` field and assigns a unique `ObjectId()` for the document. Most drivers create an ObjectId and insert the `_id` field, but the `mongod` will create and populate the `_id` if the driver or application does not.

If the document contains an `_id` field, the `_id` value must be unique within the collection to avoid duplicate key error.

### Explainability

`insertMany()` is not compatible with `db.collection.explain()`.

### Error Handling

Inserts throw a `BulkWriteError` exception.

Excluding write concern errors, ordered operations stop after an error, while unordered operations continue to process any remaining write operations in the queue.

Write concern errors are displayed in the `writeConcernErrors` field, while all other errors are displayed in the `writeErrors` field. If an error is encountered, the number of successful write operations are displayed instead of a list of inserted _ids. Ordered operations display the single error encountered while unordered operations display each error in an array.

#### Schema Validation Errors

If your collection uses schema validation and has `validationAction` set to `error`, inserting an invalid document with `insertMany()` throws a `writeError`. Documents that precede the invalid document in the `documents` array are written to the collection. The value of the `ordered` field determines if the remaining valid documents are inserted.

### Transactions

`insertMany()` can be used inside distributed transactions.

In most cases, a distributed transaction incurs a greater performance cost over single document writes, and the availability of distributed transactions should not be a replacement for effective schema design. For many scenarios, the denormalized data model (embedded documents and arrays) will continue to be optimal for your data and use cases. That is, for many scenarios, modeling your data appropriately will minimize the need for distributed transactions.

For additional transactions usage considerations (such as runtime limit and oplog size limit), see also Production Considerations.

#### Collection Creation in Transactions

You can create collections and indexes inside a distributed transaction if the transaction is not a cross-shard write transaction.

If you specify an insert on a non-existing collection in a transaction, MongoDB creates the collection implicitly.

#### Write Concerns and Transactions

Do not explicitly set the write concern for the operation if run in a transaction. To use write concern with transactions, see Transactions and Write Concern.

`insertMany()`

### Performance Consideration for Random Data

If an operation inserts a large amount of random data (for example, hashed indexes) on an indexed field, insert performance may decrease. Bulk inserts of random data create random index entries, which increase the size of the index. If the index reaches the size that requires each random insert to access a different index entry, the inserts result in a high rate of WiredTiger cache eviction and replacement. When this happens, the index is no longer fully in cache and is updated on disk, which decreases performance.

To improve the performance of bulk inserts of random data on indexed fields, you can either:

- Drop the index, then recreate it after you insert the random data.

- Insert the data into an empty unindexed collection.

Creating the index after the bulk insert sorts the data in memory and performs an ordered insert on all indexes.

### Oplog Entries

MongoDB consolidates operations that insert multiple documents, such as `insertMany()` or multiple `insertOne()` commands within a `db.collection.bulkWrite()` operation, into a single entry in the oplog. If the operation fails, the operation does not add an entry on the oplog.

## Examples

The following examples insert documents into the `products` collection.

### Insert Several Documents without Specifying an `_id` Field

The following example uses `insertMany()` to insert documents that do not contain the `_id` field:

```javascript
try {
   db.products.insertMany( [
      { item: "card", qty: 15 },
      { item: "envelope", qty: 20 },
      { item: "stamps" , qty: 30 }
   ] );
} catch (e) {
   print (e);
}
```

The operation returns the following document:

```javascript
{
   "acknowledged" : true,
   "insertedIds" : [
      ObjectId("562a94d381cb9f1cd6eb0e1a"),
      ObjectId("562a94d381cb9f1cd6eb0e1b"),
      ObjectId("562a94d381cb9f1cd6eb0e1c")
   ]
}
```

Because the documents did not include `_id`, `mongod` creates and adds the `_id` field for each document and assigns it a unique `ObjectId()` value.

The `ObjectId` values are specific to the machine and time when the operation is run. As such, your values may differ from those in the example.

### Insert Several Document Specifying an `_id` Field

The following example uses `insertMany()` to insert documents that include the `_id` field. The value of `_id` must be unique within the collection to avoid a duplicate key error.

```javascript
try {
   db.products.insertMany( [
      { _id: 10, item: "large box", qty: 20 },
      { _id: 11, item: "small box", qty: 55 },
      { _id: 12, item: "medium box", qty: 30 }
   ] );
} catch (e) {
   print (e);
}
```

The operation returns the following document:

```javascript
{ "acknowledged" : true, "insertedIds" : [ 10, 11, 12 ] }
```

Inserting a duplicate value for any key that is part of a unique index, such as `_id`, throws an exception. The following attempts to insert a document with a `_id` value that already exists:

```javascript
try {
   db.products.insertMany( [
      { _id: 13, item: "envelopes", qty: 60 },
      { _id: 13, item: "stamps", qty: 110 },
      { _id: 14, item: "packing tape", qty: 38 }
   ] );
} catch (e) {
   print (e);
}
```

Since `_id: 13` already exists, the following exception is thrown:

```javascript
BulkWriteError({
   "writeErrors" : [
      {
         "index" : 0,
         "code" : 11000,
         "errmsg" : "E11000 duplicate key error collection: inventory.products index: _id_ dup key: { : 13.0 }",
         "op" : {
            "_id" : 13,
            "item" : "stamps",
            "qty" : 110
         }
      }
   ],
   "writeConcernErrors" : [ ],
   "nInserted" : 1,
   "nUpserted" : 0,
   "nMatched" : 0,
   "nModified" : 0,
   "nRemoved" : 0,
   "upserted" : [ ]
})
```

Note that one document was inserted: The first document of `_id: 13` will insert successfully, but the second insert will fail. This will also stop additional documents left in the queue from being inserted.

With `ordered` to `false`, the insert operation would continue with any remaining documents.

### Unordered Inserts

The following attempts to insert multiple documents with `_id` field and `ordered: false`. The array of documents contains two documents with duplicate `_id` fields.

```javascript
try {
   db.products.insertMany( [
      { _id: 10, item: "large box", qty: 20 },
      { _id: 11, item: "small box", qty: 55 },
      { _id: 11, item: "medium box", qty: 30 },
      { _id: 12, item: "envelope", qty: 100},
      { _id: 13, item: "stamps", qty: 125 },
      { _id: 13, item: "tape", qty: 20},
      { _id: 14, item: "bubble wrap", qty: 30}
   ], { ordered: false } );
} catch (e) {
   print (e);
}
```

The operation throws the following exception:

```javascript
BulkWriteError({
   "writeErrors" : [
      {
         "index" : 2,
         "code" : 11000,
         "errmsg" : "E11000 duplicate key error collection: inventory.products index: _id_ dup key: { : 11.0 }",
         "op" : {
            "_id" : 11,
            "item" : "medium box",
            "qty" : 30
         }
      },
      {
         "index" : 5,
         "code" : 11000,
         "errmsg" : "E11000 duplicate key error collection: inventory.products index: _id_ dup key: { : 13.0 }",
         "op" : {
            "_id" : 13,
            "item" : "tape",
            "qty" : 20
         }
      }
   ],
   "writeConcernErrors" : [ ],
   "nInserted" : 5,
   "nUpserted" : 0,
   "nMatched" : 0,
   "nModified" : 0,
   "nRemoved" : 0,
   "upserted" : [ ]
})
```

While the document with `item: "medium box"` and `item: "tape"` failed to insert due to duplicate `_id` values, `nInserted` shows that the remaining 5 documents were inserted.

### Using Write Concern

Given a three member replica set, the following operation specifies a `w` of `majority` and `wtimeout` of `100`:

```javascript
try {
   db.products.insertMany(
      [
         { _id: 10, item: "large box", qty: 20 },
         { _id: 11, item: "small box", qty: 55 },
         { _id: 12, item: "medium box", qty: 30 }
      ],
      { w: "majority", wtimeout: 100 }
   );
} catch (e) {
   print (e);
}
```

If the primary and at least one secondary acknowledge each write operation within 100 milliseconds, it returns:

```javascript
{
  "acknowledged" : true,
  "insertedIds" : [
     ObjectId("562a94d381cb9f1cd6eb0e1a"),
     ObjectId("562a94d381cb9f1cd6eb0e1b"),
     ObjectId("562a94d381cb9f1cd6eb0e1c")
  ]
}
```

If the total time required for all required nodes in the replica set to acknowledge the write operation is greater than `wtimeout`, the following `writeConcernError` is displayed when the `wtimeout` period has passed.

This operation returns:

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
