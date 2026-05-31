> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/
> Fetch method: direct_markdown

# Find Documents

## Overview

In this guide, you can learn how to use PyMongo, the MongoDB synchronous Python driver, to retrieve data from a MongoDB collection by using read operations. You can call the `find()` or `find_one()` method to retrieve documents that match a set of criteria.

### Sample Data

The examples in this guide use the `sample_restaurants.restaurants` collection from the [Atlas sample datasets](https://www.mongodb.com/docs/atlas/sample-data/). To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see the [Get Started with PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/get-started/#std-label-pymongo-get-started) tutorial.

## Finding Documents

PyMongo includes two methods for retrieving documents from a collection: `find_one()` and `find()`. These methods take a **query filter** and return one or more matching documents. A query filter is an object that specifies the documents you want to retrieve in your query.

To learn more about query filters, see [Specify a Query](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/specify-query/#std-label-pymongo-specify-query).

### Find One Document

To find a single document in a collection, call the `find_one()` method and pass a query filter that specifies the criteria of the document you want to find. If more than one document matches the query filter, this method returns the *first* matching document from the retrieved results as a Python dictionary. If no documents match the query filter, the method returns `None`.

The `find_one()` method is useful when you know there's only one matching document, or you're only interested in the first match.

The following example uses the `find_one()` method to find the first document where the `"cuisine"` field has the value `"Bakery"`. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
restaurant = sample_restaurants.restaurants.find_one({"cuisine": "Bakery"})
```

</Tab>

<Tab name="Asynchronous">

```python
restaurant = await sample_restaurants.restaurants.find_one({"cuisine": "Bakery"})
```

</Tab>

</Tabs>

The `find_one()` method returns the first document in [natural order](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-natural-order) on disk if no sort criteria is specified.

To learn more about sorting, see the [sort guide](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/specify-documents-to-return/#std-label-pymongo-sort).

### Find Multiple Documents

To find multiple documents in a collection, pass a query filter to the `find()` method that specifies the criteria of the documents you want to retrieve.

The following example uses the `find()` method to find all documents where the `"cuisine"` field has the value `"Spanish"`.

```python
cursor = sample_restaurants.restaurants.find({"cuisine": "Spanish"})
```

You can use a **cursor** to iterate over the documents returned by the `find()` method. A cursor is a mechanism that allows an application to iterate over database results while holding only a subset of them in memory at a given time. Cursors are useful when your `find()` method returns a large amount of documents.

You can iterate over the documents in a cursor by using a `for-in` loop, as shown in the following example. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
cursor = sample_restaurants.restaurants.find({"cuisine": "Spanish"})
for restaurant in cursor:
...
```

</Tab>

<Tab name="Asynchronous">

```python
cursor = sample_restaurants.restaurants.find({"cuisine": "Spanish"})
async for restaurant in cursor:
...
```

</Tab>

</Tabs>

To find all documents in a collection, pass an empty filter to the `find()` method:

```python
all_restaurants = sample_restaurants.restaurants.find({})
```

### Modify Find Behavior

You can modify the behavior of the `find()` and `find_one()` methods by passing named arguments to them. The following table describes the commonly used arguments:

<table>
<tr>
<th id="Argument">
Argument

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Argument">
`batch_size`

</td>
<td headers="Description">
Limits the number of documents to hold in a cursor at a given time.

</td>
</tr>
<tr>
<td headers="Argument">
`collation`

</td>
<td headers="Description">
The collation options for the find operation. See the [Collation](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/find/#std-label-pymongo-retrieve-collation) guide for more information.

</td>
</tr>
<tr>
<td headers="Argument">
`comment`

</td>
<td headers="Description">
A string to attach to the query. This can help you trace and interpret the operation in the server logs and in profile data. To learn more about query comments, see the [cursor.comment()](https://www.mongodb.com/docs/manual/reference/method/cursor.comment/) page in the MongoDB Server manual.

</td>
</tr>
<tr>
<td headers="Argument">
`hint`

</td>
<td headers="Description">
The index to use for the query.

</td>
</tr>
<tr>
<td headers="Argument">
`max_time_ms`

</td>
<td headers="Description">
The maximum execution time on the server for this operation. If this time is exceeded, PyMongo aborts the operation and raises an `ExecutionTimeout`.

</td>
</tr>
</table>The following example uses the `find()` method to find all documents where the `"cuisine"` field has the value `"Italian"` and sets a maximum execution time of 10 seconds (10,000 milliseconds):

```python
cursor = sample_restaurants.restaurants.find({"cuisine": "Italian"}, max_time_ms=10000)
```

For a full list of available arguments, see the [API documentation](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.find) for the  `find() method`.

#### Collation

When you perform a query, you can specify a **collation** for the driver to follow when sorting the results.

A collation is a set of language-specific rules for string comparison, such as for letter case and accent marks.

To specify a collation, create an instance of the `Collation` class or a Python dictionary. For a list of options to pass to the `Collation` constructor or include as keys in the dictionary, see [Collation](https://www.mongodb.com/docs/manual/reference/collation/) in the MongoDB Server manual.

To create an instance of the `Collation` class, you must import it from `pymongo.collation`.

The following example performs the same find operation as the previous example, but with a default collation of `fr_CA`:

```python
cursor = sample_restaurants.restaurants.find({"cuisine": "Italian"}, max_time_ms=10000,
                                           collation=Collation(locale="fr_CA"))
```

Alternatively, you can specify a collation by chaining the `collation()` method to the `find()` method:

```python
cursor = sample_restaurants.restaurants.find({"cuisine": "Italian"}, max_time_ms=10000)
                                       .collation(Collation(locale="fr_CA"))
```

When you specify a collation as part of an operation, it overrides the default collation for the collection.

## Troubleshooting Invalid Documents

If a document that you try to find is invalid or corrupt, the driver throws an `InvalidBSON` exception. The following examples show how to troubleshoot an `InvalidBSON` exception and find the invalid documents in your collection.

### Finding Invalid Documents in Collections

The following example shows how to identify invalid documents when iterating over a collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
import bson

# Use RawBSONDocument to delay BSON decoding
raw_coll = collection.with_options(
    codec_options=collection.codec_options.with_options(
        document_class=bson.raw_bson.RawBSONDocument
    )
)

# Iterate through documents and check for BSON errors
for doc in raw_coll.find():
    try:
        bson.decode(doc.raw)
    except bson.errors.InvalidBSON as exc:
        print(f"Invalid document {exc}, raw bson: {doc.raw}")
```

</Tab>

<Tab name="Asynchronous">

```python
import bson

# Use RawBSONDocument to delay BSON decoding
raw_coll = collection.with_options(
    codec_options=collection.codec_options.with_options(
        document_class=bson.raw_bson.RawBSONDocument
    )
)

# Iterate through documents and check for BSON errors
async for doc in raw_coll.find():
    try:
        bson.decode(doc.raw)
    except bson.errors.InvalidBSON as exc:
        print(f"Invalid document {exc}, raw bson: {doc.raw}")
```

</Tab>

</Tabs>

### Finding Invalid Documents in Command Responses

The following example shows how to handle invalid BSON in database command responses. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
import bson

# Execute command with raw BSON options
res = client.admin.command(
    "serverStatus",
    codec_options=bson.raw_bson.DEFAULT_RAW_BSON_OPTIONS
)

# Check for BSON errors in the response
try:
    bson.decode(res.raw)
except bson.errors.InvalidBSON as exc:
    print(f"Invalid BSON found in serverStatus response {exc}, raw bson: {res.raw}")
```

</Tab>

<Tab name="Asynchronous">

```python
import bson

# Execute command with raw BSON options
res = await client.admin.command(
    "serverStatus",
    codec_options=bson.raw_bson.DEFAULT_RAW_BSON_OPTIONS
)

# Check for BSON errors in the response
try:
    bson.decode(res.raw)
except bson.errors.InvalidBSON as exc:
    print(f"Invalid BSON found in serverStatus response {exc}, raw bson: {res.raw}")
```

</Tab>

</Tabs>

## Additional Information

The PyMongoArrow library lets you load MongoDB query result-sets as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html), [NumPy ndarrays](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html), or [Apache Arrow Tables](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html). To learn more about PyMongoArrow, see the [PyMongoArrow documentation](https://www.mongodb.com/docs/languages/python/pymongo-arrow-driver/current/).

To learn more about query filters, see [Specify a Query](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/specify-query/#std-label-pymongo-specify-query).

For runnable code examples of retrieving documents with PyMongo, see [Query](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/#std-label-pymongo-query).

### API Documentation

To learn more about any of the methods or types discussed in this guide, see the following API documentation:

- [find()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.find)

- [find_one()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.find_one)

- [Collation](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collation.html#pymongo.collation.Collation)

- [Cursor](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/cursor.html#pymongo.cursor.Cursor)
