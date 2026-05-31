> Source: https://www.mongodb.com/docs/manual/tutorial/update-documents/
> Fetch method: direct_markdown

# Update Documents

You can update documents using:

- Your programming language's driver

- The MongoDB Atlas UI (see Update a Document with MongoDB Atlas)

- MongoDB Compass

➤➤ Use the **Select your language** drop-down menu in the upper-right to set the language of the following examples.

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

<Tabs>

<Tab name="MongoDB Shell">

This page uses the following `mongosh` methods:

- `db.collection.updateOne(<filter>, <update>, <options>)`

- `db.collection.updateMany(<filter>, <update>, <options>)`

- `db.collection.replaceOne(<filter>, <update>, <options>)`

The examples on this page use the `movies` collection from the `sample_mflix` database. To learn how to load the sample dataset into your deployment, see Load Sample Data.

</Tab>

<Tab name="Compass">

This page uses MongoDB Compass to update documents.

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C">

This page uses the following MongoDB C Driver methods:

- mongoc_collection_update_one

- mongoc_collection_replace_one

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C#">

This page uses the following MongoDB C# Driver methods:

- IMongoCollection.UpdateOne()

- IMongoCollection.UpdateMany()

- IMongoCollection.ReplaceOne()

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Go">

This page uses the following MongoDB Go Driver functions:

- Collection.UpdateOne

- Collection.UpdateMany

- Collection.ReplaceOne

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Async)">

This page uses the following Java Reactive Streams Driver methods:

- com.mongodb.reactivestreams.client.MongoCollection.updateOne)

- com.mongodb.reactivestreams.client.MongoCollection.updateMany)

- com.mongodb.reactivestreams.client.MongoCollection.replaceOne)

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Sync)">

This page uses the following Java Synchronous Driver methods:

- com.mongodb.client.MongoCollection.updateOne

- com.mongodb.client.MongoCollection.updateMany

- com.mongodb.client.MongoCollection.replaceOne

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Kotlin (Coroutine)">

This page uses the following Kotlin Coroutine Driver methods:

- MongoCollection.updateOne()

- MongoCollection.updateMany()

- MongoCollection.replaceOne()

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Motor">

This page uses the following Motor driver methods:

- `motor.motor_asyncio.AsyncIOMotorCollection.update_one`

- `motor.motor_asyncio.AsyncIOMotorCollection.update_many`

- `motor.motor_asyncio.AsyncIOMotorCollection.replace_one`

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Node.js">

This page uses the following MongoDB Node.js Driver methods:

- Collection.updateOne()

- Collection.updateMany()

- Collection.replaceOne()

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="PHP">

This page uses the following  MongoDB PHP Library methods:

- `MongoDB\\Collection::updateOne()`

- `MongoDB\\Collection::updateMany()`

- `MongoDB\\Collection::replaceOne()`

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Python">

This page uses the following PyMongo Python driver methods:

- `pymongo.collection.Collection.update_one`

- `pymongo.collection.Collection.update_many`

- `pymongo.collection.Collection.replace_one`

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Ruby">

This page uses the following MongoDB Ruby Driver methods:

- Mongo::Collection#update_one()

- Mongo::Collection#update_many()

- Mongo::Collection#replace_one()

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Scala">

This page uses the following  MongoDB Scala Driver methods:

- collection.updateOne():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult])

- collection.updateMany():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult])

- collection.replaceOne():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult])

The examples use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The following examples use the `movies` collection from the `sample_mflix` database. To learn how to load the sample dataset into your deployment, see Load Sample Data.

</Tab>

<Tab name="Compass">

```javascript
[
    { "item": "canvas", "qty": 100, "size": { "h": 28, "w": 35.5, "uom": "cm" }, "status": "A" },
    { "item": "journal", "qty": 25, "size": { "h": 14, "w": 21, "uom": "cm" }, "status": "A" },
    { "item": "mat", "qty": 85, "size": { "h": 27.9, "w": 35.5, "uom": "cm" }, "status": "A" },
    { "item": "mousepad", "qty": 25, "size": { "h": 19, "w": 22.85, "uom": "cm" }, "status": "P" },
    { "item": "notebook", "qty": 50, "size": { "h": 8.5, "w": 11, "uom": "in" }, "status": "P" },
    { "item": "paper", "qty": 100, "size": { "h": 8.5, "w": 11, "uom": "in" }, "status": "D" },
    { "item": "planner", "qty": 75, "size": { "h": 22.85, "w": 30, "uom": "cm" }, "status": "D" },
    { "item": "postcard", "qty": 45, "size": { "h": 10, "w": 15.25, "uom": "cm" }, "status": "A" },
    { "item": "sketchbook", "qty": 80, "size": { "h": 14, "w": 21, "uom": "cm" }, "status": "A" },
    { "item": "sketch pad", "qty": 95, "size": { "h": 22.85, "w": 30.5, "uom": "cm" }, "status": "A" }
]
```

For instructions on inserting documents using MongoDB Compass, see Insert Documents.

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
mongoc_bulk_operation_t *bulk;
bson_t *doc;
bool r;
bson_error_t error;
bson_t reply;

collection = mongoc_database_get_collection (db, "inventory");
bulk = mongoc_collection_create_bulk_operation_with_opts (collection, NULL);
doc = BCON_NEW (
   "item", BCON_UTF8 ("canvas"),
   "qty", BCON_INT64 (100),
   "size", "{",
   "h", BCON_DOUBLE (28),
   "w", BCON_DOUBLE (35.5),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "status", BCON_UTF8 ("A"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("journal"),
   "qty", BCON_INT64 (25),
   "size", "{",
   "h", BCON_DOUBLE (14),
   "w", BCON_DOUBLE (21),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "status", BCON_UTF8 ("A"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("mat"),
   "qty", BCON_INT64 (85),
   "size", "{",
   "h", BCON_DOUBLE (27.9),
   "w", BCON_DOUBLE (35.5),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "status", BCON_UTF8 ("A"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("mousepad"),
   "qty", BCON_INT64 (25),
   "size", "{",
   "h", BCON_DOUBLE (19),
   "w", BCON_DOUBLE (22.85),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "status", BCON_UTF8 ("P"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("notebook"),
   "qty", BCON_INT64 (50),
   "size", "{",
   "h", BCON_DOUBLE (8.5),
   "w", BCON_DOUBLE (11),
   "uom", BCON_UTF8 ("in"),
   "}",
   "status", BCON_UTF8 ("P"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("paper"),
   "qty", BCON_INT64 (100),
   "size", "{",
   "h", BCON_DOUBLE (8.5),
   "w", BCON_DOUBLE (11),
   "uom", BCON_UTF8 ("in"),
   "}",
   "status", BCON_UTF8 ("D"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("planner"),
   "qty", BCON_INT64 (75),
   "size", "{",
   "h", BCON_DOUBLE (22.85),
   "w", BCON_DOUBLE (30),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "status", BCON_UTF8 ("D"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("postcard"),
   "qty", BCON_INT64 (45),
   "size", "{",
   "h", BCON_DOUBLE (10),
   "w", BCON_DOUBLE (15.25),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "status", BCON_UTF8 ("A"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("sketchbook"),
   "qty", BCON_INT64 (80),
   "size", "{",
   "h", BCON_DOUBLE (14),
   "w", BCON_DOUBLE (21),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "status", BCON_UTF8 ("A"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("sketch pad"),
   "qty", BCON_INT64 (95),
   "size", "{",
   "h", BCON_DOUBLE (22.85),
   "w", BCON_DOUBLE (30.5),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "status", BCON_UTF8 ("A"));

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

/* "reply" is initialized on success or error */
r = (bool) mongoc_bulk_operation_execute (bulk, &reply, &error);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
}
```

</Tab>

<Tab name="C#">

```csharp
var documents = new[]
{
    new BsonDocument
    {
        { "item", "canvas" },
        { "qty", 100 },
        { "size", new BsonDocument { { "h", 28 }, { "w", 35.5 }, { "uom", "cm" } } },
        { "status", "A" }
    },
    new BsonDocument
    {
        { "item", "journal" },
        { "qty", 25 },
        { "size", new BsonDocument { { "h", 14 }, { "w", 21 }, { "uom", "cm" } } },
        { "status", "A" }
    },
    new BsonDocument
    {
        { "item", "mat" },
        { "qty", 85 },
        { "size", new BsonDocument { { "h", 27.9 }, { "w", 35.5 }, { "uom", "cm" } } },
        { "status", "A" }
    },
    new BsonDocument
    {
        { "item", "mousepad" },
        { "qty", 25 },
        { "size", new BsonDocument { { "h", 19 }, { "w", 22.85 }, { "uom", "cm" } } },
        { "status", "P" }
    },
    new BsonDocument
    {
        { "item", "notebook" },
        { "qty", 50 },
        { "size", new BsonDocument { { "h", 8.5 }, { "w", 11 }, { "uom", "in" } } },
        { "status", "P" } },
    new BsonDocument
    {
        { "item", "paper" },
        { "qty", 100 },
        { "size", new BsonDocument { { "h", 8.5 }, { "w", 11 }, { "uom", "in" } } },
        { "status", "D" }
    },
    new BsonDocument
    {
        { "item", "planner" },
        { "qty", 75 },
        { "size", new BsonDocument { { "h", 22.85 }, { "w", 30 }, { "uom", "cm" } } },
        { "status", "D" }
    },
    new BsonDocument
    {
        { "item", "postcard" },
        { "qty", 45 },
        { "size", new BsonDocument { { "h", 10 }, { "w", 15.25 }, { "uom", "cm" } } },
        { "status", "A" }
    },
    new BsonDocument
    {
        { "item", "sketchbook" },
        { "qty", 80 },
        { "size", new BsonDocument { { "h", 14 }, { "w", 21 }, { "uom", "cm" } } },
        { "status", "A" }
    },
    new BsonDocument
    {
        { "item", "sketch pad" },
        { "qty", 95 },
        { "size", new BsonDocument { { "h", 22.85 }, { "w", 30.5 }, { "uom", "cm" } } }, { "status", "A" } },
};
collection.InsertMany(documents);
```

</Tab>

<Tab name="Go">

```go

docs := []any{
	bson.D{
		{"item", "canvas"},
		{"qty", 100},
		{"size", bson.D{
			{"h", 28},
			{"w", 35.5},
			{"uom", "cm"},
		}},
		{"status", "A"},
	},
	bson.D{
		{"item", "journal"},
		{"qty", 25},
		{"size", bson.D{
			{"h", 14},
			{"w", 21},
			{"uom", "cm"},
		}},
		{"status", "A"},
	},
	bson.D{
		{"item", "mat"},
		{"qty", 85},
		{"size", bson.D{
			{"h", 27.9},
			{"w", 35.5},
			{"uom", "cm"},
		}},
		{"status", "A"},
	},
	bson.D{
		{"item", "mousepad"},
		{"qty", 25},
		{"size", bson.D{
			{"h", 19},
			{"w", 22.85},
			{"uom", "in"},
		}},
		{"status", "P"},
	},
	bson.D{
		{"item", "notebook"},
		{"qty", 50},
		{"size", bson.D{
			{"h", 8.5},
			{"w", 11},
			{"uom", "in"},
		}},
		{"status", "P"},
	},
	bson.D{
		{"item", "paper"},
		{"qty", 100},
		{"size", bson.D{
			{"h", 8.5},
			{"w", 11},
			{"uom", "in"},
		}},
		{"status", "D"},
	},
	bson.D{
		{"item", "planner"},
		{"qty", 75},
		{"size", bson.D{
			{"h", 22.85},
			{"w", 30},
			{"uom", "cm"},
		}},
		{"status", "D"},
	},
	bson.D{
		{"item", "postcard"},
		{"qty", 45},
		{"size", bson.D{
			{"h", 10},
			{"w", 15.25},
			{"uom", "cm"},
		}},
		{"status", "A"},
	},
	bson.D{
		{"item", "sketchbook"},
		{"qty", 80},
		{"size", bson.D{
			{"h", 14},
			{"w", 21},
			{"uom", "cm"},
		}},
		{"status", "A"},
	},
	bson.D{
		{"item", "sketch pad"},
		{"qty", 95},
		{"size", bson.D{
			{"h", 22.85},
			{"w", 30.5},
			{"uom", "cm"},
		}},
		{"status", "A"},
	},
}

result, err := coll.InsertMany(context.TODO(), docs)

```

</Tab>

<Tab name="Java (Async)">

```java
Publisher<Success> insertManyPublisher = collection.insertMany(asList(
        Document.parse("{ item: 'canvas', qty: 100, size: { h: 28, w: 35.5, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'journal', qty: 25, size: { h: 14, w: 21, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'mat', qty: 85, size: { h: 27.9, w: 35.5, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'mousepad', qty: 25, size: { h: 19, w: 22.85, uom: 'cm' }, status: 'P' }"),
        Document.parse("{ item: 'notebook', qty: 50, size: { h: 8.5, w: 11, uom: 'in' }, status: 'P' }"),
        Document.parse("{ item: 'paper', qty: 100, size: { h: 8.5, w: 11, uom: 'in' }, status: 'D' }"),
        Document.parse("{ item: 'planner', qty: 75, size: { h: 22.85, w: 30, uom: 'cm' }, status: 'D' }"),
        Document.parse("{ item: 'postcard', qty: 45, size: { h: 10, w: 15.25, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'sketchbook', qty: 80, size: { h: 14, w: 21, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'sketch pad', qty: 95, size: { h: 22.85, w: 30.5, uom: 'cm' }, status: 'A' }")
));
```

</Tab>

<Tab name="Java (Sync)">

```java
collection.insertMany(asList(
        Document.parse("{ item: 'canvas', qty: 100, size: { h: 28, w: 35.5, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'journal', qty: 25, size: { h: 14, w: 21, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'mat', qty: 85, size: { h: 27.9, w: 35.5, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'mousepad', qty: 25, size: { h: 19, w: 22.85, uom: 'cm' }, status: 'P' }"),
        Document.parse("{ item: 'notebook', qty: 50, size: { h: 8.5, w: 11, uom: 'in' }, status: 'P' }"),
        Document.parse("{ item: 'paper', qty: 100, size: { h: 8.5, w: 11, uom: 'in' }, status: 'D' }"),
        Document.parse("{ item: 'planner', qty: 75, size: { h: 22.85, w: 30, uom: 'cm' }, status: 'D' }"),
        Document.parse("{ item: 'postcard', qty: 45, size: { h: 10, w: 15.25, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'sketchbook', qty: 80, size: { h: 14, w: 21, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'sketch pad', qty: 95, size: { h: 22.85, w: 30.5, uom: 'cm' }, status: 'A' }")
));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
collection.insertMany(
    listOf(
        Document("item", "canvas")
            .append("qty", 100)
            .append("size", Document("h", 28).append("w", 35.5).append("uom", "cm"))
            .append("status", "A"),
        Document("item", "journal")
            .append("qty", 25)
            .append("size", Document("h", 14).append("w", 21).append("uom", "cm"))
            .append("status", "A"),
        Document("item", "mat")
            .append("qty", 85)
            .append("size", Document("h", 27.9).append("w", 35.5).append("uom", "cm"))
            .append("status", "A"),
        Document("item", "mousepad")
            .append("qty", 25)
            .append("size", Document("h", 19).append("w", 22.85).append("uom", "cm"))
            .append("status", "P"),
        Document("item", "notebook")
            .append("qty", 50)
            .append("size", Document("h", 8.5).append("w", 11).append("uom", "in"))
            .append("status", "P"),
        Document("item", "paper")
            .append("qty", 100)
            .append("size", Document("h", 8.5).append("w", 11).append("uom", "in"))
            .append("status", "D"),
        Document("item", "planner")
            .append("qty", 75)
            .append("size", Document("h", 22.85).append("w", 30).append("uom", "cm"))
            .append("status", "D"),
        Document("item", "postcard")
            .append("qty", 45)
            .append("size", Document("h", 10).append("w", 15.25).append("uom", "cm"))
            .append("status", "A"),
        Document("item", "sketchbook")
            .append("qty", 80)
            .append("size", Document("h", 14).append("w", 21).append("uom", "cm"))
            .append("status", "A"),
        Document("item", "sketch pad")
            .append("qty", 95)
            .append("size", Document("h", 22.85).append("w", 30.5).append("uom", "cm"))
            .append("status", "A"),
    )
)
```

</Tab>

<Tab name="Motor">

```python
await db.inventory.insert_many(
    [
        {
            "item": "canvas",
            "qty": 100,
            "size": {"h": 28, "w": 35.5, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "journal",
            "qty": 25,
            "size": {"h": 14, "w": 21, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "mat",
            "qty": 85,
            "size": {"h": 27.9, "w": 35.5, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "mousepad",
            "qty": 25,
            "size": {"h": 19, "w": 22.85, "uom": "cm"},
            "status": "P",
        },
        {
            "item": "notebook",
            "qty": 50,
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "status": "P",
        },
        {
            "item": "paper",
            "qty": 100,
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "status": "D",
        },
        {
            "item": "planner",
            "qty": 75,
            "size": {"h": 22.85, "w": 30, "uom": "cm"},
            "status": "D",
        },
        {
            "item": "postcard",
            "qty": 45,
            "size": {"h": 10, "w": 15.25, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "sketchbook",
            "qty": 80,
            "size": {"h": 14, "w": 21, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "sketch pad",
            "qty": 95,
            "size": {"h": 22.85, "w": 30.5, "uom": "cm"},
            "status": "A",
        },
    ]
)
```

</Tab>

<Tab name="Node.js">

```javascript
await db.collection('inventory').insertMany([
  {
    item: 'canvas',
    qty: 100,
    size: { h: 28, w: 35.5, uom: 'cm' },
    status: 'A'
  },
  {
    item: 'journal',
    qty: 25,
    size: { h: 14, w: 21, uom: 'cm' },
    status: 'A'
  },
  {
    item: 'mat',
    qty: 85,
    size: { h: 27.9, w: 35.5, uom: 'cm' },
    status: 'A'
  },
  {
    item: 'mousepad',
    qty: 25,
    size: { h: 19, w: 22.85, uom: 'cm' },
    status: 'P'
  },
  {
    item: 'notebook',
    qty: 50,
    size: { h: 8.5, w: 11, uom: 'in' },
    status: 'P'
  },
  {
    item: 'paper',
    qty: 100,
    size: { h: 8.5, w: 11, uom: 'in' },
    status: 'D'
  },
  {
    item: 'planner',
    qty: 75,
    size: { h: 22.85, w: 30, uom: 'cm' },
    status: 'D'
  },
  {
    item: 'postcard',
    qty: 45,
    size: { h: 10, w: 15.25, uom: 'cm' },
    status: 'A'
  },
  {
    item: 'sketchbook',
    qty: 80,
    size: { h: 14, w: 21, uom: 'cm' },
    status: 'A'
  },
  {
    item: 'sketch pad',
    qty: 95,
    size: { h: 22.85, w: 30.5, uom: 'cm' },
    status: 'A'
  }
]);
```

</Tab>

<Tab name="PHP">

```php
$insertManyResult = $db->inventory->insertMany([
    [
        'item' => 'canvas',
        'qty' => 100,
        'size' => ['h' => 28, 'w' => 35.5, 'uom' => 'cm'],
        'status' => 'A',
    ],
    [
        'item' => 'journal',
        'qty' => 25,
        'size' => ['h' => 14, 'w' => 21, 'uom' => 'cm'],
        'status' => 'A',
    ],
    [
        'item' => 'mat',
        'qty' => 85,
        'size' => ['h' => 27.9, 'w' => 35.5, 'uom' => 'cm'],
        'status' => 'A',
    ],
    [
        'item' => 'mousepad',
        'qty' => 25,
        'size' => ['h' => 19, 'w' => 22.85, 'uom' => 'cm'],
        'status' => 'P',
    ],
    [
        'item' => 'notebook',
        'qty' => 50,
        'size' => ['h' => 8.5, 'w' => 11, 'uom' => 'in'],
        'status' => 'P',
    ],
    [
        'item' => 'paper',
        'qty' => 100,
        'size' => ['h' => 8.5, 'w' => 11, 'uom' => 'in'],
        'status' => 'D',
    ],
    [
        'item' => 'planner',
        'qty' => 75,
        'size' => ['h' => 22.85, 'w' => 30, 'uom' => 'cm'],
        'status' => 'D',
    ],
    [
        'item' => 'postcard',
        'qty' => 45,
        'size' => ['h' => 10, 'w' => 15.25, 'uom' => 'cm'],
        'status' => 'A',
    ],
    [
        'item' => 'sketchbook',
        'qty' => 80,
        'size' => ['h' => 14, 'w' => 21, 'uom' => 'cm'],
        'status' => 'A',
    ],
    [
        'item' => 'sketch pad',
        'qty' => 95,
        'size' => ['h' => 22.85, 'w' => 30.5, 'uom' => 'cm'],
        'status' => 'A',
    ],
]);
```

</Tab>

<Tab name="Python">

```python
db.inventory.insert_many(
    [
        {
            "item": "canvas",
            "qty": 100,
            "size": {"h": 28, "w": 35.5, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "journal",
            "qty": 25,
            "size": {"h": 14, "w": 21, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "mat",
            "qty": 85,
            "size": {"h": 27.9, "w": 35.5, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "mousepad",
            "qty": 25,
            "size": {"h": 19, "w": 22.85, "uom": "cm"},
            "status": "P",
        },
        {
            "item": "notebook",
            "qty": 50,
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "status": "P",
        },
        {
            "item": "paper",
            "qty": 100,
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "status": "D",
        },
        {
            "item": "planner",
            "qty": 75,
            "size": {"h": 22.85, "w": 30, "uom": "cm"},
            "status": "D",
        },
        {
            "item": "postcard",
            "qty": 45,
            "size": {"h": 10, "w": 15.25, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "sketchbook",
            "qty": 80,
            "size": {"h": 14, "w": 21, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "sketch pad",
            "qty": 95,
            "size": {"h": 22.85, "w": 30.5, "uom": "cm"},
            "status": "A",
        },
    ]
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].insert_many([
                                 { item: 'canvas',
                                   qty: 100,
                                   size: { h: 28, w: 35.5, uom: 'cm' },
                                   status: 'A' },
                                 { item: 'journal',
                                   qty: 25,
                                   size: { h: 14, w: 21, uom: 'cm' },
                                   status: 'A' },
                                 { item: 'mat',
                                   qty: 85,
                                   size: { h: 27.9, w: 35.5, uom: 'cm' },
                                   status: 'A' },
                                 { item: 'mousepad',
                                   qty: 25,
                                   size: { h: 19, w: 22.85, uom: 'cm' },
                                   status: 'P' },
                                 { item: 'notebook',
                                   qty: 50,
                                   size: { h: 8.5, w: 11, uom: 'in' },
                                   status: 'P' },
                                 { item: 'paper',
                                   qty: 100,
                                   size: { h: 8.5, w: 11, uom: 'in' },
                                   status: 'D' },
                                 { item: 'planner',
                                   qty: 75,
                                   size: { h: 22.85, w: 30, uom: 'cm' },
                                   status: 'D' },
                                 { item: 'postcard',
                                   qty: 45,
                                   size: { h: 10, w: 15.25, uom: 'cm' },
                                   status: 'A' },
                                 { item: 'sketchbook',
                                   qty: 80,
                                   size: { h: 14, w: 21, uom: 'cm' },
                                   status: 'A' },
                                 { item: 'sketch pad',
                                   qty: 95,
                                   size: { h: 22.85, w: 30.5, uom: 'cm' },
                                   status: 'A' }
                               ])
```

</Tab>

<Tab name="Scala">

```scala
collection.insertMany(Seq(
  Document("""{ item: "canvas", qty: 100, size: { h: 28, w: 35.5, uom: "cm" }, status: "A" }"""),
  Document("""{ item: "journal", qty: 25, size: { h: 14, w: 21, uom: "cm" }, status: "A" }"""),
  Document("""{ item: "mat", qty: 85, size: { h: 27.9, w: 35.5, uom: "cm" }, status: "A" }"""),
  Document("""{ item: "mousepad", qty: 25, size: { h: 19, w: 22.85, uom: "cm" }, status: "P" }"""),
  Document("""{ item: "notebook", qty: 50, size: { h: 8.5, w: 11, uom: "in" }, status: "P" }"""),
  Document("""{ item: "paper", qty: 100, size: { h: 8.5, w: 11, uom: "in" }, status: "D" }"""),
  Document("""{ item: "planner", qty: 75, size: { h: 22.85, w: 30, uom: "cm" }, status: "D" }"""),
  Document("""{ item: "postcard", qty: 45, size: { h: 10, w: 15.25, uom: "cm" }, status: "A" }"""),
  Document("""{ item: "sketchbook", qty: 80, size: { h: 14, w: 21, uom: "cm" }, status: "A" }"""),
  Document("""{ item: "sketch pad", qty: 95, size: { h: 22.85, w: 30.5, uom: "cm" }, status: "A" }""")
)).execute()
```

</Tab>

</Tabs>

## Update Documents in a Collection

<Tabs>

<Tab name="MongoDB Shell">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update methods:

```javascript
{
  <update operator>: { <field1>: <value1>, ... },
  <update operator>: { <field2>: <value2>, ... },
  ...
}
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Compass">

To update a document in Compass, hover over the target document and click the pencil icon:

After clicking the pencil icon, the document enters edit mode:

You can now change the this document by clicking the item you wish to change and modifying the value.

For detailed instructions, see Compass documentation or follow the example below.

</Tab>

<Tab name="C">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update functions:

```c
{
  <update operator>: { <field1>: <value1>, ... },
  <update operator>: { <field2>: <value2>, ... },
  ...
}
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="C#">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update methods:

```csharp
{
  <update operator> => { <field1> => <value1>, ... },
  <update operator> => { <field2> => <value2>, ... },
  ...
}
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Go">

To modify field values, use Field Update Operators such as `$set`.

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Java (Async)">

To modify field values, use Field Update Operators such as `$set`.

The driver provides the com.mongodb.client.model.Updates class to build update documents:

```java
combine(set(<field1>, <value1>), set(<field2>, <value2>))
```

For a list of the update helpers, see com.mongodb.client.model.Updates.

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Java (Sync)">

To modify field values, use Field Update Operators such as `$set`.

The driver provides the com.mongodb.client.model.Updates class to build update documents:

```java
combine(set(<field1>, <value1>), set(<field2>, <value2>))
```

For a list of the update helpers, see com.mongodb.client.model.Updates.

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Kotlin (Coroutine)">

To modify field values, use Field Update Operators such as `$set`.

The driver provides the com.mongodb.client.model.Updates class to build update documents. The following code shows an update document that uses methods from the `Updates` builder class:

```kotlin
combine(set(<field1>, <value1>), set(<field2>, <value2>))
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Motor">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update methods:

```python
{
  <update operator>: { <field1>: <value1>, ... },
  <update operator>: { <field2>: <value2>, ... },
  ...
}
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Node.js">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update methods:

```javascript
{
  <update operator>: { <field1>: <value1>, ... },
  <update operator>: { <field2>: <value2>, ... },
  ...
}
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="PHP">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update methods:

```php
[
  <update operator> => [ <field1> => <value1>, ... ],
  <update operator> => [ <field2> => <value2>, ... ],
  ...
]
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Python">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update methods:

```python
{
  <update operator>: { <field1>: <value1>, ... },
  <update operator>: { <field2>: <value2>, ... },
  ...
}
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Ruby">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update methods:

```ruby
{
  <update operator> => { <field1> => <value1>, ... },
  <update operator> => { <field2> => <value2>, ... },
  ...
}
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

<Tab name="Scala">

To modify field values, use Field Update Operators such as `$set`.

Pass an update document to the update methods:

```scala
(
  set (<field1>, <value1>),
  set (<field2>, <value2>),
  ...
)
```

Some update operators, such as `$set`, will create the field if the field does not exist. See the individual update operator reference for details.

</Tab>

</Tabs>

MongoDB can accept an aggregation pipeline instead of an update document. For details, see the method reference page.

### Update a Single Document

<Tabs>

<Tab name="MongoDB Shell">

The following example uses the `db.collection.updateOne()` method on the `movies` collection to update the *first* document where `title` equals `"The Godfather"`:

</Tab>

<Tab name="Compass">

The following example demonstrates using MongoDB Compass to modify a single document where `item: paper` in the `inventory` collection:

This example uses the Compass Table View to modify the document. The editing process using the Compass List View follows a similar approach.

For more information on the differences between Table View and List View in Compass, refer to the Compass documentation.

</Tab>

<Tab name="C">

The following example uses the mongoc_collection_update_one function on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="C#">

The following example uses the IMongoCollection.UpdateOne() method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Go">

The following example uses the Collection.UpdateOne method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Java (Async)">

The following example uses the com.mongodb.reactivestreams.client.MongoCollection.updateOne) on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Java (Sync)">

The following example uses the com.mongodb.client.MongoCollection.updateOne method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example uses the MongoCollection.updateOne() method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Motor">

The following example uses the `update_one` method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Node.js">

The following example uses the Collection.updateOne() method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="PHP">

The following example uses the `updateOne()` method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Python">

The following example uses the `update_one` method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Ruby">

The following example uses the update_one() method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

<Tab name="Scala">

The following example uses the updateOne():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult]) method on the `inventory` collection to update the *first* document where `item` equals `"paper"`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.updateOne(
   { title: "The Godfather" },
   {
     $set: { rated: "PG", "tomatoes.viewer.rating": 4.5 },
     $currentDate: { lastupdated: true }
   }
)

```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Compass">

Modify the target document as follows:

- Change the `status` field from `D` to `P`.

- Change the `size.uom` field from `in` to `cm`.

- Add a new field called `lastModified` whose value will be today's date.

1. Click the Table button in the top navigation to access the Table View:

2. Use the Compass query bar to locate the target document.

   Copy the following filter document into the query bar and click Find:

   ```javascript
   { item: "paper" }
   ```

3. Hover over the `status` field and click the pencil icon which appears on the right side of the document to enter edit mode:

4. Change the value of the field to `"P"`.

5. Click the Update button below the field to save your changes.

6. Hover over the `size` field and click the outward-pointing arrows which appear on the right side of the field. This opens a new tab which displays the fields within the `size` object:

7. Using the same process outlined in steps 3-5 for editing the `status` field, change the value of the `size.uom` field to `"cm"`.

8. Click the left-most tab above the table labelled `inventory` to return to the original table view, which displays the top-level document:

9. Hover over the `status` field and click the pencil icon which appears on the right side of the document to re-enter edit mode.

10. Click inside of the `status` field and click the plus button icon which appears in the edit menu.

    Click the Add Field After status button which appears below the plus button:

11. Add a new field called `lastModified` with a value of today's date. Set the field type to `Date`:

12. Click the Update button below the field to save your changes.

    Because MongoDB Compass does not support `$currentDate` or any other Field Update Operators, you must manually enter the date value in Compass.

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *selector;
bson_t *update;
bool r;
bson_error_t error;

collection = mongoc_database_get_collection (db, "inventory");
selector = BCON_NEW ("item", BCON_UTF8 ("paper"));
update = BCON_NEW (
   "$set", "{",
   "size.uom", BCON_UTF8 ("cm"),
   "status", BCON_UTF8 ("P"),
   "}",
   "$currentDate", "{",
   "lastModified", BCON_BOOL (true),
   "}");

r = mongoc_collection_update_one(collection, selector, update, NULL, NULL, &error);
bson_destroy (selector);
bson_destroy (update);

if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("item", "paper");
var update = Builders<BsonDocument>.Update.Set("size.uom", "cm").Set("status", "P").CurrentDate("lastModified");
var result = collection.UpdateOne(filter, update);
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Go">

```go

result, err := coll.UpdateOne(
	context.TODO(),
	bson.D{
		{"item", "paper"},
	},
	bson.D{
		{"$set", bson.D{
			{"size.uom", "cm"},
			{"status", "P"},
		}},
		{"$currentDate", bson.D{
			{"lastModified", true},
		}},
	},
)

```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Java (Async)">

```java
Publisher<UpdateResult> updateOnePublisher = collection.updateOne(eq("item", "paper"),
        combine(set("size.uom", "cm"), set("status", "P"), currentDate("lastModified")));
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Java (Sync)">

```java
collection.updateOne(eq("item", "paper"),
        combine(set("size.uom", "cm"), set("status", "P"), currentDate("lastModified")));
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
collection.updateOne(eq("item", "paper"),
    combine(set("size.uom", "cm"), set("status", "P"), currentDate("lastModified")));
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Motor">

```python
await db.inventory.update_one(
    {"item": "paper"},
    {"$set": {"size.uom": "cm", "status": "P"}, "$currentDate": {"lastModified": True}},
)
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Node.js">

```javascript
await db.collection('inventory').updateOne(
  { item: 'paper' },
  {
    $set: { 'size.uom': 'cm', status: 'P' },
    $currentDate: { lastModified: true }
  }
);
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="PHP">

```php
$updateResult = $db->inventory->updateOne(
    ['item' => 'paper'],
    [
        '$set' => ['size.uom' => 'cm', 'status' => 'P'],
        '$currentDate' => ['lastModified' => true],
    ],
);
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Python">

```python
db.inventory.update_one(
    {"item": "paper"},
    {"$set": {"size.uom": "cm", "status": "P"}, "$currentDate": {"lastModified": True}},
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].update_one({ item: 'paper' },
                              { '$set' => { 'size.uom' => 'cm', 'status' => 'P' },
                                '$currentDate' => { 'lastModified' => true } })
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Scala">

```scala
collection.updateOne(equal("item", "paper"),
  combine(set("size.uom", "cm"), set("status", "P"), currentDate("lastModified"))
).execute()
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"cm"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

</Tabs>

### Update Multiple Documents

<Tabs>

<Tab name="MongoDB Shell">

The following example uses the `db.collection.updateMany()` method on the `movies` collection to update all documents where `num_mflix_comments` is greater than `100`:

</Tab>

<Tab name="Compass">

You can update only one document at a time in MongoDB Compass.

</Tab>

<Tab name="C">

The following example uses the mongoc_collection_update_many function on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="C#">

The following example uses the IMongoCollection.UpdateMany() method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Go">

The following example uses the Collection.UpdateMany method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Java (Async)">

The following example uses the com.mongodb.reactivestreams.client.MongoCollection.updateMany) method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Java (Sync)">

The following example uses the com.mongodb.client.MongoCollection.updateMany method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example uses the MongoCollection.updateMany() method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Motor">

The following example uses the `update_many` method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Node.js">

The following example uses the Collection.updateMany() method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="PHP">

The following example uses the `updateMany()` method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Python">

The following example uses the `update_many` method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Ruby">

The following example uses the update_many() method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

<Tab name="Scala">

The following example uses the updateMany():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult]) method on the `inventory` collection to update all documents where `qty` is less than `50`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.updateMany(
   { "num_mflix_comments": { $gt: 100 } },
   {
     $set: { popular: true },
     $currentDate: { lastupdated: true }
   }
)

```

</Tab>

<Tab name="Compass">

To update multiple documents, connect to your MongoDB deployment from `mongosh` or a MongoDB driver and follow the examples in this section for your preferred method.

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *selector;
bson_t *update;
bool r;
bson_error_t error;

collection = mongoc_database_get_collection (db, "inventory");
selector = BCON_NEW (
   "qty", "{",
   "$lt", BCON_INT64 (50),
   "}");
update = BCON_NEW (
   "$set", "{",
   "size.uom", BCON_UTF8 ("in"),
   "status", BCON_UTF8 ("P"),
   "}",
   "$currentDate", "{",
   "lastModified", BCON_BOOL (true),
   "}");

r = mongoc_collection_update_many(collection, selector, update, NULL, NULL, &error);
bson_destroy (selector);
bson_destroy (update);

if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Lt("qty", 50);
var update = Builders<BsonDocument>.Update.Set("size.uom", "in").Set("status", "P").CurrentDate("lastModified");
var result = collection.UpdateMany(filter, update);
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Go">

```go

result, err := coll.UpdateMany(
	context.TODO(),
	bson.D{
		{"qty", bson.D{
			{"$lt", 50},
		}},
	},
	bson.D{
		{"$set", bson.D{
			{"size.uom", "cm"},
			{"status", "P"},
		}},
		{"$currentDate", bson.D{
			{"lastModified", true},
		}},
	},
)

```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Java (Async)">

```java
Publisher<UpdateResult> updateManyPublisher = collection.updateMany(lt("qty", 50),
        combine(set("size.uom", "in"), set("status", "P"), currentDate("lastModified")));
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Java (Sync)">

```java
collection.updateMany(lt("qty", 50),
        combine(set("size.uom", "in"), set("status", "P"), currentDate("lastModified")));
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
collection.updateMany(lt("qty", 50),
    combine(set("size.uom", "in"), set("status", "P"), currentDate("lastModified")));
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Motor">

```python
await db.inventory.update_many(
    {"qty": {"$lt": 50}},
    {"$set": {"size.uom": "in", "status": "P"}, "$currentDate": {"lastModified": True}},
)
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Node.js">

```javascript
await db.collection('inventory').updateMany(
  { qty: { $lt: 50 } },
  {
    $set: { 'size.uom': 'in', status: 'P' },
    $currentDate: { lastModified: true }
  }
);
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="PHP">

```php
$updateResult = $db->inventory->updateMany(
    ['qty' => ['$lt' => 50]],
    [
        '$set' => ['size.uom' => 'cm', 'status' => 'P'],
        '$currentDate' => ['lastModified' => true],
    ],
);
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Python">

```python
db.inventory.update_many(
    {"qty": {"$lt": 50}},
    {"$set": {"size.uom": "in", "status": "P"}, "$currentDate": {"lastModified": True}},
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].update_many({ qty: { '$lt' => 50 } },
                               { '$set' => { 'size.uom' => 'in', 'status' => 'P' },
                                 '$currentDate' => { 'lastModified' => true } })
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

<Tab name="Scala">

```scala
collection.updateMany(lt("qty", 50),
  combine(set("size.uom", "in"), set("status", "P"), currentDate("lastModified"))
).execute()
```

The update operation:

- uses the `$set` operator to update the value of the `size.uom` field to `"in"` and the value of the `status` field to `"P"`,

- uses the `$currentDate` operator to update the value of the `lastModified` field to the current date. If `lastModified` field does not exist, `$currentDate` will create the field. See `$currentDate` for details.

</Tab>

</Tabs>

### Replace a Document

<Tabs>

<Tab name="MongoDB Shell">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to `db.collection.replaceOne()`.

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `movies` collection where `title: "The Godfather"`:

</Tab>

<Tab name="Compass">

You can't replace a document in MongoDB Compass.

</Tab>

<Tab name="C">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the third argument to mongoc_collection_replace_one.

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="C#">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to IMongoCollection.ReplaceOne().

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Go">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to Collection.ReplaceOne.

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Java (Async)">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to com.mongodb.reactivestreams.client.MongoCollection.replaceOne).

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Java (Sync)">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to com.mongodb.client.MongoCollection.replaceOne.

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Kotlin (Coroutine)">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to the MongoCollection.replaceOne() method.

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Motor">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to `replace_one`.

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Node.js">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to Collection.replaceOne().

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="PHP">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to `replaceOne()`.

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Python">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to `replace_one`.

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Ruby">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to replace_one().

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

<Tab name="Scala">

To replace the entire content of a document except for the `_id` field, pass an entirely new document as the second argument to replaceOne():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult])

When replacing a document, the replacement document must consist of only field/value pairs. The replacement document cannot include update operators expressions.

The replacement document can have different fields from the original document. In the replacement document, you can omit the `_id` field since the `_id` field is immutable. However, if you do include the `_id` field, it must have the same value as the current value.

The following example replaces the *first* document from the `inventory` collection where `item: "paper"`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.replaceOne(
   { title: "The Godfather" },
   { title: "The Godfather", plot: "Updated plot summary", year: 1972, rated: "R", runtime: 175 }
)

```

</Tab>

<Tab name="Compass">

To replace a document, connect to your MongoDB deployment from `mongosh` or a MongoDB driver and follow the examples in this section for your preferred method.

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *selector;
bson_t *replacement;
bool r;
bson_error_t error;

collection = mongoc_database_get_collection (db, "inventory");
selector = BCON_NEW ("item", BCON_UTF8 ("paper"));
replacement = BCON_NEW (
   "item", BCON_UTF8 ("paper"),
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("A"),
   "qty", BCON_INT64 (60),
   "}","{",
   "warehouse", BCON_UTF8 ("B"),
   "qty", BCON_INT64 (40),
   "}",
   "]");

/* MONGOC_UPDATE_NONE means "no special options" */
r = mongoc_collection_replace_one(collection, selector, replacement, NULL, NULL, &error);
bson_destroy (selector);
bson_destroy (replacement);

if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}
```

Clean up any open resources by calling the following methods, as appropriate:

- bson_destroy

- mongoc_bulk_operation_destroy

- mongoc_collection_destroy

- mongoc_cursor_destroy,

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("item", "paper");
var replacement = new BsonDocument
{
    { "item", "paper" },
    { "instock", new BsonArray
        {
            new BsonDocument { { "warehouse", "A" }, { "qty", 60 } },
            new BsonDocument { { "warehouse", "B" }, { "qty", 40 } } }
        }
};
var result = collection.ReplaceOne(filter, replacement);
```

</Tab>

<Tab name="Go">

```go

result, err := coll.ReplaceOne(
	context.TODO(),
	bson.D{
		{"item", "paper"},
	},
	bson.D{
		{"item", "paper"},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "A"},
				{"qty", 60},
			},
			bson.D{
				{"warehouse", "B"},
				{"qty", 40},
			},
		}},
	},
)

```

</Tab>

<Tab name="Java (Async)">

```java
Publisher<UpdateResult> replaceOnePublisher = collection.replaceOne(eq("item", "paper"),
        Document.parse("{ item: 'paper', instock: [ { warehouse: 'A', qty: 60 }, { warehouse: 'B', qty: 40 } ] }"));
```

</Tab>

<Tab name="Java (Sync)">

```java
collection.replaceOne(eq("item", "paper"),
        Document.parse("{ item: 'paper', instock: [ { warehouse: 'A', qty: 60 }, { warehouse: 'B', qty: 40 } ] }"));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
collection.replaceOne(eq("item", "paper"),
    Document.parse("{ item: 'paper', instock: [ { warehouse: 'A', qty: 60 }, { warehouse: 'B', qty: 40 } ] }"));
```

</Tab>

<Tab name="Motor">

```python
await db.inventory.replace_one(
    {"item": "paper"},
    {
        "item": "paper",
        "instock": [{"warehouse": "A", "qty": 60}, {"warehouse": "B", "qty": 40}],
    },
)
```

</Tab>

<Tab name="Node.js">

```javascript
await db.collection('inventory').replaceOne(
  { item: 'paper' },
  {
    item: 'paper',
    instock: [
      { warehouse: 'A', qty: 60 },
      { warehouse: 'B', qty: 40 }
    ]
  }
);
```

</Tab>

<Tab name="PHP">

```php
$updateResult = $db->inventory->replaceOne(
    ['item' => 'paper'],
    [
        'item' => 'paper',
        'instock' => [
            ['warehouse' => 'A', 'qty' => 60],
            ['warehouse' => 'B', 'qty' => 40],
        ],
    ],
);
```

</Tab>

<Tab name="Python">

```python
db.inventory.replace_one(
    {"item": "paper"},
    {
        "item": "paper",
        "instock": [{"warehouse": "A", "qty": 60}, {"warehouse": "B", "qty": 40}],
    },
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].replace_one({ item: 'paper' },
                               { item: 'paper',
                                 instock: [ { warehouse: 'A', qty: 60 },
                                            { warehouse: 'B', qty: 40 } ] })
```

</Tab>

<Tab name="Scala">

```scala
collection.replaceOne(equal("item", "paper"),
  Document("""{ item: "paper", instock: [ { warehouse: "A", qty: 60 }, { warehouse: "B", qty: 40 } ] }""")
).execute()
```

</Tab>

</Tabs>

## Update a Document with MongoDB Atlas

The MongoDB Atlas UI updates one document at a time. To update multiple documents or replace an entire document, connect to your Atlas deployment from `mongosh` or a MongoDB driver and follow the example for your preferred method.

This example uses the sample supplies dataset. To load the sample dataset, see Load Sample Data.

To update a document in MongoDB Atlas, follow these steps:

### In the MongoDB Atlas UI, go to the Clusters page for your project.

- If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Clusters under the Database heading.

  The Clusters page displays.

### Navigate to the collection.

- For the cluster that contains the sample data, click Browse Collections.

- In the left navigation pane, select the `sample_supplies` database.

- Select the `sales` collection.

### Specify a query filter.

You can specify a query filter document in the Filter field. A query filter document uses query operators to specify search conditions.

Copy the following query filter document into the Filter search bar and click Apply:

```javascript
{ saleDate: { $gte: { $date: "2016-01-01T00:00-00:00" }, $lte: { $date: "2016-01-02T00:00-00:00" } } }
```

This query filter returns all documents in the `sample_supplies.sales` collection where `saleDate` is on or between January 1 and 2, 2016 UTC time.

### Edit a document.

To edit a document displayed in the query results, hover over the document and click on the pencil icon. In the document editor, you can:

- Add a new field.

- Delete an existing field.

- Edit a field's name, value, or type.

- Revert a specific change.

For detailed instructions, see Create, View, Update, and Delete Documents.

### Save your changes.

To confirm and save your changes, click the Update button.

## Behavior

### Atomicity

All write operations are atomic at the document level. For more information, see Atomicity and Transactions.

### `_id` Field

Once set, you cannot update the `_id` field value nor can you replace a document with one that has a different `_id` value.

### Idempotent Operations

Use `updateMany()` only for idempotent operations.

### Field Order

For write operations, MongoDB preserves the order of the document fields *except* for the following cases:

- The `_id` field is always the first field in the document.

- Updates that include `renaming` of field names may result in the reordering of fields in the document.

### Upsert Option

<Tabs>

<Tab name="MongoDB Shell">

If `updateOne()`, `updateMany()`, or `replaceOne()` includes `upsert : true`
**and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Compass">

The upsert option is not available in MongoDB Compass.

</Tab>

<Tab name="C">

If mongoc_collection_update_one, mongoc_collection_update_many, or mongoc_collection_replace_one includes `upsert : true` **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the functions.

</Tab>

<Tab name="C#">

If UpdateOne(), UpdateMany(), or ReplaceOne() includes an UpdateOptions argument instance with the `IsUpsert` option set to `true`
**and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Go">

If Collection.UpdateOne includes the Upsert option set to true **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Java (Async)">

If the update and replace methods include the UpdateOptions parameter that specifies UpdateOptions.upsert(true)
**and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Java (Sync)">

If the update and replace methods include the com.mongodb.client.model.UpdateOptions parameter that specifies com.mongodb.client.model.UpdateOptions.upsert(true)
**and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Kotlin (Coroutine)">

If the update and replace methods include the com.mongodb.client.model.UpdateOptions parameter that specifies `upsert(true)`, **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Motor">

If `update_one`, `update_many`, or `replace_one` includes `upsert : true` **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Node.js">

If updateOne(), updateMany(), or replaceOne() include `upsert : true` in the `options` parameter document **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="PHP">

If `updateOne()`, `updateMany()`, or `replaceOne()` includes `upsert => true` **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Python">

If `update_one`, `update_many`, or `replace_one` includes `upsert : true` **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Ruby">

If update_one(), update_many(), or replace_one() includes `upsert => true` **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

<Tab name="Scala">

If updateOne():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult]), updateMany():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult]), or replaceOne():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult]) includes `upsert => true` **and** no documents match the specified filter, then the operation creates a new document and inserts it. If there are matching documents, then the operation modifies or replaces the matching document or documents.

For details on the new document created, see the individual reference pages for the methods.

</Tab>

</Tabs>

### Write Acknowledgement

Specify the level of acknowledgment requested from MongoDB for write operations with write concerns.

<Tabs>

<Tab name="MongoDB Shell">

- Updates with Aggregation Pipeline

- `db.collection.updateOne()`

- `db.collection.updateMany()`

- `db.collection.replaceOne()`

- Additional Methods

</Tab>

<Tab name="Compass">

- Compass Documents

- Compass Query Bar

</Tab>

<Tab name="C">

- mongoc_collection_update_one

- mongoc_collection_update_many

- mongoc_collection_replace_one

- Additional Methods

</Tab>

<Tab name="C#">

- IMongoCollection.UpdateOne()

- IMongoCollection.UpdateMany()

- IMongoCollection.ReplaceOne()

- Additional Methods

</Tab>

<Tab name="Go">

- Collection.UpdateOne

- Collection.UpdateMany

- Collection.ReplaceOne

- Additional Methods

</Tab>

<Tab name="Java (Async)">

- com.mongodb.reactivestreams.client.MongoCollection.updateOne)

- com.mongodb.reactivestreams.client.MongoCollection.updateMany)

- com.mongodb.reactivestreams.client.MongoCollection.replaceOne)

- Java Reactive Streams Driver Quick Tour

</Tab>

<Tab name="Java (Sync)">

- com.mongodb.client.MongoCollection.updateOne

- com.mongodb.client.MongoCollection.updateMany

- com.mongodb.client.MongoCollection.replaceOne

- Additional Java Synchronous Driver Write Examples

</Tab>

<Tab name="Kotlin (Coroutine)">

- MongoCollection.updateOne()

- MongoCollection.updateMany()

- MongoCollection.replaceOne()

- Kotlin Coroutine Driver Modify Documents Guide

</Tab>

<Tab name="Motor">

- `motor.motor_asyncio.AsyncIOMotorCollection.update_one`

- `motor.motor_asyncio.AsyncIOMotorCollection.update_many`

- `motor.motor_asyncio.AsyncIOMotorCollection.replace_one`

- Additional Methods

</Tab>

<Tab name="Node.js">

- Collection.updateOne()

- Collection.updateMany()

- Collection.replaceOne()

- Additional Methods

</Tab>

<Tab name="PHP">

- `MongoDB\\Collection::updateOne()`

- `MongoDB\\Collection::updateMany()`

- `MongoDB\\Collection::replaceOne()`

- Additional Methods

</Tab>

<Tab name="Python">

- `pymongo.collection.Collection.update_one`

- `pymongo.collection.Collection.update_many`

- `pymongo.collection.Collection.replace_one`

- Additional Methods

</Tab>

<Tab name="Ruby">

- Mongo::Collection#update_one()

- Mongo::Collection#update_many()

- Mongo::Collection#replace_one()

</Tab>

<Tab name="Scala">

- collection.updateOne():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult])

- collection.updateMany():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult])

- collection.replaceOne():org.mongodb.scala.SingleObservable[org.mongodb.scala.result.UpdateResult])

- Additional Methods

</Tab>

</Tabs>
