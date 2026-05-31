> Source: https://www.mongodb.com/docs/manual/tutorial/remove-documents/
> Fetch method: direct_markdown

# Delete Documents

You can delete documents in MongoDB using the following methods:

[Delete a Document with Atlas](https://www.mongodb.com/docs/tutorial/remove-documents/#std-label-delete-documents-atlas-ui)- Your programming language's driver.

- The [MongoDB Atlas UI](https://www.mongodb.com/docs/atlas/). To learn more, see [Delete a Document with Atlas](https://www.mongodb.com/docs/tutorial/remove-documents/#std-label-delete-documents-atlas-ui).

- [MongoDB Compass](https://www.mongodb.com/docs/compass/current/).

This page uses the following [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) methods:

- [`db.collection.deleteMany()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteMany/#mongodb-method-db.collection.deleteMany)

- [`db.collection.deleteOne()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteOne/#mongodb-method-db.collection.deleteOne)

The examples on this page use data from the [sample_mflix sample dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](https://www.mongodb.com/docs/atlas/sample-data/load-sample-data-local/#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) document `{}` to the [`db.collection.deleteMany()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteMany/#mongodb-method-db.collection.deleteMany) method.

The following example deletes all documents from the `movies` collection:

```javascript
db.movies.deleteMany({})
```

The method returns a document with the status of the operation. For more information and examples, see [`deleteMany()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteMany/#mongodb-method-db.collection.deleteMany).

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use `<field>:<value>` expressions in the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```javascript
{ <field1>: <value1>, ... }
```

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [`deleteMany()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteMany/#mongodb-method-db.collection.deleteMany) method.

The following example removes all documents from the `movies` collection where `year` equals `2023`:

```javascript
db.movies.deleteMany({ year: 2023 })

```

The method returns a document with the status of the operation. For more information and examples, see [`deleteMany()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteMany/#mongodb-method-db.collection.deleteMany).

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [`db.collection.deleteOne()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteOne/#mongodb-method-db.collection.deleteOne) method.

The following example deletes the first document from the `movies` collection where the `title` field equals `"Dune: Part Two"`:

```javascript
db.movies.deleteOne({ title: "Dune: Part Two" })

```

- [`db.collection.deleteMany()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteMany/#mongodb-method-db.collection.deleteMany)

- [`db.collection.deleteOne()`](https://www.mongodb.com/docs/reference/method/db.collection.deleteOne/#mongodb-method-db.collection.deleteOne)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses the following [PyMongo](https://pymongo.readthedocs.io/en/stable/index.html) Python driver methods:

- [`pymongo.collection.Collection.delete_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_many)

- [`pymongo.collection.Collection.delete_one`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_one)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

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
    ]
)
```

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) document `{}` to the [`pymongo.collection.Collection.delete_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_many) method.

The following example deletes *all* documents from the `inventory` collection:

```python
db.inventory.delete_many({})
```

The [`delete_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_many) method returns an instance of [`pymongo.results.DeleteResult`](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.DeleteResult) with the status of the operation.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use `<field>:<value>` expressions in the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```python
{ <field1>: <value1>, ... }
```

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```python
{ <field1>: { <operator1>: <value1> }, ... }
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [`delete_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_many) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```python
db.inventory.delete_many({"status": "A"})
```

The [`delete_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_many) method returns an instance of [`pymongo.results.DeleteResult`](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.DeleteResult) with the status of the operation.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [`pymongo.collection.Collection.delete_one`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_one) method.

The following example deletes the *first* document where `status` is `"D"`:

```python
db.inventory.delete_one({"status": "D"})
```

- [`pymongo.collection.Collection.delete_many`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_many)

- [`pymongo.collection.Collection.delete_one`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_one)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses the following [Motor](https://motor.readthedocs.io/en/stable/) driver methods:

- [`motor.motor_asyncio.AsyncIOMotorCollection.delete_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_many)

- [`motor.motor_asyncio.AsyncIOMotorCollection.delete_one`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_one)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

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
    ]
)
```

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) document `{}` to the [`motor.motor_asyncio.AsyncIOMotorCollection.delete_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_many) method.

The following example deletes *all* documents from the `inventory` collection:

```python
await db.inventory.delete_many({})
```

The [`delete_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_many) coroutine asynchronously returns an instance of [`pymongo.results.DeleteResult`](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.DeleteResult) with the status of the operation.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use `<field>:<value>` expressions in the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```python
{ <field1>: <value1>, ... }
```

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```python
{ <field1>: { <operator1>: <value1> }, ... }
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [`delete_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_many) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```python
await db.inventory.delete_many({"status": "A"})
```

The [`delete_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_many) coroutine asynchronously returns an instance of [`pymongo.results.DeleteResult`](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.DeleteResult) with the status of the operation.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [`motor.motor_asyncio.AsyncIOMotorCollection.delete_one`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_one) method.

The following example deletes the *first* document where `status` is `"D"`:

```python
await db.inventory.delete_one({"status": "D"})
```

- [`motor.motor_asyncio.AsyncIOMotorCollection.delete_many`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_many)

- [`motor.motor_asyncio.AsyncIOMotorCollection.delete_one`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.delete_one)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses the following [Java Synchronous Driver](http://mongodb.github.io/mongo-java-driver/3.4/driver/) methods:

- [com.mongodb.client.MongoCollection.deleteMany](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteMany-org.bson.conversions.Bson-)

- [com.mongodb.client.MongoCollection.deleteOne](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteOne-org.bson.conversions.Bson-)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```java
collection.insertMany(asList(
        Document.parse("{ item: 'journal', qty: 25, size: { h: 14, w: 21, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'notebook', qty: 50, size: { h: 8.5, w: 11, uom: 'in' }, status: 'A' }"),
        Document.parse("{ item: 'paper', qty: 100, size: { h: 8.5, w: 11, uom: 'in' }, status: 'D' }"),
        Document.parse("{ item: 'planner', qty: 75, size: { h: 22.85, w: 30, uom: 'cm' }, status: 'D' }"),
        Document.parse("{ item: 'postcard', qty: 45, size: { h: 10, w: 15.25, uom: 'cm' }, status: 'A' }")
));
```

## Delete All Documents

To delete all documents from a collection, pass an empty [org.bson.Document](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/org/bson/Document) object as the [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) to the [com.mongodb.client.MongoCollection.deleteMany](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteMany-org.bson.conversions.Bson-) method.

The following example deletes *all* documents from the `inventory` collection:

```java
collection.deleteMany(new Document());
```

The [com.mongodb.client.MongoCollection.deleteMany](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteMany-org.bson.conversions.Bson-) method returns an instance of [com.mongodb.client.result.DeleteResult](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/result/DeleteResult) with the status of the operation.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use the `com.mongodb.client.model.Filters.eq_` method to create the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```java
and(eq(<field1>, <value1>), eq(<field2>, <value2>) ...)
```

In addition to the equality condition, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. For example:

```java
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [com.mongodb.client.MongoCollection.deleteMany](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteMany-org.bson.conversions.Bson-) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```java
collection.deleteMany(eq("status", "A"));
```

The [com.mongodb.client.MongoCollection.deleteMany](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteMany-org.bson.conversions.Bson-) method returns an instance of [com.mongodb.client.result.DeleteResult](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/result/DeleteResult) with the status of the operation.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [com.mongodb.client.MongoCollection.deleteOne](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteOne-org.bson.conversions.Bson-) method.

The following example deletes the *first* document where `status` is `"D"`:

```java
collection.deleteOne(eq("status", "D"));
```

- [com.mongodb.client.MongoCollection.deleteMany](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteMany-org.bson.conversions.Bson-)

- [com.mongodb.client.MongoCollection.deleteOne](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#deleteOne-org.bson.conversions.Bson-)

- [Additional Java Synchronous Driver Write Examples](http://mongodb.github.io/mongo-java-driver/3.4/driver/tutorials/perform-write-operations/)

This page uses the following [Java Reactive Streams Driver](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/) methods:

- [com.mongodb.reactivestreams.client.MongoCollection.deleteMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteMany(org.bson.conversions.Bson))

- [com.mongodb.reactivestreams.client.MongoCollection.deleteOne](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteOne(org.bson.conversions.Bson))

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```java
Publisher<Success> insertManyPublisher = collection.insertMany(asList(
        Document.parse("{ item: 'journal', qty: 25, size: { h: 14, w: 21, uom: 'cm' }, status: 'A' }"),
        Document.parse("{ item: 'notebook', qty: 50, size: { h: 8.5, w: 11, uom: 'in' }, status: 'A' }"),
        Document.parse("{ item: 'paper', qty: 100, size: { h: 8.5, w: 11, uom: 'in' }, status: 'D' }"),
        Document.parse("{ item: 'planner', qty: 75, size: { h: 22.85, w: 30, uom: 'cm' }, status: 'D' }"),
        Document.parse("{ item: 'postcard', qty: 45, size: { h: 10, w: 15.25, uom: 'cm' }, status: 'A' }")
));
```

## Delete All Documents

To delete all documents from a collection, pass an empty [org.bson.Document](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/org/bson/Document) object as the [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) to the [com.mongodb.reactivestreams.client.MongoCollection.deleteMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteMany(org.bson.conversions.Bson)) method.

The following example deletes *all* documents from the `inventory` collection:

```java
Publisher<DeleteResult> deleteManyPublisher = collection.deleteMany(new Document());
```

[com.mongodb.reactivestreams.client.MongoCollection.deleteMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteMany(org.bson.conversions.Bson)) returns a [Publisher](http://www.reactive-streams.org/reactive-streams-1.0.1-javadoc/org/reactivestreams/Publisher.html) object of type [com.mongodb.client.result.DeleteResult](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/result/DeleteResult) if successful. Returns an instance of `com.mongodb.MongoException` if unsuccessful.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use the [com.mongodb.client.model.Filters.eq](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Filters.html#eq-java.lang.String-TItem-) method to create the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```java
and(eq(<field1>, <value1>), eq(<field2>, <value2>) ...)
```

In addition to the equality condition, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. For example:

```java
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [com.mongodb.reactivestreams.client.MongoCollection.deleteMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteMany(org.bson.conversions.Bson)) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```java
deleteManyPublisher = collection.deleteMany(eq("status", "A"));
```

[com.mongodb.reactivestreams.client.MongoCollection.deleteMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteMany(org.bson.conversions.Bson)) returns a [Publisher](http://www.reactive-streams.org/reactive-streams-1.0.1-javadoc/org/reactivestreams/Publisher.html) object of type [com.mongodb.client.result.DeleteResult](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/result/DeleteResult) if successful. Returns an instance of `com.mongodb.MongoException` if unsuccessful.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [com.mongodb.reactivestreams.client.MongoCollection.deleteMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteMany(org.bson.conversions.Bson)) method.

The following example deletes the *first* document where `status` is `"D"`:

```java
Publisher<DeleteResult> deleteOnePublisher = collection.deleteOne(eq("status", "D"));
```

- [com.mongodb.reactivestreams.client.MongoCollection.deleteMany](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteMany(org.bson.conversions.Bson))

- [com.mongodb.reactivestreams.client.MongoCollection.deleteOne](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#deleteOne(org.bson.conversions.Bson))

- [Java Reactive Streams Driver Quick Tour](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/getting-started/quick-tour/)

This page uses the following [Kotlin Coroutine Driver](https://www.mongodb.com/docs/drivers/kotlin/coroutine/current/) methods:

- [MongoCollection.deleteOne()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-one.html)

- [MongoCollection.deleteMany()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-many.html)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```kotlin
collection.insertMany(
    listOf(
        Document("item", "journal")
            .append("qty", 25)
            .append("size", Document("h", 14).append("w", 21).append("uom", "cm"))
            .append("status", "A"),
        Document("item", "notebook")
            .append("qty", 50)
            .append("size", Document("h", 8.5).append("w", 11).append("uom", "in"))
            .append("status", "A"),
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
    )
)
```

## Delete All Documents

To delete all documents from a collection, pass an empty `Bson` object as the [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) to the [MongoCollection.deleteMany()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-many.html) method.

The following example deletes *all* documents from the `inventory` collection:

```kotlin
collection.deleteMany(empty())
```

The [MongoCollection.deleteMany()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-many.html) method returns an instance of [com.mongodb.client.result.DeleteResult](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/result/DeleteResult.html) that describes the status of the operation and count of deleted documents.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use the [Filters.eq()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/model/Filters.html#eq(java.lang.String,TItem)) method to create the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```kotlin
and(eq(<field1>, <value1>), eq(<field2>, <value2>) ...)
```

In addition to the equality condition, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. For example:

```kotlin
and(gte(<field1>, <value1>), lt(<field2>, <value2>), eq(<field3>, <value3>))
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [MongoCollection.deleteMany()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-many.html) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```kotlin
collection.deleteMany(eq("status", "A"));
```

The [MongoCollection.deleteMany()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-many.html) method returns an instance of [com.mongodb.client.result.DeleteResult](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/client/result/DeleteResult.html) that describes the status of the operation and count of deleted documents.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter, even if multiple documents match the specified filter, use the [MongoCollection.deleteOne()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-one.html) method.

The following example deletes the *first* document where `status` is `"D"`:

- [MongoCollection.deleteOne()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-one.html)

- [MongoCollection.deleteMany()](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-kotlin-coroutine/mongodb-driver-kotlin-coroutine/com.mongodb.kotlin.client.coroutine/-mongo-collection/delete-many.html)

- [Kotlin Coroutine Driver Delete Documents Guide](https://www.mongodb.com/docs/drivers/kotlin/coroutine/current/fundamentals/crud/write-operations/delete/)

This page uses the following [MongoDB Node.js Driver](https://www.mongodb.com/docs/drivers/node/) methods:

- [Collection.deleteMany()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteMany/)

- [Collection.deleteOne()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteOne/)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

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
  }
]);
```

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) document `{}` to the [Collection.deleteMany()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteMany/) method.

The following example deletes *all* documents from the `inventory` collection:

```javascript
await db.collection('inventory').deleteMany({});
```

[Collection.deleteMany()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteMany/) returns a promise that provides a `result`. The `result.deletedCount` property contains the number of documents that matched the filter.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use `<field>:<value>` expressions in the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```javascript
{ <field1>: <value1>, ... }
```

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [deleteMany()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteMany/) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```javascript
await db.collection('inventory').deleteMany({ status: 'A' });
```

[Collection.deleteMany()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteMany/) returns a promise that provides a `result`. The `result.deletedCount` property contains the number of documents that matched the filter.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [Collection.deleteOne()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteOne/) method.

The following example deletes the *first* document where `status` is `"D"`:

```javascript
await db.collection('inventory').deleteOne({ status: 'D' });
```

- [Collection.deleteMany()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteMany/)

- [Collection.deleteOne()](https://www.mongodb.com/docs/drivers/node/current/usage-examples/deleteOne/)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses the following [MongoDB PHP Library](https://www.mongodb.com/docs/php-library/current/) methods:

- [`MongoDB\\Collection::deleteMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteMany--)

- [`MongoDB\\Collection::deleteOne()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteOne/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteOne--)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

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
]);
```

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) document `[]` to the [`MongoDB\\Collection::deleteMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteMany--) method.

The following example deletes *all* documents from the `inventory` collection:

```php
$deleteResult = $db->inventory->deleteMany([]);
```

Upon successful execution, the [`deleteMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteMany--) method returns an instance of [`MongoDB\\DeleteResult`](https://www.mongodb.com/docs/php-library/upcoming/reference/class/MongoDBDeleteResult/#mongodb-phpclass-phpclass.MongoDB-DeleteResult) whose [`getDeletedCount()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBDeleteResult-getDeletedCount/#mongodb-phpmethod-phpmethod.MongoDB-DeleteResult--getDeletedCount--) method returns the number of documents that matched the filter.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use `<field> => <value>` expressions in the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```php
[ <field1> => <value1>, ... ]
```

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```php
[ <field1> => [ <operator1> => <value1> ], ... ]
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [`deleteMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteMany--) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```php
$deleteResult = $db->inventory->deleteMany(['status' => 'A']);
```

Upon successful execution, the [`deleteMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteMany--) method returns an instance of [`MongoDB\\DeleteResult`](https://www.mongodb.com/docs/php-library/upcoming/reference/class/MongoDBDeleteResult/#mongodb-phpclass-phpclass.MongoDB-DeleteResult) whose [`getDeletedCount()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBDeleteResult-getDeletedCount/#mongodb-phpmethod-phpmethod.MongoDB-DeleteResult--getDeletedCount--) method returns the number of documents that matched the filter.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [`MongoDB\\Collection::deleteOne()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteOne/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteOne--) method.

The following example deletes the *first* document where `status` is `"D"`:

```php
$deleteResult = $db->inventory->deleteOne(['status' => 'D']);
```

- [`MongoDB\\Collection::deleteMany()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteMany/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteMany--)

- [`MongoDB\\Collection::deleteOne()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-deleteOne/#mongodb-phpmethod-phpmethod.MongoDB-Collection--deleteOne--)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses the following [MongoDB Ruby Driver](https://www.mongodb.com/docs/ruby-driver/current/) methods:

- [Mongo::Collection#delete_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_many-instance_method)

- [Mongo::Collection#delete_one()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_one-instance_method)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```ruby
client[:inventory].insert_many([
                                 { item: 'journal',
                                   qty: 25,
                                   size: { h: 14, w: 21, uom: 'cm' },
                                   status: 'A' },
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
                               ])
```

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) document `{}` to the [Mongo::Collection#delete_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_many-instance_method) method.

The following example deletes *all* documents from the `inventory` collection:

```ruby
client[:inventory].delete_many({})
```

Upon successful execution, the [delete_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_many-instance_method) method returns an instance of [Mongo::Operation::Result](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Operation/Result.html), whose `deleted_count` attribute contains the number of documents that matched the filter.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use `<field> => <value>` expressions in the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```ruby
{ <field1> => <value1>, ... }
```

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```ruby
{ <field1> => { <operator1> => <value1> }, ... }
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [delete_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_many-instance_method) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```ruby
client[:inventory].delete_many(status: 'A')
```

Upon successful execution, the [delete_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_many-instance_method) method returns an instance of [Mongo::Operation::Result](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Operation/Result.html), whose `deleted_count` attribute contains the number of documents that matched the filter.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [Mongo::Collection#delete_one()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_one-instance_method) method.

The following example deletes the *first* document where `status` is `"D"`:

```ruby
client[:inventory].delete_one(status: 'D')
```

- [Mongo::Collection#delete_many()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_many-instance_method)

- [Mongo::Collection#delete_one()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#delete_one-instance_method)

This page uses the following [MongoDB Scala Driver](http://mongodb.github.io/mongo-scala-driver/) methods:

- [collection.deleteMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteMany(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult])

- [collection.deleteOne()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteOne(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult])

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```scala
collection.insertMany(Seq(
  Document("""{ item: "journal", qty: 25, size: { h: 14, w: 21, uom: "cm" }, status: "A" }"""),
  Document("""{ item: "notebook", qty: 50, size: { h: 8.5, w: 11, uom: "in" }, status: "A" }"""),
  Document("""{ item: "paper", qty: 100, size: { h: 8.5, w: 11, uom: "in" }, status: "D" }"""),
  Document("""{ item: "planner", qty: 75, size: { h: 22.85, w: 30, uom: "cm" }, status: "D" }"""),
  Document("""{ item: "postcard", qty: 45, size: { h: 10, w: 15.25, uom: "cm" }, status: "A" }""")
)).execute()
```

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) `Document()` to the [collection.deleteMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteMany(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult]) method.

The following example deletes *all* documents from the `inventory` collection:

```scala
collection.deleteMany(Document()).execute()
```

Upon successful execution, the [collection.deleteMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteMany(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult]) method returns an [Observable](http://mongodb.github.io/mongo-scala-driver/2.1/reference/observables/) with a single element with a `DeleteResult` type parameter or with an `com.mongodb.MongoException`.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use the `com.mongodb.client.model.Filters.eq_` method to create the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```scala
and(equal(<field1>, <value1>), equal(<field2>, <value2>) ...)
```

In addition to the equality condition, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the `com.mongodb.client.model.Filters_` helper methods to facilitate the creation of filter documents. For example:

```scala
and(gte(<field1>, <value1>), lt(<field2>, <value2>), equal(<field3>, <value3>))
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [deleteMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteMany(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult]) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```scala
collection.deleteMany(equal("status", "A")).execute()
```

Upon successful execution, the [collection.deleteMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteMany(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult]) method returns an [Observable](http://mongodb.github.io/mongo-scala-driver/2.1/reference/observables/) with a single element with a `DeleteResult` type parameter or with an `com.mongodb.MongoException`.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [collection.deleteOne()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteOne(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult]) method.

The following example deletes the *first* document where `status` is `"D"`:

```scala
collection.deleteOne(equal("status", "D")).execute()
```

- [collection.deleteMany()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteMany(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult])

- [collection.deleteOne()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#deleteOne(filter:org.mongodb.scala.bson.conversions.Bson,options:org.mongodb.scala.model.DeleteOptions):org.mongodb.scala.SingleObservable[org.mongodb.scala.result.DeleteResult])

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses the following [MongoDB C# Driver](https://www.mongodb.com/docs/drivers/csharp/) methods:

- [IMongoCollection.DeleteMany()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteMany.htm)

- [IMongoCollection.DeleteOne()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteOne.htm)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

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
        { "status", "P" }
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
        { "status", "A" }
    }
};
collection.InsertMany(documents);
```

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter)
`Builders<BsonDocument>.Filter.Empty` to the [IMongoCollection.DeleteMany()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteMany.htm) method.

The following example deletes *all* documents from the `inventory` collection:

```csharp
var filter = Builders<BsonDocument>.Filter.Empty;
var result = collection.DeleteMany(filter);
```

Upon successful execution, the [IMongoCollection.DeleteMany()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteMany.htm) method returns an instance of [DeleteResult](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/T_MongoDB_Driver_DeleteResult.htm) whose `DeletedCount` property contains the number of documents that matched the filter.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, construct a filter using the [Eq](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/Overload_MongoDB_Driver_FilterDefinitionBuilder_1_Eq.htm) method:

```csharp
Builders<BsonDocument>.Filter.Eq(<field>, <value>);
```

In addition to the equality filter, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the [FilterDefinitionBuilder](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/T_MongoDB_Driver_FilterDefinitionBuilder_1.htm) methods to create a filter document. For example:

```csharp
var builder = Builders<BsonDocument>.Filter;
builder.And(builder.Eq(<field1>, <value1>), builder.Lt(<field2>, <value2>));
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [IMongoCollection.DeleteMany()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteMany.htm) method.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var result = collection.DeleteMany(filter);
```

Upon successful execution, the [IMongoCollection.DeleteMany()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteMany.htm) method returns an instance of [DeleteResult](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/T_MongoDB_Driver_DeleteResult.htm) whose `DeletedCount` property contains the number of documents that matched the filter.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [IMongoCollection.DeleteOne()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteOne.htm) method.

The following example deletes the *first* document where `status` is `"D"`:

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "D");
var result = collection.DeleteOne(filter);
```

- [IMongoCollection.DeleteMany()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteMany.htm)

- [IMongoCollection.DeleteOne()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_IMongoCollection_1_DeleteOne.htm)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses the following [MongoDB C Driver](https://mongoc.org/libmongoc/current/index.html) methods:

- [mongoc_collection_delete_one](https://mongoc.org/libmongoc/current/mongoc_collection_delete_one.html)

- [mongoc_collection_delete_many](https://mongoc.org/libmongoc/current/mongoc_collection_delete_many.html)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

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

/* "reply" is initialized on success or error */
r = (bool) mongoc_bulk_operation_execute (bulk, &reply, &error);
if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
}
```

## Delete All Documents

To delete all documents from a collection, pass the [mongoc_collection_t](https://mongoc.org/libmongoc/current/mongoc_collection_t.html) and a [bson_t](https://mongoc.org/libbson/current/bson_t.html) that matches all documents to the [mongoc_collection_delete_many](https://mongoc.org/libmongoc/current/mongoc_collection_delete_many.html) method.

The following example deletes *all* documents from the `inventory` collection:

```c
mongoc_collection_t *collection;
bson_t *selector;
bool r;
bson_error_t error;

collection = mongoc_database_get_collection (db, "inventory");
selector = BCON_NEW (NULL);

r = mongoc_collection_delete_many (collection, selector, NULL, NULL, &error);
bson_destroy (selector);

if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}
```

The [mongoc_collection_delete_many](https://mongoc.org/libmongoc/current/mongoc_collection_delete_many.html) method returns `true` if successful, or returns `false` and sets an error if there are invalid arguments or a server or network error occurs.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use `<field>:<value>` expressions in the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```c
{ <field1>: <value1>, ... }
```

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```c
{ <field1>: { <operator1>: <value1> }, ... }
```

To delete all documents that match a deletion criteria, pass the [mongoc_collection_t](https://mongoc.org/libmongoc/current/mongoc_collection_t.html) and a [bson_t](https://mongoc.org/libbson/current/bson_t.html) that matches the documents you want to delete to the [mongoc_collection_delete_many](https://mongoc.org/libmongoc/current/mongoc_collection_delete_many.html) method.

```c
mongoc_collection_t *collection;
bson_t *selector;
bool r;
bson_error_t error;

collection = mongoc_database_get_collection (db, "inventory");
selector = BCON_NEW ("status", BCON_UTF8 ("A"));

r = mongoc_collection_delete_many (collection, selector, NULL, NULL, &error);
bson_destroy (selector);

if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}
```

The [mongoc_collection_delete_many](https://mongoc.org/libmongoc/current/mongoc_collection_delete_many.html) method returns `true` if successful, or returns `false` and sets an error if there are invalid arguments or a server or network error occurs.

## Delete Only One Document that Matches a Condition

To delete a single document from a collection, pass the [mongoc_collection_t](https://mongoc.org/libmongoc/current/mongoc_collection_t.html) and a [bson_t](https://mongoc.org/libbson/current/bson_t.html) that matches the document you want to delete to the [mongoc_collection_delete_one](https://mongoc.org/libmongoc/current/mongoc_collection_delete_one.html) method.

The following example deletes the *first* document where `status` is `"D"`:

```c
mongoc_collection_t *collection;
bson_t *selector;
bool r;
bson_error_t error;

collection = mongoc_database_get_collection (db, "inventory");
selector = BCON_NEW ("status", BCON_UTF8 ("D"));

r = mongoc_collection_delete_one (collection, selector, NULL, NULL, &error);
bson_destroy (selector);

if (!r) {
   MONGOC_ERROR ("%s\n", error.message);
   goto done;
}
```

Clean up any open resources by calling the following methods, as appropriate:

- [bson_destroy](http://mongoc.org/libbson/current/bson_destroy.html)

- [mongoc_bulk_operation_destroy](https://mongoc.org/libmongoc/current/mongoc_bulk_operation_destroy.html)

- [mongoc_collection_destroy](https://mongoc.org/libmongoc/current/mongoc_collection_destroy)

- [mongoc_cursor_destroy](https://mongoc.org/libmongoc/current/mongoc_cursor_destroy.html),

- [mongoc_collection_delete_one](https://mongoc.org/libmongoc/current/mongoc_collection_delete_one.html)

- [mongoc_collection_delete_many](https://mongoc.org/libmongoc/current/mongoc_collection_delete_many.html)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses the following [MongoDB Go Driver](https://www.mongodb.com/docs/drivers/go/) functions:

- [Collection.DeleteMany](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteMany)

- [Collection.DeleteOne](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteOne)

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

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
}

result, err := coll.InsertMany(context.TODO(), docs)

```

## Delete All Documents

To delete all documents from a collection, pass an empty [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) document to the [Collection.DeleteMany](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteMany) function.

The following example deletes *all* documents from the `inventory` collection:

```go

result, err := coll.DeleteMany(context.TODO(), bson.D{})

```

Upon successful execution, the [Collection.DeleteMany](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteMany) function returns an instance of [DeleteResult](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#DeleteResult) whose `DeletedCount` property contains the number of documents that matched the filter.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use the `bson.D` type to create a filter document:

```go
filter := bson.D{{"<field>", <value>}}
```

In addition to the equality filter, MongoDB provides various [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify filter conditions. Use the bson package to create query operators for filter documents. For example:

```go
filter := bson.D{
    {"$and", bson.A{
        bson.D{{"field1", bson.D{{"$eq", value1}}}},
        bson.D{{"field2", bson.D{{"$lt", value2}}}},
    }},
}
```

To delete all documents that match a deletion criteria, pass a [filter](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) parameter to the [Collection.DeleteMany](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteMany) function.

The following example removes all documents from the `inventory` collection where the `status` field equals `"A"`:

```go

result, err := coll.DeleteMany(
	context.TODO(),
	bson.D{
		{"status", "A"},
	},
)

```

Upon successful execution, the [Collection.DeleteMany](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteMany) function returns an instance of [DeleteResult](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#DeleteResult) whose `DeletedCount` property contains the number of documents that matched the filter.

## Delete Only One Document that Matches a Condition

To delete at most a single document that matches a specified filter (even though multiple documents may match the specified filter) use the [Collection.DeleteOne](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteOne) function.

The following example deletes the *first* document where `status` is `"D"`:

```go

result, err := coll.DeleteOne(
	context.TODO(),
	bson.D{
		{"status", "D"},
	},
)

```

- [Collection.DeleteMany](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteMany)

- [Collection.DeleteOne](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.DeleteOne)

- [Collections](https://www.mongodb.com/docs/reference/method/#std-label-additional-deletes)

This page uses [MongoDB Compass](https://www.mongodb.com/docs/compass/current/#std-label-compass-index) to delete the documents.

Populate the `inventory` collection with the following documents:

```javascript
[
    { "item": "journal", "qty": 25, "size": { "h": 14, "w": 21, "uom": "cm" }, "status": "A" },
    { "item": "notebook", "qty": 50, "size": { "h": 8.5, "w": 11, "uom": "in" }, "status": "P" },
    { "item": "paper", "qty": 100, "size": { "h": 8.5, "w": 11, "uom": "in" }, "status": "D" },
    { "item": "planner", "qty": 75, "size": { "h": 22.85, "w": 30, "uom": "cm" }, "status": "D" },
    { "item": "postcard", "qty": 45, "size": { "h": 10, "w": 15.25, "uom": "cm" }, "status": "A" }
]
```

For instructions on inserting documents in MongoDB Compass, see [Insert Documents](https://www.mongodb.com/docs/tutorial/insert-documents/#std-label-write-op-insert).

For complete reference on inserting documents in MongoDB Compass, see the [Compass documentation](https://www.mongodb.com/docs/compass/current/documents/insert/#std-label-compass-insert-documents).

## Delete All Documents

To delete all documents from a collection, click the DELETE button under the Documents tab.

The following example deletes *all* documents from the `inventory` collection:

When you confirm the deletion in the pop-up window that appears after you click DELETE, MongoDB Compass deletes all documents and displays a message indicating how many documents were deleted.

## Delete All Documents that Match a Condition

You can specify criteria, or filters, that identify the documents to delete. The [filters](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) use the same syntax as read operations.

To specify equality conditions, use `<field>:<value>` expressions in the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter):

```javascript
{ <field1>: <value1>, ... }
```

A [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) can use the [query operators](https://www.mongodb.com/docs/reference/mql/query-predicates/#std-label-query-selectors) to specify conditions in the following form:

```javascript
{ <field1>: { <operator1>: <value1> }, ... }
```

To delete all documents that match a deletion criteria, write your query filter in the Compass query bar, then click the DELETE button under the Documents tab. The following example deletes all documents where `{ status: "A" }`:

When you confirm the deletion in the pop-up window that appears after you click DELETE, MongoDB Compass deletes all documents and displays a message indicating how many documents were deleted.

## Delete Only One Document that Matches a Condition

To delete a single document that matches a specified filter:

1. Write your query filter in the Compass query bar and click Find.

2. Hover your mouse over the document you want to delete.

3. Click the  button on the right side of your document.

The following example deletes a document with `{ status: "A" }` from the `inventory` collection:

- [Compass Documents](https://www.mongodb.com/docs/compass/current/documents/)

- [Compass Query Bar](https://www.mongodb.com/docs/compass/current/query/filter/#std-label-compass-query-bar)

## Delete a Document with Atlas

You can delete only one document at a time in the MongoDB Atlas UI. To delete multiple documents, connect to your Atlas deployment from [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) or a MongoDB driver and follow the examples on this page for your preferred method.

The example in this section uses the [sample movies dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/). To learn how to load the sample dataset into your MongoDB Atlas deployment, see [Load Sample Data](https://www.mongodb.com/docs/atlas/sample-data/#std-label-load-sample-data).

To delete a document in MongoDB Atlas, follow these steps:

### In the MongoDB Atlas UI, go to the Clusters page for your project.

- If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Clusters under the Database heading.

  The [Clusters](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fclusters) page displays.

### Navigate to the collection.

- For the cluster that contains the sample data, click Browse Collections.

- In the left navigation pane, select the `sample_mflix` database.

- Select the `movies` collection.

### Specify a query filter document.

Optionally, you can specify a [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) in the Filter field. A query filter document uses [query operators](https://www.mongodb.com/docs/core/csfle/reference/supported-operations/#std-label-csfle-supported-query-operators) to specify search conditions.

Copy the following query filter document into the Filter search bar and click Apply:

```javascript
{ genres: "Action", rated: { $in: [ "PG", "PG-13" ] } }
```

This query filter returns all documents in the `sample_mflix.movies` collection where `genres` equals `Action` and `rated` equals either `PG` or `PG-13`.

### Delete a document.

- For the document that you want to delete, hover over the document and click the trash icon that appears on the right-hand side.

  After clicking the delete button, MongoDB Atlas flags the document for deletion and asks for your confirmation.

- Click Delete to confirm your selection.

To learn more, see [Create, View, Update, and Delete Documents](https://www.mongodb.com/docs/atlas/atlas-ui/documents/).

## Behavior

### Indexes

Delete operations do not drop indexes, even if deleting all documents from a collection.

### Atomicity

All write operations in MongoDB are atomic on the level of a single document. For more information on MongoDB and atomicity, see [Atomicity and Transactions](https://www.mongodb.com/docs/core/write-operations-atomicity/).

### Write Acknowledgement

With write concerns, you can specify the level of acknowledgment requested from MongoDB for write operations. For details, see [Write Concern](https://www.mongodb.com/docs/reference/write-concern/).
