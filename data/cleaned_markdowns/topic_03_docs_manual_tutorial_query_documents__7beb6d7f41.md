> Source: https://www.mongodb.com/docs/manual/tutorial/query-documents/
> Fetch method: direct_markdown

# Query Documents

To query documents, specify a query predicate that indicates which documents to return. An empty query predicate `{ }` returns all documents in the collection.

You can query documents in MongoDB with the following methods:

Query Documents with MongoDB Atlas- Your programming language's driver.

- The MongoDB Atlas UI. To learn more, see Query Documents with MongoDB Atlas.

- MongoDB Compass.

➤➤ Use the **Select your language** drop-down menu in the upper-right to set the language of the following examples or select MongoDB Compass.

query operations

<Tabs>

<Tab name="MongoDB Shell">

This page provides examples of query operations using the `db.collection.find()` method in `mongosh`.

</Tab>

<Tab name="Compass">

This page provides examples of query operations using MongoDB Compass.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C">

This page provides examples of query operations using mongoc_collection_find_with_opts.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C#">

This page provides examples of query operations using the MongoCollection.Find() method in the MongoDB C# Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Go">

This page provides examples of query operations using the Collection.Find function in the MongoDB Go Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Async)">

This page provides examples of query operations using the com.mongodb.reactivestreams.client.MongoCollection.find) method in the MongoDB Java Reactive Streams Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Sync)">

This page provides examples of query operations using the com.mongodb.client.MongoCollection.find method in the MongoDB Java Synchronous Driver.

The driver provides com.mongodb.client.model.Filters helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Kotlin (Coroutine)">

This page provides examples of query operations by using the MongoCollection.find() method in the MongoDB Kotlin Coroutine Driver.

The driver provides com.mongodb.client.model.Filters helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Motor">

As of May 14, 2025, Motor is deprecated in favor of the GA release of the PyMongo Async API in the PyMongo library. We will not add new features to Motor, and we will provide only bug fixes until it reaches end of life on May 14, 2026. After that, we will fix only critical bugs until final support ends on May 14, 2027. We strongly recommend migrating to the PyMongo Async API while Motor is still supported.

For more information about migrating, see the Migrate to PyMongo Async guide in the PyMongo documentation.

This page provides examples of query operations using the `pymongo.asynchronous.collection.AsyncCollection.find` method in the PyMongo Async API.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Node.js">

This page provides examples of query operations using the Collection.find() method in the MongoDB Node.js Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="PHP">

This page provides examples of query operations using the `MongoDB\\Collection::find()` method in the MongoDB PHP Library.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Python">

This page provides examples of query operations using the `pymongo.collection.Collection.find` method in the PyMongo Python driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Ruby">

This page provides examples of query operations using the Mongo::Collection#find() method in the MongoDB Ruby Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Scala">

This page provides examples of query operations using the collection.find()(implicite:org.mongodb.scala.bson.DefaultHelper.DefaultsTo[C,TResult],implicitct:scala.reflect.ClassTag[C]):org.mongodb.scala.FindObservable[C]) method in the MongoDB Scala Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The examples on this page use data from the sample_mflix sample dataset. For details on how to load this dataset into your self-managed MongoDB deployment, see Load the sample dataset. If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

</Tab>

<Tab name="Compass">

```javascript
[
    { "item": "journal", "qty": 25, "size": { "h": 14, "w": 21, "uom": "cm" }, "status": "A" },
    { "item": "notebook", "qty": 50, "size": { "h": 8.5, "w": 11, "uom": "in" }, "status": "A" },
    { "item": "paper", "qty": 100, "size": { "h": 8.5, "w": 11, "uom": "in" }, "status": "D" },
    { "item": "planner", "qty": 75, "size": { "h": 22.85, "w": 30, "uom": "cm" }, "status": "D" },
    { "item": "postcard", "qty": 45, "size": { "h": 10, "w": 15.25, "uom": "cm" }, "status": "A" }
]
```

For instructions on inserting documents in MongoDB Compass, see Insert Documents.

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
   "item", BCON_UTF8 ("notebook"),
   "qty", BCON_INT64 (50),
   "size", "{",
   "h", BCON_DOUBLE (8.5),
   "w", BCON_DOUBLE (11),
   "uom", BCON_UTF8 ("in"),
   "}",
   "status", BCON_UTF8 ("A"));

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

/* "reply" is initialized on success or error */
r = (bool) mongoc_bulk_operation_execute (bulk, &reply, &error);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
}
```

</Tab>

<Tab name="C#">

```csharp
var documents = new BsonDocument[]
{
    new BsonDocument
    {
        { "item", "journal" },
        { "qty", 25 },
        { "size", new BsonDocument { { "h", 14 }, { "w", 21 }, {  "uom", "cm"} } },
        { "status", "A" }
    },
    new BsonDocument
    {
        { "item", "notebook" },
        { "qty", 50 },
        { "size", new BsonDocument { { "h",  8.5 }, { "w", 11 }, {  "uom", "in"} } },
        { "status", "A" }
    },
    new BsonDocument
    {
        { "item", "paper" },
        { "qty", 100 },
        { "size", new BsonDocument { { "h",  8.5 }, { "w", 11 }, {  "uom", "in"} } },
        { "status", "D" }
    },
    new BsonDocument
    {
        { "item", "planner" },
        { "qty", 75 },
        { "size", new BsonDocument { { "h", 22.85 }, { "w", 30  }, {  "uom", "cm"} } },
        { "status", "D" }
    },
    new BsonDocument
    {
        { "item", "postcard" },
        { "qty", 45 },
        { "size", new BsonDocument { { "h", 10 }, { "w", 15.25 }, {  "uom", "cm"} } },
        { "status", "A" }
    },
};
collection.InsertMany(documents);
```

</Tab>

<Tab name="Go">

```go

docs := []any{
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
		{"item", "notebook"},
		{"qty", 50},
		{"size", bson.D{
			{"h", 8.5},
			{"w", 11},
			{"uom", "in"},
		}},
		{"status", "A"},
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
}

result, err := coll.InsertMany(context.TODO(), docs)

```

</Tab>

<Tab name="Java (Async)">

```java
Publisher<Success> insertManyPublisher = collection.insertMany(asList(
        Document.parse("{ item: 'journal', qty: 25, size: { h: 14, w: 21, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'notebook', qty: 50, size: { h: 8.5, w: 11, uom: 'in' }, status: 'A' }"),
        Document.parse("{ item: 'paper', qty: 100, size: { h: 8.5, w: 11, uom: 'in' }, status: 'D' }"),
        Document.parse("{ item: 'planner', qty: 75, size: { h: 22.85, w: 30, uom: 'cm' }, status: 'D' }"),
        Document.parse("{ item: 'postcard', qty: 45, size: { h: 10, w: 15.25, uom: 'cm' }, status: 'A' }")
));
```

</Tab>

<Tab name="Java (Sync)">

```java
collection.insertMany(asList(
        Document.parse("{ item: 'journal', qty: 25, size: { h: 14, w: 21, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'notebook', qty: 50, size: { h: 8.5, w: 11, uom: 'in' }, status: 'A' }"),
        Document.parse("{ item: 'paper', qty: 100, size: { h: 8.5, w: 11, uom: 'in' }, status: 'D' }"),
        Document.parse("{ item: 'planner', qty: 75, size: { h: 22.85, w: 30, uom: 'cm' }, status: 'D' }"),
        Document.parse("{ item: 'postcard', qty: 45, size: { h: 10, w: 15.25, uom: 'cm' }, status: 'A' }")
));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
collection.insertMany(
    listOf(
        Document("item", "journal")
            .append("qty", 25)
            .append("size", Document("h", 14)
                .append("w", 21)
                .append("uom", "cm")
            )
            .append("status", "A"),
        Document("item", "notebook")
            .append("qty", 50)
            .append("size", Document("h", 8.5)
                .append("w", 11)
                .append("uom", "in")
            )
            .append("status", "A"),
        Document("item", "paper")
            .append("qty", 100)
            .append("size", Document("h", 8.5)
                .append("w", 11)
                .append("uom", "in")
            )
            .append("status", "D"),
        Document("item", "planner")
            .append("qty", 75)
            .append("size", Document("h", 22.85)
                .append("w", 30)
                .append("uom", "cm")
            )
            .append("status", "D"),
        Document("item", "postcard")
            .append("qty", 45)
            .append("size", Document("h", 10)
                .append("w", 15.25)
                .append("uom", "cm")
            )
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
            "item": "journal",
            "qty": 25,
            "size": {"h": 14, "w": 21, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "notebook",
            "qty": 50,
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "status": "A",
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
    ]
)
```

</Tab>

<Tab name="Node.js">

```javascript
await db.collection('inventory').insertMany([
  {
    item: 'journal',
    qty: 25,
    size: { h: 14, w: 21, uom: 'cm' },
    status: 'A'
  },
  {
    item: 'notebook',
    qty: 50,
    size: { h: 8.5, w: 11, uom: 'in' },
    status: 'A'
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
  }
]);
```

</Tab>

<Tab name="PHP">

```php
$insertManyResult = $db->inventory->insertMany([
    [
        'item' => 'journal',
        'qty' => 25,
        'size' => ['h' => 14, 'w' => 21, 'uom' => 'cm'],
        'status' => 'A',
    ],
    [
        'item' => 'notebook',
        'qty' => 50,
        'size' => ['h' => 8.5, 'w' => 11, 'uom' => 'in'],
        'status' => 'A',
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
]);
```

</Tab>

<Tab name="Python">

```python
db.inventory.insert_many(
    [
        {
            "item": "journal",
            "qty": 25,
            "size": {"h": 14, "w": 21, "uom": "cm"},
            "status": "A",
        },
        {
            "item": "notebook",
            "qty": 50,
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "status": "A",
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
    ]
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].insert_many([ { item: 'journal',
                                   qty: 25,
                                   size: { h: 14, w: 21, uom: 'cm' },
                                   status: 'A' },
                                 { item: 'notebook',
                                   qty: 50,
                                   size: { h: 8.5, w: 11, uom: 'in' },
                                   status: 'A' },
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
                                   status: 'A' } ])
```

</Tab>

<Tab name="Scala">

```scala
collection.insertMany(Seq(
  Document("""{ item: "journal", qty: 25, size: { h: 14, w: 21, uom: "cm" }, status: "A" }"""),
  Document("""{ item: "notebook", qty: 50, size: { h: 8.5, w: 11, uom: "in" }, status: "A" }"""),
  Document("""{ item: "paper", qty: 100, size: { h: 8.5, w: 11, uom: "in" }, status: "D" }"""),
  Document("""{ item: "planner", qty: 75, size: { h: 22.85, w: 30, uom: "cm" }, status: "D" }"""),
  Document("""{ item: "postcard", qty: 45, size: { h: 10, w: 15.25, uom: "cm" }, status: "A" }""")
)).execute()
```

</Tab>

</Tabs>

## Select All Documents in a Collection

<Tabs>

<Tab name="MongoDB Shell">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Compass">

To select all documents in the collection, pass an empty document as the query filter parameter to the query bar. The query filter parameter determines the select criteria:

</Tab>

<Tab name="C">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="C#">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Go">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Java (Async)">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Java (Sync)">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Kotlin (Coroutine)">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Motor">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Node.js">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="PHP">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Python">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Ruby">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

<Tab name="Scala">

To select all documents in the collection, pass an empty document as the query filter parameter to the find method. The query filter parameter determines the select criteria:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( {} )

```

</Tab>

<Tab name="Compass">

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (NULL);
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

Clean up any open resources by calling the following methods, as appropriate:

- bson_destroy

- mongoc_bulk_operation_destroy

- mongoc_collection_destroy

- mongoc_cursor_destroy,

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Empty;
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{},
)

```

</Tab>

<Tab name="Java (Async)">

```java
FindPublisher<Document> findPublisher = collection.find(new Document());
```

</Tab>

<Tab name="Java (Sync)">

```java
FindIterable<Document> findIterable = collection.find(new Document());
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val flowInsertMany = collection
    .find(empty())
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find([]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find({})
```

</Tab>

<Tab name="Scala">

```scala
var findObservable = collection.find(Document())
```

</Tab>

</Tabs>

This operation uses a query predicate of `{}`, which corresponds to the following SQL statement:

<Tabs>

<Tab name="MongoDB Shell">

```sql
SELECT * FROM movies
```

</Tab>

<Tab name="Compass">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="C">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="C#">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Go">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Java (Async)">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Java (Sync)">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Motor">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Node.js">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="PHP">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Python">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Ruby">

```sql
SELECT * FROM inventory
```

</Tab>

<Tab name="Scala">

```sql
SELECT * FROM inventory
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

For more information, see `find()`.

</Tab>

<Tab name="Compass">

For more information, see Query Bar.

</Tab>

<Tab name="C">

For more information, see mongoc_collection_find_with_opts.

</Tab>

<Tab name="C#">

For more information, see Find().

</Tab>

<Tab name="Go">

For more information, see Collection.Find.

</Tab>

<Tab name="Java (Async)">

For more information, see com.mongodb.reactivestreams.client.MongoCollection.find).

</Tab>

<Tab name="Java (Sync)">

For more information, see com.mongodb.client.MongoCollection.find.

</Tab>

<Tab name="Kotlin (Coroutine)">

For more information, see MongoCollection.find().

</Tab>

<Tab name="Motor">

For more information, see `find`.

</Tab>

<Tab name="Node.js">

For more information, see find().

</Tab>

<Tab name="PHP">

For more information, see `find()`.

</Tab>

<Tab name="Python">

For more information, see `find`.

</Tab>

<Tab name="Ruby">

For more information, see find().

</Tab>

<Tab name="Scala">

For more information, see collection.find()(implicite:org.mongodb.scala.bson.DefaultHelper.DefaultsTo[C,TResult],implicitct:scala.reflect.ClassTag[C]):org.mongodb.scala.FindObservable[C]).

</Tab>

</Tabs>

## Specify Equality Condition

<Tabs>

<Tab name="MongoDB Shell">

To specify equality conditions, use `<field>:<value>` expressions in the query filter document:

```javascript
{ <field1>: <value1>, ... }
```

</Tab>

<Tab name="Compass">

To specify equality conditions, use `<field>:<value>` expressions in the query filter document:

```javascript
{ <field1>: <value1>, ... }
```

</Tab>

<Tab name="C">

To specify equality conditions, use `<field>:<value>` expressions in the query filter document:

```c
{ <field1>: <value1>, ... }
```

</Tab>

<Tab name="C#">

To specify equality conditions, construct a filter using the Eq method:

```csharp
Builders<BsonDocument>.Filter.Eq(<field>, <value>);
```

</Tab>

<Tab name="Go">

To specify equality conditions, use the `bson.D` type to create a filter document:

```go
filter := bson.D{{"<field>", <value>}}
```

</Tab>

<Tab name="Java (Async)">

To specify equality conditions, use the com.mongodb.client.model.Filters.eq method to create the query filter document:

```java
and(eq(<field1>, <value1>), eq(<field2>, <value2>) ...)
```

</Tab>

<Tab name="Java (Sync)">

To specify equality conditions, use the `com.mongodb.client.model.Filters.eq_` method to create the query filter document:

```java
and(eq(<field1>, <value1>), eq(<field2>, <value2>) ...)
```

</Tab>

<Tab name="Kotlin (Coroutine)">

To specify equality conditions, use the Filters.eq()) method to create the query filter document:

```kotlin
and(eq(<field1>, <value1>), eq(<field2>, <value2>) ...)
```

</Tab>

<Tab name="Motor">

To specify equality conditions, use `<field>:<value>` expressions in the query filter document:

```python
{ <field1>: <value1>, ... }
```

</Tab>

<Tab name="Node.js">

To specify equality conditions, use `<field>:<value>` expressions in the query filter document:

```javascript
{ <field1>: <value1>, ... }
```

</Tab>

<Tab name="PHP">

To specify equality conditions, use `<field> => <value>` expressions in the query filter document:

```php
[ <field1> => <value1>, ... ]
```

</Tab>

<Tab name="Python">

To specify equality conditions, use `<field>:<value>` expressions in the query filter document:

```python
{ <field1>: <value1>, ... }
```

</Tab>

<Tab name="Ruby">

To specify equality conditions, use `<field> => <value>` expressions in the query filter document:

```ruby
{ <field1> => <value1>, ... }
```

</Tab>

<Tab name="Scala">

To specify equality conditions, use the `com.mongodb.client.model.Filters.eq_` method to create the query filter document:

```scala
and(equal(<field1>, <value1>), equal(<field2>, <value2>) ...)
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The following example selects all documents from the `sample_mflix.movies` collection where `rated` equals `"PG-13"`:

</Tab>

<Tab name="Compass">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="C">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="C#">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Go">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Java (Async)">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Java (Sync)">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Motor">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Node.js">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="PHP">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Python">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Ruby">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

<Tab name="Scala">

The following example selects all documents from the `inventory` collection where `status` equals `"D"`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { rated: "PG-13" } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ status: "D" }
```

The MongoDB Compass query bar autocompletes the current query based on the keys in your collection's documents, including keys in embedded sub-documents.

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("D"));
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "D");
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{{"status", "D"}},
)

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(eq("status", "D"));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(eq("status", "D"));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(eq("status", "D"))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"status": "D"})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({ status: 'D' });
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['status' => 'D']);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"status": "D"})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(status: 'D')
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(equal("status", "D"))
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

This operation uses a query predicate of `{ rated: "PG-13" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM movies WHERE rated = "PG-13"
```

</Tab>

<Tab name="Compass">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="C">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="C#">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Go">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Java (Async)">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Java (Sync)">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Kotlin (Coroutine)">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Motor">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Node.js">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="PHP">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Python">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Ruby">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

<Tab name="Scala">

This operation uses a query predicate of `{ status: "D" }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "D"
```

</Tab>

</Tabs>

## Specify Conditions Using Query Operators

<Tabs>

<Tab name="MongoDB Shell">

A query filter document can use the query operators to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="Compass">

A query filter document can use the query operators to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="C">

A query filter document can use the query operators to specify conditions in the following form:

```c
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="C#">

In addition to the equality filter, MongoDB provides various query operators to specify filter conditions. Use the FilterDefinitionBuilder methods to create a filter document. For example:

```csharp
var builder = Builders<BsonDocument>.Filter;
builder.And(builder.Eq(<field1>, <value1>), builder.Lt(<field2>, <value2>));
```

</Tab>

<Tab name="Go">

In addition to the equality filter, MongoDB provides various query operators to specify filter conditions. Use the bson package to create query operators for filter documents. For example:

```go
filter := bson.D{
    {"$and", bson.A{
        bson.D{{"field1", bson.D{{"$eq", value1}}}},
        bson.D{{"field2", bson.D{{"$lt", value2}}}},
    }},
}
```

</Tab>

<Tab name="Java (Async)">

In addition to the equality condition, MongoDB provides various query operators to specify filter conditions. Use the com.mongodb.client.model.Filters helper methods to facilitate the creation of filter documents. For example:

```java
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

</Tab>

<Tab name="Java (Sync)">

In addition to the equality condition, MongoDB provides various query operators to specify filter conditions. Use the com.mongodb.client.model.Filters helper methods to facilitate the creation of filter documents. For example:

```java
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

</Tab>

<Tab name="Kotlin (Coroutine)">

In addition to the equality condition, MongoDB provides various query operators to specify filter conditions. Use the com.mongodb.client.model.Filters helper methods to facilitate the creation of filter documents. For example:

```kotlin
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

</Tab>

<Tab name="Motor">

A query filter document can use the query operators to specify conditions in the following form:

```python
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="Node.js">

A query filter document can use the query operators to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="PHP">

A query filter document can use the query operators to specify conditions in the following form:

```php
[ <field1> => [ <operator1> => <value1> ], ... ]
```

</Tab>

<Tab name="Python">

A query filter document can use the query operators to specify conditions in the following form:

```python
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="Ruby">

A query filter document can use the query operators to specify conditions in the following form:

```ruby
{ <field1> => { <operator1> => <value1> }, ... }
```

</Tab>

<Tab name="Scala">

In addition to the equality condition, MongoDB provides various query operators to specify filter conditions. Use the `com.mongodb.client.model.Filters_` helper methods to facilitate the creation of filter documents. For example:

```scala
and(gte(<field1>, <value1>), lt(<field2>, <value2>), equal(<field3>, <value3>))
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The following example retrieves all documents from the `sample_mflix.movies` collection where `rated` equals either `"G"` or `"PG-13"`:

</Tab>

<Tab name="Compass">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="C">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="C#">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Go">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Java (Async)">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Java (Sync)">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Motor">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Node.js">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="PHP">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Python">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Ruby">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

<Tab name="Scala">

The following example retrieves all documents from the `inventory` collection where `status` equals either `"A"` or `"D"`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { rated: { $in: [ "G", "PG-13" ] } } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ status: { $in: [ "A", "D" ] } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "status", "{",
   "$in", "[",
   BCON_UTF8 ("A"), BCON_UTF8 ("D"),
   "]",
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.In("status", new[] { "A", "D" });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{{"status", bson.D{{"$in", bson.A{"A", "D"}}}}})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(in("status", "A", "D"));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(in("status", "A", "D"));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(`in`("status", "A", "D"))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"status": {"$in": ["A", "D"]}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  status: { $in: ['A', 'D'] }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['status' => ['$in' => ['A', 'D']]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"status": {"$in": ["A", "D"]}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(status: { '$in' => %w[A D] })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(in("status", "A", "D"))
```

</Tab>

</Tabs>

Although you can use the `$or` operator for this query, use the `$in` operator instead of `$or` when performing equality checks on the same field.

<Tabs>

<Tab name="MongoDB Shell">

The operation uses a query predicate of `{ rated: { $in: [ "G", "PG-13" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM movies WHERE rated in ("G", "PG-13")
```

</Tab>

<Tab name="Compass">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="C">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="C#">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Go">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Java (Async)">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Java (Sync)">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Kotlin (Coroutine)">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Motor">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Node.js">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="PHP">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Python">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Ruby">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

<Tab name="Scala">

The operation uses a query predicate of `{ status: { $in: [ "A", "D" ] } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status in ("A", "D")
```

</Tab>

</Tabs>

For the complete list of MongoDB query operators, see Query Predicates.

## Specify `AND` Conditions

A compound query can specify conditions for more than one field in the collection's documents. Implicitly, a logical `AND` conjunction connects the clauses of a compound query so that the query selects the documents in the collection that match all the conditions.

<Tabs>

<Tab name="MongoDB Shell">

The following example retrieves all documents in the `sample_mflix.movies` collection where `rated` equals `"G"` **and** `runtime` is less than (`$lt`) `90`:

</Tab>

<Tab name="Compass">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="C">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="C#">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Go">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Java (Async)">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Java (Sync)">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Motor">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Node.js">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="PHP">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Python">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Ruby">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Scala">

The following example retrieves all documents in the `inventory` collection where `status` equals `"A"` **and** `qty` is less than (`$lt`) `30`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { rated: "G", runtime: { $lt: 90 } } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ status: "A", qty: { $lt: 30 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "status", BCON_UTF8 ("A"),
   "qty", "{",
   "$lt", BCON_INT64 (30),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var builder = Builders<BsonDocument>.Filter;
var filter = builder.And(builder.Eq("status", "A"), builder.Lt("qty", 30));
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
		{"qty", bson.D{{"$lt", 30}}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(and(eq("status", "A"), lt("qty", 30)));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(and(eq("status", "A"), lt("qty", 30)));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(and(eq("status", "A"), lt("qty", 30)))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"status": "A", "qty": {"$lt": 30}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  status: 'A',
  qty: { $lt: 30 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find([
    'status' => 'A',
    'qty' => ['$lt' => 30],
]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"status": "A", "qty": {"$lt": 30}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(status: 'A', qty: { '$lt' => 30 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(and(equal("status", "A"), lt("qty", 30)))
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The operation uses a query predicate of `{ rated: "G", runtime: { $lt: 90 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM movies WHERE rated = "G" AND runtime < 90
```

</Tab>

<Tab name="Compass">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="C">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="C#">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Go">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Java (Async)">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Java (Sync)">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Kotlin (Coroutine)">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Motor">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Node.js">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="PHP">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Python">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Ruby">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

<Tab name="Scala">

The operation uses a query predicate of `{ status: "A", qty: { $lt: 30 } }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" AND qty < 30
```

</Tab>

</Tabs>

See comparison operators for other MongoDB comparison operators.

## Specify `OR` Conditions

Use the `$or` operator to specify a compound query that joins each clause with a logical `OR` conjunction. The query selects documents that match at least one condition.

<Tabs>

<Tab name="MongoDB Shell">

The following example retrieves all documents in the `sample_mflix.movies` collection where `rated` equals `"G"` **or** `runtime` is less than (`$lt`) `90`:

</Tab>

<Tab name="Compass">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="C">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="C#">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Go">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Java (Async)">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Java (Sync)">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Motor">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Node.js">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="PHP">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Python">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Ruby">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

<Tab name="Scala">

The following example retrieves all documents in the collection where `status` equals `"A"` **or**
`qty` is less than (`$lt`) `30`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { $or: [ { rated: "G" }, { runtime: { $lt: 90 } } ] } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ $or: [ { status: "A" }, { qty: { $lt: 30 } } ] }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "$or", "[",
   "{",
   "status", BCON_UTF8 ("A"),
   "}","{",
   "qty", "{",
   "$lt", BCON_INT64 (30),
   "}",
   "}",
   "]");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var builder = Builders<BsonDocument>.Filter;
var filter = builder.Or(builder.Eq("status", "A"), builder.Lt("qty", 30));
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{
			"$or",
			bson.A{
				bson.D{{"status", "A"}},
				bson.D{{"qty", bson.D{{"$lt", 30}}}},
			},
		},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(or(eq("status", "A"), lt("qty", 30)));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(or(eq("status", "A"), lt("qty", 30)));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(or(eq("status", "A"), lt("qty", 30)))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"$or": [{"status": "A"}, {"qty": {"$lt": 30}}]})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  $or: [{ status: 'A' }, { qty: { $lt: 30 } }]
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find([
    '$or' => [
        ['status' => 'A'],
        ['qty' => ['$lt' => 30]],
    ],
]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"$or": [{"status": "A"}, {"qty": {"$lt": 30}}]})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('$or' => [ { status: 'A' },
                                   { qty: { '$lt' => 30 } } ])
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(or(equal("status", "A"), lt("qty", 30)))
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The operation uses a query predicate of `{ $or: [ { rated: 'G' }, { runtime: { $lt: 90 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM movies WHERE rated = "G" OR runtime < 90
```

</Tab>

<Tab name="Compass">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="C">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="C#">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Go">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Java (Async)">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Java (Sync)">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Kotlin (Coroutine)">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Motor">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Node.js">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="PHP">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Python">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Ruby">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

<Tab name="Scala">

The operation uses a query predicate of `{ $or: [ { status: 'A' }, { qty: { $lt: 30 } } ] }`, which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A" OR qty < 30
```

</Tab>

</Tabs>

Queries with comparison operators are subject to Type Bracketing.

## Specify `AND` as well as `OR` Conditions

<Tabs>

<Tab name="MongoDB Shell">

In the following example, the compound query document selects all documents in the `sample_mflix.movies` collection where `rated` equals `"G"` **and** *either* `runtime` is less than (`$lt`) `90` *or* `title` starts with the character `T`:

</Tab>

<Tab name="Compass">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="C">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="C#">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Go">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Java (Async)">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Java (Sync)">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Kotlin (Coroutine)">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Motor">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Node.js">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="PHP">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Python">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Ruby">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

<Tab name="Scala">

In the following example, the compound query document selects all documents in the collection where `status` equals `"A"` **and** *either* `qty` is less than (`$lt`) `30` *or* `item` starts with the character `p`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( {
     rated: "G",
     $or: [ { runtime: { $lt: 90 } }, { title: /^T/ } ]
} )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ status: "A", $or: [ { qty: { $lt: 30 } }, { item: /^p/ } ] }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "status", BCON_UTF8 ("A"),
   "$or", "[",
   "{",
   "qty", "{",
   "$lt", BCON_INT64 (30),
   "}",
   "}","{",
   "item", BCON_REGEX ("^p", ""),
   "}",
   "]");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var builder = Builders<BsonDocument>.Filter;
var filter = builder.And(
    builder.Eq("status", "A"),
    builder.Or(builder.Lt("qty", 30), builder.Regex("item", new BsonRegularExpression("^p"))));
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
		{"$or", bson.A{
			bson.D{{"qty", bson.D{{"$lt", 30}}}},
			bson.D{{"item", bson.Regex{Pattern: "^p", Options: ""}}},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(
        and(eq("status", "A"),
                or(lt("qty", 30), regex("item", "^p")))
);
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(
        and(eq("status", "A"),
                or(lt("qty", 30), regex("item", "^p")))
);
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(
        and(eq("status", "A"),
            or(lt("qty", 30), regex("item", "^p")))
    )
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find(
    {"status": "A", "$or": [{"qty": {"$lt": 30}}, {"item": {"$regex": "^p"}}]}
)
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  status: 'A',
  $or: [{ qty: { $lt: 30 } }, { item: { $regex: '^p' } }]
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find([
    'status' => 'A',
    '$or' => [
        ['qty' => ['$lt' => 30]],
        // Alternatively: ['item' => new \MongoDB\BSON\Regex('^p')]
        ['item' => ['$regex' => '^p']],
    ],
]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find(
    {"status": "A", "$or": [{"qty": {"$lt": 30}}, {"item": {"$regex": "^p"}}]}
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(status: 'A',
                        '$or' => [ { qty: { '$lt' => 30 } },
                                   { item: { '$regex' => BSON::Regexp::Raw.new('^p') } } ])
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(and(
  equal("status", "A"),
  or(lt("qty", 30), regex("item", "^p")))
)
```

</Tab>

</Tabs>

The operation uses a query predicate of:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
{
   rated: 'G',
   $or: [
     { runtime: { $lt: 90 } },
     { title: { $regex: '^T' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM movies WHERE rated = "G"
AND ( runtime < 90 OR title LIKE "T%")
```

</Tab>

<Tab name="Compass">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="C">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="C#">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Go">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Java (Async)">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Java (Sync)">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Motor">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Node.js">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="PHP">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Python">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Ruby">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

<Tab name="Scala">

```javascript
{
   status: 'A',
   $or: [
     { qty: { $lt: 30 } },
     { item: { $regex: '^p' } }
   ]
}
```

which corresponds to the following SQL statement:

```sql
SELECT * FROM inventory WHERE status = "A"
AND ( qty < 30 OR item LIKE "p%")
```

</Tab>

</Tabs>

MongoDB supports regular expressions `$regex` queries to perform string pattern matches.

## Query Documents with MongoDB Atlas

This example uses the sample movies dataset. To load the sample dataset into your MongoDB Atlas deployment, see Load Sample Data.

To project fields for a query in MongoDB Atlas, follow these steps:

### In the MongoDB Atlas UI, go to the Clusters page for your project.

- If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Clusters under the Database heading.

  The Clusters page displays.

### Navigate to the collection

- For the cluster that contains the sample data, click Browse Collections.

- In the left navigation pane, select the `sample_mflix` database.

- Select the `movies` collection.

### Specify the Filter field

Specify the query filter document in the Filter field. A query filter document uses query operators to specify search conditions.

Copy the following query filter document into the Filter search bar:

```javascript
{ year: 1924 }
```

### Click Apply

The query returns all documents in the `sample_mflix.movies` collection where the `year` field matches `1924`.

## Additional Query Tutorials

For more query examples, see:

- Query on Embedded/Nested Documents

- Query an Array

- Query an Array of Embedded Documents

- Project Fields to Return from Query

- Query for Null or Missing Fields

## Behavior

### Cursor

<Tabs>

<Tab name="MongoDB Shell">

The `db.collection.find()` method returns a cursor to the matching documents.

</Tab>

<Tab name="Compass">

The Find operation opens a cursor to the matching documents of the collection based on the find query.

For more information on sampling, see the Compass FAQ.

</Tab>

<Tab name="C">

The mongoc_collection_find_with_opts method returns a cursor to the matching documents.

</Tab>

<Tab name="C#">

The MongoCollection.Find() method returns a cursor to the matching documents. See the MongoDB C# driver documentation for iterating over a cursor.

</Tab>

<Tab name="Go">

The Collection.Find function returns a Cursor to the matching documents. See the Cursor documentation for more information.

</Tab>

<Tab name="Java (Async)">

com.mongodb.reactivestreams.client.MongoCollection.find) returns an instance of the com.mongodb.reactivestreams.client.FindPublisher interface.

</Tab>

<Tab name="Java (Sync)">

The com.mongodb.client.MongoCollection.find method returns an instance of the com.mongodb.client.FindIterable interface.

</Tab>

<Tab name="Kotlin (Coroutine)">

The MongoCollection.find() method returns an instance of the FindFlow class.

</Tab>

<Tab name="Motor">

The `pymongo.asynchronous.collection.AsyncCollection.find` method returns a cursor to the matching documents.

</Tab>

<Tab name="Node.js">

The Collection.find() method returns a cursor.

</Tab>

<Tab name="PHP">

The `MongoDB\\Collection::find()` method returns a cursor to the matching documents. See the MongoDB PHP Library documentation for iterating over a cursor.

</Tab>

<Tab name="Python">

The `pymongo.collection.Collection.find` method returns a cursor to the matching documents. See the PyMongo documentation for iterating over a cursor.

</Tab>

<Tab name="Ruby">

The Mongo::Collection#find() method returns a CollectionView, which is an `Enumerable`. A Cursor is created when the `View` is enumerated; for example, by calling `#to_a()` or `#each()`. You can also get an `Enumerator` by calling `#to_enum()` on the `View`. See the Ruby driver API documentation for iterating over a cursor.

</Tab>

<Tab name="Scala">

The collection.find()(implicite:org.mongodb.scala.bson.DefaultHelper.DefaultsTo[C,TResult],implicitct:scala.reflect.ClassTag[C]):org.mongodb.scala.FindObservable[C]) method returns the find Observable.

</Tab>

</Tabs>

### Concurrent Updates While Using a Cursor

As a cursor returns documents, other operations may run in the background and affect the results, depending on the read concern level. For details, see Read Isolation, Consistency, and Recency.

### Read Isolation

For reads to replica sets and replica set shards, read concern lets clients choose an isolation level for their reads. For more information, see Read Concern.

### Query Result Format

When you run a find operation with a MongoDB driver or `mongosh`, MongoDB returns a cursor that manages query results. Query results are not returned as an array of documents.

To learn how to iterate through documents in a cursor, see your driver's documentation. If you are using `mongosh`, see Iterate a Cursor in `mongosh`.

## Additional Methods and Options

<Tabs>

<Tab name="MongoDB Shell">

You can also read documents from a collection with:

- The `db.collection.findOne()` method

- The `$match` pipeline stage in an aggregation pipeline

The `db.collection.findOne()` method performs the same operation as `db.collection.find()` with a limit of 1.

</Tab>

<Tab name="Compass">

MongoDB Compass also accepts the following query bar options:

| Project | Specify which fields to return in the resulting data. |
| --- | --- |
| Sort | Specify the sort order of the returned documents. |
| Skip | Specify the first n-number of documents to skip before returning the result set. |
| Limit | Specify the maximum number of documents to return. |

</Tab>

<Tab name="C">

You can also read documents from a collection with:

- mongoc_find_and_modify_opts_t

</Tab>

<Tab name="C#">

You can also read documents from a collection with:

- MongoCollection.FindOne()

- The `$match` pipeline stage in an aggregation pipeline. For more information, see the LINQ documentation.

The MongoCollection.FindOne() method performs the same operation as MongoCollection.Find() with a limit of 1.

</Tab>

<Tab name="Go">

You can also read documents from a collection with:

- Collection.FindOne

- The `$match` pipeline stage in an aggregation pipeline. For more information, see Collection.Aggregate.

</Tab>

<Tab name="Java (Async)">

You can also read documents from a collection with the `$match` pipeline stage in an aggregation pipeline. For more information, see the Java Asynchronous Driver Aggregation Examples.

</Tab>

<Tab name="Java (Sync)">

You can also read documents from a collection with the `$match` pipeline stage in an aggregation pipeline. For more information, see the Java Synchronous Driver Aggregation Examples.

</Tab>

<Tab name="Kotlin (Coroutine)">

You can also read documents from a collection with the `$match` pipeline stage in an aggregation pipeline. For more information, see the Kotlin Coroutine Driver Find Operation Examples.

</Tab>

<Tab name="Motor">

You can also read documents from a collection with:

- `pymongo.asynchronous.collection.AsyncCollection.find_one`

- The `$match` pipeline stage in an aggregation pipeline

The `pymongo.asynchronous.collection.AsyncCollection.find_one` method performs the same operation as `pymongo.asynchronous.collection.AsyncCollection.find` with a limit of 1.

</Tab>

<Tab name="Node.js">

You can also read documents from a collection with:

- Collection.findOne()

- The `$match` pipeline stage in an aggregation pipeline. For more information, see the aggregation tutorial.

The Collection.findOne() method performs the same operation as Collection.find() with a limit of 1.

</Tab>

<Tab name="PHP">

You can also read documents from a collection with:

- `MongoDB\\Collection::findOne()`

- The `$match` pipeline stage in an aggregation pipeline. For more information, see the aggregation example.

The `MongoDB\\Collection::findOne()` method performs the same operation as `MongoDB\\Collection::find()` with a limit of 1.

</Tab>

<Tab name="Python">

You can also read documents from a collection with:

- `pymongo.collection.Collection.find_one`

- The `$match` pipeline stage in an aggregation pipeline. See the PyMongo Aggregation Examples.

The `pymongo.collection.Collection.find_one` method performs the same operation as the the `pymongo.collection.Collection.find` method with a limit of 1.

</Tab>

<Tab name="Ruby">

You can also read documents from a collection with the `$match` pipeline stage in an aggregation pipeline. For more information, see the aggregation examples.

</Tab>

<Tab name="Scala">

You can also read documents from a collection with the `$match` pipeline stage in an aggregation pipeline. For more information, see the aggregate method(implicite:org.mongodb.scala.bson.DefaultHelper.DefaultsTo[C,TResult],implicitct:scala.reflect.ClassTag[C]):org.mongodb.scala.AggregateObservable[C]).

</Tab>

</Tabs>
