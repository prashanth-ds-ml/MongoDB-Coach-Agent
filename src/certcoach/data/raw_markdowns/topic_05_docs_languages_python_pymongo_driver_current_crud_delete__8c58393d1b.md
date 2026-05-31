> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/delete/
> Fetch method: direct_markdown

# Delete Documents

## Overview

In this guide, you can learn how to use PyMongo to remove documents from a MongoDB collection by performing delete operations.

A delete operation removes one or more documents from a MongoDB collection. You can perform a delete operation by using the `delete_one()` or `delete_many()` methods.

### Sample Data

The examples in this guide use the `sample_restaurants.restaurants` collection from the [Atlas sample datasets](https://www.mongodb.com/docs/atlas/sample-data/). To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see the [Get Started with PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/get-started/#std-label-pymongo-get-started) tutorial.

## Delete Operations

You can perform delete operations in MongoDB by using the following methods:

- `delete_one()`, which deletes *the first document* that matches the search criteria

- `delete_many()`, which deletes *all documents* that match the search criteria

Each delete method requires a **query filter** document, which specifies the search criteria that determine which documents to select for removal. For more information about query filters, see the [Query Filter Documents section](https://www.mongodb.com/docs/manual/core/document/#query-filter-documents) in the MongoDB Server manual.

### Delete One Document

The following example uses the `delete_one()` method to remove a document in the `restaurants` collection with a `name` value of `"Ready Penny Inn"`. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
query_filter = { "name": "Ready Penny Inn" }

result = restaurants.delete_one(query_filter)
```

</Tab>

<Tab name="Asynchronous">

```python
query_filter = { "name": "Ready Penny Inn" }

result = await restaurants.delete_one(query_filter)
```

</Tab>

</Tabs>

### Delete Multiple Documents

The following example uses the `delete_many()` method to remove all documents in the `restaurants` collection with a `borough` value of `"Brooklyn"`. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
query_filter = { "borough": "Brooklyn" }

result = restaurants.delete_many(query_filter)
```

</Tab>

<Tab name="Asynchronous">

```python
query_filter = { "borough": "Brooklyn" }

result = await restaurants.delete_many(query_filter)
```

</Tab>

</Tabs>

### Customize the Delete Operation

The `delete_one()` and `delete_many()` methods optionally accept additional parameters, which represent options you can use to configure the delete operation. If you don't specify any additional options, the driver does not customize the delete operation.

<table>
<tr>
<th id="Property">
Property

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Property">
`collation`

</td>
<td headers="Description">
Specifies the kind of language collation to use when sorting results. See [Collation](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/delete/#std-label-pymongo-delete-collation) for more information.

</td>
</tr>
<tr>
<td headers="Property">
`hint`

</td>
<td headers="Description">
Gets or sets the index to scan for documents. For more information, see the [hint statement](https://www.mongodb.com/docs/manual/reference/command/delete/#std-label-deletes-array-hint) in the MongoDB Server manual.

</td>
</tr>
<tr>
<td headers="Property">
`session`

</td>
<td headers="Description">
An instance of `ClientSession`.

</td>
</tr>
<tr>
<td headers="Property">
`let`

</td>
<td headers="Description">
A map of parameter names and values. Values must be constant or closed expressions that don't reference document fields. For more information, see the [let statement](https://www.mongodb.com/docs/manual/reference/command/delete/#std-label-delete-let-syntax) in the MongoDB Server manual.

</td>
</tr>
<tr>
<td headers="Property">
`comment`

</td>
<td headers="Description">
A comment to attach to the operation. For more information, see the [delete command fields](https://www.mongodb.com/docs/manual/reference/command/delete/#command-fields) guide in the MongoDB Server manual for more information.

</td>
</tr>
</table>The following code uses the `delete_many()` method to delete all documents in the `restaurants` collection with a `name` value that includes the string `"Mongo"`. It also uses the `comment` option to add a comment to the operation. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
query_filter = { 'name': {'$regex': 'Mongo' }}

result = restaurants.delete_many(query_filter, comment="Deleting Mongo restaurants")
```

</Tab>

<Tab name="Asynchronous">

```python
query_filter = { 'name': {'$regex': 'Mongo' }}

result = await restaurants.delete_many(query_filter, comment="Deleting Mongo restaurants")
```

</Tab>

</Tabs>

If the preceding example used the `delete_one()` method instead of `delete_many()`, the driver would delete only the first document with a `name` value that includes `"Mongo"`.

#### Collation

When you perform a delete operation, you can specify a **collation** for the driver to use.

A collation is a set of language-specific rules for string comparison, such as for letter case and accent marks.

To specify a collation, create an instance of the `Collation` class or a Python dictionary. For a list of options to pass to the `Collation` constructor or include as keys in the dictionary, see [Collation](https://www.mongodb.com/docs/manual/reference/collation/) in the MongoDB Server manual.

To create an instance of the `Collation` class, you must import it from `pymongo.collation`.

The following example performs the same delete operation as the previous example, but with a default collation of `fr_CA`. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from pymongo.collation import Collation

query_filter = { "borough": "Brooklyn" }

result = restaurants.delete_many(query_filter, collation=Collation(locale='fr_CA'))
```

</Tab>

<Tab name="Asynchronous">

```python
from pymongo.collation import Collation

query_filter = { "borough": "Brooklyn" }

result = await restaurants.delete_many(query_filter, collation=Collation(locale='fr_CA'))
```

</Tab>

</Tabs>

When you specify a collation as part of an operation, it overrides the default collation for the collection.

### Return Value

The `delete_one()` and `delete_many()` methods return a `DeleteResult` type. This type contains the following properties:

- `deleted_count`, which indicates the number of documents deleted

- `acknowledged`, which indicates if the server acknowledges the result

- `raw_result`, which is the raw result returned by the server

If the `acknowledged` attribute is `False`, all other attributes of `DeleteResult` raise an `InvalidOperation` exception when accessed. The driver cannot determine these values if the server does not acknowledge the write operation.

If the query filter does not match any documents, the driver doesn't delete any documents and `deleted_count` is 0.

### API Documentation

To learn more about any of the methods or types discussed in this guide, see the following API Documentation:

- [delete_one()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.delete_one)

- [delete_many()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.delete_many)

- [DeleteResult](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/results.html#pymongo.results.DeleteResult)

- [ClientSession](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/client_session.html#pymongo.client_session.ClientSession)
