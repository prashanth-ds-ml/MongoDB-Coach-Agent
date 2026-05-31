> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/update/
> Fetch method: direct_markdown

# Update Documents

## Overview

In this guide, you can learn how to use PyMongo to update documents in a MongoDB collection by using the `update_one()` or `update_many()` methods.

### Sample Data

The examples in this guide use the `sample_restaurants.restaurants` collection from the Atlas sample datasets. To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see the Get Started with PyMongo tutorial.

## Update Operations

You can perform update operations in MongoDB by using the following methods:

- `update_one()`, which updates *the first document* that matches the search criteria

- `update_many()`, which updates *all documents* that match the search criteria

Each update method requires the following parameters:

- A **query filter** document, which determines which documents to update. For more information about query filters, see the Query Filter Documents section in the MongoDB Server manual.

- An **update** document, which specifies the **update operator** (the kind of update to perform) and the fields and values that should change. For a list of update operators and their usage, see the Field Update Operators guide page in the MongoDB Server manual.

### Update One Document

The following example uses the `update_one()` method to update the `name` value of a document named `"Bagels N Buns"` in the `restaurants` collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
restaurants = database["restaurants"]

query_filter = {'name' : 'Bagels N Buns'}
update_operation = { '$set' :
    { 'name' : '2 Bagels 2 Buns' }
}

result = restaurants.update_one(query_filter, update_operation)
```

</Tab>

<Tab name="Asynchronous">

```python
restaurants = database["restaurants"]

query_filter = {'name' : 'Bagels N Buns'}
update_operation = { '$set' :
    { 'name' : '2 Bagels 2 Buns' }
}

result = await restaurants.update_one(query_filter, update_operation)
```

</Tab>

</Tabs>

### Update Many Documents

The following example uses the `update_many()` method to update all documents with a `cuisine` value of `"Pizza"`. After the update, the documents have a `cuisine` value of `"Pasta"`. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
restaurants = database["restaurants"]

query_filter = {'cuisine' : 'Pizza'}
update_operation = { '$set' :
    { 'cuisine' : 'Pasta' }
}

result = restaurants.update_many(query_filter, update_operation)
```

</Tab>

<Tab name="Asynchronous">

```python
restaurants = database["restaurants"]

query_filter = {'cuisine' : 'Pizza'}
update_operation = { '$set' :
    { 'cuisine' : 'Pasta' }
}

result = await restaurants.update_many(query_filter, update_operation)
```

</Tab>

</Tabs>

### Customize the Update Operation

The `update_one()` and `update_many()` methods optionally accept additional parameters, which represent options you can use to configure the update operation. If you don't specify any additional options, the driver does not customize the update operation.

| Property | Description |
| --- | --- |
| `upsert` | Specifies whether the update operation performs an upsert operation if no documents match the query filter. For more information, see the upsert statement in the MongoDB Server manual.Defaults to `False` |
| `bypass_document_validation` | Specifies whether the update operation bypasses document validation. This lets you update documents that don't meet the schema validation requirements, if any exist. For more information about schema validation, see Schema Validation in the MongoDB Server manual.Defaults to `False`. |
| `collation` | Specifies the kind of language collation to use when sorting results. See Collation for more information. |
| `array_filters` | A list of filters that specifies which array elements an update applies to. |
| `hint` | Gets or sets the index to scan for documents. For more information, see the hint statement in the MongoDB Server manual. |
| `session` | An instance of `ClientSession`. |
| `let` | A Map of parameter names and values. Values must be constant or closed expressions that don't reference document fields. For more information, see the let statement in the MongoDB Server manual. |
| `comment` | A comment to attach to the operation. For more information, see the insert command fields guide in the MongoDB Server manual for more information. |
The following code uses the `update_many()` method to find all documents where the `borough` field has the value `"Manhattan"`. It then updates the `borough` value in these documents to `"Manhattan (north)"`. Because the `upsert` option is set to `True`, PyMongo inserts a new document if the query filter doesn't match any existing documents. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
restaurants = database["restaurants"]

query_filter = {'borough' : 'Manhattan'}
update_operation = { '$set' :
    { 'borough' : 'Manhattan (north)' }
}

result = restaurants.update_many(query_filter, update_operation, upsert = True)
```

</Tab>

<Tab name="Asynchronous">

```python
restaurants = database["restaurants"]

query_filter = {'borough' : 'Manhattan'}
update_operation = { '$set' :
    { 'borough' : 'Manhattan (north)' }
}

result = await restaurants.update_many(query_filter, update_operation, upsert = True)
```

</Tab>

</Tabs>

#### Collation

When you perform an update operation, you can specify a **collation** for the driver to use.

A collation is a set of language-specific rules for string comparison, such as for letter case and accent marks.

To specify a collation, create an instance of the `Collation` class or a Python dictionary. For a list of options to pass to the `Collation` constructor or include as keys in the dictionary, see Collation in the MongoDB Server manual.

To create an instance of the `Collation` class, you must import it from `pymongo.collation`.

The following example performs the same update operation as the previous example, but with a default collation of `fr_CA`. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from pymongo.collation import Collation

restaurants = database["restaurants"]

query_filter = {'cuisine' : 'Pizza'}
update_operation = { '$set' :
    { 'cuisine' : 'Pasta' }
}

result = restaurants.update_many(query_filter, update_operation,
                                 collation=Collation(locale='fr_CA'))
```

</Tab>

<Tab name="Asynchronous">

```python
from pymongo.collation import Collation

restaurants = database["restaurants"]

query_filter = {'cuisine' : 'Pizza'}
update_operation = { '$set' :
    { 'cuisine' : 'Pasta' }
}

result = await restaurants.update_many(query_filter, update_operation,
                                       collation=Collation(locale='fr_CA'))
```

</Tab>

</Tabs>

When you specify a collation as part of an operation, it overrides the default collation for the collection.

### Return Value

The `update_one()` and `update_many()` methods each return an `UpdateResult` object. The `UpdateResult` type contains the following properties:

| Property | Description |
| --- | --- |
| `matched_count` | The number of documents that matched the query filter, regardless of how many were updated. |
| `modified_count` | The number of documents modified by the update operation. If an updated document is identical to the original, it is not included in this count. |
| `raw_result` | The raw result document returned by the server. |
| `upserted_id` | The ID of the document that was upserted in the database, if the driver performed an upsert. Otherwise `None`. |

## Additional Information

To learn more about creating query filters, see the Specify a Query guide.

### API Documentation

To learn more about any of the methods or types discussed in this guide, see the following API documentation:

- update_one()

- update_many()

- UpdateResult
