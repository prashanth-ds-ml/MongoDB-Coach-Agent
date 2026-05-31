> Source: https://www.mongodb.com/docs/manual/tutorial/project-fields-from-query-results/
> Fetch method: direct_markdown

# Project Fields to Return from Query

Use projection to select which document fields a query returns. You can use the following methods:

[Project Fields to Return from a Query with MongoDB Atlas](https://www.mongodb.com/docs/tutorial/project-fields-from-query-results/#std-label-project-fields-atlas-ui)- Your programming language's driver.

- The [MongoDB Atlas UI](https://www.mongodb.com/docs/atlas/). To learn more, see [Project Fields to Return from a Query with MongoDB Atlas](https://www.mongodb.com/docs/tutorial/project-fields-from-query-results/#std-label-project-fields-atlas-ui).

- [MongoDB Compass](https://www.mongodb.com/docs/compass/current/).

By default, queries in MongoDB return all fields in matching documents. To limit the amount of data that MongoDB sends to applications, you can include a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document to specify or restrict fields to return.

query operations with projectionThis page provides examples of query operations with projection using the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```javascript
db.inventory.insertMany( [
   { item: "journal", status: "A", size: { h: 14, w: 21, uom: "cm" }, instock: [ { warehouse: "A", qty: 5 } ] },
   { item: "notebook", status: "A",  size: { h: 8.5, w: 11, uom: "in" }, instock: [ { warehouse: "C", qty: 5 } ] },
   { item: "paper", status: "D", size: { h: 8.5, w: 11, uom: "in" }, instock: [ { warehouse: "A", qty: 60 } ] },
   { item: "planner", status: "D", size: { h: 22.85, w: 30, uom: "cm" }, instock: [ { warehouse: "A", qty: 40 } ] },
   { item: "postcard", status: "A", size: { h: 10, w: 15.25, uom: "cm" }, instock: [ { warehouse: "B", qty: 15 }, { warehouse: "C", qty: 35 } ] }
]);
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```javascript
db.inventory.find( { status: "A" } )
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```javascript
db.inventory.find( { status: "A" }, { item: 1, status: 1 } )
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```javascript
db.inventory.find( { status: "A" }, { item: 1, status: 1, _id: 0 } )
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```javascript
db.inventory.find( { status: "A" }, { status: 0, instock: 0 } )
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```javascript
db.inventory.find(
   { status: "A" },
   { item: 1, status: 1, "size.uom": 1 }
)
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```javascript
db.inventory.find(
   { status: "A" },
   { "size.uom": 0 }
)
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```javascript
db.inventory.find( { status: "A" }, { item: 1, status: 1, "instock.qty": 1 } )
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```javascript
db.inventory.find( { status: "A" }, { item: 1, status: 1, instock: { $slice: -1 } } )
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `{ "instock.0": 1 }` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [`pymongo.collection.Collection.find`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.find) method in the [PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/) Python driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```python
db.inventory.insert_many(
    [
        {
            "item": "journal",
            "status": "A",
            "size": {"h": 14, "w": 21, "uom": "cm"},
            "instock": [{"warehouse": "A", "qty": 5}],
        },
        {
            "item": "notebook",
            "status": "A",
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "instock": [{"warehouse": "C", "qty": 5}],
        },
        {
            "item": "paper",
            "status": "D",
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "instock": [{"warehouse": "A", "qty": 60}],
        },
        {
            "item": "planner",
            "status": "D",
            "size": {"h": 22.85, "w": 30, "uom": "cm"},
            "instock": [{"warehouse": "A", "qty": 40}],
        },
        {
            "item": "postcard",
            "status": "A",
            "size": {"h": 10, "w": 15.25, "uom": "cm"},
            "instock": [{"warehouse": "B", "qty": 15}, {"warehouse": "C", "qty": 35}],
        },
    ]
)
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`find`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```python
cursor = db.inventory.find({"status": "A"})
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```python
cursor = db.inventory.find({"status": "A"}, {"item": 1, "status": 1})
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```python
cursor = db.inventory.find({"status": "A"}, {"item": 1, "status": 1, "_id": 0})
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```python
cursor = db.inventory.find({"status": "A"}, {"status": 0, "instock": 0})
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```python
cursor = db.inventory.find({"status": "A"}, {"item": 1, "status": 1, "size.uom": 1})
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```python
cursor = db.inventory.find({"status": "A"}, {"size.uom": 0})
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```python
cursor = db.inventory.find({"status": "A"}, {"item": 1, "status": 1, "instock.qty": 1})
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```python
cursor = db.inventory.find(
    {"status": "A"}, {"item": 1, "status": 1, "instock": {"$slice": -1}}
)
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `{ "instock.0": 1 }` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [com.mongodb.client.MongoCollection.find](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#find--) method in the MongoDB [Java Synchronous Driver](http://mongodb.github.io/mongo-java-driver/3.4/driver/).

The driver provides [com.mongodb.client.model.Filters](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Filters.html) helper methods to facilitate the creation of filter documents. The examples on this page use these methods to create the filter documents.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```java
collection.insertMany(asList(
    Document.parse("{ item: 'journal', status: 'A', size: { h: 14, w: 21, uom: 'cm' }, instock: [ { warehouse: 'A', qty: 5 }]}"),
    Document.parse("{ item: 'notebook', status: 'A',  size: { h: 8.5, w: 11, uom: 'in' }, instock: [ { warehouse: 'C', qty: 5}]}"),
    Document.parse("{ item: 'paper', status: 'D', size: { h: 8.5, w: 11, uom: 'in' }, instock: [ { warehouse: 'A', qty: 60 }]}"),
    Document.parse("{ item: 'planner', status: 'D', size: { h: 22.85, w: 30, uom: 'cm' }, instock: [ { warehouse: 'A', qty: 40}]}"),
    Document.parse("{ item: 'postcard', status: 'A', size: { h: 10, w: 15.25, uom: 'cm' }, "
            + "instock: [ { warehouse: 'B', qty: 15 }, { warehouse: 'C', qty: 35 } ] }")
));
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection), the [com.mongodb.client.MongoCollection.find](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/MongoCollection.html#find--) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```java
FindIterable<Document> findIterable = collection.find(eq("status", "A"));
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

To specify a projection document, chain the [com.mongodb.client.FindIterable.projection](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/FindIterable.html#projection-org.bson.conversions.Bson-) method to the `find` method. The example uses the [com.mongodb.client.model.Projections](http://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Projections.html) class to create the projection documents.

```java
findIterable = collection.find(eq("status", "A")).projection(include("item", "status"));
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

To specify a projection document, chain the [com.mongodb.client.FindIterable.projection](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/FindIterable.html#projection-org.bson.conversions.Bson-) method to the `find` method. The example uses the [com.mongodb.client.model.Projections](http://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Projections.html) class to create the projection documents.

```java
findIterable = collection.find(eq("status", "A"))
        .projection(fields(include("item", "status"), excludeId()));
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

To specify a projection document, chain the [com.mongodb.client.FindIterable.projection](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/FindIterable.html#projection-org.bson.conversions.Bson-) method to the `find` method. The example uses the [com.mongodb.client.model.Projections](http://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Projections.html) class to create the projection documents.

```java
findIterable = collection.find(eq("status", "A")).projection(exclude("item", "status"));
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

To specify a projection document, chain the [com.mongodb.client.FindIterable.projection](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/FindIterable.html#projection-org.bson.conversions.Bson-) method to the `find` method. The example uses the [com.mongodb.client.model.Projections](http://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Projections.html) class to create the projection documents.

```java
findIterable = collection.find(eq("status", "A")).projection(include("item", "status", "size.uom"));
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

To specify a projection document, chain the [com.mongodb.client.FindIterable.projection](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/FindIterable.html#projection-org.bson.conversions.Bson-) method to the `find` method. The example uses the [com.mongodb.client.model.Projections](http://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Projections.html) class to create the projection documents.

```java
findIterable = collection.find(eq("status", "A")).projection(exclude("size.uom"));
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

To specify a projection document, chain the [com.mongodb.client.FindIterable.projection](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/FindIterable.html#projection-org.bson.conversions.Bson-) method to the `find` method. The example uses the [com.mongodb.client.model.Projections](http://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Projections.html) class to create the projection documents.

```java
findIterable = collection.find(eq("status", "A")).projection(include("item", "status", "instock.qty"));
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

To specify a projection document, chain the [com.mongodb.client.FindIterable.projection](https://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/FindIterable.html#projection-org.bson.conversions.Bson-) method to the `find` method. The example uses the [com.mongodb.client.model.Projections](http://mongodb.github.io/mongo-java-driver/3.4/javadoc/com/mongodb/client/model/Projections.html) class to create the projection documents.

```java
findIterable = collection.find(eq("status", "A"))
        .projection(fields(include("item", "status"), slice("instock", -1)));
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `include("instock.0")` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [com.mongodb.reactivestreams.client.MongoCollection.find](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#find()) method in the MongoDB [Java Reactive Streams Driver](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```java
Publisher<Success> insertManyPublisher = collection.insertMany(asList(
    Document.parse("{ item: 'journal', status: 'A', size: { h: 14, w: 21, uom: 'cm' }, instock: [ { warehouse: 'A', qty: 5 }]}"),
    Document.parse("{ item: 'notebook', status: 'A',  size: { h: 8.5, w: 11, uom: 'in' }, instock: [ { warehouse: 'C', qty: 5}]}"),
    Document.parse("{ item: 'paper', status: 'D', size: { h: 8.5, w: 11, uom: 'in' }, instock: [ { warehouse: 'A', qty: 60 }]}"),
    Document.parse("{ item: 'planner', status: 'D', size: { h: 22.85, w: 30, uom: 'cm' }, instock: [ { warehouse: 'A', qty: 40}]}"),
    Document.parse("{ item: 'postcard', status: 'A', size: { h: 10, w: 15.25, uom: 'cm' }, "
            + "instock: [ { warehouse: 'B', qty: 15 }, { warehouse: 'C', qty: 35 } ] }")
));
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection), the [com.mongodb.reactivestreams.client.MongoCollection.find](http://mongodb.github.io/mongo-java-driver-reactivestreams/1.6/javadoc/com/mongodb/reactivestreams/client/MongoCollection.html#find(org.bson.conversions.Bson)) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```java
FindPublisher<Document> findPublisher = collection.find(eq("status", "A"));
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```java
findPublisher = collection.find(eq("status", "A")).projection(include("item", "status"));
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```java
findPublisher = collection.find(eq("status", "A"))
        .projection(fields(include("item", "status"), excludeId()));
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```java
findPublisher = collection.find(eq("status", "A")).projection(exclude("item", "status"));
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```java
findPublisher = collection.find(eq("status", "A")).projection(include("item", "status", "size.uom"));
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```java
findPublisher = collection.find(eq("status", "A")).projection(exclude("size.uom"));
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```java
findPublisher = collection.find(eq("status", "A")).projection(include("item", "status", "instock.qty"));
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```java
findPublisher = collection.find(eq("status", "A"))
        .projection(fields(include("item", "status"), slice("instock", -1)));
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `include("instock.0")` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```kotlin
collection.insertMany(
    listOf(
        Document("item", "journal")
            .append("status", "A")
            .append("size", Document("h", 14).append("w", 21).append("uom", "cm"))
            .append("instock", listOf(
                Document("warehouse", "A").append("qty", 5),
            )),
        Document("item", "notebook")
            .append("status", "A")
            .append("size", Document("h", 8.5).append("w", 11).append("uom", "in"))
            .append("instock", listOf(
                Document("warehouse", "C").append("qty", 5),
            )),
        Document("item", "paper")
            .append("status", "D")
            .append("size", Document("h", 8.5).append("w", 11).append("uom", "in"))
            .append("instock", listOf(
                Document("warehouse", "A").append("qty", 60),
            )),
        Document("item", "planner")
            .append("status", "D")
            .append("size", Document("h", 22.85).append("w", 30).append("uom", "cm"))
            .append("instock", listOf(
                Document("warehouse", "A").append("qty", 40),
            )),
        Document("item", "postcard")
            .append("status", "A")
            .append("size", Document("h", 10).append("w", 15.25).append("uom", "cm"))
            .append("instock", listOf(
                Document("warehouse", "B").append("qty", 15),
                Document("warehouse", "C").append("qty", 35)
            )),
    )
)
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```kotlin
val findFlow = collection
    .find(eq("status", "A"))
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```kotlin
val findFlow = collection
    .find(eq("status", "A")).projection(include("item", "status"))
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```kotlin
val findFlow = collection
    .find(eq("status", "A")).projection(fields(include("item", "status"), excludeId()))
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```kotlin
val findFlow = collection
    .find(eq("status", "A")).projection(exclude("item", "status"))
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```kotlin
val findFlow = collection
    .find(eq("status", "A")).projection(include("item", "status", "size.uom"))
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```kotlin
val findFlow = collection
    .find(eq("status", "A")).projection(exclude("size.uom"))
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```kotlin
val findFlow = collection
    .find(eq("status", "A")).projection(include("item", "status", "instock.qty"))
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```kotlin
val findFlow = collection
    .find(eq("status", "A"))
    .projection(fields(include("item", "status"), slice("instock", -1)))
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `{ "instock.0": 1 }` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [Collection.find()](http://mongodb.github.io/node-mongodb-native/3.6/api/Collection.html#find) method in the [MongoDB Node.js Driver](http://mongodb.github.io/node-mongodb-native/3.6/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```javascript
await db.collection('inventory').insertMany([
  {
    item: 'journal',
    status: 'A',
    size: { h: 14, w: 21, uom: 'cm' },
    instock: [{ warehouse: 'A', qty: 5 }]
  },
  {
    item: 'notebook',
    status: 'A',
    size: { h: 8.5, w: 11, uom: 'in' },
    instock: [{ warehouse: 'C', qty: 5 }]
  },
  {
    item: 'paper',
    status: 'D',
    size: { h: 8.5, w: 11, uom: 'in' },
    instock: [{ warehouse: 'A', qty: 60 }]
  },
  {
    item: 'planner',
    status: 'D',
    size: { h: 22.85, w: 30, uom: 'cm' },
    instock: [{ warehouse: 'A', qty: 40 }]
  },
  {
    item: 'postcard',
    status: 'A',
    size: { h: 10, w: 15.25, uom: 'cm' },
    instock: [
      { warehouse: 'B', qty: 15 },
      { warehouse: 'C', qty: 35 }
    ]
  }
]);
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```javascript
const cursor = db.collection('inventory').find({
  status: 'A'
});
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```javascript
const cursor = db
  .collection('inventory')
  .find({
    status: 'A'
  })
  .project({ item: 1, status: 1 });
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```javascript
const cursor = db
  .collection('inventory')
  .find({
    status: 'A'
  })
  .project({ item: 1, status: 1, _id: 0 });
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```javascript
const cursor = db
  .collection('inventory')
  .find({
    status: 'A'
  })
  .project({ status: 0, instock: 0 });
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```javascript
const cursor = db
  .collection('inventory')
  .find({
    status: 'A'
  })
  .project({ item: 1, status: 1, 'size.uom': 1 });
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```javascript
const cursor = db
  .collection('inventory')
  .find({
    status: 'A'
  })
  .project({ 'size.uom': 0 });
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```javascript
const cursor = db
  .collection('inventory')
  .find({
    status: 'A'
  })
  .project({ item: 1, status: 1, 'instock.qty': 1 });
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```javascript
const cursor = db
  .collection('inventory')
  .find({
    status: 'A'
  })
  .project({ item: 1, status: 1, instock: { $slice: -1 } });
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `{ "instock.0": 1 }` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [`MongoDB\\Collection::find()`](https://www.mongodb.com/docs/php-library/upcoming/reference/method/MongoDBCollection-find/#mongodb-phpmethod-phpmethod.MongoDB-Collection--find--) method in the [MongoDB PHP Library](https://www.mongodb.com/docs/drivers/php-libraries/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```php
$insertManyResult = $db->inventory->insertMany([
    [
        'item' => 'journal',
        'status' => 'A',
        'size' => ['h' => 14, 'w' => 21, 'uom' => 'cm'],
        'instock' => [
            ['warehouse' => 'A', 'qty' => 5],
        ],
    ],
    [
        'item' => 'notebook',
        'status' => 'A',
        'size' => ['h' => 8.5, 'w' => 11, 'uom' => 'in'],
        'instock' => [
            ['warehouse' => 'C', 'qty' => 5],
        ],
    ],
    [
        'item' => 'paper',
        'status' => 'D',
        'size' => ['h' => 8.5, 'w' => 11, 'uom' => 'in'],
        'instock' => [
            ['warehouse' => 'A', 'qty' => 60],
        ],
    ],
    [
        'item' => 'planner',
        'status' => 'D',
        'size' => ['h' => 22.85, 'w' => 30, 'uom' => 'cm'],
        'instock' => [
            ['warehouse' => 'A', 'qty' => 40],
        ],
    ],
    [
        'item' => 'postcard',
        'status' => 'A',
        'size' => ['h' => 10, 'w' => 15.25, 'uom' => 'cm'],
        'instock' => [
            ['warehouse' => 'B', 'qty' => 15],
            ['warehouse' => 'C', 'qty' => 35],
        ],
    ],
]);
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```php
$cursor = $db->inventory->find(['status' => 'A']);
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```php
$cursor = $db->inventory->find(
    ['status' => 'A'],
    ['projection' => ['item' => 1, 'status' => 1]],
);
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```php
$cursor = $db->inventory->find(
    ['status' => 'A'],
    ['projection' => ['item' => 1, 'status' => 1, '_id' => 0]],
);
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```php
$cursor = $db->inventory->find(
    ['status' => 'A'],
    ['projection' => ['status' => 0, 'instock' => 0]],
);
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```php
$cursor = $db->inventory->find(
    ['status' => 'A'],
    ['projection' => ['item' => 1, 'status' => 1, 'size.uom' => 1]],
);
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```php
$cursor = $db->inventory->find(
    ['status' => 'A'],
    ['projection' => ['size.uom' => 0]],
);
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```php
$cursor = $db->inventory->find(
    ['status' => 'A'],
    ['projection' => ['item' => 1, 'status' => 1, 'instock.qty' => 1]],
);
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```php
$cursor = $db->inventory->find(
    ['status' => 'A'],
    ['projection' => ['item' => 1, 'status' => 1, 'instock' => ['$slice' => -1]]],
);
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `{ "instock.0": 1 }` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [Mongo::Collection#find()](https://www.mongodb.com/docs/ruby-driver/current/api/Mongo/Collection.html#find-instance_method) method in the [MongoDB Ruby Driver](https://www.mongodb.com/docs/ruby-driver/current/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```ruby
client[:inventory].insert_many([ { item: 'journal',
                                   status: 'A',
                                   size: { h: 14, w: 21, uom: 'cm' },
                                   instock: [ { warehouse: 'A', qty: 5 } ] },
                                 { item: 'notebook',
                                   status: 'A',
                                   size: { h: 8.5, w: 11, uom: 'in' },
                                   instock: [ { warehouse: 'C', qty: 5 } ] },
                                 { item: 'paper',
                                   status: 'D',
                                   size: { h: 8.5, w: 11, uom: 'in' },
                                   instock: [ { warehouse: 'A', qty: 60 } ] },
                                 { item: 'planner',
                                   status: 'D',
                                   size: { h: 22.85, w: 30, uom: 'cm' },
                                   instock: [ { warehouse: 'A', qty: 40 } ] },
                                 { item: 'postcard',
                                   status: 'A',
                                   size: { h: 10, w: 15.25, uom: 'cm' },
                                   instock: [ { warehouse: 'B', qty: 15 },
                                              { warehouse: 'C', qty: 35 } ] } ])
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```ruby
client[:inventory].find(status: 'A')
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```ruby
client[:inventory].find({ status: 'A' },
                        projection: { item: 1, status: 1 })
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```ruby
client[:inventory].find({ status: 'A' },
                        projection: { item: 1, status: 1, _id: 0 })
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```ruby
client[:inventory].find({ status: 'A' },
                        projection: { status: 0, instock: 0 })
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```ruby
client[:inventory].find({ status: 'A' },
                        projection: { 'item' => 1, 'status' => 1, 'size.uom' => 1 })
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```ruby
client[:inventory].find({ status: 'A' },
                        projection: { 'size.uom' => 0 })
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```ruby
client[:inventory].find({ status: 'A' },
                        projection: { 'item' => 1, 'status' => 1, 'instock.qty' => 1 })
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```ruby
client[:inventory].find({ status: 'A' },
                        projection: { 'item' => 1,
                                      'status' => 1,
                                      'instock' => { '$slice' => -1 } })
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `{ "instock.0" => 1 }` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [collection.find()](http://mongodb.github.io/mongo-scala-driver/2.9/scaladoc/org/mongodb/scala/MongoCollection.html#find[C](filter:org.mongodb.scala.bson.conversions.Bson)(implicite:org.mongodb.scala.bson.DefaultHelper.DefaultsTo[C,TResult],implicitct:scala.reflect.ClassTag[C]):org.mongodb.scala.FindObservable[C]) method in the [MongoDB Scala Driver](http://mongodb.github.io/mongo-scala-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```scala
collection.insertMany(Seq(
  Document("""{ item: "journal", status: "A", size: { h: 14, w: 21, uom: "cm" }, instock: [ { warehouse: "A", qty: 5 } ] }"""),
  Document("""{ item: "notebook", status: "A",  size: { h: 8.5, w: 11, uom: "in" }, instock: [ { warehouse: "C", qty: 5 } ] }"""),
  Document("""{ item: "paper", status: "D", size: { h: 8.5, w: 11, uom: "in" }, instock: [ { warehouse: "A", qty: 60 } ] }"""),
  Document("""{ item: "planner", status: "D", size: { h: 22.85, w: 30, uom: "cm" }, instock: [ { warehouse: "A", qty: 40 } ] }"""),
  Document("""{ item: "postcard", status: "A", size: { h: 10, w: 15.25, uom: "cm" },
                instock: [ { warehouse: "B", qty: 15 }, { warehouse: "C", qty: 35 } ] }""")

)).execute()
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```scala
var findObservable = collection.find(equal("status", "A"))
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```scala
findObservable = collection.find(equal("status", "A")).projection(include("item", "status"))
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```scala
findObservable = collection.find(equal("status", "A"))
  .projection(fields(include("item", "status"), excludeId()))
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```scala
findObservable = collection.find(equal("status", "A")).projection(exclude("item", "status"))
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```scala
findObservable = collection.find(equal("status", "A")).projection(include("item", "status", "size.uom"))
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```scala
findObservable = collection.find(equal("status", "A")).projection(exclude("size.uom"))
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```scala
findObservable = collection.find(equal("status", "A")).projection(include("item", "status", "instock.qty"))
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```scala
findObservable = collection.find(equal("status", "A"))
  .projection(fields(include("item", "status"), slice("instock", -1)))
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array. For instance, you *cannot* project specific array elements using the array index; e.g. `include("instock.0")` projection does *not* project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [MongoCollection.Find()](https://mongodb.github.io/mongo-csharp-driver/2.10/apidocs/html/M_MongoDB_Driver_MongoCollection_1_Find.htm) method in the [MongoDB C# Driver](https://mongodb.github.io/mongo-csharp-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```csharp
var documents = new[]
{
    new BsonDocument
    {
        { "item", "journal" },
        { "status", "A" },
        { "size", new BsonDocument { { "h", 14 }, { "w", 21 }, { "uom", "cm" } } },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "A" }, { "qty", 5 } } }
            }
    },
    new BsonDocument
    {
        { "item", "notebook" },
        { "status", "A" },
        { "size", new BsonDocument { { "h", 8.5 }, { "w", 11 }, { "uom", "in" } } },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "C" }, { "qty", 5 } } }
            }
    },
    new BsonDocument
    {
        { "item", "paper" },
        { "status", "D" },
        { "size", new BsonDocument { { "h", 8.5 }, { "w", 11 }, { "uom", "in" } } },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "A" }, { "qty", 60 } } }
            }
    },
    new BsonDocument
    {
        { "item", "planner" },
        { "status", "D" },
        { "size", new BsonDocument { { "h", 22.85 }, { "w", 30 }, { "uom", "cm" } } },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "A" }, { "qty", 40 } } }
            }
    },
    new BsonDocument
    {
        { "item", "postcard" },
        { "status", "A" },
        { "size", new BsonDocument { { "h", 10 }, { "w", 15.25 }, { "uom", "cm" } } },
        { "instock", new BsonArray
            {
                new BsonDocument { { "warehouse", "B" }, { "qty", 15 } },
                new BsonDocument { { "warehouse", "C" }, { "qty", 35 } } }
            }
    }
};
collection.InsertMany(documents);
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var result = collection.Find(filter).ToList();
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var projection = Builders<BsonDocument>.Projection.Include("item").Include("status");
var result = collection.Find<BsonDocument>(filter).Project(projection).ToList();
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var projection = Builders<BsonDocument>.Projection.Include("item").Include("status").Exclude("_id");
var result = collection.Find<BsonDocument>(filter).Project(projection).ToList();
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var projection = Builders<BsonDocument>.Projection.Exclude("status").Exclude("instock");
var result = collection.Find<BsonDocument>(filter).Project(projection).ToList();
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var projection = Builders<BsonDocument>.Projection.Include("item").Include("status").Include("size.uom");
var result = collection.Find<BsonDocument>(filter).Project(projection).ToList();
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var projection = Builders<BsonDocument>.Projection.Exclude("size.uom");
var result = collection.Find<BsonDocument>(filter).Project(projection).ToList();
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var projection = Builders<BsonDocument>.Projection.Include("item").Include("status").Include("instock.qty");
var result = collection.Find<BsonDocument>(filter).Project(projection).ToList();
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```csharp
var filter = Builders<BsonDocument>.Filter.Eq("status", "A");
var projection = Builders<BsonDocument>.Projection.Include("item").Include("status").Slice("instock", -1);
var result = collection.Find<BsonDocument>(filter).Project(projection).ToList();
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the *only* operators that you can use to project specific elements to include in the returned array.

For example, the following operation will not project the array with the first element:

```c#
Builders<BsonDocument>.Projection.Include("instock.0")
```

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using [mongoc_collection_find_with_opts](https://mongoc.org/libmongoc/current/mongoc_collection_find_with_opts.html).

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
   "status", BCON_UTF8 ("A"),
   "size", "{",
   "h", BCON_DOUBLE (14),
   "w", BCON_DOUBLE (21),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("A"),
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
   "item", BCON_UTF8 ("notebook"),
   "status", BCON_UTF8 ("A"),
   "size", "{",
   "h", BCON_DOUBLE (8.5),
   "w", BCON_DOUBLE (11),
   "uom", BCON_UTF8 ("in"),
   "}",
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
   "status", BCON_UTF8 ("D"),
   "size", "{",
   "h", BCON_DOUBLE (8.5),
   "w", BCON_DOUBLE (11),
   "uom", BCON_UTF8 ("in"),
   "}",
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("A"),
   "qty", BCON_INT64 (60),
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
   "status", BCON_UTF8 ("D"),
   "size", "{",
   "h", BCON_DOUBLE (22.85),
   "w", BCON_DOUBLE (30),
   "uom", BCON_UTF8 ("cm"),
   "}",
   "instock", "[",
   "{",
   "warehouse", BCON_UTF8 ("A"),
   "qty", BCON_INT64 (40),
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
   "status", BCON_UTF8 ("A"),
   "size", "{",
   "h", BCON_DOUBLE (10),
   "w", BCON_DOUBLE (15.25),
   "uom", BCON_UTF8 ("cm"),
   "}",
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

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```c
mongoc_collection_t *collection;
bson_t *filter;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("A"));
cursor = mongoc_collection_find_with_opts (collection, filter, NULL, NULL);
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```c
mongoc_collection_t *collection;
bson_t *filter;
bson_t *opts;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("A"));
opts = BCON_NEW ("projection", "{", "item", BCON_INT64 (1),
"status", BCON_INT64 (1), "}");
cursor = mongoc_collection_find_with_opts (collection, filter, opts, NULL);
```

Clean up any open resources by calling the following methods, as appropriate:

- [bson_destroy](http://mongoc.org/libbson/current/bson_destroy.html)

- [mongoc_bulk_operation_destroy](https://mongoc.org/libmongoc/current/mongoc_bulk_operation_destroy.html)

- [mongoc_collection_destroy](https://mongoc.org/libmongoc/current/mongoc_collection_destroy)

- [mongoc_cursor_destroy](https://mongoc.org/libmongoc/current/mongoc_cursor_destroy.html),

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```c
mongoc_collection_t *collection;
bson_t *filter;
bson_t *opts;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("A"));
opts = BCON_NEW ("projection", "{", "item", BCON_INT64 (1),
"status", BCON_INT64 (1),
"_id", BCON_INT64 (0), "}");
cursor = mongoc_collection_find_with_opts (collection, filter, opts, NULL);
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```c
mongoc_collection_t *collection;
bson_t *filter;
bson_t *opts;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("A"));
opts = BCON_NEW ("projection", "{", "status", BCON_INT64 (0),
"instock", BCON_INT64 (0), "}");
cursor = mongoc_collection_find_with_opts (collection, filter, opts, NULL);
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```c
mongoc_collection_t *collection;
bson_t *filter;
bson_t *opts;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("A"));
opts = BCON_NEW ("projection", "{", "item", BCON_INT64 (1),
"status", BCON_INT64 (1),
"size.uom", BCON_INT64 (1), "}");
cursor = mongoc_collection_find_with_opts (collection, filter, opts, NULL);
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```c
mongoc_collection_t *collection;
bson_t *filter;
bson_t *opts;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("A"));
opts = BCON_NEW ("projection", "{", "size.uom", BCON_INT64 (0), "}");
cursor = mongoc_collection_find_with_opts (collection, filter, opts, NULL);
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```c
mongoc_collection_t *collection;
bson_t *filter;
bson_t *opts;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("A"));
opts = BCON_NEW ("projection", "{", "item", BCON_INT64 (1),
"status", BCON_INT64 (1),
"instock.qty", BCON_INT64 (1), "}");
cursor = mongoc_collection_find_with_opts (collection, filter, opts, NULL);
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```c
mongoc_collection_t *collection;
bson_t *filter;
bson_t *opts;
mongoc_cursor_t *cursor;

collection = mongoc_database_get_collection (db, "inventory");
filter = BCON_NEW ("status", BCON_UTF8 ("A"));
opts = BCON_NEW ("projection", "{", "item", BCON_INT64 (1),
"status", BCON_INT64 (1),
"instock", "{",
"$slice", BCON_INT64 (-1),
"}", "}");
cursor = mongoc_collection_find_with_opts (collection, filter, opts, NULL);
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the only operators that you can use to project specific elements to include in the returned array. For instance, you cannot project specific array elements using the array index; e.g. `{ "instock.0": 1 }` projection does not project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [Collection.Find](https://godoc.org/github.com/mongodb/mongo-go-driver/mongo#Collection.Find) function in the [MongoDB Go Driver](https://github.com/mongodb/mongo-go-driver/).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```javascript

```

```go

docs := []any{
	bson.D{
		{"item", "journal"},
		{"status", "A"},
		{"size", bson.D{
			{"h", 14},
			{"w", 21},
			{"uom", "cm"},
		}},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "A"},
				{"qty", 5},
			},
		}},
	},
	bson.D{
		{"item", "notebook"},
		{"status", "A"},
		{"size", bson.D{
			{"h", 8.5},
			{"w", 11},
			{"uom", "in"},
		}},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "EC"},
				{"qty", 5},
			},
		}},
	},
	bson.D{
		{"item", "paper"},
		{"status", "D"},
		{"size", bson.D{
			{"h", 8.5},
			{"w", 11},
			{"uom", "in"},
		}},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "A"},
				{"qty", 60},
			},
		}},
	},
	bson.D{
		{"item", "planner"},
		{"status", "D"},
		{"size", bson.D{
			{"h", 22.85},
			{"w", 30},
			{"uom", "cm"},
		}},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "A"},
				{"qty", 40},
			},
		}},
	},
	bson.D{
		{"item", "postcard"},
		{"status", "A"},
		{"size", bson.D{
			{"h", 10},
			{"w", 15.25},
			{"uom", "cm"},
		}},
		{"instock", bson.A{
			bson.D{
				{"warehouse", "B"},
				{"qty", 15},
			},
			bson.D{
				{"warehouse", "EC"},
				{"qty", 35},
			},
		}},
	},
}

result, err := coll.InsertMany(context.TODO(), docs)

```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```go

cursor, err := coll.Find(
	context.TODO(),
	bson.D{{"status", "A"}},
)

```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```go

projection := bson.D{
	{"item", 1},
	{"status", 1},
}

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
	},
	options.Find().SetProjection(projection),
)

```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```go

projection := bson.D{
	{"item", 1},
	{"status", 1},
	{"_id", 0},
}

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
	},
	options.Find().SetProjection(projection),
)

```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```go

projection := bson.D{
	{"status", 0},
	{"instock", 0},
}

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
	},
	options.Find().SetProjection(projection),
)

```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```go

projection := bson.D{
	{"item", 1},
	{"status", 1},
	{"size.uom", 1},
}

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
	},
	options.Find().SetProjection(projection),
)

```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```go

projection := bson.D{
	{"size.uom", 0},
}

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
	},
	options.Find().SetProjection(projection),
)

```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```go

projection := bson.D{
	{"item", 1},
	{"status", 1},
	{"instock.qty", 1},
}

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
	},
	options.Find().SetProjection(projection),
)

```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```go

projection := bson.D{
	{"item", 1},
	{"status", 1},
	{"instock", bson.D{
		{"$slice", -1},
	}},
}

cursor, err := coll.Find(
	context.TODO(),
	bson.D{
		{"status", "A"},
	},
	options.Find().SetProjection(projection),
)

```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the only operators that you can use to project specific elements to include in the returned array. For instance, you cannot project specific array elements using the array index; e.g. `{ "instock.0": 1 }` projection does not project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using the [`motor.motor_asyncio.AsyncIOMotorCollection.find`](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.find) method in the [Motor](https://motor.readthedocs.io/en/stable/) driver.

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```python
await db.inventory.insert_many(
    [
        {
            "item": "journal",
            "status": "A",
            "size": {"h": 14, "w": 21, "uom": "cm"},
            "instock": [{"warehouse": "A", "qty": 5}],
        },
        {
            "item": "notebook",
            "status": "A",
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "instock": [{"warehouse": "C", "qty": 5}],
        },
        {
            "item": "paper",
            "status": "D",
            "size": {"h": 8.5, "w": 11, "uom": "in"},
            "instock": [{"warehouse": "A", "qty": 60}],
        },
        {
            "item": "planner",
            "status": "D",
            "size": {"h": 22.85, "w": 30, "uom": "cm"},
            "instock": [{"warehouse": "A", "qty": 40}],
        },
        {
            "item": "postcard",
            "status": "A",
            "size": {"h": 10, "w": 15.25, "uom": "cm"},
            "instock": [{"warehouse": "B", "qty": 15}, {"warehouse": "C", "qty": 35}],
        },
    ]
)
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

```python
cursor = db.inventory.find({"status": "A"})
```

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

```python
cursor = db.inventory.find({"status": "A"}, {"item": 1, "status": 1})
```

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

```python
cursor = db.inventory.find({"status": "A"}, {"item": 1, "status": 1, "_id": 0})
```

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

```python
cursor = db.inventory.find({"status": "A"}, {"status": 0, "instock": 0})
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

```python
cursor = db.inventory.find({"status": "A"}, {"item": 1, "status": 1, "size.uom": 1})
```

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

```python
cursor = db.inventory.find({"status": "A"}, {"size.uom": 0})
```

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

```python
cursor = db.inventory.find({"status": "A"}, {"item": 1, "status": 1, "instock.qty": 1})
```

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

```python
cursor = db.inventory.find(
    {"status": "A"}, {"item": 1, "status": 1, "instock": {"$slice": -1}}
)
```

[`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-) are the only operators that you can use to project specific elements to include in the returned array. For instance, you cannot project specific array elements using the array index; e.g. `{ "instock.0": 1 }` projection does not project the array with the first element.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

query operations with projectionThis page provides examples of query operations with projection using [MongoDB Compass](https://www.mongodb.com/docs/compass/current/#std-label-compass-index).

The examples on this page use the `inventory` collection. Connect to a test database in your MongoDB instance then create the `inventory` collection:

```javascript
[
      { "item": "journal", "status": "A", "size": { "h": 14, "w": 21, "uom": "cm" }, "instock": [ { "warehouse": "A", "qty": 5 } ] },
      { "item": "notebook", "status": "A", "size": { "h": 8.5, "w": 11, "uom": "in" }, "instock": [ { "warehouse": "C", "qty": 5 } ] },
      { "item": "paper", "status": "D", "size": { "h": 8.5, "w": 11, "uom": "in" }, "instock": [ { "warehouse": "A", "qty": 60 } ] },
      { "item": "planner", "status": "D", "size": { "h": 22.85, "w": 30, "uom": "cm" }, "instock": [ { "warehouse": "A", "qty": 40 } ] },
      { "item": "postcard", "status": "A", "size": { "h": 10, "w": 15.25, "uom": "cm" }, "instock": [ { "warehouse": "B", "qty": 15 }, { "warehouse": "C", "qty": 35 } ] }
]
```

## Return All Fields in Matching Documents

If you do not specify a [projection](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) document, the [`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find) method returns all fields in the matching documents.

The following example returns all fields from all documents in the `inventory` collection where the `status` equals `"A"`:

1. Copy the following expression into the Filter field:

   ```javascript
   { status: "A" }
   ```

2. Click Find.

The operation corresponds to the following SQL statement:

```sql
SELECT * from inventory WHERE status = "A"
```

## Return the Specified Fields and the `_id` Field Only

A projection can explicitly include several fields by setting the `<field>` to `1` in the projection document. The following operation returns all documents that match the query. In the result set, only the `item`, `status` and, by default, the `_id` fields return in the matching documents.

1. Copy the following expression into the Filter field:

   ```javascript
   { status: "A" }
   ```

2. Click Options to open the additional query options.

3. Copy the following expression into the Project field:

   ```javascript
   { item: 1, status: 1 }
   ```

4. Click Find.

The operation corresponds to the following SQL statement:

```sql
SELECT _id, item, status from inventory WHERE status = "A"
```

## Suppress `_id` Field

You can remove the `_id` field from the results by setting it to `0` in the projection, as in the following example:

1. Copy the following expression into the Filter field:

   ```javascript
   { status: "A" }
   ```

2. Click Options to open the additional query options.

3. Copy the following expression into the Project field:

   ```javascript
   { item: 1, status: 1, _id: 0 }
   ```

4. Click Find.

The operation corresponds to the following SQL statement:

```sql
SELECT item, status from inventory WHERE status = "A"
```

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return All But the Excluded Fields

Instead of listing the fields to return in the matching document, you can use a projection to exclude specific fields. The following example which returns all fields except for the `status` and the `instock` fields in the matching documents:

1. Copy the following expression into the Filter field:

   ```javascript
   { status: "A" }
   ```

2. Click Options to open the additional query options.

3. Copy the following expression into the Project field:

   ```javascript
   { status: 0, instock: 0 }
   ```

4. Click Find.

With the exception of the `_id` field, you cannot combine inclusion and exclusion statements in projection documents.

## Return Specific Fields in Embedded Documents

You can return specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field and set to `1` in the projection document.

The following example returns:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `uom` field in the `size` document.

The `uom` field remains embedded in the `size` document.

1. Copy the following expression into the Filter field:

   ```javascript
   { status: "A" }
   ```

2. Click Options to open the additional query options.

3. Copy the following expression into the Project field:

   ```javascript
   { item: 1, status: 1, "size.uom": 1 }
   ```

4. Click Find.

You can also specify embedded fields using the nested form. For example, `{ item: 1, status: 1, size: { uom: 1 } }`.

## Suppress Specific Fields in Embedded Documents

You can suppress specific fields in an embedded document. Use the [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to refer to the embedded field in the projection document and set to `0`.

The following example specifies a projection to exclude the `uom` field inside the `size` document. All other fields are returned in the matching documents:

1. Copy the following expression into the Filter field:

   ```javascript
   { status: "A" }
   ```

2. Click Options to open the additional query options.

3. Copy the following expression into the Project field:

   ```javascript
   { "size.uom": 0 }
   ```

4. Click Find.

You can also specify embedded fields using the nested form. For example, `{ size: { uom: 0 } }`.

## Projection on Embedded Documents in an Array

Use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation) to project specific fields inside documents embedded in an array.

The following example specifies a projection to return:

- The `_id` field (returned by default),

- The `item` field,

- The `status` field,

- The `qty` field in the documents embedded in the `instock` array.

1. Copy the following expression into the Filter field:

   ```javascript
   { status: "A" }
   ```

2. Click Options to open the additional query options.

3. Copy the following expression into the Project field:

   ```javascript
   { item: 1, status: 1, "instock.qty": 1 }
   ```

4. Click Find.

## Project Specific Array Elements in the Returned Array

For fields that contain arrays, MongoDB provides the following projection operators for manipulating arrays: [`$elemMatch`](https://www.mongodb.com/docs/reference/operator/projection/elemMatch/#mongodb-projection-proj.-elemMatch), [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice), and [`$`](https://www.mongodb.com/docs/reference/operator/projection/positional/#mongodb-projection-proj.-).

The following example uses the [`$slice`](https://www.mongodb.com/docs/reference/operator/projection/slice/#mongodb-projection-proj.-slice) projection operator to return the last element in the `instock` array:

1. Copy the following expression into the Filter field:

   ```javascript
   { status: "A" }
   ```

2. Click Options to open the additional query options.

3. Copy the following expression into the Project field:

   ```javascript
   { item: 1, status: 1, instock: { $slice: -1 } }
   ```

4. Click Find.

## Project Fields with Aggregation Expressions

You can specify [aggregation expressions](https://www.mongodb.com/docs/reference/mql/expressions/#std-label-aggregation-expressions) in a query projection. Aggregation expressions let you project new fields and modify the values of existing fields.

For example, the following operation uses aggregation expressions to override the value of the `status` field, and project new fields `area` and `reportNumber`.

The following example uses MongoDB Shell syntax. For driver examples of projection with aggregation, see your [driver documentation](https://www.mongodb.com/docs/drivers/).

```javascript
db.inventory.find(
   { },
   {
      _id: 0,
      item: 1,
      status: {
         $switch: {
            branches: [
               {
                  case: { $eq: [ "$status", "A" ] },
                  then: "Available"
               },
               {
                  case: { $eq: [ "$status", "D" ] },
                  then: "Discontinued"
               },
            ],
            default: "No status found"
         }
      },
      area: {
         $concat: [
            { $toString: { $multiply: [ "$size.h", "$size.w" ] } },
            " ",
            "$size.uom"
         ]
      },
      reportNumber: { $literal: 1 }
   }
)
```

```javascript
[
   {
      item: 'journal',
      status: 'Available',
      area: '294 cm',
      reportNumber: 1
   },
   {
      item: 'planner',
      status: 'Discontinued',
      area: '685.5 cm',
      reportNumber: 1
   },
   {
      item: 'notebook',
      status: 'Available',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'paper',
      status: 'Discontinued',
      area: '93.5 in',
      reportNumber: 1
   },
   {
      item: 'postcard',
      status: 'Available',
      area: '152.5 cm',
      reportNumber: 1
   }
]
```

## Project Fields to Return from a Query with MongoDB Atlas

This example uses the [sample movies dataset](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/). To load the sample dataset into your MongoDB Atlas deployment, see [Load Sample Data](https://www.mongodb.com/docs/atlas/sample-data/#std-label-load-sample-data).

To project fields to return from a query in MongoDB Atlas, follow these steps:

### In the MongoDB Atlas UI, go to the Clusters page for your project.

- If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Clusters under the Database heading.

  The [Clusters](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fclusters) page displays.

### Navigate to the collection

- For the cluster that contains the sample data, click Browse Collections.

- In the left navigation pane, select the `sample_mflix` database.

- Select the `movies` collection.

### Specify the Filter field

- Click More Options on the right side of the Filter field.

- Specify the query filter.

  Specify the [query filter document](https://www.mongodb.com/docs/core/document/#std-label-document-query-filter) in the Filter field. A query filter document uses [query operators](https://www.mongodb.com/docs/core/csfle/reference/supported-operations/#std-label-csfle-supported-query-operators) to specify search conditions.

  Copy the following query filter document into the Filter search bar:

  ```javascript
  { year: 1924 }
  ```

### Specify the fields to project

Specify the fields to return in the query results.

Copy the following project document into the Project bar:

```javascript
{ title: 1, plot: 1 }
```

### Click Apply

This query filter returns the following fields for all documents in the `sample_mflix.movies` collection where the `year` field matches `1924`:

- `_id`

- `title`

- `plot`

MongoDB Atlas returns the `_id` field by default. To omit the `_id` field, copy the following project document into the Project bar and click Apply:

```javascript
{ title: 1, plot: 1, _id: 0 }
```

## Additional Considerations

- [`$project`](https://www.mongodb.com/docs/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project) aggregationWhen you use a [`$project`](https://www.mongodb.com/docs/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project) aggregation stage it should typically be the last stage in your pipeline, used to specify which fields to return to the client.

  Using a `$project` stage at the beginning or middle of a pipeline to reduce the number of fields passed to subsequent pipeline stages is unlikely to improve performance, because the database performs this optimization automatically.

- MongoDB enforces additional restrictions with regards to projections. See [Projection Restrictions](https://www.mongodb.com/docs/reference/limits/#mongodb-limit-Projection-Restrictions) for details.

- [Projection](https://www.mongodb.com/docs/reference/method/db.collection.find/#std-label-find-projection)

- [Query Documents](https://www.mongodb.com/docs/tutorial/query-documents/)
