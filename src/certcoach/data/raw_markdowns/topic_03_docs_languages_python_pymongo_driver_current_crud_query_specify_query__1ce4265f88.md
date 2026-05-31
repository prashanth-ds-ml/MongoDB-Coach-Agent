> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/specify-query/
> Fetch method: direct_markdown

# Specify a Query

## Overview

In this guide, you can learn how to specify a query by using PyMongo.

You can refine the set of documents that a query returns by creating a **query filter**. A query filter is an expression that specifies the search criteria MongoDB uses to match documents in a read or write operation. In a query filter, you can prompt the driver to search for documents with an exact match to your query, or you can compose query filters to express more complex matching criteria.

### Sample Data

The examples in this guide run operations on a collection called `fruits` that contains the following documents:

```json
{ "_id": 1, "name": "apples", "qty": 5, "rating": 3, "color": "red", "type": ["fuji", "honeycrisp"] },
{ "_id": 2, "name": "bananas", "qty": 7, "rating": 4, "color": "yellow", "type": ["cavendish"] },
{ "_id": 3, "name": "oranges", "qty": 6, "rating": 2, "type": ["naval", "mandarin"] },
{ "_id": 4, "name": "pineapple", "qty": 3, "rating": 5, "color": "yellow" },
```

The following code example shows how to create a database and collection, then insert the sample documents into your collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from pymongo import MongoClient

uri = "<connection string URI>"
client = MongoClient(uri)

try:
    database = client["sample_fruit"]
    collection = database["fruits"]

    collection.insert_many([
        { "_id": 1, "name": "apples", "qty": 5, "rating": 3, "color": "red", "type": ["fuji", "honeycrisp"] },
        { "_id": 2, "name": "bananas", "qty": 7, "rating": 4, "color": "yellow", "type": ["cavendish"] },
        { "_id": 3, "name": "oranges", "qty": 6, "rating": 2, "type": ["naval", "mandarin"] },
        { "_id": 4, "name": "pineapple", "qty": 3, "rating": 5, "color": "yellow" },
    ])

    client.close()

except Exception as e:
    raise Exception("Error inserting documents: ", e)
```

</Tab>

<Tab name="Asynchronous">

```python
from pymongo import AsyncMongoClient

uri = "<connection string URI>"
client = AsyncMongoClient(uri)

try:
    database = client["sample_fruit"]
    collection = database["fruits"]

    await collection.insert_many([
        { "_id": 1, "name": "apples", "qty": 5, "rating": 3, "color": "red", "type": ["fuji", "honeycrisp"] },
        { "_id": 2, "name": "bananas", "qty": 7, "rating": 4, "color": "yellow", "type": ["cavendish"] },
        { "_id": 3, "name": "oranges", "qty": 6, "rating": 2, "type": ["naval", "mandarin"] },
        { "_id": 4, "name": "pineapple", "qty": 3, "rating": 5, "color": "yellow" },
    ])

    await client.close()

except Exception as e:
    raise Exception("Error inserting documents: ", e)
```

</Tab>

</Tabs>

## Exact Match

Literal value queries return documents with an exact match to your query filter.

The following example specifies a query filter as a parameter to the `find()` method. The code returns all documents with a `color` field value of `"yellow"`:

```python
results = collection.find({ "color": "yellow" })
```

```
{'_id': 2, 'name': 'bananas', 'qty': 7, 'rating': 4, 'color': 'yellow', 'type': ['cavendish']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

To find all documents in a collection, call the `find()` method and pass it an empty query filter. The following example finds all documents in a collection:

```python
results = collection.find({})
```

## Comparison Operators

Comparison operators evaluate a document field value against a specified value in your query filter. The following is a list of common comparison operators:

- `$gt`: Greater than

- `$lte`: Less than or Equal

- `$ne`: Not equal

To view a full list of comparison operators, see the [Comparison Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query-comparison/) guide in the MongoDB Server manual.

The following example specifies a comparison operator in a query filter as a parameter to the `find()` method. The code returns all documents with a `rating` field value greater than `2`:

<Tabs>

<Tab name="Synchronous">

```python
results = collection.find({ "rating": { "$gt" : 2 }})

for f in results:
    print(f)
```

```
{'_id': 1, 'name': 'apples', 'qty': 5, 'rating': 3, 'color': 'red', 'type': ['fuji', 'honeycrisp']}
{'_id': 2, 'name': 'bananas', 'qty': 7, 'rating': 4, 'color': 'yellow', 'type': ['cavendish']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

</Tab>

<Tab name="Asynchronous">

```python
results = collection.find({ "rating": { "$gt" : 2 }})

async for f in results:
    print(f)
```

```
{'_id': 1, 'name': 'apples', 'qty': 5, 'rating': 3, 'color': 'red', 'type': ['fuji', 'honeycrisp']}
{'_id': 2, 'name': 'bananas', 'qty': 7, 'rating': 4, 'color': 'yellow', 'type': ['cavendish']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

</Tab>

</Tabs>

## Logical Operators

Logical operators match documents by using logic applied to the results of two or more sets of expressions. The following is a list of logical operators:

- `$and`, which returns all documents that match the conditions of *all* clauses

- `$or`, which returns all documents that match the conditions of *one* clause

- `$nor`, which returns all documents that *do not* match the conditions of any clause

- `$not`, which returns all documents that *do not* match the expression

To learn more about logical operators, see the [Logical Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query-logical/) guide in the MongoDB Server manual.

The following example specifies a logical operator in a query filter as a parameter to the `find()` method. The code returns all documents with a `qty` field value greater than `5` **or** a `color` field value of `"yellow"`. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
results = collection.find({
    "$or": [
        { "qty": { "$gt": 5 }},
        { "color": "yellow" }
    ]
})

for f in results:
    print(f)
```

```
{'_id': 2, 'name': 'bananas', 'qty': 7, 'rating': 4, 'color': 'yellow', 'type': ['cavendish']}
{'_id': 3, 'name': 'oranges', 'qty': 6, 'rating': 2, 'type': ['naval', 'mandarin']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

</Tab>

<Tab name="Asynchronous">

```python
results = collection.find({
    "$or": [
        { "qty": { "$gt": 5 }},
        { "color": "yellow" }
    ]
})

async for f in results:
    print(f)
```

```
{'_id': 2, 'name': 'bananas', 'qty': 7, 'rating': 4, 'color': 'yellow', 'type': ['cavendish']}
{'_id': 3, 'name': 'oranges', 'qty': 6, 'rating': 2, 'type': ['naval', 'mandarin']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

</Tab>

</Tabs>

## Array Operators

Array operators match documents based on the value or quantity of elements in an array field. The following is a list of available array operators:

- `$all`, which returns documents with arrays that contain all elements in the query

- `$elemMatch`, which returns documents if an element in their array field matches all conditions in the query

- `$size`, which returns all documents with arrays of a specified size

To learn more about array operators, see the [Array Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query-array/) guide in the MongoDB Server manual.

The following example specifies an array operator in a query filter as a parameter to the `find()` method. The code returns all documents with a `type` array field containing `2` elements. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
results = collection.find({
    "type" : { "$size": 2 }
})

for f in results:
    print(f)
```

```
{'_id': 1, 'name': 'apples', 'qty': 5, 'rating': 3, 'color': 'red', 'type': ['fuji', 'honeycrisp']}
{'_id': 3, 'name': 'oranges', 'qty': 6, 'rating': 2, 'type': ['naval', 'mandarin']}
```

</Tab>

<Tab name="Asynchronous">

```python
results = collection.find({
    "type" : { "$size": 2 }
})

async for f in results:
    print(f)
```

```
{'_id': 1, 'name': 'apples', 'qty': 5, 'rating': 3, 'color': 'red', 'type': ['fuji', 'honeycrisp']}
{'_id': 3, 'name': 'oranges', 'qty': 6, 'rating': 2, 'type': ['naval', 'mandarin']}
```

</Tab>

</Tabs>

## Element Operators

Element operators query data based on the presence or type of a field.

To learn more about element operators, see the [Element Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query-element/) guide in the MongoDB Server manual.

The following example specifies an element operator in a query filter as a parameter to the `find()` method. The code returns all documents that have a `color` field. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
results = collection.find( { "color" : { "$exists": "true" }} )

for f in results:
    print(f)
```

```
{'_id': 1, 'name': 'apples', 'qty': 5, 'rating': 3, 'color': 'red', 'type': ['fuji', 'honeycrisp']}
{'_id': 2, 'name': 'bananas', 'qty': 7, 'rating': 4, 'color': 'yellow', 'type': ['cavendish']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

</Tab>

<Tab name="Asynchronous">

```python
results = collection.find( { "color" : { "$exists": "true" }} )

async for f in results:
    print(f)
```

```
{'_id': 1, 'name': 'apples', 'qty': 5, 'rating': 3, 'color': 'red', 'type': ['fuji', 'honeycrisp']}
{'_id': 2, 'name': 'bananas', 'qty': 7, 'rating': 4, 'color': 'yellow', 'type': ['cavendish']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

</Tab>

</Tabs>

## Evaluation Operators

Evaluation operators return data based on evaluations of either individual fields or the entire collection's documents.

The following is a list of common evaluation operators:

- `$text`, which performs a text search on the documents

- `$regex`, which returns documents that match a specified regular expression

- `$mod`, which performs a modulo operation on the value of a field and returns documents where the remainder is a specified value

To view a full list of evaluation operators, see the [Evaluation Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query-evaluation/) guide in the MongoDB Server manual.

The following example specifies an evaluation operator in a query filter as a parameter to the `find()` method. The code uses a regular expression to return all documents with a `name` field value that has at least two consecutive `"p"` characters. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
results = collection.find({ "name" : { "$regex" : "p{2,}" }} )

for f in results:
    print(f)
```

```
{'_id': 1, 'name': 'apples', 'qty': 5, 'rating': 3, 'color': 'red', 'type': ['fuji', 'honeycrisp']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

</Tab>

<Tab name="Asynchronous">

```python
results = collection.find({ "name" : { "$regex" : "p{2,}" }} )

async for f in results:
    print(f)
```

```
{'_id': 1, 'name': 'apples', 'qty': 5, 'rating': 3, 'color': 'red', 'type': ['fuji', 'honeycrisp']}
{'_id': 4, 'name': 'pineapple', 'qty': 3, 'rating': 5, 'color': 'yellow'}
```

</Tab>

</Tabs>

## Troubleshooting

### No Results When Querying for a Document by ObjectId in Web Applications

It's common in web applications to encode documents' ObjectIds in URLs, as shown in the following code example:

```python
"/posts/50b3bda58a02fb9a84d8991e"
```

Your web framework passes the ObjectId part of the URL to your request handler as a string. You must convert the string to an `ObjectId` instance before passing it to the `find_one()` method.

The following code example shows how to perform this conversion in a [Flask](http://flask.pocoo.org/) application. The process is similar for other web frameworks.

```python
from pymongo import MongoClient
from bson.objectid import ObjectId

from flask import Flask, render_template

client = MongoClient()
app = Flask(__name__)

@app.route("/posts/<_id>")
def show_post(_id):
   # NOTE!: converting _id from string to ObjectId before passing to find_one
   post = client.db.posts.find_one({'_id': ObjectId(_id)})
   return render_template('post.html', post=post)

if __name__ == "__main__":
    app.run()
```

## Additional Information

To learn more about querying documents, see the [Query Documents](https://www.mongodb.com/docs/manual/tutorial/query-documents/) guide in the MongoDB Server manual.

To learn more about retrieving documents with PyMongo, see [Find Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/find/#std-label-pymongo-retrieve).

### API Documentation

To learn more about any of the methods or types discussed in this guide, see the following API documentation:

- [find()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.find)
