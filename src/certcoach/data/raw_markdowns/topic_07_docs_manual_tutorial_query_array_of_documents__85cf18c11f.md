> Source: https://www.mongodb.com/docs/manual/tutorial/query-array-of-documents/
> Fetch method: direct_markdown

# Query an Array of Embedded Documents

You can query documents in MongoDB by using the following methods:

[Query an Array of Documents with MongoDB Atlas](https://www.mongodb.com/docs/tutorial/query-array-of-documents/#std-label-query-array-documents-atlas-ui)- Your programming language's driver.

- The [MongoDB Atlas UI](https://www.mongodb.com/docs/atlas/). To learn more, see [Query an Array of Documents with MongoDB Atlas](https://www.mongodb.com/docs/tutorial/query-array-of-documents/#std-label-query-array-documents-atlas-ui).

- [MongoDB Compass](https://www.mongodb.com/docs/compass/current/).

➤➤ Use the **Select your language** drop-down menu in the upper-right to set the language of the following examples or select MongoDB Compass.

query operations on an array of nested documents

<Tabs>

<Tab name="MongoDB Shell">

This page provides examples of query operations on an array of nested documents using the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh).

</Tab>

<Tab name="Compass">

This page provides examples of query operations on an array of nested documents using [MongoDB Compass](https://www.mongodb.com/docs/compass/current/#std-label-compass-index).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C">

This page provides examples of query operations on an array of nested documents using [mongoc_collection_find_with_opts](https://mongoc.org/libmongoc/current/mongoc_collection_find_with_opts.html).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C#">

This page provides examples of query operations on an array of nested documents using the [MongoCollection.Find()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_MongoCollection_1_Find.htm) method in the [MongoDB C# Driver](https://mongodb.github.io/mongo-csharp-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Go">

This page provides examples of query operations on an array of nested documents using the [Collection.Find](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.Find) function in the [MongoDB Go Driver](https://github.com/mongodb/mongo-go-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Async)">

This page provides examples of query operations on an array of nested documents using the [com.mongodb.reactivestreams.client.MongoCollection.find](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#find()) method in the MongoDB [Java Reactive Streams Driver](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Sync)">

This page provides examples of query operations on an array of nested documents using the [com.mongodb.client.MongoCollection.find](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#find--) method in the MongoDB [Java Synchronous Driver](http://mongodb.github.io/mongo-java-driver/3.4/driver/).

The driver provides [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Kotlin (Coroutine)">

This page provides examples of query operations on an array of nested documents by using the [MongoCollection.find()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/find.html) method in the MongoDB [Kotlin Coroutine Driver](https://www.mongodb.com/docs/drivers/kotlin/coroutine/current/).

The driver provides [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Motor">

As of May 14, 2025, Motor is deprecated in favor of the GA release of the PyMongo Async API in the PyMongo library. We will not add new features to Motor, and we will provide only bug fixes until it reaches end of life on May 14, 2026. After that, we will fix only critical bugs until final support ends on May 14, 2027. We strongly recommend migrating to the PyMongo Async API while Motor is still supported.

For more information about migrating, see the [Migrate to PyMongo Async](https://www.mongodb.com/docs/languages/python/pymongo-driver/reference/migration/#std-label-pymongo-async-motor-migration) guide in the PyMongo documentation.

This page provides examples of query operations on an array of nested documents using the [`pymongo.asynchronous.collection.AsyncCollection.find`](https://pymongo.readthedocs.io/en/stable/api/pymongo/asynchronous/collection.html#pymongo.asynchronous.collection.AsyncCollection.find) method in the [PyMongo Async API](https://pymongo.readthedocs.io/en/stable/api/pymongo/asynchronous/index.html).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Node.js">

This page provides examples of query operations on an array of nested documents using the [Collection.find()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#find) method in the [MongoDB Node.js Driver](http://mongodb.github.io/node-mongodb-native/3.6/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="PHP">

This page provides examples of query operations on an array of nested documents using the [`MongoDB\\Collection::find()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-find/#mongodb-phpmethod-phpmethod.MongoDB-Collection--find--) method in the [MongoDB PHP Library](https://www.mongodb.com/docs/drivers/php-libraries/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Python">

This page provides examples of query operations on an array of nested documents using the [`pymongo.collection.Collection.find`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.find) method in the [PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/) Python driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Ruby">

This page provides examples of query operations on an array of nested documents using the [Mongo::Collection#find()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#find-instance_method) method in the [MongoDB Ruby Driver](https://www.mongodb.com/docs/ruby-driver/current/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Scala">

This page provides examples of query operations on an array of nested documents using the [collection.find()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#find[C](filter:org.mongodb.scala.bson.conversions.Bson)(implicite:org.mongodb.scala.bson.DefaultHelper.DefaultsTo[C,TResult],implicitct:scala.reflect.ClassTag[C]):org.mongodb.scala.FindObservable[C]) method in the [MongoDB Scala Driver](http://mongodb.github.io/mongo-scala-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.insertMany( [
   { item: "journal", instock: [ { warehouse: "A", qty: 5 }, { warehouse: "C", qty: 15 } ] },
   { item: "notebook", instock: [ { warehouse: "C", qty: 5 } ] },
   { item: "paper", instock: [ { warehouse: "A", qty: 60 }, { warehouse: "B", qty: 15 } ] },
   { item: "planner", instock: [ { warehouse: "A", qty: 40 }, { warehouse: "B", qty: 5 } ] },
   { item: "postcard", instock: [ { warehouse: "B", qty: 15 }, { warehouse: "C", qty: 35 } ] }
]);
```

</Tab>

<Tab name="Compass">

```javascript
[
    { "item": "journal", "instock": [ { "warehouse": "A", "qty": 5 }, { "warehouse": "C", "qty": 15 } ] },
    { "item": "notebook", "instock": [ { "warehouse": "C", "qty": 5 } ] },
    { "item": "paper", "instock": [ { "warehouse": "A", "qty": 60 }, { "warehouse": "B", "qty": 15 } ] },
    { "item": "planner", "instock": [ { "warehouse": "A", "qty": 40 }, { "warehouse": "B", "qty": 5 } ] },
    { "item": "postcard", "instock": [ { "warehouse": "B","qty": 15 }, { "warehouse": "C", "qty": 35 } ] }
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
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("A"),
   "qty", BCON_INT64 (5),
   "}","{",
   "warehouse", BCON_UTF8 ("C"),
   "qty", BCON_INT64 (15),
   "}",
   "]");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("notebook"),
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("C"),
   "qty", BCON_INT64 (5),
   "}",
   "]");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("paper"),
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("A"),
   "qty", BCON_INT64 (60),
   "}","{",
   "warehouse", BCON_UTF8 ("B"),
   "qty", BCON_INT64 (15),
   "}",
   "]");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("planner"),
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("A"),
   "qty", BCON_INT64 (40),
   "}","{",
   "warehouse", BCON_UTF8 ("B"),
   "qty", BCON_INT64 (5),
   "}",
   "]");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("postcard"),
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("B"),
   "qty", BCON_INT64 (15),
   "}","{",
   "warehouse", BCON_UTF8 ("C"),
   "qty", BCON_INT64 (35),
   "}",
   "]");

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
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "A" }, { "qty", 5 } },
                new BsonDocument { { "warehouse", "C" }, { "qty", 15 } } }
            }
    },
    new BsonDocument
    {
        { "item", "notebook" },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "C" }, { "qty", 5 } } }
            }
    },
    new BsonDocument
    {
        { "item", "paper" },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "A" }, { "qty", 60 } },
                new BsonDocument { { "warehouse", "B" }, { "qty", 15 } } }
            }
    },
    new BsonDocument
    {
        { "item", "planner" },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "A" }, { "qty", 40 } },
                new BsonDocument { { "warehouse", "B" }, { "qty", 5 } } }
            }
    },
    new BsonDocument
    {
        { "item", "postcard" },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "B" }, { "qty", 15 } },
                new BsonDocument { { "warehouse", "C" }, { "qty", 35 } } }
            }
    }
};
collection.InsertMany(documents);
```

</Tab>

<Tab name="Go">

```go

docs := []any{
	bson.D{
		{"item", "journal"},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "A"},
				{"qty", 5},
			},
			bson.D{
				{"warehouse", "C"},
				{"qty", 15},
			},
		}},
	},
	bson.D{
		{"item", "notebook"},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "C"},
				{"qty", 5},
			},
		}},
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
				{"qty", 15},
			},
		}},
	},
	bson.D{
		{"item", "planner"},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "A"},
				{"qty", 40},
			},
			bson.D{
				{"warehouse", "B"},
				{"qty", 5},
			},
		}},
	},
	bson.D{
		{"item", "postcard"},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "B"},
				{"qty", 15},
			},
			bson.D{
				{"warehouse", "C"},
				{"qty", 35},
			},
		}},
	},
}

result, err := coll.InsertMany(context.TODO(), docs)

```

</Tab>

<Tab name="Java (Async)">

```java
Publisher<Success> insertManyPublisher = collection.insertMany(asList(
        Document.parse("{ item: 'journal', instock: [ { warehouse: 'A', qty: 5 }, { warehouse: 'C', qty: 15 } ] }"),
        Document.parse("{ item: 'notebook', instock: [ { warehouse: 'C', qty: 5 } ] }"),
        Document.parse("{ item: 'paper', instock: [ { warehouse: 'A', qty: 60 }, { warehouse: 'B', qty: 15 } ] }"),
        Document.parse("{ item: 'planner', instock: [ { warehouse: 'A', qty: 40 }, { warehouse: 'B', qty: 5 } ] }"),
        Document.parse("{ item: 'postcard', instock: [ { warehouse: 'B', qty: 15 }, { warehouse: 'C', qty: 35 } ] }")
));
```

</Tab>

<Tab name="Java (Sync)">

```java
collection.insertMany(asList(
        Document.parse("{ item: 'journal', instock: [ { warehouse: 'A', qty: 5 }, { warehouse: 'C', qty: 15 } ] }"),
        Document.parse("{ item: 'notebook', instock: [ { warehouse: 'C', qty: 5 } ] }"),
        Document.parse("{ item: 'paper', instock: [ { warehouse: 'A', qty: 60 }, { warehouse: 'B', qty: 15 } ] }"),
        Document.parse("{ item: 'planner', instock: [ { warehouse: 'A', qty: 40 }, { warehouse: 'B', qty: 5 } ] }"),
        Document.parse("{ item: 'postcard', instock: [ { warehouse: 'B', qty: 15 }, { warehouse: 'C', qty: 35 } ] }")
));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
collection.insertMany(
    listOf(
        Document("item", "journal")
            .append("instock", listOf(
                Document("warehouse", "A").append("qty", 5),
                Document("warehouse", "C").append("qty", 15)
            )),
        Document("item", "notebook")
            .append("instock", listOf(
                Document("warehouse", "C").append("qty", 5)
            )),
        Document("item", "paper")
            .append("instock", listOf(
                Document("warehouse", "A").append("qty", 60),
                Document("warehouse", "B").append("qty", 15)
            )),
        Document("item", "planner")
            .append("instock", listOf(
                Document("warehouse", "A").append("qty", 40),
                Document("warehouse", "B").append("qty", 5)
            )),
        Document("item", "postcard")
            .append("instock", listOf(
                Document("warehouse", "B").append("qty", 15),
                Document("warehouse", "C").append("qty", 35)
            )),
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
            "instock": [
                SON([("warehouse", "A"), ("qty", 5)]),
                SON([("warehouse", "C"), ("qty", 15)]),
            ],
        },
        {"item": "notebook", "instock": [SON([("warehouse", "C"), ("qty", 5)])]},
        {
            "item": "paper",
            "instock": [
                SON([("warehouse", "A"), ("qty", 60)]),
                SON([("warehouse", "B"), ("qty", 15)]),
            ],
        },
        {
            "item": "planner",
            "instock": [
                SON([("warehouse", "A"), ("qty", 40)]),
                SON([("warehouse", "B"), ("qty", 5)]),
            ],
        },
        {
            "item": "postcard",
            "instock": [
                SON([("warehouse", "B"), ("qty", 15)]),
                SON([("warehouse", "C"), ("qty", 35)]),
            ],
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
    instock: [
      { warehouse: 'A', qty: 5 },
      { warehouse: 'C', qty: 15 }
    ]
  },
  {
    item: 'notebook',
    instock: [{ warehouse: 'C', qty: 5 }]
  },
  {
    item: 'paper',
    instock: [
      { warehouse: 'A', qty: 60 },
      { warehouse: 'B', qty: 15 }
    ]
  },
  {
    item: 'planner',
    instock: [
      { warehouse: 'A', qty: 40 },
      { warehouse: 'B', qty: 5 }
    ]
  },
  {
    item: 'postcard',
    instock: [
      { warehouse: 'B', qty: 15 },
      { warehouse: 'C', qty: 35 }
    ]
  }
]);
```

</Tab>

<Tab name="PHP">

```php
$insertManyResult = $db->inventory->insertMany([
    [
        'item' => 'journal',
        'instock' => [
            ['warehouse' => 'A',  'qty' => 5],
            ['warehouse' => 'C',  'qty' => 15],
        ],
    ],
    [
        'item' => 'notebook',
        'instock' => [
            ['warehouse' => 'C',  'qty' => 5],
        ],
    ],
    [
        'item' => 'paper',
        'instock' => [
            ['warehouse' => 'A',  'qty' => 60],
            ['warehouse' => 'B',  'qty' => 15],
        ],
    ],
    [
        'item' => 'planner',
        'instock' => [
            ['warehouse' => 'A',  'qty' => 40],
            ['warehouse' => 'B',  'qty' => 5],
        ],
    ],
    [
        'item' => 'postcard',
        'instock' => [
            ['warehouse' => 'B',  'qty' => 15],
            ['warehouse' => 'C',  'qty' => 35],
        ],
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
            "instock": [
                {"warehouse": "A", "qty": 5},
                {"warehouse": "C", "qty": 15},
            ],
        },
        {"item": "notebook", "instock": [{"warehouse": "C", "qty": 5}]},
        {
            "item": "paper",
            "instock": [
                {"warehouse": "A", "qty": 60},
                {"warehouse": "B", "qty": 15},
            ],
        },
        {
            "item": "planner",
            "instock": [
                {"warehouse": "A", "qty": 40},
                {"warehouse": "B", "qty": 5},
            ],
        },
        {
            "item": "postcard",
            "instock": [
                {"warehouse": "B", "qty": 15},
                {"warehouse": "C", "qty": 35},
            ],
        },
    ]
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].insert_many([ { item: 'journal',
                                   instock: [ { warehouse: 'A', qty: 5 },
                                              { warehouse: 'C', qty: 15 } ] },
                                 { item: 'notebook',
                                   instock: [ { warehouse: 'C', qty: 5 } ] },
                                 { item: 'paper',
                                   instock: [ { warehouse: 'A', qty: 60 },
                                              { warehouse: 'B', qty: 15 } ] },
                                 { item: 'planner',
                                   instock: [ { warehouse: 'A', qty: 40 },
                                              { warehouse: 'B', qty: 5 } ] },
                                 { item: 'postcard',
                                   instock: [ { warehouse: 'B', qty: 15 },
                                              { warehouse: 'C', qty: 35 } ] } ])
```

</Tab>

<Tab name="Scala">

```scala
collection.insertMany(Seq(
  Document("""{ item: "journal", instock: [ { warehouse: "A", qty: 5 }, { warehouse: "C", qty: 15 } ] }"""),
  Document("""{ item: "notebook", instock: [ { warehouse: "C", qty: 5 } ] }"""),
  Document("""{ item: "paper", instock: [ { warehouse: "A", qty: 60 }, { warehouse: "B", qty: 15 } ] }"""),
  Document("""{ item: "planner", instock: [ { warehouse: "A", qty: 40 }, { warehouse: "B", qty: 5 } ] }"""),
  Document("""{ item: "postcard", instock: [ { warehouse: "B", qty: 15 }, { warehouse: "C", qty: 35 } ] }""")
)).execute()
```

</Tab>

</Tabs>

## Query for a Document Nested in an Array

The following example selects all documents where an element in the `instock` array matches the specified document:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "instock": { warehouse: "A", qty: 5 } } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "instock": { warehouse: "A", qty: 5 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "instock", "{",
   "warehouse", BCON_UTF8 ("A"),
   "qty", BCON_INT64 (5),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.AnyEq("instock", new BsonDocument { { "warehouse", "A" }, { "qty", 5 } });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"instock", bson.D{
			{"warehouse", "A"},
			{"qty", 5},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
FindPublisher<Document> findPublisher = collection.find(eq("instock", Document.parse("{ warehouse: 'A', qty: 5 }")));
```

</Tab>

<Tab name="Java (Sync)">

```java
FindIterable<Document> findIterable = collection.find(eq("instock", Document.parse("{ warehouse: 'A', qty: 5 }")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(eq("instock", Document.parse("{ warehouse: 'A', qty: 5 }")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"instock": SON([("warehouse", "A"), ("qty", 5)])})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  instock: { warehouse: 'A', qty: 5 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['instock' => ['warehouse' => 'A', 'qty' => 5]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"instock": {"warehouse": "A", "qty": 5}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(instock: { warehouse: 'A', qty: 5 })
```

</Tab>

<Tab name="Scala">

```scala
var findObservable = collection.find(equal("instock", Document("warehouse" -> "A", "qty" -> 5)))
```

</Tab>

</Tabs>

Equality matches on the whole embedded/nested document require an *exact* match of the specified document, including the field order. For example, the following query does not match any documents in the `inventory` collection:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "instock": { qty: 5, warehouse: "A" } } )
```

</Tab>

<Tab name="Compass">

```javascript
instock: { qty: 5, warehouse: 'A' }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "instock", "{",
   "qty", BCON_INT64 (5),
   "warehouse", BCON_UTF8 ("A"),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.AnyEq("instock", new BsonDocument { { "qty", 5 }, { "warehouse", "A" } });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"instock", bson.D{
			{"qty", 5},
			{"warehouse", "A"},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(eq("instock", Document.parse("{ qty: 5, warehouse: 'A' }")));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(eq("instock", Document.parse("{ qty: 5, warehouse: 'A' }")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(eq("instock", Document.parse("{ qty: 5, warehouse: 'A' }")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"instock": SON([("qty", 5), ("warehouse", "A")])})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  instock: { qty: 5, warehouse: 'A' }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['instock' => ['qty' => 5, 'warehouse' => 'A']]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"instock": {"qty": 5, "warehouse": "A"}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(instock: { qty: 5, warehouse: 'A' })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(equal("instock", Document("qty" -> 5, "warehouse" -> "A")))
```

</Tab>

</Tabs>

## Specify a Query Condition on a Field in an Array of Documents

### Specify a Query Condition on a Field Embedded in an Array of Documents

If you do not know the index position of the document nested in the array, concatenate the name of the array field, with a dot (`.`) and the name of the field in the nested document.

The following example selects all documents where the `instock` array has at least one embedded document that contains the field `qty` whose value is less than or equal to `20`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { 'instock.qty': { $lte: 20 } } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ 'instock.qty': { $lte: 20 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "instock.qty", "{",
   "$lte", BCON_INT64 (20),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Lte("instock.qty", 20);
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"instock.qty", bson.D{
			{"$lte", 20},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(lte("instock.qty", 20));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(lte("instock.qty", 20));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(lte("instock.qty", 20))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"instock.qty": {"$lte": 20}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  'instock.qty': { $lte: 20 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['instock.qty' => ['$lte' => 20]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"instock.qty": {"$lte": 20}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('instock.qty' => { '$lte' => 20 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(lte("instock.qty", 20))
```

</Tab>

</Tabs>

### Use the Array Index to Query for a Field in the Embedded Document

Using [dot notation](https://www.mongodb.com/docs/reference/glossary/#std-term-dot-notation), you can specify query conditions for a field in a document at a particular index or position of the array. The array uses zero-based indexing.

When querying using dot notation, the field and index must be inside quotation marks.

The following example selects all documents where the `instock` array has as its first element a document that contains the field `qty` whose value is less than or equal to `20`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { 'instock.0.qty': { $lte: 20 } } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ 'instock.0.qty': { $lte: 20 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "instock.0.qty", "{",
   "$lte", BCON_INT64 (20),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Lte("instock.0.qty", 20);
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"instock.0.qty", bson.D{
			{"$lte", 20},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(lte("instock.0.qty", 20));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(lte("instock.0.qty", 20));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(lte("instock.0.qty", 20))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"instock.0.qty": {"$lte": 20}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  'instock.0.qty': { $lte: 20 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['instock.0.qty' => ['$lte' => 20]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"instock.0.qty": {"$lte": 20}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('instock.0.qty' => { '$lte' => 20 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(lte("instock.0.qty", 20))
```

</Tab>

</Tabs>

## Specify Multiple Conditions for Array of Documents

When you specify conditions on more than one field nested in an array of documents, you can specify the query such that either a single document meets these conditions or any combination of documents in the array meets the conditions.

### A Single Nested Document Meets Multiple Query Conditions on Nested Fields

Use the [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch) operator to specify multiple criteria on an array of embedded documents such that at least one embedded document satisfies all the specified criteria.

The following example queries for documents where the `instock` array has at least one embedded document that contains both the field `qty` equal to `5` and the field `warehouse` equal to `A`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "instock": { $elemMatch: { qty: 5, warehouse: "A" } } } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "instock": { $elemMatch: { qty: 5, warehouse: "A" } } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "instock", "{",
   "$elemMatch", "{",
   "qty", BCON_INT64 (5),
   "warehouse", BCON_UTF8 ("A"),
   "}",
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.ElemMatch<BsonValue>("instock", new BsonDocument { { "qty", 5 }, { "warehouse", "A" } });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"instock", bson.D{
			{"$elemMatch", bson.D{
				{"qty", 5},
				{"warehouse", "A"},
			}},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(elemMatch("instock", Document.parse("{ qty: 5, warehouse: 'A' }")));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(elemMatch("instock", Document.parse("{ qty: 5, warehouse: 'A' }")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(elemMatch("instock", Document.parse("{ qty: 5, warehouse: 'A' }")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"instock": {"$elemMatch": {"qty": 5, "warehouse": "A"}}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  instock: { $elemMatch: { qty: 5, warehouse: 'A' } }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['instock' => ['$elemMatch' => ['qty' => 5, 'warehouse' => 'A']]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"instock": {"$elemMatch": {"qty": 5, "warehouse": "A"}}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(instock: { '$elemMatch' => { qty: 5,
                                                     warehouse: 'A' } })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(elemMatch("instock", Document("qty" -> 5, "warehouse" -> "A")))
```

</Tab>

</Tabs>

The following example queries for documents where the `instock` array has at least one embedded document that contains the field `qty` that is greater than `10` and less than or equal to `20`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "instock": { $elemMatch: { qty: { $gt: 10, $lte: 20 } } } } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "instock": { $elemMatch: { qty: { $gt: 10, $lte: 20 } } } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "instock", "{",
   "$elemMatch", "{",
   "qty", "{",
   "$gt", BCON_INT64 (10),
   "$lte", BCON_INT64 (20),
   "}",
   "}",
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.ElemMatch<BsonValue>("instock", new BsonDocument { { "qty", new BsonDocument { { "$gt", 10 }, { "$lte", 20 } } } });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"instock", bson.D{
			{"$elemMatch", bson.D{
				{"qty", bson.D{
					{"$gt", 10},
					{"$lte", 20},
				}},
			}},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(elemMatch("instock", Document.parse("{ qty: { $gt: 10, $lte: 20 } }")));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(elemMatch("instock", Document.parse("{ qty: { $gt: 10, $lte: 20 } }")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(elemMatch("instock", Document.parse("{ qty: { \$gt: 10, \$lte: 20 } }")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"instock": {"$elemMatch": {"qty": {"$gt": 10, "$lte": 20}}}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  instock: { $elemMatch: { qty: { $gt: 10, $lte: 20 } } }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['instock' => ['$elemMatch' => ['qty' => ['$gt' => 10, '$lte' => 20]]]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"instock": {"$elemMatch": {"qty": {"$gt": 10, "$lte": 20}}}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(instock: { '$elemMatch' => { qty: { '$gt' => 10,
                                                            '$lte' => 20 } } })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(elemMatch("instock", Document("""{ qty: { $gt: 10, $lte: 20 } }""")))
```

</Tab>

</Tabs>

### Combination of Elements Satisfies the Criteria

If the compound query conditions on an array field do not use the [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch) operator, the query selects those documents whose array contains any combination of elements that satisfies the conditions.

For example, the following query matches documents where any document nested in the `instock` array has the `qty` field greater than `10` and any document (but not necessarily the same embedded document) in the array has the `qty` field less than or equal to `20`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "instock.qty": { $gt: 10,  $lte: 20 } } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "instock.qty": { $gt: 10,  $lte: 20 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "instock.qty", "{",
   "$gt", BCON_INT64 (10),
   "$lte", BCON_INT64 (20),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var builder = Builders<BsonDocument>.Filter;
var filter = builder.And(builder.Gt("instock.qty", 10), builder.Lte("instock.qty", 20));
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"instock.qty", bson.D{
			{"$gt", 10},
			{"$lte", 20},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(and(gt("instock.qty", 10), lte("instock.qty", 20)));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(and(gt("instock.qty", 10), lte("instock.qty", 20)));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(and(gt("instock.qty", 10), lte("instock.qty", 20)))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"instock.qty": {"$gt": 10, "$lte": 20}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  'instock.qty': { $gt: 10, $lte: 20 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['instock.qty' => ['$gt' => 10, '$lte' => 20]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"instock.qty": {"$gt": 10, "$lte": 20}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('instock.qty' => { '$gt' => 10, '$lte' => 20 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(and(gt("instock.qty", 10), lte("instock.qty", 20)))
```

</Tab>

</Tabs>

The following example queries for documents where the `instock` array has at least one embedded document that contains the field `qty` equal to `5` and at least one embedded document (but not necessarily the same embedded document) that contains the field `warehouse` equal to `A`:

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.inventory.find( { "instock.qty": 5, "instock.warehouse": "A" } )
```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "instock.qty": 5, "instock.warehouse": "A" }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "instock.qty", BCON_INT64 (5),
   "instock.warehouse", BCON_UTF8 ("A"));
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var builder = Builders<BsonDocument>.Filter;
var filter = builder.And(builder.Eq("instock.qty", 5), builder.Eq("instock.warehouse", "A"));
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"instock.qty", 5},
		{"instock.warehouse", "A"},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(and(eq("instock.qty", 5), eq("instock.warehouse", "A")));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(and(eq("instock.qty", 5), eq("instock.warehouse", "A")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(and(eq("instock.qty", 5), eq("instock.warehouse", "A")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"instock.qty": 5, "instock.warehouse": "A"})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  'instock.qty': 5,
  'instock.warehouse': 'A'
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['instock.qty' => 5, 'instock.warehouse' => 'A']);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"instock.qty": 5, "instock.warehouse": "A"})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('instock.qty' => 5,
                        'instock.warehouse' => 'A')
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(and(equal("instock.qty", 5), equal("instock.warehouse", "A")))
```

</Tab>

</Tabs>

## Query an Array of Documents with MongoDB Atlas

This example uses the [sample training dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-training/). To load the sample dataset into your MongoDB Atlas deployment, see [Load Sample Data](https://www.mongodb.com/docs/atlas/sample-data/#std-label-load-sample-data).

To query an array of documents in MongoDB Atlas, follow these steps:

### In the MongoDB Atlas UI, go to the Clusters page for your project.

- If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Clusters under the Database heading.

  The [Clusters](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fclusters) page displays.

### Navigate to the collection

- For the cluster that contains the sample data, click Browse Collections.

- In the left navigation pane, select the sample_training database.

- Select the grades collection.

### Specify the Filter field

Specify the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) in the Filter field. A query filter document uses [query operators](https://www.mongodb.com/docs/core/csfle/reference/supported-operations/#std-label-csfle-supported-query-operators) to specify search conditions.

Copy the following query filter document into the Filter search bar:

```javascript
{"scores.type": "exam"}
```

### Click Apply

This query filter returns all documents in the `sample_training.grades` collection that contain a subdocument in the `scores` array where `type` is set to `exam`. The full document, including the entire `scores` array, is returned. For more information on modifying the returned array, see [Project Specific Array Elements in the Returned Array](https://www.mongodb.com/docs/tutorial/project-fields-from-query-results/#std-label-project-array-elements-in-returned-array).

## Additional Query Tutorials

For additional query examples, see:

- [Query an Array](https://www.mongodb.com/docs/tutorial/query-arrays/)

- [Query Documents](https://www.mongodb.com/docs/tutorial/query-documents/)

- [Query on Embedded/Nested Documents](https://www.mongodb.com/docs/tutorial/query-embedded-documents/)
