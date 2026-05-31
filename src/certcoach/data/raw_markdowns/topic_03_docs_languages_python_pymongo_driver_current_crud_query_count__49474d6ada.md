> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/count/
> Fetch method: direct_markdown

# Count Documents

## Overview

In this guide, you can learn how to retrieve an accurate and estimated count of the number of documents in a collection.

## Retrieve an Accurate Count

Use the `count_documents()` method to count the number of documents that are in a collection. To count the number of documents that match a specific search critera, pass a dictionary that includes a query filter to the `count_documents()` method.

To learn more about specifying a query, see [Specify a Query](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/query/specify-query/#std-label-pymongo-specify-query).

### Count All Documents

To return a count of all documents in the collection, pass an empty dictionary to the `count_documents()` method, as shown in the following example. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
collection.count_documents({})
```

</Tab>

<Tab name="Asynchronous">

```python
await collection.count_documents({})
```

</Tab>

</Tabs>

### Count Specific Documents

To return a count of documents that match specific search criteria, specify your query in the `count_documents()` method, as shown in the following example. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
collection.count_documents({ "author": "Mike" })
```

</Tab>

<Tab name="Asynchronous">

```python
await collection.count_documents({ "author": "Mike" })
```

</Tab>

</Tabs>

### Customize Count Behavior

The `count_documents()` method accepts optional parameters, which represent options you can use to configure the count operation. If you don't specify any options, the driver does not customize the count operation.

The following table describes the options you can set to customize `count_documents()`:

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
`comment`

</td>
<td headers="Description">
A comment to attach to the operation.

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
`skip`

</td>
<td headers="Description">
The number of documents to skip before returning results.

</td>
</tr>
<tr>
<td headers="Property">
`limit`

</td>
<td headers="Description">
The maximum number of documents to count. Must be a positive integer.

</td>
</tr>
<tr>
<td headers="Property">
`maxTimeMS`

</td>
<td headers="Description">
The maximum amount of time to allow the operation to run, in milliseconds.

</td>
</tr>
<tr>
<td headers="Property">
`collation`

</td>
<td headers="Description">
An instance of `Collation`.

</td>
</tr>
<tr>
<td headers="Property">
`hint`

</td>
<td headers="Description">
Gets or sets the index to scan for documents.

</td>
</tr>
</table>

## Retrieve an Estimated Count

You can get an estimate of the number of documents in a collection by calling the `estimated_document_count()` method. The method estimates the amount of documents based on collection metadata, which might be faster than performing an accurate count.

The following example estimates the number of documents in a collection. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
collection.estimated_document_count()
```

</Tab>

<Tab name="Asynchronous">

```python
await collection.estimated_document_count()
```

</Tab>

</Tabs>

### Customize Estimated Count Behavior

The `estimated_document_count()` method accepts optional parameters, which represent options you can use to configure the count operation. If you don't specify any options, the driver does not customize the count operation.

The following table describes the options you can set to customize `estimated_document_count()`:

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
`comment`

</td>
<td headers="Description">
A comment to attach to the operation.

</td>
</tr>
<tr>
<td headers="Property">
`maxTimeMS`

</td>
<td headers="Description">
The maximum amount of time to allow the operation to run, in milliseconds.

</td>
</tr>
</table>

## Troubleshooting

### DeprecationWarning: Count Is Deprecated

PyMongo no longer supports the `count()` method. Instead, use the `count_documents()` method from the `Collection` class.

The `count_documents()` method belongs to the `Collection` class. If you try to call `Cursor.count_documents()`, PyMongo raises the following error:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Cursor' object has no attribute 'count'
```

## API Documentation

To learn more about any of the methods or types discussed in this guide, see the following API documentation:

- [count_documents()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.count_documents)

- [estimated_document_count()](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collection.html#pymongo.collection.Collection.count_documents)

- [Collation](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/collation.html#pymongo.collation.Collation)

- [ClientSession](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/client_session.html#pymongo.client_session.ClientSession)
