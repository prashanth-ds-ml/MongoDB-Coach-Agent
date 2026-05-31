> Source: https://www.mongodb.com/docs/manual/tutorial/query-arrays/
> Fetch method: direct_markdown

# Query an Array

You can query arrays in MongoDB using the following methods:

Query an Array with MongoDB Atlas- Your programming language's driver.

- The MongoDB Atlas UI. To learn more, see Query an Array with MongoDB Atlas.

- MongoDB Compass.

➤➤ Use the **Select your language** drop-down menu in the upper-right to set the language of the following examples or select MongoDB Compass.

query operations on array fields

<Tabs>

<Tab name="MongoDB Shell">

This page provides examples of query operations on array fields using the `db.collection.find()` method in `mongosh`.

</Tab>

<Tab name="Compass">

This page provides examples of query operations on array fields using MongoDB Compass.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C">

This page provides examples of query operations on array fields using mongoc_collection_find_with_opts.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="C#">

This page provides examples of query operations on array fields using the MongoCollection.Find() method in the MongoDB C# Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Go">

This page provides examples of query operations on array fields using the Collection.Find function in the MongoDB Go Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Async)">

This page provides examples of query operations on array fields using the com.mongodb.reactivestreams.client.MongoCollection.find) method in the MongoDB Java Reactive Streams Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Java (Sync)">

This page provides examples of query operations on array fields using the com.mongodb.client.MongoCollection.find method in the MongoDB Java Synchronous Driver.

The driver provides com.mongodb.client.model.Filters helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Kotlin (Coroutine)">

This page provides examples of query operations on array fields by using the MongoCollection.find() method in the MongoDB Kotlin Coroutine Driver.

The driver provides com.mongodb.client.model.Filters helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Motor">

As of May 14, 2025, Motor is deprecated in favor of the GA release of the PyMongo Async API in the PyMongo library. We will not add new features to Motor, and we will provide only bug fixes until it reaches end of life on May 14, 2026. After that, we will fix only critical bugs until final support ends on May 14, 2027. We strongly recommend migrating to the PyMongo Async API while Motor is still supported.

For more information about migrating, see the Migrate to PyMongo Async guide in the PyMongo documentation.

This page provides examples of query operations on array fields using the `pymongo.asynchronous.collection.AsyncCollection.find` method in the PyMongo Async API.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Node.js">

This page provides examples of query operations on array fields using the Collection.find() method in the MongoDB Node.js Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="PHP">

This page provides examples of query operations on array fields using the `MongoDB\\Collection::find()` method in the MongoDB PHP Library.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Python">

This page provides examples of query operations on array fields using the `pymongo.collection.Collection.find` method in the PyMongo Python driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Ruby">

This page provides examples of query operations on array fields using the Mongo::Collection#find() method in the MongoDB Ruby Driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

</Tab>

<Tab name="Scala">

This page provides examples of query operations on array fields using the collection.find()(implicite:org.mongodb.scala.bson.DefaultHelper.DefaultsTo[C,TResult],implicitct:scala.reflect.ClassTag[C]):org.mongodb.scala.FindObservable[C]) method in the MongoDB Scala Driver.

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
    { "item": "journal", "qty": 25, "tags": ["blank", "red"], "dim_cm": [ 14, 21 ] },
    { "item": "notebook", "qty": 50, "tags": ["red", "blank"], "dim_cm": [ 14, 21 ] },
    { "item": "paper", "qty": 100, "tags": ["red", "blank", "plain"], "dim_cm": [ 14, 21 ] },
    { "item": "planner", "qty": 75, "tags": ["blank", "red"], "dim_cm": [ 22.85, 30 ] },
    { "item": "postcard", "qty": 45, "tags": ["blue"], "dim_cm": [ 10, 15.25 ] }
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
   "tags", "[",
   BCON_UTF8 ("blank"), BCON_UTF8 ("red"),
   "]",
   "dim_cm", "[",
   BCON_INT64 (14), BCON_INT64 (21),
   "]");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("notebook"),
   "qty", BCON_INT64 (50),
   "tags", "[",
   BCON_UTF8 ("red"), BCON_UTF8 ("blank"),
   "]",
   "dim_cm", "[",
   BCON_INT64 (14), BCON_INT64 (21),
   "]");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("paper"),
   "qty", BCON_INT64 (100),
   "tags", "[",
   BCON_UTF8 ("red"), BCON_UTF8 ("blank"), BCON_UTF8 ("plain"),
   "]",
   "dim_cm", "[",
   BCON_INT64 (14), BCON_INT64 (21),
   "]");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("planner"),
   "qty", BCON_INT64 (75),
   "tags", "[",
   BCON_UTF8 ("blank"), BCON_UTF8 ("red"),
   "]",
   "dim_cm", "[",
   BCON_DOUBLE (22.85), BCON_INT64 (30),
   "]");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("postcard"),
   "qty", BCON_INT64 (45),
   "tags", "[",
   BCON_UTF8 ("blue"),
   "]",
   "dim_cm", "[",
   BCON_INT64 (10), BCON_DOUBLE (15.25),
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
        { "qty", 25 },
        { "tags", new BsonArray { "blank", "red" } },
        { "dim_cm", new BsonArray { 14, 21 } }
    },
    new BsonDocument
    {
        { "item", "notebook" },
        { "qty", 50 },
        { "tags", new BsonArray { "red", "blank" } },
        { "dim_cm", new BsonArray { 14, 21 } }
    },
    new BsonDocument
    {
        { "item", "paper" },
        { "qty", 100 },
        { "tags", new BsonArray { "red", "blank", "plain" } },
        { "dim_cm", new BsonArray { 14, 21 } }
    },
    new BsonDocument
    {
        { "item", "planner" },
        { "qty", 75 },
        { "tags", new BsonArray { "blank", "red" } },
        { "dim_cm", new BsonArray { 22.85, 30 } }
    },
    new BsonDocument
    {
        { "item", "postcard" },
        { "qty", 45 },
        { "tags", new BsonArray { "blue" } },
        { "dim_cm", new BsonArray { 10, 15.25 } }
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
		{"qty", 25},
		{"tags", bson.A{"blank", "red"}},
		{"dim_cm", bson.A{14, 21}},
	},
	bson.D{
		{"item", "notebook"},
		{"qty", 50},
		{"tags", bson.A{"red", "blank"}},
		{"dim_cm", bson.A{14, 21}},
	},
	bson.D{
		{"item", "paper"},
		{"qty", 100},
		{"tags", bson.A{"red", "blank", "plain"}},
		{"dim_cm", bson.A{14, 21}},
	},
	bson.D{
		{"item", "planner"},
		{"qty", 75},
		{"tags", bson.A{"blank", "red"}},
		{"dim_cm", bson.A{22.85, 30}},
	},
	bson.D{
		{"item", "postcard"},
		{"qty", 45},
		{"tags", bson.A{"blue"}},
		{"dim_cm", bson.A{10, 15.25}},
	},
}

result, err := coll.InsertMany(context.TODO(), docs)

```

</Tab>

<Tab name="Java (Async)">

```java
Publisher<Success> insertManyPublisher = collection.insertMany(asList(
        Document.parse("{ item: 'journal', qty: 25, tags: ['blank', 'red'], dim_cm: [ 14, 21 ] }"),
        Document.parse("{ item: 'notebook', qty: 50, tags: ['red', 'blank'], dim_cm: [ 14, 21 ] }"),
        Document.parse("{ item: 'paper', qty: 100, tags: ['red', 'blank', 'plain'], dim_cm: [ 14, 21 ] }"),
        Document.parse("{ item: 'planner', qty: 75, tags: ['blank', 'red'], dim_cm: [ 22.85, 30 ] }"),
        Document.parse("{ item: 'postcard', qty: 45, tags: ['blue'], dim_cm: [ 10, 15.25 ] }")
));
```

</Tab>

<Tab name="Java (Sync)">

```java
collection.insertMany(asList(
        Document.parse("{ item: 'journal', qty: 25, tags: ['blank', 'red'], dim_cm: [ 14, 21 ] }"),
        Document.parse("{ item: 'notebook', qty: 50, tags: ['red', 'blank'], dim_cm: [ 14, 21 ] }"),
        Document.parse("{ item: 'paper', qty: 100, tags: ['red', 'blank', 'plain'], dim_cm: [ 14, 21 ] }"),
        Document.parse("{ item: 'planner', qty: 75, tags: ['blank', 'red'], dim_cm: [ 22.85, 30 ] }"),
        Document.parse("{ item: 'postcard', qty: 45, tags: ['blue'], dim_cm: [ 10, 15.25 ] }")
));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
collection.insertMany(
    listOf(
        Document("item", "journal")
            .append("qty", 25)
            .append("tags", listOf("blank", "red"))
            .append("dim_cm", listOf(14, 21)),
        Document("item", "notebook")
            .append("qty", 50)
            .append("tags", listOf("red", "blank"))
            .append("dim_cm", listOf(14, 21)),
        Document("item", "paper")
            .append("qty", 100)
            .append("tags", listOf("red", "blank", "plain"))
            .append("dim_cm", listOf(14, 21)),
        Document("item", "planner")
            .append("qty", 75)
            .append("tags", listOf("blank", "red"))
            .append("dim_cm", listOf(22.85, 30)),
        Document("item", "postcard")
            .append("qty", 45)
            .append("tags", listOf("blue"))
            .append("dim_cm", listOf(10, 15.25)),
    )
)
```

</Tab>

<Tab name="Motor">

```python
await db.inventory.insert_many(
    [
        {"item": "journal", "qty": 25, "tags": ["blank", "red"], "dim_cm": [14, 21]},
        {"item": "notebook", "qty": 50, "tags": ["red", "blank"], "dim_cm": [14, 21]},
        {
            "item": "paper",
            "qty": 100,
            "tags": ["red", "blank", "plain"],
            "dim_cm": [14, 21],
        },
        {"item": "planner", "qty": 75, "tags": ["blank", "red"], "dim_cm": [22.85, 30]},
        {"item": "postcard", "qty": 45, "tags": ["blue"], "dim_cm": [10, 15.25]},
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
    tags: ['blank', 'red'],
    dim_cm: [14, 21]
  },
  {
    item: 'notebook',
    qty: 50,
    tags: ['red', 'blank'],
    dim_cm: [14, 21]
  },
  {
    item: 'paper',
    qty: 100,
    tags: ['red', 'blank', 'plain'],
    dim_cm: [14, 21]
  },
  {
    item: 'planner',
    qty: 75,
    tags: ['blank', 'red'],
    dim_cm: [22.85, 30]
  },
  {
    item: 'postcard',
    qty: 45,
    tags: ['blue'],
    dim_cm: [10, 15.25]
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
        'tags' => ['blank', 'red'],
        'dim_cm' => [14, 21],
    ],
    [
        'item' => 'notebook',
        'qty' => 50,
        'tags' => ['red', 'blank'],
        'dim_cm' => [14, 21],
    ],
    [
        'item' => 'paper',
        'qty' => 100,
        'tags' => ['red', 'blank', 'plain'],
        'dim_cm' => [14, 21],
    ],
    [
        'item' => 'planner',
        'qty' => 75,
        'tags' => ['blank', 'red'],
        'dim_cm' => [22.85, 30],
    ],
    [
        'item' => 'postcard',
        'qty' => 45,
        'tags' => ['blue'],
        'dim_cm' => [10, 15.25],
    ],
]);
```

</Tab>

<Tab name="Python">

```python
db.inventory.insert_many(
    [
        {"item": "journal", "qty": 25, "tags": ["blank", "red"], "dim_cm": [14, 21]},
        {"item": "notebook", "qty": 50, "tags": ["red", "blank"], "dim_cm": [14, 21]},
        {
            "item": "paper",
            "qty": 100,
            "tags": ["red", "blank", "plain"],
            "dim_cm": [14, 21],
        },
        {"item": "planner", "qty": 75, "tags": ["blank", "red"], "dim_cm": [22.85, 30]},
        {"item": "postcard", "qty": 45, "tags": ["blue"], "dim_cm": [10, 15.25]},
    ]
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].insert_many([ { item: 'journal',
                                   qty: 25,
                                   tags: %w[blank red],
                                   dim_cm: [ 14, 21 ] },
                                 { item: 'notebook',
                                   qty: 50,
                                   tags: %w[red blank],
                                   dim_cm: [ 14, 21 ] },
                                 { item: 'paper',
                                   qty: 100,
                                   tags: %w[red blank plain],
                                   dim_cm: [ 14, 21 ] },
                                 { item: 'planner',
                                   qty: 75,
                                   tags: %w[blank red],
                                   dim_cm: [ 22.85, 30 ] },
                                 { item: 'postcard',
                                   qty: 45,
                                   tags: [ 'blue' ],
                                   dim_cm: [ 10, 15.25 ] } ])
```

</Tab>

<Tab name="Scala">

```scala
collection.insertMany(Seq(
  Document("""{ item: "journal", qty: 25, tags: ["blank", "red"], dim_cm: [ 14, 21 ] }"""),
  Document("""{ item: "notebook", qty: 50, tags: ["red", "blank"], dim_cm: [ 14, 21 ] }"""),
  Document("""{ item: "paper", qty: 100, tags: ["red", "blank", "plain"], dim_cm: [ 14, 21 ] }"""),
  Document("""{ item: "planner", qty: 75, tags: ["blank", "red"], dim_cm: [ 22.85, 30 ] }"""),
  Document("""{ item: "postcard", qty: 45, tags: ["blue"], dim_cm: [ 10, 15.25 ] }""")
)).execute()
```

</Tab>

</Tabs>

## Match an Array

<Tabs>

<Tab name="MongoDB Shell">

To specify equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Compass">

To specify equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="C">

To specify equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="C#">

To specify equality condition on an array, construct a filter using the Eq method, where `<value>` is the exact array to match, including the order of the elements:

```csharp
Builders<BsonDocument>.Filter.Eq(<field>, <value>)
```

</Tab>

<Tab name="Go">

To specify equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Java (Async)">

To specify equality condition on an array, use the query document `eq( <field>, <value>)` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Java (Sync)">

To specify equality condition on an array, use the query document `eq( <field>, <value>)` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Kotlin (Coroutine)">

To specify equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Motor">

To specify equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Node.js">

To specify equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="PHP">

To specify equality condition on an array, use the query document `[ <field> => <value> ]` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Python">

To specify equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Ruby">

To specify equality condition on an array, use the query document `{ <field> => <value> }` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

<Tab name="Scala">

To specify equality condition on an array, use the query document `equal( <field>, <value> )` where `<value>` is the exact array to match, including the order of the elements.

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The following example queries for all documents where `genres` is an array with exactly two elements, `"Action"` and `"Comedy"`, in the specified order:

</Tab>

<Tab name="Compass">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="C">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="C#">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Go">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Java (Async)">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Java (Sync)">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Motor">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Node.js">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="PHP">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Python">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Ruby">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

<Tab name="Scala">

The following example queries for all documents where `tags` is an array with exactly two elements, `"red"` and `"blank"`, in the specified order:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { genres: ["Action", "Comedy"] } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ tags: ["red", "blank"] }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "tags", "[",
   BCON_UTF8 ("red"), BCON_UTF8 ("blank"),
   "]");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("tags", new[] { "red", "blank" });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{{"tags", bson.A{"red", "blank"}}},
)

```

</Tab>

<Tab name="Java (Async)">

```java
FindPublisher<Document> findPublisher = collection.find(eq("tags", asList("red", "blank")));
```

</Tab>

<Tab name="Java (Sync)">

```java
FindIterable<Document> findIterable = collection.find(eq("tags", asList("red", "blank")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(eq("tags", listOf("red", "blank")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"tags": ["red", "blank"]})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  tags: ['red', 'blank']
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['tags' => ['red', 'blank']]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"tags": ["red", "blank"]})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(tags: %w[red blank])
```

</Tab>

<Tab name="Scala">

```scala
var findObservable = collection.find(equal("tags", Seq("red", "blank")))
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

To find an array that contains both `"Action"` and `"Comedy"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Compass">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="C">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="C#">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Go">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Java (Async)">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Java (Sync)">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Kotlin (Coroutine)">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Motor">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Node.js">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="PHP">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Python">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Ruby">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

<Tab name="Scala">

To find an array that contains both `"red"` and `"blank"` regardless of order or other elements in the array, use the `$all` operator:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { genres: { $all: ["Action", "Comedy"] } } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ tags: { $all: ["red", "blank"] } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "tags", "{",
   "$all", "[",
   BCON_UTF8 ("red"), BCON_UTF8 ("blank"),
   "]",
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.All("tags", new[] { "red", "blank" });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"tags", bson.D{{"$all", bson.A{"red", "blank"}}}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(all("tags", asList("red", "blank")));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(all("tags", asList("red", "blank")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(all("tags", listOf("red", "blank")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"tags": {"$all": ["red", "blank"]}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  tags: { $all: ['red', 'blank'] }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['tags' => ['$all' => ['red', 'blank']]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"tags": {"$all": ["red", "blank"]}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(tags: { '$all' => %w[red blank] })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(all("tags", "red", "blank"))
```

</Tab>

</Tabs>

## Query an Array for an Element

<Tabs>

<Tab name="MongoDB Shell">

To query if the array field contains at least *one* element with the specified value, use the filter `{ <field>: <value> }` where `<value>` is the element value.

</Tab>

<Tab name="Compass">

To query if the array field contains at least *one* element with the specified value, use the filter `{ <field>: <value> }` where `<value>` is the element value.

</Tab>

<Tab name="C">

To query if the array field contains at least *one* element with the specified value, use the filter `{ <field>: <value> }` where `<value>` is the element value.

</Tab>

<Tab name="C#">

To query if the array field contains at least *one* element with the specified value, construct a filter using the Eq method, where `<value>` is the element value to match:

```csharp
Builders<BsonDocument>.Filter.Eq(<field>, <value>)
```

</Tab>

<Tab name="Go">

To query if the array field contains at least *one* element with the specified value, use the filter `eq( <field>, <value>)` where `<value>` is the element value.

</Tab>

<Tab name="Java (Async)">

To query if the array field contains at least *one* element with the specified value, use the filter `eq( <field>, <value>)` where value is the element value.

</Tab>

<Tab name="Java (Sync)">

To query if the array field contains at least *one* element with the specified value, use the filter `eq( <field>, <value>)` where `<value>` is the element value.

</Tab>

<Tab name="Kotlin (Coroutine)">

To query if the array field contains at least *one* element with the specified value, use the filter `eq( <field>, <value>)` where `<value>` is the element value.

</Tab>

<Tab name="Motor">

To query if the array field contains at least *one* element with the specified value, use the filter `{ <field>: <value> }` where `<value>` is the element value.

</Tab>

<Tab name="Node.js">

To query if the array field contains at least *one* element with the specified value, use the filter `{ <field>: <value> }` where `<value>` is the element value.

</Tab>

<Tab name="PHP">

To query if the array field contains at least *one* element with the specified value, use the filter `[ <field> => <value> ]` where `<value>` is the element value.

</Tab>

<Tab name="Python">

To query if the array field contains at least *one* element with the specified value, use the filter `{ <field>: <value> }` where `<value>` is the element value.

</Tab>

<Tab name="Ruby">

To query if the array field contains at least *one* element with the specified value, use the filter `{ <field> => <value> }` where `<value>` is the element value.

</Tab>

<Tab name="Scala">

To query if the array field contains at least *one* element with the specified value, use the filter `equal( <field>, <value> )` where `<value>` is the element value.

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The following example queries for all documents where the `genres` array contains the string `"Short"` as one of its elements:

</Tab>

<Tab name="Compass">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="C">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="C#">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Go">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Java (Async)">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Java (Sync)">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Motor">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Node.js">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="PHP">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Python">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Ruby">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

<Tab name="Scala">

The following example queries for all documents where the `tags` array contains the string `"red"` as one of its elements:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { genres: "Short" } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ tags: "red" }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("tags", BCON_UTF8 ("red"));
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("tags", "red");
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"tags", "red"},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(eq("tags", "red"));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(eq("tags", "red"));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(eq("tags", "red"))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"tags": "red"})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  tags: 'red'
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['tags' => 'red']);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"tags": "red"})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(tags: 'red')
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(equal("tags", "red"))
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```javascript
{ <array field>: { <operator1>: <value1>, ... } }
```

</Tab>

<Tab name="Compass">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```javascript
{ <array field>: { <operator1>: <value1>, ... } }
```

</Tab>

<Tab name="C">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```c
{ <array field>: { <operator1>: <value1>, ... } }
```

</Tab>

<Tab name="C#">

To specify conditions on the elements in the array field, use query operators in the query filter document. For example:

```csharp
var builder = Builders<BsonDocument>.Filter;
builder.And(builder.Eq(<array field>, <value1>), builder.Lt(<array field>, <value2>));
```

</Tab>

<Tab name="Go">

To specify conditions on the elements in the array field, use query operators in the query filter document. For example:

```go
filter := bson.D{
    {"$and", bson.A{
        bson.D{{<array field>, bson.D{{"$eq", <value1>}}}},
        bson.D{{<array field>, bson.D{{"$lt", <value2>}}}},
    }},
}
```

</Tab>

<Tab name="Java (Async)">

To specify conditions on the elements in the array field, use query operators in the query filter document. For example:

```java
and(gte(<array field>, <value1>), lt(<array field>, <value2>) ...)
```

</Tab>

<Tab name="Java (Sync)">

To specify conditions on the elements in the array field, use query operators in the query filter document. For example:

```java
and(gte(<array field>, <value1>), lt(<array field>, <value2>) ...)
```

</Tab>

<Tab name="Kotlin (Coroutine)">

To specify conditions on the elements in the array field, use query operators in the query filter document. For example:

```kotlin
and(gte(<array field>, <value1>), lt(<array field>, <value2>) ...)
```

</Tab>

<Tab name="Motor">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```python
{ <array field>: { <operator1>: <value1>, ... } }
```

</Tab>

<Tab name="Node.js">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```javascript
{ <array field>: { <operator1>: <value1>, ... } }
```

</Tab>

<Tab name="PHP">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```php
[ <array field> => [ <operator1> => <value1>, ... ] ]
```

</Tab>

<Tab name="Python">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```python
{ <array field>: { <operator1>: <value1>, ... } }
```

</Tab>

<Tab name="Ruby">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```ruby
{ <array field> => { <operator1> => <value1>, ... } }
```

</Tab>

<Tab name="Scala">

To specify conditions on the elements in the array field, use query operators in the query filter document:

```scala
and(gte(<array field>, <value1>), lt(<array field>, <value2>) ...)
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

The following example queries for all documents where the `cast` array contains at least one element that matches the regular expression `^A`:

</Tab>

<Tab name="Compass">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="C">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="C#">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Go">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Java (Async)">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Java (Sync)">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Motor">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Node.js">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="PHP">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Python">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Ruby">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

<Tab name="Scala">

The following example queries for all documents where the array `dim_cm` contains at least one element whose value is greater than `25`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { cast: { $regex: "^A" } } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ dim_cm: { $gt: 25 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "dim_cm", "{",
   "$gt", BCON_INT64 (25),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Gt("dim_cm", 25);
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"dim_cm", bson.D{
			{"$gt", 25},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(gt("dim_cm", 25));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(gt("dim_cm", 25));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(gt("dim_cm", 25))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"dim_cm": {"$gt": 25}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  dim_cm: { $gt: 25 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['dim_cm' => ['$gt' => 25]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"dim_cm": {"$gt": 25}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(dim_cm: { '$gt' => 25 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(gt("dim_cm", 25))
```

</Tab>

</Tabs>

## Specify Multiple Conditions for Array Elements

When you specify compound conditions on array elements, you can query for documents where either:

- A single array element meets all the specified conditions

- Different array elements collectively meet all the conditions, with each element satisfying one or more conditions

### Query an Array with Compound Filter Conditions on the Array Elements

<Tabs>

<Tab name="MongoDB Shell">

The following example queries for documents where the `cast` array contains elements that in some combination satisfy the query conditions. One element can satisfy the `$regex: "^A"` condition and another element can satisfy the `$ne: "Adam Sandler"` condition, or a single element can satisfy both:

</Tab>

<Tab name="Compass">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="C">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="C#">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Go">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Java (Async)">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Java (Sync)">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Motor">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Node.js">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="PHP">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Python">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Ruby">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

<Tab name="Scala">

The following example queries for documents where the `dim_cm` array contains elements that in some combination satisfy the query conditions. One element can satisfy the greater than `15` condition and another element can satisfy the less than `20` condition, or a single element can satisfy both:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find(
   { cast: { $regex: "^A", $ne: "Adam Sandler" } }
)

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ dim_cm: { $gt: 15, $lt: 20 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "dim_cm", "{",
   "$gt", BCON_INT64 (15),
   "$lt", BCON_INT64 (20),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var builder = Builders<BsonDocument>.Filter;
var filter = builder.And(builder.Gt("dim_cm", 15), builder.Lt("dim_cm", 20));
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"dim_cm", bson.D{
			{"$gt", 15},
			{"$lt", 20},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(and(gt("dim_cm", 15), lt("dim_cm", 20)));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(and(gt("dim_cm", 15), lt("dim_cm", 20)));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(and(gt("dim_cm", 15), lt("dim_cm", 20)))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"dim_cm": {"$gt": 15, "$lt": 20}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  dim_cm: { $gt: 15, $lt: 20 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find([
    'dim_cm' => [
        '$gt' => 15,
        '$lt' => 20,
    ],
]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"dim_cm": {"$gt": 15, "$lt": 20}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(dim_cm: { '$gt' => 15,
                                  '$lt' => 20 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(and(gt("dim_cm", 15), lt("dim_cm", 20)))
```

</Tab>

</Tabs>

### Query for an Array Element that Meets Multiple Criteria

Use the `$elemMatch` operator to specify multiple criteria on array elements so that at least one array element satisfies all the specified criteria.

<Tabs>

<Tab name="MongoDB Shell">

The following example queries for documents where the `cast` array contains at least one element that both matches the regular expression `^A` and is not equal to `"Adam Sandler"`:

</Tab>

<Tab name="Compass">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="C">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="C#">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Go">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Java (Async)">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Java (Sync)">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Motor">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Node.js">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="PHP">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Python">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Ruby">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

<Tab name="Scala">

The following example queries for documents where the `dim_cm` array contains at least one element that is both greater than (`$gt`) `22` and less than (`$lt`) `30`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find(
   { cast: { $elemMatch: { $regex: "^A", $ne: "Adam Sandler" } } }
)

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ dim_cm: { $elemMatch: { $gt: 22, $lt: 30 } } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "dim_cm", "{",
   "$elemMatch", "{",
   "$gt", BCON_INT64 (22),
   "$lt", BCON_INT64 (30),
   "}",
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.ElemMatch<BsonValue>("dim_cm", new BsonDocument { { "$gt", 22 }, { "$lt", 30 } });
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"dim_cm", bson.D{
			{"$elemMatch", bson.D{
				{"$gt", 22},
				{"$lt", 30},
			}},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(elemMatch("dim_cm", Document.parse("{ $gt: 22, $lt: 30 }")));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(elemMatch("dim_cm", Document.parse("{ $gt: 22, $lt: 30 }")));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(elemMatch("dim_cm", Document.parse("{ \$gt: 22, \$lt: 30 }")))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"dim_cm": {"$elemMatch": {"$gt": 22, "$lt": 30}}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  dim_cm: { $elemMatch: { $gt: 22, $lt: 30 } }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find([
    'dim_cm' => [
        '$elemMatch' => [
            '$gt' => 22,
            '$lt' => 30,
        ],
    ],
]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"dim_cm": {"$elemMatch": {"$gt": 22, "$lt": 30}}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(dim_cm: { '$elemMatch' => { '$gt' => 22,
                                                    '$lt' => 30 } })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(elemMatch("dim_cm", Document("$gt" -> 22, "$lt" -> 30)))

```

</Tab>

</Tabs>

### Query for an Element by the Array Index Position

Use dot notation to specify query conditions for an element at a particular index or position of the array. The array uses zero-based indexing.

When you query using dot notation, the field and nested field must be inside quotation marks.

<Tabs>

<Tab name="MongoDB Shell">

The following example queries for all documents where the first element in the array `cast` equals `"Tom Hanks"`:

</Tab>

<Tab name="Compass">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="C">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="C#">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Go">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Java (Async)">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Java (Sync)">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Motor">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Node.js">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="PHP">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Python">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Ruby">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

<Tab name="Scala">

The following example queries for all documents where the second element in the array `dim_cm` is greater than `25`:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { "cast.0": "Tom Hanks" } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "dim_cm.1": { $gt: 25 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "dim_cm.1", "{",
   "$gt", BCON_INT64 (25),
   "}");
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Gt("dim_cm.1", 25);
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"dim_cm.1", bson.D{
			{"$gt", 25},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(elemMatch("dim_cm", Document.parse("{ $gt: 22, $lt: 30 }")));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(gt("dim_cm.1", 25));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(gt("dim_cm.1", 25))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"dim_cm.1": {"$gt": 25}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  'dim_cm.1': { $gt: 25 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['dim_cm.1' => ['$gt' => 25]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"dim_cm.1": {"$gt": 25}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find('dim_cm.1' => { '$gt' => 25 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(gt("dim_cm.1", 25))
```

</Tab>

</Tabs>

### Query an Array by Array Length

Use the `$size` operator to query for arrays by number of elements.

<Tabs>

<Tab name="MongoDB Shell">

The following example selects documents where `genres` has 3 elements:

</Tab>

<Tab name="Compass">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="C">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="C#">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Go">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Java (Async)">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Java (Sync)">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Kotlin (Coroutine)">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Motor">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Node.js">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="PHP">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Python">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Ruby">

The following example selects documents where `tags` has 3 elements:

</Tab>

<Tab name="Scala">

The following example selects documents where `tags` has 3 elements:

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { genres: { $size: 3 } } )

```

</Tab>

<Tab name="Compass">

Copy the following filter into the Compass query bar and click Find:

```javascript
{ "tags": { $size: 3 } }
```

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW (
   "tags", "{",
   "$size", BCON_INT64 (3),
   "}");
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
var filter = Builders<BsonDocument>.Filter.Size("tags", 3);
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"tags", bson.D{
			{"$size", 3},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
findPublisher = collection.find(size("tags", 3));
```

</Tab>

<Tab name="Java (Sync)">

```java
findIterable = collection.find(size("tags", 3));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val findFlow = collection
    .find(size("tags", 3))
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"tags": {"$size": 3}})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({
  tags: { $size: 3 }
});
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['tags' => ['$size' => 3]]);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"tags": {"$size": 3}})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(tags: { '$size' => 3 })
```

</Tab>

<Tab name="Scala">

```scala
findObservable = collection.find(size("tags", 3))
```

</Tab>

</Tabs>

## Query an Array with MongoDB Atlas

The example in this section uses the sample movies dataset. To learn how to load the sample dataset into your MongoDB Atlas deployment, see Load Sample Data.

To query an array in MongoDB Atlas, follow these steps:

### In the MongoDB Atlas UI, go to the Clusters page for your project.

- If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Clusters under the Database heading.

  The Clusters page displays.

### Navigate to the collection.

- For the cluster that contains the sample data, click Browse Collections.

- In the left navigation pane, select the `sample_mflix` database.

- Select the `movies` collection.

### Specify a query filter document.

To query a document that contains an array, specify a query filter document. A query filter document uses query operators to specify search conditions. Use the following example documents to query array fields in the `sample_mflix.movies` collection.

To apply a query filter, copy an example document into the Filter search bar and click Apply.

<Tabs>

<Tab name="Match an Array">

To specify an equality condition on an array, use the query document `{ <field>: <value> }` where `<value>` is the exact array to match, including the order of the elements. The following example finds documents where `genres` contains the `["Action", "Comedy"]` array in the specified order:

```
{ genres: ["Action", "Comedy"] }
```

To find an array that contains both `Action` and `Comedy` regardless of order or other elements in the array, use the `$all` operator:

```
{ genres: { $all: ["Action", "Comedy"] } }
```

</Tab>

<Tab name="Query for an Element">

To query if the array field contains at least one element with the specified value, use the filter `{ <field>: <value> }` where `<value>` is the element value.

The following example queries for all documents where the `genres` field contains the string `Short` as one of its elements:

```
{ genres: "Short" }
```

To specify conditions on the elements in the array field, use query operators in the query filter document:

```
{ <array field>: { <operator1>: <value1>, ... } }
```

The following example uses the `$nin` operator to query for all documents where the `genres` field does not contain `Drama`:

```
{ genres: { $nin: ["Drama"] } }
```

</Tab>

<Tab name="Specify Multiple Conditions">

When you specify compound conditions on array elements, you can query for either a single array element that meets all conditions or any combination of array elements that together meet the conditions.

#### Query an Array with Compound Filter Conditions on the Array Elements

The following example queries for documents where the `cast` array contains elements that in some combination satisfy the query conditions. The following filter uses the `$regex` and `$eq` operators to return documents where a single array element ends in `Olsen` and another element equals `Mary-Kate Olsen` or a single element that satisfies both conditions:

```
{ cast: { $regex: "Olsen$", $eq: "Mary-Kate Olsen" } }
```

This query filter returns movies that include `Mary-Kate Olsen` in their cast, and movies that include both `Mary-Kate Olsen` and `Ashley Olsen` in their cast.

#### Query for an Array Element that Meets Multiple Criteria

Use the `$elemMatch` operator to specify multiple criteria on array elements such that at least one array element satisfies all the specified criteria.

The following example uses the `$elemMatch` and `$ne` operators to query for documents where `languages` contains at least one element that is both not `null` and does not equal `English`:

```
{ languages: { $elemMatch: { $ne: null, $ne: "English" } } }
```

#### Query for an Element by the Array Index Position

Use dot notation to specify query conditions for an element at a particular index or position of the array. The array uses zero-based indexing.

When you query using dot notation, the field and nested field must be inside quotation marks.

The following example uses the `$ne` operator to query for all documents where the first element in the `countries` array is not equal to `USA`:

```
{ "countries.0": { $ne: "USA" } }
```

#### Query an Array by Array Length

Use the `$size` operator to query for arrays by number of elements. The following example selects documents where `genres` has 3 elements:

```
{ genres: { $size: 3 } }
```

</Tab>

</Tabs>

## Additional Query Tutorials

For additional query examples, see:

- Query Documents

- Query on Embedded/Nested Documents

- Query an Array of Embedded Documents
