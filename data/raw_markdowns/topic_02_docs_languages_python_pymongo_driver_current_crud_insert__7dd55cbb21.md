> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/insert/
> Fetch method: direct_markdown

# Insert Documents

## Overview

In this guide, you can learn how to use PyMongo to add documents to a MongoDB collection by performing insert operations.

An insert operation inserts one or more documents into a MongoDB collection. You can perform an insert operation by using the `insert_one()` or `insert_many()` method.

In a MongoDB collection, each document must contain an `_id` field with a unique value.

If you specify a value for the `_id` field, you must ensure that the value is unique across the collection. If you don't specify a value, the driver automatically generates a unique `ObjectId` value for the field.

We recommend letting the driver automatically generate `_id` values to ensure uniqueness. Duplicate `_id` values violate unique index constraints, which causes the driver to return an error.

### Sample Data

The examples in this guide use the `sample_restaurants.restaurants` collection from the [Atlas sample datasets](https://www.mongodb.com/docs/atlas/sample-data/). To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see the [Get Started with PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/get-started/#std-label-pymongo-get-started) tutorial.

## Insert One Document

To add a single document to a MongoDB collection, call the `insert_one()` method and pass the document you want to add.

The following example inserts a document into the `restaurants` collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
sample_restaurants.restaurants.insert_one({"name" : "Mongo's Burgers"})
```

</Tab>

<Tab name="Asynchronous">

```python
await sample_restaurants.restaurants.insert_one({"name" : "Mongo's Burgers"})
```

</Tab>

</Tabs>

You can also pass an instance of a custom class to the `insert_one()` method. This provides additional type safety if you're using a type-checking tool. The instance you pass must inherit from the `TypedDict` class.

The [TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict) class is in the `typing` module, which is available only in Python 3.8 and later. To use the `TypedDict` class in earlier versions of Python, install the [typing_extensions](https://pypi.org/project/typing-extensions/) package.

The following example passes an instance of the `Restaurant` class to the `insert_one()` method for added type safety. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
class Restaurant(TypedDict):
   name: str

sample_restaurants.restaurants.insert_one(Restaurant(name="Mongo's Burgers"))
```

</Tab>

<Tab name="Asynchronous">

```python
class Restaurant(TypedDict):
   name: str

await sample_restaurants.restaurants.insert_one(Restaurant(name="Mongo's Burgers"))
```

</Tab>

</Tabs>

To learn more about type-checking tools available for Python, see [Type Checkers](https://www.mongodb.com/docs/languages/python/pymongo-driver/integrations/#std-label-pymongo-tools-type-checkers) on the Tools page.

## Insert Multiple Documents

To add multiple documents to a MongoDB collection, call the `insert_many()` method and pass a list of documents you want to add.

The following example inserts a list of documents into the `restaurants` collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
document_list = [
   { "name" : "Mongo's Burgers" },
   { "name" : "Mongo's Pizza" }
]

sample_restaurants.restaurants.insert_many(document_list)
```

</Tab>

<Tab name="Asynchronous">

```python
document_list = [
   { "name" : "Mongo's Burgers" },
   { "name" : "Mongo's Pizza" }
]

await sample_restaurants.restaurants.insert_many(document_list)
```

</Tab>

</Tabs>

You can also pass a list of instances of a custom class to the `insert_many()` method. This provides additional type safety if you're using a type-checking tool. The instances you pass must inherit from the `TypedDict` class.

The [TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict) class is in the `typing` module, which is available only in Python 3.8 and later. To use the `TypedDict` class in earlier versions of Python, install the [typing_extensions](https://pypi.org/project/typing-extensions/) package.

The following example calls the `insert_many()` method and passes a list that contains instances of the `Restaurant` class. This adds type safety to the insert operation. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
class Restaurant(TypedDict):
   name: str

document_list = [
   Restaurant(name="Mongo's Burgers"),
   Restaurant(name="Mongo's Pizza")
]

sample_restaurants.restaurants.insert_many(document_list)
```

</Tab>

<Tab name="Asynchronous">

```python
class Restaurant(TypedDict):
   name: str

document_list = [
   Restaurant(name="Mongo's Burgers"),
   Restaurant(name="Mongo's Pizza")
]

await sample_restaurants.restaurants.insert_many(document_list)
```

</Tab>

</Tabs>

To learn more about type-checking tools available for Python, see [Type Checkers](https://www.mongodb.com/docs/languages/python/pymongo-driver/integrations/#std-label-pymongo-tools-type-checkers) on the Tools page.

## Modify Insert Behavior

The `insert_one()` method optionally accepts additional parameters which represent options you can use to configure the insert operation. If you don't specify any additional parameters, the driver does not customize the insert.

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
`bypass_document_validation`

</td>
<td headers="Description">
If set to `True`, allows the write to opt out of [document-level validation](https://www.mongodb.com/docs/manual/core/schema-validation/).Defaults to `False`.

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
`comment`

</td>
<td headers="Description">
A comment to attach to the operation. For more information, see the [insert command fields](https://www.mongodb.com/docs/manual/reference/command/insert/#command-fields) guide in the MongoDB Server manual for more information.

</td>
</tr>
</table>The `insert_many()` method accepts the preceding optional parameters, as well as the optional `ordered` property:

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
`ordered`

</td>
<td headers="Description">
If set to `True`, the driver sends documents to the server in the order provided. If an error occurs, the driver and server cancel all remaining insert operations.Defaults to `True`.

</td>
</tr>
</table>### Example

The following code uses the `insert_many()` method to insert three new documents into a collection. Because the second method argument is `bypass_document_validation = True`, this insert operation bypasses document-level validation. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
document_list = [
   { "name" : "Mongo's Burgers" },
   { "name" : "Mongo's Pizza" },
   { "name" : "Mongo's Tacos" }
]

sample_restaurants.restaurants.insert_many(document_list, bypass_document_validation = True)
```

</Tab>

<Tab name="Asynchronous">

```python
document_list = [
   { "name" : "Mongo's Burgers" },
   { "name" : "Mongo's Pizza" },
   { "name" : "Mongo's Tacos" }
]

await sample_restaurants.restaurants.insert_many(document_list, bypass_document_validation = True)
```

</Tab>

</Tabs>

## Troubleshooting

### Client Type Annotations

If you don't add a type annotation for your `MongoClient` object, your type checker might show an error similar to the following:

```python
from pymongo import MongoClient
client = MongoClient()  # error: Need type annotation for "client"
```

The solution is to annotate the `MongoClient` object as `client: MongoClient` or `client: MongoClient[Dict[str, Any]]`.

### Incompatible Type

If you specify `MongoClient` as a type hint but don't include data types for the document, keys, and values, your type checker might show an error similar to the following:

```python
error: Dict entry 0 has incompatible type "str": "int";
expected "Mapping[str, Any]": "int"
```

The solution is to add the following type hint to your `MongoClient` object:

```python
client: MongoClient[Dict[str, Any]]
```

You might see a similar error if you pass a list to the `insert_one()` method:

```bash
error: Argument 1 to "insert_one" of "Collection" has
incompatible type "List[Dict[<nothing>, <nothing>]]";
expected "Mapping[str, Any]"
```

This error occurs because the `insert_one()` method accepts a document, not a list. You can resolve this error by passing a document to the `insert_one()` method or by calling the `insert_many()` method instead.

### TypedDict Missing _id Key

If you don't specify the `_id` field, PyMongo automatically inserts it into the document. You can retrieve the value of the `_id` field at runtime, but if you use MyPy or another tool to perform static type-checking, it won't find the `_id` field in your class and will show an error similar to the following:

```bash
TypedDict has no key "_id"
```

This is caused by code similar to the following:

```python
from typing import TypedDict
from pymongo import MongoClient
from pymongo.collection import Collection
class Movie(TypedDict):
    name: str
    year: int

client: MongoClient = MongoClient()
collection: Collection[Movie] = client.test.test
inserted = collection.insert_one(Movie(name="Jurassic Park", year=1993))
result = collection.find_one({"name": "Jurassic Park"})
# _id is present but was added by PyMongo; this will raise a type-checking error
assert result["_id"]
```

One solution is to add a `# type:ignore` comment to the end of the line that uses the `_id` field. This comment instructs the type-checking tool to ignore any errors that the line causes. The following example shows how to implement this solution;

```python
from typing import TypedDict
from pymongo import MongoClient
from pymongo.collection import Collection

class Movie(TypedDict):
    name: str
    year: int

collection: Collection[Movie] = client.test.test
inserted = collection.insert_one(
    Movie(name="Jurassic Park", year=1993)
)
result = collection.find_one({"name": "Jurassic Park"})
assert result is not None
assert result["_id"] # type:ignore[typeddict-item]
```

Instead of ignoring the type error, you can avoid it by including the `_id` field in your model class, and explicitly specifying a value for this field when you create the class instance. The following code shows how to implement this solution:

```python
from typing import TypedDict
from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId

class Movie(TypedDict):
    _id: ObjectId
    name: str
    year: int

collection: Collection[ExplicitMovie] = client.test.test
inserted = collection.insert_one(
    ExplicitMovie(_id=ObjectId(), name="Jurassic Park", year=1993)
)
result = collection.find_one({"name": "Jurassic Park"})
assert result is not None
assert result["_id"]
```

One drawback to adding the `_id` field to your custom class is that you must include a value for the field for every instance of the class that you create. To avoid this, you can install the `typing.NotRequired` package, which includes the `NotRequired` type hint. If you use this type hint for the `_id` field, you can access the value of the `_id` field at runtime without seeing any compile-time type errors.

The following code example shows how to implement this solution:

```python
from typing import TypedDict, NotRequired
from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId

class Movie(TypedDict):
     _id: NotRequired[ObjectId]
    name: str
    year: int

client: MongoClient = MongoClient()
collection: Collection[Movie] = client.test.test
inserted = collection.insert_one(Movie(name="Jurassic Park", year=1993))
result = collection.find_one({"name": "Jurassic Park"})
assert result is not None
assert result["_id"]
```

The [NotRequired](https://docs.python.org/3/library/typing.html#typing.NotRequired) class is available only in Python 3.11 and later. To use `NotRequired` in earlier versions of Python, install the [typing_extensions](https://pypi.org/project/typing-extensions/) package instead.

## Additional Information

For runnable code examples of inserting documents with PyMongo, see [CRUD Operations](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/#std-label-pymongo-crud).

### API Documentation

To learn more about any of the methods or types discussed in this guide, see the following API Documentation:

- [insert_one()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.insert_one)

- [insert_many()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.insert_many)

- [ClientSession](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/client_session.html#pymongo.client_session.ClientSession)
