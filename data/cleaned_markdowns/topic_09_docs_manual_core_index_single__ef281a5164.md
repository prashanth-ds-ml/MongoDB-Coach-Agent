> Source: https://www.mongodb.com/docs/manual/core/index-single/
> Fetch method: html_fallback

# Single Field Indexes - Database Manual - MongoDB Docs Single Field Indexes

Single Field Indexes - Database Manual - MongoDB Docs

Make the MongoDB docs better! We value your opinion. Share your feedback for a chance to win $100.

Click here >

Docs Menu

Ask MongoDB AI

Docs Home/
/
Types

Docs Home/
Development/
Indexes/
Types

Docs Home/
Development/
Indexes/
Types

# Single Field Indexes

Copy page

Single field indexes store information from a single field in a collection. By default, all collections have an index on the _id field. You can add additional indexes to speed up important queries and operations.

You can create an index on any field in a document, including top-level fields, embedded fields, or fields inside embedded documents. When you create an index, specify the field and the sort order ( `1 `for ascending, `-1 `for descending).

To create a single-field index, use the following prototype:

```

db.<collection>.createIndex( { <field>: <sort-order> } )
```

This image shows an ascending index on a single field, `score `:

In this example, each document in the collection that has a value for the `score `field is added to the index in ascending order.

You can create and manage single field indexes in the UIfor deployments hosted in MongoDB Atlas.

## Use Cases

If your application repeatedly runs queries on the same field, you can create an index on that field to improve performance. For example, your human resources department often needs to look up employees by employee ID. You can create an index on the employee ID field to improve the performance of that query.

## Get Started

To create an index on a single field, see these examples:

-
Create an Index on a Single Field

-
Create an Index on an Embedded Field

-
Create an Index on an Embedded Document

Back

Types

Next

Create

Rate this page

On this page

- Use Cases

- Get Started

On this page

- Use Cases

- Get Started
