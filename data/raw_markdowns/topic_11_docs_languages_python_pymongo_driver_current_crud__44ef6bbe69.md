> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/
> Fetch method: direct_markdown

# CRUD Operations

## Overview

This page contains code examples that show how to connect your Python application to MongoDB with various settings.

To learn more about the connection options on this page, see the link provided in each section.

To use a connection example from this page, copy the code example into the [sample application](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/#std-label-pymongo-crud-sample) or your own application. Be sure to replace all placeholders in the code examples, such as `<hostname>`, with the relevant values for your MongoDB deployment.

### Sample Application

You can use the following sample application to test the code examples on this page. To use the sample application, perform the following steps:

1. Ensure you have PyMongo installed.

2. Copy the following code and paste it into a new `.py` file.

3. Copy a code example from this page and paste it on the specified lines in the file.

Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
import pymongo
from pymongo import MongoClient

try:
    uri = "<connection string URI>"
    client = MongoClient(uri)

    database = client["<database name>"]
    collection = database["<collection name>"]

    # start example code here

    # end example code here

    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

```

</Tab>

<Tab name="Asynchronous">

```python
import asyncio
import pymongo
from pymongo import AsyncMongoClient

async def main():
    try:
        uri = "<connection string URI>"
        client = AsyncMongoClient(uri)

        database = client["<database name>"]
        collection = database["<collection name>"]

        # start example code here

        # end example code here

        await client.close()

    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)

asyncio.run(main())
```

</Tab>

</Tabs>

## Insert One

<Tabs>

<Tab name="Synchronous">

```python
result = collection.insert_one({ "<field name>" : "<value>" })

print(result.acknowledged)
```

</Tab>

<Tab name="Asynchronous">

```python
result = await collection.insert_one({ "<field name>" : "<value>" })

print(result.acknowledged)
```

</Tab>

</Tabs>

To learn more about the `insert_one()` method, see the [Insert Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/insert/#std-label-pymongo-write-insert) guide.

## Insert Multiple

<Tabs>

<Tab name="Synchronous">

```python
document_list = [
   { "<field name>" : "<value>" },
   { "<field name>" : "<value>" }
]

result = collection.insert_many(document_list)

print(result.acknowledged)
```

</Tab>

<Tab name="Asynchronous">

```python
document_list = [
   { "<field name>" : "<value>" },
   { "<field name>" : "<value>" }
]

result = await collection.insert_many(document_list)

print(result.acknowledged)
```

</Tab>

</Tabs>

To learn more about the `insert_many()` method, see the [Insert Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/insert/#std-label-pymongo-write-insert) guide.

## Update One

<Tabs>

<Tab name="Synchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }
update_operation = { "$set" :
    { "<field name>" : "<value>" }
}
result = collection.update_one(query_filter, update_operation)

print(result.modified_count)
```

</Tab>

<Tab name="Asynchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }
update_operation = { "$set" :
    { "<field name>" : "<value>" }
}
result = await collection.update_one(query_filter, update_operation)

print(result.modified_count)
```

</Tab>

</Tabs>

To learn more about the `update_one()` method, see the [Update Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/update/#std-label-pymongo-write-update) guide.

## Update Multiple

<Tabs>

<Tab name="Synchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }
update_operation = { "$set" :
    { "<field name>" : "<value>" }
}
result = collection.update_many(query_filter, update_operation)

print(result.modified_count)
```

</Tab>

<Tab name="Asynchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }
update_operation = { "$set" :
    { "<field name>" : "<value>" }
}
result = await collection.update_many(query_filter, update_operation)

print(result.modified_count)
```

</Tab>

</Tabs>

To learn more about the `update_many()` method, see the [Update Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/update/#std-label-pymongo-write-update) guide.

## Replace One

<Tabs>

<Tab name="Synchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }
replace_document = { "<new document field name>" : "<new document value>" }

result = collection.replace_one(query_filter, replace_document)

print(result.modified_count)
```

</Tab>

<Tab name="Asynchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }
replace_document = { "<new document field name>" : "<new document value>" }

result = await collection.replace_one(query_filter, replace_document)

print(result.modified_count)
```

</Tab>

</Tabs>

To learn more about the `replace_one()` method, see the [Replace Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/replace/#std-label-pymongo-write-replace) guide.

## Delete One

<Tabs>

<Tab name="Synchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }

result = collection.delete_one(query_filter)

print(result.deleted_count)
```

</Tab>

<Tab name="Asynchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }

result = await collection.delete_one(query_filter)

print(result.deleted_count)
```

</Tab>

</Tabs>

To learn more about the `delete_one()` method, see the [Delete Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/delete/#std-label-pymongo-write-delete) guide.

## Delete Multiple

<Tabs>

<Tab name="Synchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }

result = collection.delete_many(query_filter)

print(result.deleted_count)
```

</Tab>

<Tab name="Asynchronous">

```python
query_filter = { "<field to match>" : "<value to match>" }

result = await collection.delete_many(query_filter)

print(result.deleted_count)
```

</Tab>

</Tabs>

To learn more about the `delete_many()` method, see the [Delete Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/delete/#std-label-pymongo-write-delete) guide.

## Bulk Write

<Tabs>

<Tab name="Synchronous">

```python
operations = [
    pymongo.InsertOne(
        {
            "<field name>" : "<value>"
        }
    ),
    pymongo.UpdateMany(
        { "<field to match>" : "<value to match>" },
        { "$set" : { "<field name>" : "<value>" }},
    ),
    pymongo.DeleteOne(
        { "<field to match>" : "<value to match>" }
    ),
]

result = collection.bulk_write(operations)

print(result)
```

</Tab>

<Tab name="Asynchronous">

```python
operations = [
    pymongo.InsertOne(
        {
            "<field name>" : "<value>"
        }
    ),
    pymongo.UpdateMany(
        { "<field to match>" : "<value to match>" },
        { "$set" : { "<field name>" : "<value>" }},
    ),
    pymongo.DeleteOne(
        { "<field to match>" : "<value to match>" }
    ),
]

result = await collection.bulk_write(operations)

print(result)
```

</Tab>

</Tabs>

To learn more about the `bulk_write()` method, see the [Bulk Write](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/bulk-write/#std-label-pymongo-bulk-write) guide.

## Find One

<Tabs>

<Tab name="Synchronous">

```python
results = collection.find_one({ "<field name>" : "<value>" })

print(results)
```

</Tab>

<Tab name="Asynchronous">

```python
results = await collection.find_one({ "<field name>" : "<value>" })

print(results)
```

</Tab>

</Tabs>

To learn more about the `find_one()` method, see [Find One Document](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/find/#std-label-pymongo-retrieve-find-one) in the Retrieve Data guide.

## Find Multiple

<Tabs>

<Tab name="Synchronous">

```python
results = collection.find({ "<field name>" : "<value>" })

for document in results:
    print(document)
```

</Tab>

<Tab name="Asynchronous">

```python
results = collection.find({ "<field name>" : "<value>" })

async for document in results:
    print(document)
```

</Tab>

</Tabs>

To learn more about the `find()` method, see [Find Multiple Documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/find/#std-label-pymongo-retrieve-find-multiple) in the Retrieve Data guide.

## Count Documents in a Collection

<Tabs>

<Tab name="Synchronous">

```python
count = collection.count_documents({})

print(count)
```

</Tab>

<Tab name="Asynchronous">

```python
count = await collection.count_documents({})

print(count)
```

</Tab>

</Tabs>

To learn more about the `count_documents()` method, see the [Retrieve an Accurate Count](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/count/#std-label-pymongo-accurate-count) guide.

## Count Documents Returned from a Query

<Tabs>

<Tab name="Synchronous">

```python
count = collection.count_documents({ "<field name>": "<value>" })

print(count)
```

</Tab>

<Tab name="Asynchronous">

```python
count = await collection.count_documents({ "<field name>": "<value>" })

print(count)
```

</Tab>

</Tabs>

To learn more about the `count_documents()` method, see the [Retrieve an Accurate Count](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/count/#std-label-pymongo-accurate-count) guide.

## Estimated Document Count

<Tabs>

<Tab name="Synchronous">

```python
count = collection.estimated_document_count()

print(count)
```

</Tab>

<Tab name="Asynchronous">

```python
count = await collection.estimated_document_count()

print(count)
```

</Tab>

</Tabs>

To learn more about the `estimated_document_count()` method, see the [Retrieve an Estimated Count](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/count/#std-label-pymongo-estimated-count) guide.

## Retrieve Distinct Values

<Tabs>

<Tab name="Synchronous">

```python
results = collection.distinct("<field name>")

for document in results:
    print(document)
```

</Tab>

<Tab name="Asynchronous">

```python
results = await collection.distinct("<field name>")

for document in results:
    print(document)
```

</Tab>

</Tabs>

To learn more about the `distinct()` method, see the [Retrieve Distinct Field Values](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/distinct/#std-label-pymongo-distinct) guide.
