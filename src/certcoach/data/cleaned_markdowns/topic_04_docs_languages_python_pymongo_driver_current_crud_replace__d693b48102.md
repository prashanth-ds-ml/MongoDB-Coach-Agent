> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/replace/
> Fetch method: direct_markdown

# Replace Documents

## Overview

In this guide, you can learn how to use PyMongo to perform a replace operation on a document in a MongoDB collection. A replace operation performs differently than an update operation. An update operation modifies only the specified fields in a target document. A replace operation removes *all* fields in the target document and replaces them with new ones.

To learn more about update operations, see the Update Documents guide.

### Sample Data

The examples in this guide use the `sample_restaurants.restaurants` collection from the Atlas sample datasets. To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see the Get Started with PyMongo tutorial.

## Replace Operation

You can perform a replace operation in MongoDB by using the `replace_one()` method. This method removes all fields except the `_id` field from the first document that matches the search criteria. It then inserts the fields and values you specify into the document.

### Required Parameters

The `replace_one()` method requires the following parameters:

- A **query filter** document, which determines which documents to replace. For more information about query filters, see the Query Filter Documents section in the MongoDB Server manual.

- A **replace** document, which specifies the fields and values to insert in the new document.

## Replace One

The following example uses the `replace_one()` method to replace the fields and values of a document with a `name` field value of `"Pizza Town"`:

```python
restaurants = database["restaurants"]

query_filter = {"name" : "Pizza Town"}
replace_document = { "name" : "Mongo's Pizza",
                     "cuisine" : "Pizza",
                     "address" : {
                         "street" : "123 Pizza St",
                         "zipCode" : "10003"
                     },
                     "borough" : "Manhattan"
                   }

result = restaurants.replace_one(query_filter, replace_document)
```

The values of `_id` fields are immutable. If your replacement document specifies a value for the `_id` field, it must match the `_id` value of the existing document.

### Customize the Replace Operation

The `replace_one()` method optionally accepts additional parameters, which represent options you can use to configure the replace operation. If you don't specify any additional options, the driver does not customize the replace operation.

| Property | Description |
| --- | --- |
| `upsert` | Specifies whether the replace operation performs an upsert operation if no documents match the query filter. For more information, see the upsert statement in the MongoDB Server manual.Defaults to `False` |
| `bypass_document_validation` | Specifies whether the replace operation bypasses document validation. This lets you replace documents that don't meet the schema validation requirements, if any exist. For more information about schema validation, see Schema Validation in the MongoDB Server manual.Defaults to `False`. |
| `collation` | Specifies the kind of language collation to use when sorting results. For more information, see Collation in the MongoDB Server manual. |
| `hint` | Gets or sets the index to scan for documents. For more information, see the hint statement in the MongoDB Server manual. |
| `session` | An instance of `ClientSession`. |
| `let` | A Map of parameter names and values. Values must be constant or closed expressions that don't reference document fields. For more information, see the let statement in the MongoDB Server manual. |
| `comment` | A comment to attach to the operation. For more information, see the insert command fields guide in the MongoDB Server manual. |
The following code uses the `replace_one()` method to find the first document where the `name` field has the value `"Food Town"`, then replaces this document with a new document named `"Food World"`. Because the `upsert` option is set to `True`, the driver inserts a new document if the query filter doesn't match any existing documents.

```python
restaurants = database["restaurants"]

query_filter = {"name" : "Food Town"}
replace_document = { "name" : "Food World",
                     "cuisine" : "Mixed",
                     "address" : {
                         "street" : "123 Food St",
                         "zipCode" : "10003"
                     },
                     "borough" : "Manhattan"
                   }

result = restaurants.replace_one(query_filter, replace_document, upsert = True)
```

### Return Value

The `replace_one()` method returns an `UpdateResult` object. The `UpdateResult` type contains the following properties:

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

- replace_one()

- UpdateResult
