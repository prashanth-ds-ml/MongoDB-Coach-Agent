> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/indexes/
> Fetch method: direct_markdown

# Indexes

## Overview

In this guide, you can learn how to use **indexes** with PyMongo. Indexes can improve the efficiency of queries and add additional functionality to querying and storing documents.

Without indexes, MongoDB must scan every document in a collection to find the documents that match each query. These collection scans are slow and can negatively affect the performance of your application. However, if an appropriate index exists for a query, MongoDB can use the index to limit the documents it must inspect.

### Operational Considerations

To improve query performance, build indexes on fields that appear often in your application's queries and operations that return sorted results. Each index that you add consumes disk space and memory when active, so we recommend that you track index memory and disk usage for capacity planning. In addition, when a write operation updates an indexed field, MongoDB updates the related index.

Because MongoDB supports dynamic schemas, applications can query against fields whose names are not known in advance or are arbitrary. [Wildcard indexes](https://www.mongodb.com/docs/manual/core/index-wildcard/) help support these queries. Wildcard indexes are not designed to replace workload-based index planning.

For more information about designing your data model and choosing indexes appropriate for your application, see the [Data Modeling and Indexes](https://www.mongodb.com/docs/manual/core/data-model-operations/#indexes) guide in the MongoDB Server manual.

### Sample Data

The examples in this guide use the `sample_mflix.movies` collection from the [Atlas sample datasets](https://www.mongodb.com/docs/atlas/sample-data/). To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see the [Get Started with PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/get-started/#std-label-pymongo-get-started).

## Index Types

### Single Field and Compound Indexes

#### Single Field Indexes

[Single field indexes](https://www.mongodb.com/docs/manual/core/index-single/) are indexes with a reference to a single field within a collection's documents. They improve single field query and sort performance, and support [TTL Indexes](https://www.mongodb.com/docs/manual/core/index-ttl/) that automatically remove documents from a collection after a certain amount of time or at a specific clock time.

The `_id_` index is an example of a single field index. This index is automatically created on the `_id` field when a new collection is created.

The following example creates an index in ascending order on the `title` field. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
movies.create_index("title")
```

</Tab>

<Tab name="Asynchronous">

```python
await movies.create_index("title")
```

</Tab>

</Tabs>

The following is an example of a query that is covered by the index created in the preceding code example:

```python
query = { "title": "Batman" }
sort = [("title", 1)]

cursor = movies.find(query).sort(sort)
```

To learn more, see [Single Field Indexes](https://www.mongodb.com/docs/manual/core/index-single/) in the MongoDB Server manual.

#### Compound Indexes

[Compound indexes](https://www.mongodb.com/docs/manual/core/index-compound/) hold references to multiple fields within a collection's documents, improving query and sort performance.

The following example creates a compound index on the `type` and `genre` fields. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
movies.create_index([("type", pymongo.ASCENDING), ("genre", pymongo.ASCENDING)])
```

</Tab>

<Tab name="Asynchronous">

```python
await movies.create_index([("type", pymongo.ASCENDING), ("genre", pymongo.ASCENDING)])
```

</Tab>

</Tabs>

The following is an example of a query that uses the index created in the preceding code example:

```python
query = { "type": "movie", "genre": "Drama" }
sort = [("type", pymongo.ASCENDING), ("genre", pymongo.ASCENDING)]

cursor = movies.find(query).sort(sort)
```

For more information, see [Compound Indexes](https://www.mongodb.com/docs/manual/core/index-compound/) in the MongoDB Server manual.

### Multikey Indexes (Indexes on Array Fields)

**Multikey indexes** are indexes that improve performance for queries that specify a field with an index that contains an array value. You can define a multikey index by using the same syntax as a single field or compound index. Select the Synchronous or Asynchronous tab to see the corresponding code:

The following example creates a multikey index on the `cast` field. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
result = movies.create_index("cast")
```

</Tab>

<Tab name="Asynchronous">

```python
result = await movies.create_index("cast")
```

</Tab>

</Tabs>

The following is an example of a query that uses the index created in the preceding code example:

```python
query = { "cast": "Viola Davis" }

cursor = movies.find(query)
```

Multikey indexes behave differently from other indexes in terms of query coverage, index- bound computation, and sort behavior. To learn more about multikey indexes, including a discussion of their behavior and limitations, see the [Multikey Indexes](https://www.mongodb.com/docs/manual/core/index-multikey/) guide in the MongoDB Server manual.

### MongoDB Search and Vector Search Indexes

You can manage your [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) and [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/) indexes by using PyMongo. The indexes specify the behavior of the search and which fields to index.

MongoDB Search enables you to perform full-text searches on collections hosted on MongoDB Atlas. MongoDB Search indexes specify the behavior of the search and which fields to index.

MongoDB Vector Search enables you to perform semantic searches on vector embeddings stored in MongoDB Atlas. Vector Search indexes define the indexes for the vector embeddings that you want to query and the boolean, date, objectId, numeric, string, or UUID values that you want to use to pre-filter your data.

You can call the following methods on a collection to manage your MongoDB Search and Vector Search indexes:

- `create_search_index()`

- `create_search_indexes()`

- `list_search_indexes()`

- `update_search_index()`

- `drop_search_index()`

The MongoDB Search Index management methods run asynchronously. The driver methods can return before confirming that they ran successfully. To determine the current status of the indexes, call the `list_search_indexes()` method.

The following sections provide code examples that demonstrate how to use each of the preceding methods.

#### Create a Search Index

You can use the [create_search_index()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.create_search_index) and the [create_search_indexes()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.create_search_indexes) methods to create MongoDB Search indexes or MongoDB Vector Search indexes.

The following code example shows how to create a single MongoDB Search index. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
index = {
    "definition": {
        "mappings": {
            "dynamic": True
        }
    },
    "name": "<index name>",
}

collection.create_search_index(index)
```

</Tab>

<Tab name="Asynchronous">

```python
index = {
    "definition": {
        "mappings": {
            "dynamic": True
        }
    },
    "name": "<index name>",
}

await collection.create_search_index(index)
```

</Tab>

</Tabs>

The following code example shows how to create a single MongoDB Vector Search index by using the [SearchIndexModel](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/operations.html#pymongo.operations.SearchIndexModel) object. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python

from pymongo.operations import SearchIndexModel

search_index_model = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "numDimensions": <number of dimensions>,
        "path": "<field to index>",
        "similarity":  "<select from euclidean, cosine, dotProduct>"
      }
    ]
  },
  name="<index name>",
  type="vectorSearch",
)

collection.create_search_index(model=search_index_model)

```

</Tab>

<Tab name="Asynchronous">

```python
from pymongo.operations import SearchIndexModel

search_index_model = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "numDimensions": <number of dimensions>,
        "path": "<field to index>",
        "similarity":  "<select from euclidean, cosine, dotProduct>"
      }
    ]
  },
  name="<index name>",
  type="vectorSearch",
)

await collection.create_search_index(model=search_index_model)
```

</Tab>

</Tabs>

You can use the [create_search_indexes()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.create_search_indexes) method to create multiple indexes. These indexes can be MongoDB Search or Vector Search indexes. The `create_search_indexes()` method takes a list of `SearchIndexModel` objects that correspond to each index you want to create.

The following code example shows how to create a MongoDB Search index and an Atlas Vector Search index. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python

search_idx = SearchIndexModel(
    definition ={
        "mappings": {
            "dynamic": True
        }
    },
    name="my_index",
)

vector_idx = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "numDimensions": <number of dimensions>,
        "path": "<field to index>",
        "similarity": "<select from euclidean, cosine, dotProduct>"
      }
    ]
  },
  name="my_vector_index",
  type="vectorSearch",
)

indexes = [search_idx, vector_idx]

collection.create_search_indexes(models=indexes)
```

</Tab>

<Tab name="Asynchronous">

```python
search_idx = SearchIndexModel(
    definition ={
        "mappings": {
            "dynamic": True
        }
    },
    name="my_index",
)

vector_idx = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "numDimensions": <number of dimensions>,
        "path": "<field to index>",
        "similarity": "<select from euclidean, cosine, dotProduct>"
      }
    ]
  },
  name="my_vector_index",
  type="vectorSearch",
)

indexes = [search_idx, vector_idx]

await collection.create_search_indexes(models=indexes)
```

</Tab>

</Tabs>

#### List Search Indexes

You can use the [list_search_indexes()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.list_search_indexes) method to get information about the MongoDB Search and Vector Search indexes of a collection.

The following code example shows how to print a list of the search indexes of a collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
results = list(collection.list_search_indexes())

for index in results:
    print(index)
```

</Tab>

<Tab name="Asynchronous">

```python
results = await (await collection.list_search_indexes()).to_list()

async for index in results:
    print(index)
```

</Tab>

</Tabs>

#### Update a Search Index

You can use the [update_search_index()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.update_search_index) method to update a MongoDB Search or Vector Search index.

The following code example shows how to update a MongoDB Search index. Select the Synchronous or Asynchronous tab to see the corresponding code:

```python
new_index_definition = {
    "mappings": {
        "dynamic": False
    }
}

collection.update_search_index("my_index", new_index)
```

The following code example shows how to update a MongoDB Vector Search index. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
new_index_definition = {
    "fields": [
        {
            "type": "vector",
            "numDimensions": 1536,
            "path": "<field to index>",
            "similarity": "euclidean"
        },
    ]
}

collection.update_search_index("my_vector_index", new_index_definition)
```

</Tab>

<Tab name="Asynchronous">

```python
new_index_definition = {
    "fields": [
        {
            "type": "vector",
            "numDimensions": 1536,
            "path": "<field to index>",
            "similarity": "euclidean"
        },
    ]
}

await collection.update_search_index("my_vector_index", new_index_definition)
```

</Tab>

</Tabs>

#### Delete a Search Index

You can use the [drop_search_index()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.drop_search_index) method to remove a MongoDB Search or MongoDB Vector Search index.

The following code shows how to delete a search index from a collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
collection.drop_search_index("my_index")
```

</Tab>

<Tab name="Asynchronous">

```python
await collection.drop_search_index("my_index")
```

</Tab>

</Tabs>

### Text Indexes

**Text indexes** support text search queries on string content. These indexes can include any field whose value is a string or an array of string elements. MongoDB supports text search for various languages. You can specify the default language as an option when creating the index.

MongoDB offers an improved full-text search solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/). To learn more about MongoDB Search indexes and how to use them, see the [MongoDB Search and Vector Search Indexes](https://www.mongodb.com/docs/languages/python/pymongo-driver/indexes/#std-label-pymongo-atlas-search-index) section of this page.

#### Text Index on a Single Field

The following example creates a text index on the `plot` field. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
movies.create_index(
    [( "plot", "text" )]
)
```

</Tab>

<Tab name="Asynchronous">

```python
await movies.create_index(
    [( "plot", "text" )]
)
```

</Tab>

</Tabs>

The following is an example of a query that uses the index created in the preceding code example:

```python
query = { "$text": { "$search": "a time-traveling DeLorean" } }

cursor = movies.find(query)
```

#### Text Index on Multiple Fields

A collection can contain only one text index. If you want to create a text index for multiple text fields, create a compound index. A text search runs on all the text fields within the compound index.

The following example creates a compound text index for the `title` and `genre` fields. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from pymongo.collation import Collation

result = myColl.create_index(
    [("title", "text"), ("genre", "text")],
    default_language="english",
    weights={ "title": 10, "genre": 3 },
    collation=Collation(locale='fr_CA')
)
```

</Tab>

<Tab name="Asynchronous">

```python
from pymongo.collation import Collation

result = await myColl.create_index(
    [("title", "text"), ("genre", "text")],
    default_language="english",
    weights={ "title": 10, "genre": 3 },
    collation=Collation(locale='fr_CA')
)
```

</Tab>

</Tabs>

For more information, see [Compound Text Index Restrictions](https://www.mongodb.com/docs/manual/core/index-text/#std-label-text-index-compound) and [Text Indexes](https://www.mongodb.com/docs/manual/core/index-text/) in the MongoDB Server manual.

### Geospatial Indexes

MongoDB supports queries of geospatial coordinate data using **2dsphere indexes**. With a `2dsphere` index, you can query the geospatial data for inclusion, intersection, and proximity. For more information about querying geospatial data, see [Geospatial Queries](https://www.mongodb.com/docs/manual/geospatial-queries/).

To create a `2dsphere` index, you must specify a field that contains only **GeoJSON objects**. For more details on this type, see the [GeoJSON objects](https://www.mongodb.com/docs/manual/reference/geojson/) guide in the MongoDB Server manual.

The `location.geo` field in the following sample document from the `theaters` collection in the `sample_mflix` database is a GeoJSON Point object that describes the coordinates of the theater:

```javascript
{
   "_id" : ObjectId("59a47286cfa9a3a73e51e75c"),
   "theaterId" : 104,
   "location" : {
      "address" : {
         "street1" : "5000 W 147th St",
         "city" : "Hawthorne",
         "state" : "CA",
         "zipcode" : "90250"
      },
      "geo" : {
         "type" : "Point",
         "coordinates" : [
            -118.36559,
            33.897167
         ]
      }
   }
}
```

#### Create a Geospatial Index

The following example creates a `2dsphere` index on the `location.geo` field. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
theaters.create_index(
    [( "location.geo", "2dsphere" )]
)
```

</Tab>

<Tab name="Asynchronous">

```python
await theaters.create_index(
    [( "location.geo", "2dsphere" )]
)
```

</Tab>

</Tabs>

MongoDB also supports `2d` indexes for calculating distances on a Euclidean plane and for working with the "legacy coordinate pairs" syntax used in MongoDB 2.2 and earlier. For more information, see the [Geospatial Queries guide](https://www.mongodb.com/docs/manual/geospatial-queries/) in the MongoDB Server manual.

### Unique Indexes

Unique indexes ensure that the indexed fields do not store duplicate values. By default, MongoDB creates a unique index on the `_id` field during the creation of a collection. To create a unique index, perform the following steps:

- Specify the field or combination of fields that you want to prevent duplication on.

- Set the `unique` option to``True``.

#### Create a Unique Index

The following example creates a descending unique index on the `theaterId` field. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
theaters.create_index("theaterId", unique=True)
```

</Tab>

<Tab name="Asynchronous">

```python
await theaters.create_index("theaterId", unique=True)
```

</Tab>

</Tabs>

For more information, see the [Unique Indexes](https://www.mongodb.com/docs/manual/core/index-unique/) guide in the MongoDB Server manual.

### Wildcard Indexes

Wildcard indexes enable queries against unknown or arbitrary fields. These indexes can be beneficial if you are using a dynamic schema.

#### Create a Wildcard Index

The following example creates an ascending wildcard index on all values of the `location` field, including values nested in subdocuments and arrays. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
movies.create_index({ "location.$**": pymongo.ASCENDING })
```

</Tab>

<Tab name="Asynchronous">

```python
await movies.create_index({ "location.$**": pymongo.ASCENDING })
```

</Tab>

</Tabs>

For more information, see the [Wildcard Indexes](https://www.mongodb.com/docs/manual/core/index-wildcard/) page in the MongoDB Server manual.

### Clustered Indexes

**Clustered indexes** instruct a collection to store documents ordered by a key value. To create a clustered index, perform the following steps when you create your collection:

- Specify the clustered index option with the `_id` field as the key.

- Set the unique field to `True`.

#### Create a Clustered Index

The following example creates a clustered index on the `_id` field in a new `movie_reviews` collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
sample_mflix.create_collection("movies", clusteredIndex={
    "key": { "_id": 1 },
    "unique": True
})
```

</Tab>

<Tab name="Asynchronous">

```python
await sample_mflix.create_collection("movies", clusteredIndex={
    "key": { "_id": 1 },
    "unique": True
})
```

</Tab>

</Tabs>

For more information, see the [Clustered Index](https://www.mongodb.com/docs/manual/reference/method/db.createCollection/#std-label-db.createCollection.clusteredIndex) and [Clustered Collections](https://www.mongodb.com/docs/manual/core/clustered-collections/) sections in the MongoDB Server manual.

## Remove an Index

You can remove any unused index except the default unique index on the `_id` field.

The following sections show how to remove a single index or to remove all indexes in a collection.

### Remove a Single Index

Pass an instance of an index or the index name to the `drop_index()` method to remove an index from a collection.

The following example removes an index with the name `"_title_"` from the `movies` collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
movies.drop_index("_title_")
```

</Tab>

<Tab name="Asynchronous">

```python
await movies.drop_index("_title_")
```

</Tab>

</Tabs>

You cannot remove a single field from a compound text index. You must drop the entire index and create a new one to update the indexed fields.

### Remove All Indexes

Starting with MongoDB 4.2, you can drop all indexes by calling the `drop_indexes()` method on your collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
collection.drop_indexes()
```

</Tab>

<Tab name="Asynchronous">

```python
await collection.drop_indexes()
```

</Tab>

</Tabs>

For earlier versions of MongoDB, pass `"*"` as a parameter to your call to `drop_index()` on your collection:

<Tabs>

<Tab name="Synchronous">

```python
collection.drop_index("*")
```

</Tab>

<Tab name="Asynchronous">

```python
await collection.drop_index("*")
```

</Tab>

</Tabs>

## Troubleshooting

### DuplicateKeyException

If you perform a write operation that stores a duplicate value that violates a [unique index](https://www.mongodb.com/docs/languages/python/pymongo-driver/indexes/#std-label-pymongo-unique-index), the driver raises a `DuplicateKeyException`, and MongoDB throws an error resembling the following:

```none
E11000 duplicate key error index
```

## Additional Information

To learn more about indexes in MongoDB, see the [Indexes](https://www.mongodb.com/docs/manual/indexes/) guide in the MongoDB Server manual.

### API Documentation

To learn more about any of the methods or types discussed in this guide, see the following API documentation:

- [create_index()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.create_index)

- [create_indexes()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.create_indexes)

- [drop_index()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.drop_index)

- [drop_indexes()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.drop_indexes)
