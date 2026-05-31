> Source: https://www.mongodb.com/docs/manual/tutorial/insert-documents/
> Fetch method: direct_markdown

# Insert Documents

➤➤ Use the **Select your language** drop-down menu in the upper-right to set the language of the following examples or select MongoDB Compass.

This page provides examples of insert operations in MongoDB.

You can insert documents in MongoDB by using the following methods:

[Insert Documents in the MongoDB Atlas UI](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-insert-documents-atlas)- Your programming language's driver.

- The [MongoDB Atlas UI](https://www.mongodb.com/docs/atlas/). To learn more, see [Insert Documents in the MongoDB Atlas UI](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-insert-documents-atlas).

- [MongoDB Compass](https://www.mongodb.com/docs/compass/current/).

If the collection does not currently exist, insert operations will create the collection.

## Insert Documents in the MongoDB Atlas UI

To insert a document in the MongoDB Atlas UI, complete the following steps. To learn more about working with documents in the MongoDB Atlas UI, see [Create, View, Update, and Delete Documents](https://www.mongodb.com/docs/atlas/atlas-ui/documents/).

### In the MongoDB Atlas UI, go to the Clusters page for your project.

- If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Clusters under the Database heading.

  The [Clusters](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fclusters) page displays.

### Navigate to the collection

- For the cluster to which you want to add documents, click Browse Collections.

- In the left navigation pane, select the database.

- In the left navigation pane, select the collection.

### Add the documents

- Click Insert Document.

- Click the {} icon, which opens the JSON view.

- Paste the document array into the text entry field. For example, the following entry creates four documents, each of which contain three fields:

  ```
  [
     { "prodId": 100, "price": 20, "quantity": 125 },
     { "prodId": 101, "price": 10, "quantity": 234 },
     { "prodId": 102, "price": 15, "quantity": 432 },
     { "prodId": 103, "price": 17, "quantity": 320 }
  ]
  ```

### Click Insert.

MongoDB Atlas adds the documents to the collection.

## Insert a Single Document

<Tabs>

<Tab name="MongoDB Shell">

[`db.collection.insertOne()`](https://www.mongodb.com/docs/reference/method/db.collection.insertOne/#mongodb-method-db.collection.insertOne) inserts a *single*
[document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts one document into the `movies` collection. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Compass">

To insert a single document using [MongoDB Compass](https://www.mongodb.com/docs/compass/current/#std-label-compass-index):

1. Navigate to the collection you wish to insert the document into:

   - In the left-hand MongoDB Compass navigation pane, click the database to which your target collection belongs.

   - From the database view, click the target collection name.

2. Click the Add Data button, then click Insert document:

3. Paste in your document. For example, you can paste the following code into Compass to insert a `canvas` document into the `inventory` collection:

   ```json
   {
     "item": "canvas",
     "qty": 100,
     "tags": ["cotton"],
     "size": {
       "h": 28,
       "w": 35.5,
       "uom": "cm"
     }
   }
   ```

4. Click Insert.

The following example inserts a new document into the test.inventory collection:

</Tab>

<Tab name="C">

The following example inserts a new document into the `inventory` collection. If the document does not specify an `_id` field, the C driver adds the `_id` field with an ObjectId value to the new document. For more information, see [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="C#">

[IMongoCollection.InsertOne()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_InsertOne.htm) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts one document into `inventory`. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Go">

[Collection.InsertOne](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.InsertOne) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts one document into `inventory`. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Java (Async)">

[com.mongodb.reactivestreams.client.MongoCollection.insertOne](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#insertOne(TDocument)) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection with the [Java Reactive Streams Driver](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/):

```json
{ item: "canvas", qty: 100, tags: ["cotton"], size: { h: 28, w: 35.5, uom: "cm" } }
```

This example inserts one document into `inventory`. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Java (Sync)">

[com.mongodb.client.MongoCollection.insertOne](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#insertOne-TDocument-) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts one document into `inventory`. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Kotlin (Coroutine)">

[MongoCollection.insertOne](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/insert-one.html) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts one document into `inventory`. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Motor">

[`motor.motor_asyncio.AsyncIOMotorCollection.insert_one`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_one) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

The following example inserts a new document into the `inventory` collection. If the document does not specify an `_id` field, the Motor driver adds the `_id` field with an ObjectId value to the new document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Node.js">

[Collection.insertOne()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#insertOne) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

The following example inserts a new document into the `inventory` collection. If the document does not specify an `_id` field, the Node.js driver adds the `_id` field with an ObjectId value to the new document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="PHP">

[`MongoDB\\Collection::insertOne()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-insertOne/#mongodb-phpmethod-phpmethod.MongoDB-Collection--insertOne--) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts one document into `inventory`. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Python">

[`pymongo.collection.Collection.insert_one`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.insert_one) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

The following example inserts a new document into the `inventory` collection. If the document does not specify an `_id` field, the PyMongo driver adds the `_id` field with an ObjectId value to the new document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Ruby">

[Mongo::Collection#insert_one()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#insert_one-instance_method) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts one document into `inventory`. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Scala">

[collection.insertOne()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#insertOne(document:TResult,options:org.mongodb.scala.model.InsertOneOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.Completed]) inserts a *single* [document](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts one document into `inventory`. If the document does not specify `_id`, MongoDB adds one. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.insertOne({
   title: "The Substance",
   genres: ["Drama", "Horror", "Sci-Fi"],
   runtime: 140,
   rated: "R",
   year: 2024,
   directors: ["Coralie Fargeat"],
   cast: ["Demi Moore", "Margaret Qualley"],
   type: "movie"
})

```

</Tab>

<Tab name="Compass">

</Tab>

<Tab name="C">

```c
mongoc_collection_t *collection;
bson_t *doc;
bool r;
bson_error_t error;

collection = mongoc_database_get_collection (db, "inventory");
doc = BCON_NEW (
   "item", BCON_UTF8 ("canvas"),
   "qty", BCON_INT64 (100),
   "tags", "[",
   BCON_UTF8 ("cotton"),
   "]",
   "size", "{",
   "h", BCON_DOUBLE (28),
   "w", BCON_DOUBLE (35.5),
   "uom", BCON_UTF8 ("cm"),
   "}");

r = mongoc_collection_insert_one (collection, doc, NULL, NULL, &error);
bson_destroy (doc);

if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}
```

</Tab>

<Tab name="C#">

```csharp
var document = new BsonDocument
{
    { "item", "canvas" },
    { "qty", 100 },
    { "tags", new BsonArray { "cotton" } },
    { "size", new BsonDocument { { "h", 28 }, { "w", 35.5 }, { "uom", "cm" } } }
};
collection.InsertOne(document);
```

</Tab>

<Tab name="Go">

```go

result, err := coll.InsertOne(
	context.TODO(),
	bson.D{
		{"item", "canvas"},
		{"qty", 100},
		{"tags", bson.A{"cotton"}},
		{"size", bson.D{
			{"h", 28},
			{"w", 35.5},
			{"uom", "cm"},
		}},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
Document canvas = new Document("item", "canvas")
        .append("qty", 100)
        .append("tags", singletonList("cotton"));

Document size = new Document("h", 28)
        .append("w", 35.5)
        .append("uom", "cm");
canvas.put("size", size);

Publisher<Success> insertOnePublisher = collection.insertOne(canvas);
```

</Tab>

<Tab name="Java (Sync)">

```java
Document canvas = new Document("item", "canvas")
        .append("qty", 100)
        .append("tags", singletonList("cotton"));

Document size = new Document("h", 28)
        .append("w", 35.5)
        .append("uom", "cm");
canvas.put("size", size);

collection.insertOne(canvas);
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
result = collection.insertOne(
Document("item", "canvas")
    .append("qty", 100)
    .append("tags", listOf("cotton"))
    .append("size", Document("h", 28)
        .append("w", 35.5)
        .append("uom", "cm")
    )

```

</Tab>

<Tab name="Motor">

```python
await db.inventory.insert_one(
    {
        "item": "canvas",
        "qty": 100,
        "tags": ["cotton"],
        "size": {"h": 28, "w": 35.5, "uom": "cm"},
    }
)
```

</Tab>

<Tab name="Node.js">

```javascript
await db.collection('inventory').insertOne({
  item: 'canvas',
  qty: 100,
  tags: ['cotton'],
  size: { h: 28, w: 35.5, uom: 'cm' }
});
```

</Tab>

<Tab name="PHP">

```php
$insertOneResult = $db->inventory->insertOne([
    'item' => 'canvas',
    'qty' => 100,
    'tags' => ['cotton'],
    'size' => ['h' => 28, 'w' => 35.5, 'uom' => 'cm'],
]);
```

</Tab>

<Tab name="Python">

```python
db.inventory.insert_one(
    {
        "item": "canvas",
        "qty": 100,
        "tags": ["cotton"],
        "size": {"h": 28, "w": 35.5, "uom": "cm"},
    }
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].insert_one({ item: 'canvas',
                                qty: 100,
                                tags: [ 'cotton' ],
                                size: { h: 28, w: 35.5, uom: 'cm' } })
```

</Tab>

<Tab name="Scala">

```scala
collection.insertOne(
  Document("item" -> "canvas", "qty" -> 100, "tags" -> Seq("cotton"), "size" -> Document("h" -> 28, "w" -> 35.5, "uom" -> "cm"))
).execute()
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

[`insertOne()`](https://www.mongodb.com/docs/reference/method/db.collection.insertOne/#mongodb-method-db.collection.insertOne) returns a document that includes the newly inserted document's `_id` field value. For an example of a return document, see [db.collection.insertOne() reference](https://www.mongodb.com/docs/reference/method/db.collection.insertOne/#std-label-insertOne-examples).

</Tab>

<Tab name="Compass">

MongoDB Compass generates the `_id` field and its value automatically. The generated [ObjectId](https://www.mongodb.com/docs/reference/glossary/#std-term-ObjectId) consists of a unique randomly generated hexadecimal value.

You can change this value prior to inserting your document so long as it remains unique and is a valid `ObjectId`. For more information on the `_id` field, see [_id Field](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-insert-id-field).

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) by specifying a filter in the MongoDB Compass query bar and clicking Find to execute the query.

The following filter specifies that MongoDB Compass only return documents where the `item` field is equal to `canvas`. For more information on the MongoDB Compass Query Bar, see [Query Bar](https://www.mongodb.com/docs/compass/current/query/filter/#std-label-compass-query-bar).

</Tab>

<Tab name="C">

[mongoc_collection_insert_one](https://mongoc.org/libmongoc/current/mongoc_collection_insert_one.html) returns `true` if successful, or returns `false` and sets error if there are invalid arguments or a server or network error.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="C#">

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Go">

[Collection.InsertOne](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.InsertOne) function returns an instance of [InsertOneResult](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#InsertOneResult) whose `InsertedID` attribute contains the `_id` of the newly inserted document.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Java (Async)">

[com.mongodb.reactivestreams.client.MongoCollection.insertOne](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#insertOne(TDocument)) returns a [Publisher](http://www.reactive-streams.org/reactive-streams-1.0.1-javadoc/org/reactivestreams/Publisher.html) object. The `Publisher` inserts the document into a collection when subscribers request data.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Java (Sync)">

[com.mongodb.client.MongoCollection.insertOne](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-sync/com/mongodb/client/MongoCollection.html#insertOne(TDocument)) returns an instance of [InsertOneResult](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/result/InsertOneResult.html). You can access the `_id` field of the inserted document by calling the [getInsertedId()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/result/InsertOneResult.html#getInsertedId()) method on the result.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Kotlin (Coroutine)">

[MongoCollection.insertOne](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/insert-one.html) returns an instance of [InsertOneResult](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/result/InsertOneResult.html). You can access the `_id` field of the inserted document by accessing the `insertedId` field of the result.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Motor">

[`insert_one`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_one) returns an instance of [`pymongo.results.InsertOneResult`](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.InsertOneResult) whose `inserted_id` field contains the `_id` of the newly inserted document.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Node.js">

[insertOne()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#insertOne) returns a promise that provides a `result`.  The `result.insertedId` promise contains the `_id` of the newly inserted document.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="PHP">

Upon successful insert, the [`insertOne()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-insertOne/#mongodb-phpmethod-phpmethod.MongoDB-Collection--insertOne--) method returns an instance of [`MongoDB\\InsertOneResult`](https://www.mongodb.com/docs/php-library/upcoming/reference/class/MongoDBInsertOneResult/#mongodb-phpclass-phpclass.MongoDB-InsertOneResult) whose [`getInsertedId()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBInsertOneResult-getInsertedId/#mongodb-phpmethod-phpmethod.MongoDB-InsertOneResult--getInsertedId--) method returns the `_id` of the newly inserted document.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Python">

[`insert_one`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.insert_one) returns an instance of [`pymongo.results.InsertOneResult`](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.InsertOneResult) whose `inserted_id` field contains the `_id` of the newly inserted document.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Ruby">

Upon successful insert, the [insert_one()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#insert_one-instance_method) method returns an instance of [Mongo::Operation::Result](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Operation/Result.html), whose `inserted_id` attribute contains the `_id` of the newly inserted document.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

<Tab name="Scala">

Upon successful insert, the [collection.insertOne()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#MongoCollection.html#insertOne(document:TResult,options:org.mongodb.scala.model.InsertOneOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.Completed]) method returns an instance of [collection.insertOne().results();](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#InsertOneResult) whose `inserted_id` attribute contains the `_id` of the newly inserted document.

To retrieve the document that you just inserted, [query the collection](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { title: "The Substance" } )
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
filter = BCON_NEW ("item", BCON_UTF8 ("canvas"));
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

</Tab>

<Tab name="C#">

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("item", "canvas");
var result = collection.Find(filter).ToList();
```

</Tab>

<Tab name="Go">

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{{"item", "canvas"}},
)

```

</Tab>

<Tab name="Java (Async)">

```java
FindPublisher<Document> findPublisher = collection.find(eq("item", "canvas"));
```

</Tab>

<Tab name="Java (Sync)">

```java
FindIterable<Document> findIterable = collection.find(eq("item", "canvas"));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
val flowInsertOne = collection
    .find(eq("item", "canvas"))
    .firstOrNull()
```

</Tab>

<Tab name="Motor">

```python
cursor = db.inventory.find({"item": "canvas"})
```

</Tab>

<Tab name="Node.js">

```javascript
const cursor = db.collection('inventory').find({ item: 'canvas' });
```

</Tab>

<Tab name="PHP">

```php
$cursor = $db->inventory->find(['item' => 'canvas']);
```

</Tab>

<Tab name="Python">

```python
cursor = db.inventory.find({"item": "canvas"})
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].find(item: 'canvas')
```

</Tab>

<Tab name="Scala">

```scala
val observable = collection.find(equal("item", "canvas"))
```

</Tab>

</Tabs>

## Insert Multiple Documents

<Tabs>

<Tab name="MongoDB Shell">

[`db.collection.insertMany()`](https://www.mongodb.com/docs/reference/method/db.collection.insertMany/#mongodb-method-db.collection.insertMany) can insert *multiple*
[documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass an array of documents to the method.

This example inserts multiple documents into the `movies` collection. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Compass">

For instructions on inserting documents using MongoDB Compass, see [Insert Documents](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert). You can paste the following documents into the Insert Document dialog in Compass to insert multiple `item` documents into the `inventory` collection:

</Tab>

<Tab name="C">

[mongoc_bulk_operation_insert_with_opts](https://mongoc.org/libmongoc/current/mongoc_bulk_operation_insert_with_opts.html) inserts *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. You must pass an iterable of documents to the method.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="C#">

[IMongoCollection.InsertMany()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_InsertMany.htm) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass an enumerable collection of documents to the method.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Go">

[Collection.InsertMany](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.InsertMany) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Java (Async)">

[com.mongodb.reactivestreams.client.MongoCollection.html.insertMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#insertMany(java.util.List)) inserts the following documents with the [Java Reactive Streams Driver](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/):

```json
{ item: "journal", qty: 25, tags: ["blank", "red"], size: { h: 14, w: 21, uom: "cm" } }
{ item: "mat", qty: 85, tags: ["gray"], size: { h: 27.9, w: 35.5, uom: "cm" } }
{ item: "mousepad", qty: 25, tags: ["gel", "blue"], size: { h: 19, w: 22.85, uom: "cm" } }
```

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Java (Sync)">

[com.mongodb.client.MongoCollection.insertMany](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#insertMany-java.util.List-) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass a list of documents to the method.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Kotlin (Coroutine)">

[MongoCollection.insertMany](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/insert-many.html) inserts *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass a list of documents as a parameter to the method.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Motor">

[`motor.motor_asyncio.AsyncIOMotorCollection.insert_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_many) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass an iterable of documents to the method.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Node.js">

[Collection.insertMany()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#insertMany) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass an array of documents to the method.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="PHP">

[`MongoDB\\Collection::insertMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-insertMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--insertMany--) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass an array of documents to the method.

The following example inserts three new documents into the This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Python">

[`pymongo.collection.Collection.insert_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.insert_many) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass an iterable of documents to the method.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Ruby">

[Mongo::Collection#insert_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#insert_many-instance_method) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection. Pass an array of documents to the method.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

<Tab name="Scala">

[collection.insertMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#insertMany(documents:Seq[_<:TResult],options:org.mongodb.scala.model.InsertManyOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.Completed]) can insert *multiple* [documents](https://www.mongodb.com/docs/core/document/#std-label-bson-document-format) into a collection.

This example inserts multiple documents into `inventory`. If documents do not specify `_id`, MongoDB adds one for each document. See [Insert Behavior](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert-behavior).

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.insertMany([
   {
      title: "Oppenheimer",
      genres: ["Biography", "Drama", "History"],
      runtime: 180,
      rated: "R",
      year: 2023,
      directors: ["Christopher Nolan"],
      cast: ["Cillian Murphy", "Emily Blunt", "Matt Damon"],
      type: "movie"
   },
   {
      title: "Barbie",
      genres: ["Adventure", "Comedy", "Fantasy"],
      runtime: 114,
      rated: "PG-13",
      year: 2023,
      directors: ["Greta Gerwig"],
      cast: ["Margot Robbie", "Ryan Gosling"],
      type: "movie"
   },
   {
      title: "Poor Things",
      genres: ["Comedy", "Drama", "Romance"],
      runtime: 141,
      rated: "R",
      year: 2023,
      directors: ["Yorgos Lanthimos"],
      cast: ["Emma Stone", "Mark Ruffalo", "Willem Dafoe"],
      type: "movie"
   }
])

```

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
   "size", "{",
   "h", BCON_DOUBLE (14),
   "w", BCON_DOUBLE (21),
   "uom", BCON_UTF8 ("cm"),
   "}");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("mat"),
   "qty", BCON_INT64 (85),
   "tags", "[",
   BCON_UTF8 ("gray"),
   "]",
   "size", "{",
   "h", BCON_DOUBLE (27.9),
   "w", BCON_DOUBLE (35.5),
   "uom", BCON_UTF8 ("cm"),
   "}");

r = mongoc_bulk_operation_insert_with_opts (bulk, doc, NULL, &error);
bson_destroy (doc);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}

doc = BCON_NEW (
   "item", BCON_UTF8 ("mousepad"),
   "qty", BCON_INT64 (25),
   "tags", "[",
   BCON_UTF8 ("gel"), BCON_UTF8 ("blue"),
   "]",
   "size", "{",
   "h", BCON_DOUBLE (19),
   "w", BCON_DOUBLE (22.85),
   "uom", BCON_UTF8 ("cm"),
   "}");

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
        { "tags", new BsonArray { "blank", "red" } },
        { "size", new BsonDocument { { "h", 14 }, { "w", 21 }, {  "uom", "cm"} } }
    },
    new BsonDocument
    {
        { "item", "mat" },
        { "qty", 85 },
        { "tags", new BsonArray { "gray" } },
        { "size", new BsonDocument { { "h", 27.9 }, { "w", 35.5 }, {  "uom", "cm"} } }
    },
    new BsonDocument
    {
        { "item", "mousepad" },
        { "qty", 25 },
        { "tags", new BsonArray { "gel", "blue" } },
        { "size", new BsonDocument { { "h", 19 }, { "w", 22.85 }, {  "uom", "cm"} } }
    },
};
collection.InsertMany(documents);
```

</Tab>

<Tab name="Go">

```go

result, err := coll.InsertMany(
	context.TODO(),
	[]any{
		bson.D{
			{"item", "journal"},
			{"qty", int32(25)},
			{"tags", bson.A{"blank", "red"}},
			{"size", bson.D{
				{"h", 14},
				{"w", 21},
				{"uom", "cm"},
			}},
		},
		bson.D{
			{"item", "mat"},
			{"qty", int32(25)},
			{"tags", bson.A{"gray"}},
			{"size", bson.D{
				{"h", 27.9},
				{"w", 35.5},
				{"uom", "cm"},
			}},
		},
		bson.D{
			{"item", "mousepad"},
			{"qty", 25},
			{"tags", bson.A{"gel", "blue"}},
			{"size", bson.D{
				{"h", 19},
				{"w", 22.85},
				{"uom", "cm"},
			}},
		},
	})

```

</Tab>

<Tab name="Java (Async)">

```java
Document journal = new Document("item", "journal")
        .append("qty", 25)
        .append("tags", asList("blank", "red"));

Document journalSize = new Document("h", 14)
        .append("w", 21)
        .append("uom", "cm");
journal.put("size", journalSize);

Document mat = new Document("item", "mat")
        .append("qty", 85)
        .append("tags", singletonList("gray"));

Document matSize = new Document("h", 27.9)
        .append("w", 35.5)
        .append("uom", "cm");
mat.put("size", matSize);

Document mousePad = new Document("item", "mousePad")
        .append("qty", 25)
        .append("tags", asList("gel", "blue"));

Document mousePadSize = new Document("h", 19)
        .append("w", 22.85)
        .append("uom", "cm");
mousePad.put("size", mousePadSize);

Publisher<Success> insertManyPublisher = collection.insertMany(asList(journal, mat, mousePad));
```

</Tab>

<Tab name="Java (Sync)">

```java
Document journal = new Document("item", "journal")
        .append("qty", 25)
        .append("tags", asList("blank", "red"));

Document journalSize = new Document("h", 14)
        .append("w", 21)
        .append("uom", "cm");
journal.put("size", journalSize);

Document mat = new Document("item", "mat")
        .append("qty", 85)
        .append("tags", singletonList("gray"));

Document matSize = new Document("h", 27.9)
        .append("w", 35.5)
        .append("uom", "cm");
mat.put("size", matSize);

Document mousePad = new Document("item", "mousePad")
        .append("qty", 25)
        .append("tags", asList("gel", "blue"));

Document mousePadSize = new Document("h", 19)
        .append("w", 22.85)
        .append("uom", "cm");
mousePad.put("size", mousePadSize);

collection.insertMany(asList(journal, mat, mousePad));
```

</Tab>

<Tab name="Kotlin (Coroutine)">

```kotlin
results = collection.insertMany(
listOf(
    Document("item", "journal")
        .append("qty", 25)
        .append("tags", listOf("blank", "red"))
        .append("size", Document("h", 14)
            .append("w", 21)
            .append("uom", "cm")
        ),
    Document("item", "mat")
        .append("qty", 25)
        .append("tags", listOf("gray"))
        .append("size", Document("h", 27.9)
            .append("w", 35.5)
            .append("uom", "cm")
        ),
    Document("item", "mousepad")
        .append("qty", 25)
        .append("tags", listOf("gel", "blue"))
        .append("size", Document("h", 19)
            .append("w", 22.85)
            .append("uom", "cm")
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
            "tags": ["blank", "red"],
            "size": {"h": 14, "w": 21, "uom": "cm"},
        },
        {
            "item": "mat",
            "qty": 85,
            "tags": ["gray"],
            "size": {"h": 27.9, "w": 35.5, "uom": "cm"},
        },
        {
            "item": "mousepad",
            "qty": 25,
            "tags": ["gel", "blue"],
            "size": {"h": 19, "w": 22.85, "uom": "cm"},
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
    tags: ['blank', 'red'],
    size: { h: 14, w: 21, uom: 'cm' }
  },
  {
    item: 'mat',
    qty: 85,
    tags: ['gray'],
    size: { h: 27.9, w: 35.5, uom: 'cm' }
  },
  {
    item: 'mousepad',
    qty: 25,
    tags: ['gel', 'blue'],
    size: { h: 19, w: 22.85, uom: 'cm' }
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
        'size' => ['h' => 14, 'w' => 21, 'uom' => 'cm'],
    ],
    [
        'item' => 'mat',
        'qty' => 85,
        'tags' => ['gray'],
        'size' => ['h' => 27.9, 'w' => 35.5, 'uom' => 'cm'],
    ],
    [
        'item' => 'mousepad',
        'qty' => 25,
        'tags' => ['gel', 'blue'],
        'size' => ['h' => 19, 'w' => 22.85, 'uom' => 'cm'],
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
            "tags": ["blank", "red"],
            "size": {"h": 14, "w": 21, "uom": "cm"},
        },
        {
            "item": "mat",
            "qty": 85,
            "tags": ["gray"],
            "size": {"h": 27.9, "w": 35.5, "uom": "cm"},
        },
        {
            "item": "mousepad",
            "qty": 25,
            "tags": ["gel", "blue"],
            "size": {"h": 19, "w": 22.85, "uom": "cm"},
        },
    ]
)
```

</Tab>

<Tab name="Ruby">

```ruby
client[:inventory].insert_many([ { item: 'journal',
                                   qty: 25,
                                   tags: %w[blank red],
                                   size: { h: 14, w: 21, uom: 'cm' } },
                                 { item: 'mat',
                                   qty: 85,
                                   tags: [ 'gray' ],
                                   size: { h: 27.9, w: 35.5, uom: 'cm' } },
                                 { item: 'mousepad',
                                   qty: 25,
                                   tags: %w[gel blue],
                                   size: { h: 19, w: 22.85, uom: 'cm' } } ])
```

</Tab>

<Tab name="Scala">

```scala
collection.insertMany(Seq(
  Document("item" -> "journal", "qty" -> 25, "tags" -> Seq("blank", "red"), "size" -> Document("h" -> 14, "w" -> 21, "uom" -> "cm")),
  Document("item" -> "mat", "qty" -> 85, "tags" -> Seq("gray"), "size" -> Document("h" -> 27.9, "w" -> 35.5, "uom" -> "cm")),
  Document("item" -> "mousepad", "qty" -> 25, "tags" -> Seq("gel", "blue"), "size" -> Document("h" -> 19, "w" -> 22.85, "uom" -> "cm"))
)).execute()
```

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

[`insertMany()`](https://www.mongodb.com/docs/reference/method/db.collection.insertMany/#mongodb-method-db.collection.insertMany) returns a document that includes the newly inserted documents `_id` field values. See the [reference](https://www.mongodb.com/docs/reference/method/db.collection.insertMany/#std-label-insertMany-examples) for an example.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Compass">

To view the newly inserted documents, specify a filter of `{}` in the MongoDB Compass query bar and click Find to view your documents.

</Tab>

<Tab name="C">

[mongoc_bulk_operation_insert_with_opts](https://mongoc.org/libmongoc/current/mongoc_bulk_operation_insert_with_opts.html) returns `true` on success, or `false` if passed invalid arguments.

To retrieve the inserted documents, use [mongoc_collection_find_with_opts](https://mongoc.org/libmongoc/current/mongoc_collection_find_with_opts.html) to [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="C#">

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Go">

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Java (Async)">

[com.mongodb.reactivestreams.client.MongoCollection.html.insertMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#insertMany(java.util.List)) returns a [Publisher](http://www.reactive-streams.org/reactive-streams-1.0.1-javadoc/org/reactivestreams/Publisher.html) object. The `Publisher` inserts the document into a collection when subscribers request data.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Java (Sync)">

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Kotlin (Coroutine)">

[MongoCollection.insertMany()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/insert-many.html) returns an `InsertManyResult` instance. The `insertedIds` field of `InsertManyResult` contains the `_id` values of the inserted documents.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Motor">

[`insert_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_many) returns an instance of [`pymongo.results.InsertManyResult`](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.InsertManyResult) whose `inserted_ids` field is a list containing the `_id` of each newly inserted document.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Node.js">

[insertMany()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#insertMany) returns a promise that provides a `result`. The `result.insertedIds` field contains an array with the `_id` of each newly inserted document.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="PHP">

Upon successful insert, the [`insertMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-insertMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--insertMany--) method returns an instance of [`MongoDB\\InsertManyResult`](https://www.mongodb.com/docs/php-library/upcoming/reference/class/MongoDBInsertManyResult/#mongodb-phpclass-phpclass.MongoDB-InsertManyResult) whose [`getInsertedIds()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBInsertManyResult-getInsertedIds/#mongodb-phpmethod-phpmethod.MongoDB-InsertManyResult--getInsertedIds--) method returns the `_id` of each newly inserted document.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Python">

[`insert_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.insert_many) returns an instance of [`pymongo.results.InsertManyResult`](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.InsertManyResult) whose `inserted_ids` field is a list containing the `_id` of each newly inserted document.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Ruby">

Upon successful insert, the [insert_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#insert_many) method returns an instance of [Mongo::BulkWrite::Result](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/BulkWrite/Result.html) whose `inserted_ids` attribute is a list containing the `_id` of each newly inserted document.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

<Tab name="Scala">

Upon successful insert, the [insertMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#insertMany(documents:Seq[_<:TResult],options:org.mongodb.scala.model.InsertManyOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.Completed]) method returns an [Observable](http://mongodb.github.io/mongo-scala-driver/2.1/reference/observables/) with a type parameter indicating when the operation has completed or with either a `com.mongodb.DuplicateKeyException` or `com.mongodb.MongoException`.

To retrieve the inserted documents, [query the collection](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document):

</Tab>

</Tabs>

<Tabs>

<Tab name="MongoDB Shell">

```javascript
db.movies.find( { year: 2023 } )
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

- [bson_destroy](http://mongoc.org/libbson/current/bson_destroy.html)

- [mongoc_bulk_operation_destroy](https://mongoc.org/libmongoc/current/mongoc_bulk_operation_destroy.html)

- [mongoc_collection_destroy](https://mongoc.org/libmongoc/current/mongoc_collection_destroy)

- [mongoc_cursor_destroy](https://mongoc.org/libmongoc/current/mongoc_cursor_destroy.html),

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

## Insert Behavior

### Collection Creation

If the collection does not currently exist, insert operations create the collection.

### `_id` Field

In MongoDB, each document stored in a standard collection requires a unique [_id](https://www.mongodb.com/docs/reference/glossary/#std-term-_id) field that acts as a [primary key](https://www.mongodb.com/docs/reference/glossary/#std-term-primary-key). If an inserted document omits the `_id` field, the MongoDB driver automatically generates an [ObjectId](https://www.mongodb.com/docs/reference/bson-types/#std-label-objectid) for the `_id` field.

This also applies to documents inserted through update operations with [upsert: true](https://www.mongodb.com/docs/reference/method/db.collection.update/#std-label-upsert-parameter).

### Atomicity

All write operations in MongoDB are atomic on the level of a single document. For more information on MongoDB and atomicity, see [Atomicity and Transactions](https://www.mongodb.com/docs/core/write-operations-atomicity/).

### Write Acknowledgement

With write concerns, you can specify the level of acknowledgment requested from MongoDB for write operations. For more information, see [Write Concern](https://www.mongodb.com/docs/reference/write-concern/).

<Tabs>

<Tab name="MongoDB Shell">

- [`db.collection.insertOne()`](https://www.mongodb.com/docs/reference/method/db.collection.insertOne/#mongodb-method-db.collection.insertOne)

- [`db.collection.insertMany()`](https://www.mongodb.com/docs/reference/method/db.collection.insertMany/#mongodb-method-db.collection.insertMany)

- [Collection Methods](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

<Tab name="Compass">

</Tab>

<Tab name="C">

- [mongoc_bulk_operation_insert_with_opts](https://mongoc.org/libmongoc/current/mongoc_bulk_operation_insert_with_opts.html)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

<Tab name="C#">

- [IMongoCollection.InsertOne()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_InsertOne.htm)

- [IMongoCollection.InsertMany()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_InsertMany.htm)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

<Tab name="Go">

- [Collection.InsertOne](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.InsertOne)

- [Collection.InsertMany](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.InsertMany)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

<Tab name="Java (Async)">

- [com.mongodb.reactivestreams.client.MongoCollection.insertOne](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#insertOne(TDocument))

- [com.mongodb.reactivestreams.client.MongoCollection.html.insertMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#insertMany(java.util.List))

- [Java Reactive Streams Driver Quick Tour](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/getting-started/quick-tour/)

</Tab>

<Tab name="Java (Sync)">

- [com.mongodb.client.MongoCollection.insertOne](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#insertOne-TDocument-)

- [com.mongodb.client.MongoCollection.insertMany](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#insertMany-java.util.List-)

- [Additional Java Synchronous Driver Write Examples](http://mongodb.github.io/mongo-java-driver/3.4/driver/tutorials/perform-write-operations/)

</Tab>

<Tab name="Kotlin (Coroutine)">

- [MongoCollection.insertOne](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/insert-one.html)

- [MongoCollection.insertMany](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/insert-many.html)

- [Kotlin Driver Write Operation Examples](https://www.mongodb.com/docs/drivers/kotlin/coroutine/current/fundamentals/crud/write-operations/insert/)

</Tab>

<Tab name="Motor">

- [`motor.motor_asyncio.AsyncIOMotorCollection.insert_one`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_one)

- [`motor.motor_asyncio.AsyncIOMotorCollection.insert_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.insert_many)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

<Tab name="Node.js">

- [Collection.insertOne()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#insertOne)

- [Collection.insertMany()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#insertMany)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

<Tab name="PHP">

- [`MongoDB\\Collection::insertOne()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-insertOne/#mongodb-phpmethod-phpmethod.MongoDB-Collection--insertOne--)

- [`MongoDB\\Collection::insertMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-insertMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--insertMany--)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

<Tab name="Python">

- [`pymongo.collection.Collection.insert_one`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.insert_one)

- [`pymongo.collection.Collection.insert_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.insert_many)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

<Tab name="Ruby">

- [Mongo::Collection#insert_one()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#insert_one-instance_method)

- [Mongo::Collection#insert_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#insert_many-instance_method)

</Tab>

<Tab name="Scala">

- [collection.insertOne()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#insertOne(document:TResult,options:org.mongodb.scala.model.InsertOneOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.Completed])

- [collection.insertMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#insertMany(documents:Seq[_<:TResult],options:org.mongodb.scala.model.InsertManyOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.Completed])

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-inserts)

</Tab>

</Tabs>
