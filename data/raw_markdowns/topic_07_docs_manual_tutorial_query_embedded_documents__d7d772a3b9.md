> Source: https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
> Fetch method: direct_markdown

# Query on Embedded/Nested Documents

Query embedded documents in MongoDBwith the following methods:

[Query Embedded Documents with MongoDB Atlas](https://www.mongodb.com/docs/tutorial/query-embedded-documents/#std-label-query-embedded-documents-atlas-ui)- Your programming language's driver.

- The [MongoDB Atlas UI](https://www.mongodb.com/docs/atlas/). To learn more, see [Query Embedded Documents with MongoDB Atlas](https://www.mongodb.com/docs/tutorial/query-embedded-documents/#std-label-query-embedded-documents-atlas-ui).

- [MongoDB Compass](https://www.mongodb.com/docs/compass/current/).

➤➤ Use the **Select your language** drop-down menu in the upper-right to set the language of the following examples or select MongoDB Compass.

query operations on embedded/nested documents

<Tabs>

<Tab name="MongoDB Shell">

This page provides examples of query operations on embedded/nested documents using the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh).

</Tab>

<Tab name="Compass">

This page provides examples of query operations on embedded/nested documents using [MongoDB Compass](https://www.mongodb.com/docs/compass/current/#std-label-compass-index).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C">

This page provides examples of query operations on embedded/nested documents using [mongoc_collection_find_with_opts](https://mongoc.org/libmongoc/current/mongoc_collection_find_with_opts.html).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C#">

This page provides examples of query operations on embedded/nested documents using the [MongoCollection.Find()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_MongoCollection_1_Find.htm) method in the [MongoDB C# Driver](https://mongodb.github.io/mongo-csharp-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Go">

This page provides examples of query operations on embedded/nested documents using the [Collection.Find](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.Find) function in the [MongoDB Go Driver](https://github.com/mongodb/mongo-go-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Async)">

This page provides examples of query operations on embedded/nested documents using the [com.mongodb.reactivestreams.client.MongoCollection.find](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#find()) method in the MongoDB [Java Reactive Streams Driver](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Sync)">

This page provides examples of query operations on embedded/nested documents using the [com.mongodb.client.MongoCollection.find](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#find--) method in the MongoDB [Java Synchronous Driver](http://mongodb.github.io/mongo-java-driver/3.4/driver/).

The driver provides [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Kotlin (Coroutine)">

This page provides examples of query operations on embedded/nested documents by using the [MongoCollection.find()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/find.html) method in the MongoDB [Kotlin Coroutine Driver](https://www.mongodb.com/docs/drivers/kotlin/coroutine/current/).

The driver provides [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Motor">

As of May 14, 2025, Motor is deprecated in favor of the GA release of the PyMongo Async API in the PyMongo library. We will not add new features to Motor, and we will provide only bug fixes until it reaches end of life on May 14, 2026. After that, we will fix only critical bugs until final support ends on May 14, 2027. We strongly recommend migrating to the PyMongo Async API while Motor is still supported.

For more information about migrating, see the [Migrate to PyMongo Async](https://www.mongodb.com/docs/languages/python/pymongo-driver/reference/migration/#std-label-pymongo-async-motor-migration) guide in the PyMongo documentation.

This page provides examples of query operations on embedded/nested documents using the [`pymongo.asynchronous.collection.AsyncCollection.find`](https://pymongo.readthedocs.io/en/stable/api/pymongo/asynchronous/collection.html#pymongo.asynchronous.collection.AsyncCollection.find) method in the [PyMongo Async API](https://pymongo.readthedocs.io/en/stable/api/pymongo/asynchronous/index.html).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Node.js">

This page provides examples of query operations on embedded/nested documents using the [Collection.find()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#find) method in the [MongoDB Node.js Driver](http://mongodb.github.io/node-mongodb-native/3.6/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="PHP">

This page provides examples of query operations on embedded/nested documents using the [`MongoDB\\Collection::find()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-find/#mongodb-phpmethod-phpmethod.MongoDB-Collection--find--) method in the [MongoDB PHP Library](https://www.mongodb.com/docs/drivers/php-libraries/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Python">

This page provides examples of query operations on embedded/nested documents using the [`pymongo.collection.Collection.find`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.find) method in the [PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/) Python driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Ruby">

This page provides examples of query operations on embedded/nested documents using the [Mongo::Collection#find()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#find-instance_method) method in the [MongoDB Ruby Driver](https://www.mongodb.com/docs/ruby-driver/current/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Scala">

This page provides examples of query operations on embedded/nested documents using the [collection.find()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#find[C](filter:org.mongodb.scala.bson.conversions.Bson)(implicite:org.mongodb.scala.bson.DefaultHelper.DefaultsTo[C,TResult],implicitct:scala.reflect.ClassTag[C]):org.mongodb.scala.FindObservable[C]) method in the [MongoDB Scala Driver](http://mongodb.github.io/mongo-scala-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.insertMany( [
   { item: "journal", qty: 25, size: { h: 14, w: 21, uom: "cm" }, status: "A" },
   { item: "notebook", qty: 50, size: { h: 8.5, w: 11, uom: "in" }, status: "A" },
   { item: "paper", qty: 100, size: { h: 8.5, w: 11, uom: "in" }, status: "D" },
   { item: "planner", qty: 75, size: { h: 22.85, w: 30, uom: "cm" }, status: "D" },
   { item: "postcard", qty: 45, size: { h: 10, w: 15.25, uom: "cm" }, status: "A" }
]);
```

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

For instructions on inserting documents in MongoDB Compass, see [Insert Documents](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert).

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
var documents = new[]
{
    new BsonDocument
    {
        { "item", "journal" },
        { "qty", 25 },
        { "size", new BsonDocument { { "h", 14 }, { "w", 21 }, { "uom", "cm" } } },
        { "status", "A" }
    },
    new BsonDocument
    {
        { "item", "notebook" },
        { "qty", 50 },
        { "size", new BsonDocument { { "h", 8.5 }, { "w", 11 }, { "uom", "in" } } },
        { "status", "A" }
    },
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
        { "status", "A" } },
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
# Subdocument key order matters in a few of these examples so we have
# to use bson.son.SON instead of a Python dict.
from bson.son import SON

await db.inventory.insert_many(
    [
        {
            "item": "journal",
            "qty": 25,
            "size": SON([("h", 14), ("w", 21), ("uom", "cm")]),
            "status": "A",
        },
        {
            "item": "notebook",
            "qty": 50,
            "size": SON([("h", 8.5), ("w", 11), ("uom", "in")]),
            "status": "A",
        },
        {
            "item": "paper",
            "qty": 100,
            "size": SON([("h", 8.5), ("w", 11), ("uom", "in")]),
            "status": "D",
        },
        {
            "item": "planner",
            "qty": 75,
            "size": SON([("h", 22.85), ("w", 30), ("uom", "cm")]),
            "status": "D",
        },
        {
            "item": "postcard",
            "qty": 45,
            "size": SON([("h", 10), ("w", 15.25), ("uom", "cm")]),
            "status": "A",
        },
    ]
)
```

</Tab>

<Tab name="Node.js">

```javascript
const documentsToInsert = [
  {
    item: 'journal',
    qty: 25,
    size: { h: 14, w: 21, uom: 'cm' },
    status: 'A',
  },
  {
    item: 'notebook',
    qty: 50,
    size: { h: 8.5, w: 11, uom: 'in' },
    status: 'P',
  },
  {
    item: 'paper',
    qty: 100,
    size: { h: 8.5, w: 11, uom: 'in' },
    status: 'D',
  },
  {
    item: 'planner',
    qty: 75,
    size: { h: 22.85, w: 30, uom: 'cm' },
    status: 'D',
  },
  {
    item: 'postcard',
    qty: 45,
    size: { h: 10, w: 15.25, uom: 'cm' },
    status: 'A',
  },
];

await collection.insertMany(documentsToInsert);

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
client[:inventory].insert_many([
                                 { item: 'journal',
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
                                   status: 'A' }
                               ])
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

## Query Nested Fields with Dot Notation

Specify query conditions on fields in an embedded/nested document with [dot notation](https://www.mongodb.com/docs/reference/glossary/#std-term-dot-notation) `"field.nestedField"`.

When you query with dot notation, the field and nested field must be inside quotation marks.

### Specify Equality Match on a Nested Field

The following example selects all documents where the field `uom` nested in the `size` field equals `"in"`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "size.uom": "in" } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "size.uom": "in" }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("size.uom", BCON_UTF8 ("in"));
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("size.uom", "in");
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{{"size.uom", "in"}},
)

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(eq("size.uom", "in"));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(eq("size.uom", "in"));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(eq("size.uom", "in"))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"size.uom": "in"})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  'size.uom': 'in'
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['size.uom' => 'in']);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"size.uom": "in"})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('size.uom' => 'in')
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(equal("size.uom", "in"))
```

</Tab>

</Tabs>

### Specify Match using Query Operator

<Tabs>

<Tab name="MongoDB Shell">

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="Compass">

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="C">

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```c
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="C#">

In addition to the equality filter, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the [FilterDefinitionBuilder](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/T_MongoDB_Driver_FilterDefinitionBuilder_1.htm) methods to create a filter document. For example:

```csharp
var builder = Builders<BsonDocument>.Filter;
builder.And(builder.Eq(<field1>, <value1>), builder.Lt(<field2>, <value2>));
```

</Tab>

<Tab name="Go">

In addition to the equality filter, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the bson package to create query operators for filter documents. For example:

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

In addition to the equality condition, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. For example:

```java
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

</Tab>

<Tab name="Java (Sync)">

In addition to the equality condition, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. For example:

```java
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

</Tab>

<Tab name="Kotlin (Coroutine)">

In addition to the equality condition, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. For example:

```kotlin
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

</Tab>

<Tab name="Motor">

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```python
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="Node.js">

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="PHP">

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```php
[ <field1> => [ <operator1> => <value1> ], ... ]
```

</Tab>

<Tab name="Python">

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```python
{ <field1>: { <operator1>: <value1> }, ... }
```

</Tab>

<Tab name="Ruby">

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```ruby
{ <field1> => { <operator1> => <value1> }, ... }
```

</Tab>

<Tab name="Scala">

In addition to the equality condition, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the `com.mongodb.client.model.Filters_` helper methods to facilitate the creation of filter documents. For example:

```scala
and(gte(<field1>, <value1>), lt(<field2>, <value2>), equal(<field3>, <value3>))
```

</Tab>

</Tabs>

The following query uses the less than operator ([`$lt`](https://www.mongodb.com/docs/reference/operator/query/lt/#mongodb-query-op.-lt)) on the field `h` embedded in the `size` field:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "size.h": { $lt: 15 } } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "size.h": { $lt: 15 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "size.h", "{",
   "$lt", BCON_INT64 (15),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Lt("size.h", 15);
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"size.h", bson.D{
			{"$lt", 15},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(lt("size.h", 15));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(lt("size.h", 15));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(lt("size.h", 15))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"size.h": {"$lt": 15}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  'size.h': { $lt: 15 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['size.h' => ['$lt' => 15]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"size.h": {"$lt": 15}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('size.h' => { '$lt' => 15 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(lt("size.h", 15))
```

</Tab>

</Tabs>

### Specify `AND` Condition

The following query selects all documents where the nested field `h` is less than `15`, the nested field `uom` equals `"in"`, and the `status` field equals `"D"`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "size.h": { $lt: 15 }, "size.uom": "in", status: "D" } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "size.h": { $lt: 15 }, "size.uom": "in", status: "D" }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "size.h", "{",
   "$lt", BCON_INT64 (15),
   "}",
   "size.uom", BCON_UTF8 ("in"),
   "status", BCON_UTF8 ("D"));
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var builder = Builders<BsonDocument>.Filter;
var filter = builder.And(builder.Lt("size.h", 15), builder.Eq("size.uom", "in"), builder.Eq("status", "D"));
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"size.h", bson.D{
			{"$lt", 15},
		}},
		{"size.uom", "in"},
		{"status", "D"},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(and(
        lt("size.h", 15),
        eq("size.uom", "in"),
        eq("status", "D")
));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(and(
        lt("size.h", 15),
        eq("size.uom", "in"),
        eq("status", "D")
));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(and(
        lt("size.h", 15),
        eq("size.uom", "in"),
        eq("status", "D")
    ))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"size.h": {"$lt": 15}, "size.uom": "in", "status": "D"})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  'size.h': { $lt: 15 },
  'size.uom': 'in',
  status: 'D'
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find([
    'size.h' => ['$lt' => 15],
    'size.uom' => 'in',
    'status' => 'D',
]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"size.h": {"$lt": 15}, "size.uom": "in", "status": "D"})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('size.h' => { '$lt' => 15 },
                        'size.uom' => 'in',
                        'status' => 'D')
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(and(
  lt("size.h", 15),
  equal("size.uom", "in"),
  equal("status", "D")
))
```

</Tab>

</Tabs>

## Match an Embedded/Nested Document

<Tabs>

<Tab name="MongoDB Shell">

To specify an equality condition on a field that is an embedded/nested document, use the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`{ <field>: <value> }` where `<value>` is the document to match.

</Tab>

<Tab name="Compass">

To specify an equality condition on a field that is an embedded/nested document, use the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`{ <field>: <value> }` where `<value>` is the document to match.

</Tab>

<Tab name="C">

To specify an equality condition on a field that is an embedded/nested document, use the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`{ <field>: <value> }` where `<value>` is the document to match.

</Tab>

<Tab name="C#">

To specify an equality condition on a field that is an embedded/nested document, construct a filter using the [Eq](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/Overload_MongoDB_Driver_FilterDefinitionBuilder_1_Eq.htm) method, where `<value>` is the document to match:

```csharp
Builders<BsonDocument>.Filter.Eq(<field>, <value>)
```

</Tab>

<Tab name="Go">

To specify an equality condition on a field that is an embedded document, use the [bson.D](https://godoc.org/github.com/mongodb/mongo-go-driver/bson#D) type to create a filter where `<value>` is the document to match:

```go
filter := bson.D{
    {<field>, bson.D{
        {"nestedField1", value1},
        {"nestedField2", value2},
    }},
}
```

</Tab>

<Tab name="Java (Async)">

To specify an equality condition on a field that is an embedded/nested document, use the filter document `eq( <field1>, <value>)` where `<value>` is the document to match.

</Tab>

<Tab name="Java (Sync)">

To specify an equality condition on a field that is an embedded/nested document, use the filter document `eq( <field1>, <value>)` where `<value>` is the document to match.

</Tab>

<Tab name="Kotlin (Coroutine)">

To specify an equality condition on a field that is an embedded document, use the [Document](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/bson/org/bson/Document.html) class or [eq()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/model/Filters.html#eq(java.lang.String,TItem)) method where `<value>` is the document to match:

```kotlin
eq(<field>, Document()
   .append("nestedField1", value1)
   .append("nestedField2", value2))
```

</Tab>

<Tab name="Motor">

To specify an equality condition on a field that is an embedded/nested document, use the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`{ <field>: <value> }` where `<value>` is the document to match.

</Tab>

<Tab name="Node.js">

To specify an equality condition on a field that is an embedded/nested document, use the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`{ <field>: <value> }` where `<value>` is the document to match.

</Tab>

<Tab name="PHP">

To specify an equality condition on a field that is an embedded/nested document, use the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`[ <field> => <value> ]` where `<value>` is the document to match.

</Tab>

<Tab name="Python">

To specify an equality condition on a field that is an embedded/nested document, use the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`{ <field>: <value> }` where `<value>` is the document to match.

</Tab>

<Tab name="Ruby">

To specify an equality condition on a field that is an embedded/nested document, use the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`{ <field> => <value> }` where `<value>` is the document to match.

</Tab>

<Tab name="Scala">

To specify an equality condition on a field that is an embedded/nested document, use the filter document `equal( <field1>, <value> )` where `<value>` is the document to match.

</Tab>

</Tabs>

For example, the following query selects all documents where the field `size` equals the document `{ h: 14, w: 21, uom: "cm" }`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { size: { h: 14, w: 21, uom: "cm" } } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ size: { h: 14, w: 21, uom: "cm" } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "size", "{",
   "h", BCON_DOUBLE (14),
   "w", BCON_DOUBLE (21),
   "uom", BCON_UTF8 ("cm"),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("size", new BsonDocument { { "h", 14 }, { "w", 21 }, { "uom", "cm" } });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"size", bson.D{
			{"h", 14},
			{"w", 21},
			{"uom", "cm"},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
FindPublisher<Document> findPublisher = collection.find(eq("size", Document.parse("{ h: 14, w: 21, uom: 'cm' }")));
```

</Tab>

<Tab name="Java (Sync)">

```java
FindIterable<Document> findIterable = collection.find(eq("size", Document.parse("{ h: 14, w: 21, uom: 'cm' }")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(eq("size", Document.parse("{ h: 14, w: 21, uom: 'cm' }")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"size": SON([("h", 14), ("w", 21), ("uom", "cm")])})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = collection.find({
  size: { h: 14, w: 21, uom: 'cm' },
});

```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['size' => ['h' => 14, 'w' => 21, 'uom' => 'cm']]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"size": {"h": 14, "w": 21, "uom": "cm"}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(size: { h: 14, w: 21, uom: 'cm' })
```

</Tab>

<Tab name="Scala">

```scala
var findObservable = collection.find(equal("size", Document("h" -> 14, "w" -> 21, "uom" -> "cm")))
```

</Tab>

</Tabs>

MongoDB does not recommend [comparisons](https://www.mongodb.com/docs/reference/mql/query-predicates/comparison/#std-label-query-comparison) on embedded documents because the operations require an *exact* match of the specified `<value>` document, including the field order.

For example, the following query does not match any documents in the `inventory` collection:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find(  { size: { w: 21, h: 14, uom: "cm" } }  )
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
filter = BCON_NEW (
   "size", "{",
   "w", BCON_DOUBLE (21),
   "h", BCON_DOUBLE (14),
   "uom", BCON_UTF8 ("cm"),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("size", new BsonDocument { { "w", 21 }, { "h", 14 }, { "uom", "cm" } });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"size", bson.D{
			{"w", 21},
			{"h", 14},
			{"uom", "cm"},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(eq("size", Document.parse("{ w: 21, h: 14, uom: 'cm' }")));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(eq("size", Document.parse("{ w: 21, h: 14, uom: 'cm' }")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(eq("size", Document.parse("{ w: 21, h: 14, uom: 'cm' }")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"size": SON([("w", 21), ("h", 14), ("uom", "cm")])})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  size: { w: 21, h: 14, uom: 'cm' }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['size' => ['w' => 21, 'h' => 14, 'uom' => 'cm']]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"size": {"w": 21, "h": 14, "uom": "cm"}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(size: { h: 21, w: 14, uom: 'cm' })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(equal("size", Document("w" -> 21, "h" -> 14, "uom" -> "cm")))
```

</Tab>

</Tabs>

Queries that use comparisons on embedded documents can result in unpredictable behavior when used with a driver that does not use ordered data structures for expressing queries.

## Query Embedded Documents with MongoDB Atlas

This example uses the [sample movies dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/). To load the sample dataset into your MongoDB Atlas deployment, see [Load Sample Data](https://www.mongodb.com/docs/atlas/sample-data/#std-label-load-sample-data).

To query an embedded document in MongoDB Atlas, follow these steps:

### In the MongoDB Atlas UI, go to the Clusters page for your project.

- If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Clusters under the Database heading.

  The [Clusters](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fclusters) page displays.

### Navigate to the collection

- For the cluster that contains the sample data, click Browse Collections.

- In the left navigation pane, select the `sample_mflix` database.

- Select the `movies` collection.

### Specify the query filter document

Specify the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) in the Filter field. A query filter document uses [query operators](https://www.mongodb.com/docs/core/csfle/reference/supported-operations/#std-label-csfle-supported-query-operators) to specify search conditions.

Copy the following query filter document into the Filter search bar:

```javascript
{ "awards.wins": 1 }
```

### Click Apply

This query filter returns all documents in the `sample_mflix.movies` collection where the embedded  document for the `awards` field contains `{ wins: 1 }`.

## Additional Query Tutorials

For additional query examples, see:

- [Use `$all` to Match Values](https://www.mongodb.com/docs/reference/operator/query/all/#std-label-match-values-with-all)

- [Use `$all` with `$elemMatch`](https://www.mongodb.com/docs/reference/operator/query/all/#std-label-all-with-elemMatch)

- [Query Documents](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-queries)

- [Query an Array](https://www.mongodb.com/docs/tutorial/query-arrays/#std-label-read-operations-arrays)

- [Query an Array of Embedded Documents](https://www.mongodb.com/docs/tutorial/query-array-of-documents/#std-label-array-match-embedded-documents)
