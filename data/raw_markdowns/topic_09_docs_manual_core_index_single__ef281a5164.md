> Source: https://www.mongodb.com/docs/manual/core/index-single/
> Fetch method: html_fallback

# Single Field Indexes - Database Manual - MongoDB Docs Single Field Indexes

Single Field Indexes - Database Manual - MongoDB Docs

[Make the MongoDB docs better! We value your opinion. Share your feedback for a chance to win $100.](https://research.rallyuxr.com/recruit/clf9wl0m50006e31jbdt7hn51/study/cmobv8cnk2hpei2l3h8qw9zax?channel=share)

[Click here >](https://research.rallyuxr.com/recruit/clf9wl0m50006e31jbdt7hn51/study/cmobv8cnk2hpei2l3h8qw9zax?channel=share)

Docs Menu

Ask MongoDB AI

[Docs Home](https://www.mongodb.com/docs/)/
/
[Types](/docs/manual/core/indexes/index-types)

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Indexes](/docs/manual/indexes)/
[Types](/docs/manual/core/indexes/index-types)

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Indexes](/docs/manual/indexes)/
[Types](/docs/manual/core/indexes/index-types)

# Single Field Indexes

Copy page

Single field indexes store information from a single field in a collection. By default, all collections have an index on the [_id field](/docs/manual/indexes/#std-label-index-type-id). You can add additional indexes to speed up important queries and operations.

You can create an index on any field in a document, including top-level fields, embedded fields, or fields inside embedded documents. When you create an index, specify the field and the sort order ( `1 `for ascending, `-1 `for descending).

To create a single-field index, use the following prototype:

```

db.<collection>.createIndex( { <field>: <sort-order> } )
```

This image shows an ascending index on a single field, `score `:

In this example, each document in the collection that has a value for the `score `field is added to the index in ascending order.

You can [create and manage single field indexes in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/indexes/)for deployments hosted in [MongoDB Atlas](https://www.mongodb.com/docs/atlas)[.](https://www.mongodb.com/docs/atlas)

## Use Cases

If your application repeatedly runs queries on the same field, you can create an index on that field to improve performance. For example, your human resources department often needs to look up employees by employee ID. You can create an index on the employee ID field to improve the performance of that query.

## Get Started

To create an index on a single field, see these examples:

-
[Create an Index on a Single Field](/docs/manual/core/indexes/index-types/index-single/create-single-field-index/#std-label-index-create-ascending-single-field)

-
[Create an Index on an Embedded Field](/docs/manual/core/indexes/index-types/index-single/create-single-field-index/#std-label-index-embedded-fields)

-
[Create an Index on an Embedded Document](/docs/manual/core/indexes/index-types/index-single/create-embedded-object-index/#std-label-index-embedded-documents)

[Back](/docs/manual/core/indexes/index-types/)

[Types](/docs/manual/core/indexes/index-types/)

[Next](/docs/manual/core/indexes/index-types/index-single/create-single-field-index/)

[Create](/docs/manual/core/indexes/index-types/index-single/create-single-field-index/)

Rate this page

On this page

- [Use Cases](#use-cases)

- [Get Started](#get-started)

On this page

- [Use Cases](#use-cases)

- [Get Started](#get-started)
