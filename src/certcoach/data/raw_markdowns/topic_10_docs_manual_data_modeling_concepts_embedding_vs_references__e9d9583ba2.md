> Source: https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/
> Fetch method: html_fallback

# Best Practices for Data Modeling in MongoDB - Database Manual - MongoDB Docs Best Practices for Data Modeling in MongoDB

Best Practices for Data Modeling in MongoDB - Database Manual - MongoDB Docs

[Make the MongoDB docs better! We value your opinion. Share your feedback for a chance to win $100.](https://research.rallyuxr.com/recruit/clf9wl0m50006e31jbdt7hn51/study/cmobv8cnk2hpei2l3h8qw9zax?channel=share)

[Click here >](https://research.rallyuxr.com/recruit/clf9wl0m50006e31jbdt7hn51/study/cmobv8cnk2hpei2l3h8qw9zax?channel=share)

Docs Menu

Ask MongoDB AI

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Data Modeling](/docs/manual/data-modeling)

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Data Modeling](/docs/manual/data-modeling)

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Data Modeling](/docs/manual/data-modeling)

# Best Practices for Data Modeling in MongoDB

Copy page

MongoDB's flexible data model allows you to strategically balance performance and adaptability while ensuring data consistency and integrity. In addition to the general guidance on [planning your schema](/docs/manual/data-modeling/schema-design-process/#std-label-data-modeling-schema-design), consider the following best practices to optimize your data model and determine which [schema design pattern](/docs/manual/data-modeling/design-patterns/#std-label-schema-design-patterns)may be best suited for your application use case.

## Plan Your Schema Early and Iterate

Plan and design your schema early in the development process. This helps prevent performance issues as your application grows.

MongoDB's flexible schema allows you to design your schema iteratively. However, it can still be difficult to modify large-scale schemas that are used in production. Depending on your application, you may want to establish a simple schema to cover basic functionality before optimizing.

### Modify Your Data Model

Consider the following example:

You're tasked with building the backend of an online user learning platform that stores information on courses and their lessons. Initially, the platform only needs to store the following basic information for each course:

-
Course title

-
Instructor

-
Description

-
Lessons, embedded as an array of sub-documents inside each course document. At this time, each lesson sub-document only contains a title, description, and presentation slides.

As the platform evolves, each course needs additional learning and testing formats, such as videos, quizzes, assignments, and external resource links. Embedding all of this new data in each course document would make the data model too complex.

Instead, consider creating a separate `lessons `collection. This way, you can link the `course `and `lessons `collections by using [reference](/docs/manual/data-modeling/referencing/#std-label-data-modeling-referencing)IDs. By using references, each lesson can include different content types and be more flexible for future format changes.

## Link Related Data

When you design your data model in MongoDB, consider the structure of your documents and the ways your application uses data from related entities.

To link related data, you can either:

-
Embed related data within a single document.

-
Reference related data stored in a separate collection.

For examples of when to use embedding or referencing, refer to the following table:

Scenario

Linking Method

Keeping related data together will lead to a simpler data model and code.

Embedding

You have a "has-a" or "contains" relationship between entities.

Embedding

Your application queries pieces of information together.

Embedding

You have data that's often updated together.

Embedding

You have data that should be archived at the same time.

Embedding

The child side of the relationship has high cardinality.

Referencing

Data duplication is too complicated to manage and not preferred.

Referencing

The combined size of your data takes up too much memory or transfer bandwidth for your application.

Referencing

Your embedded data grows without bounds.

Referencing

Your data is written at different times in a write-heavy workload.

Referencing

For the child side of the relationship, your data can exist by itself without a parent.

Referencing

To learn more about use cases, performance considerations, and benefits for each data-linking method, see:

-
[Embedded Data in Your MongoDB Schema](/docs/manual/data-modeling/embedding/#std-label-data-modeling-embedding)

-
[Reference Data in Your MongoDB Schema](/docs/manual/data-modeling/referencing/#std-label-data-modeling-referencing)

## Duplicate Data

When you embed related data in a single document, you may duplicate data between two collections. Duplicating data lets your application query related information about multiple entities in a single query while logically separating entities in your model.

Before you duplicate data, consider the following factors:

-
The performance benefit for reads when data is duplicated. Duplicating data can remove the need to perform joins across multiple collections, which can improve application performance.

-
How often the duplicated data needs to be updated. The extra logic needed to handle infrequent updates is less costly than performing joins (lookups) on read operations. However, frequently updating duplicate data can cause heavy workloads and performance issues.

The following table lists the different types of duplicate data that might exist in your schema:

Type of Duplicate Data

Description

Example

Immutable

Data that never changes. Immutable data is a good candidate for data duplication

The date a user account was created.

Temporal

Data that may change over time, but where it is important to preserve the historical value of the data.

The address of a customer at the time that they placed an order. If the customer moves to a new address, it doesn't affect the recorded addresses where previous orders were shipped.

Sensitive to staleness

Data that requires frequent updates to ensure that all occurrences of the data are consistent. Applications can use transactions or triggers to update all occurrences.

The number of items in stock for a given product, which needs to be updated every time a customer places an order for the product.

Not sensitive to staleness

Data that can tolerate staleness for a longer period of time. Applications can use a background job to periodically update all occurrences of the data based on acceptable staleness and the cost of updates.

A list of recommended products for a customer, which doesn't need to be recomputed every time a new product is added to the system.

If you don't need to update the duplicated data often, minimal additional work would be required to keep the two collections consistent. However, if the duplicated data is updated often, using a [reference](/docs/manual/data-modeling/referencing/#std-label-data-modeling-referencing)to link related data may be a better approach.

For examples on how duplicating related data can help optimize your data model, see [Handle Duplicate Data](/docs/manual/data-modeling/handle-duplicate-data/#std-label-data-modeling-duplicate-data)[.](/docs/manual/data-modeling/handle-duplicate-data/#std-label-data-modeling-duplicate-data)

### Enforce Data Consistency

If you duplicate data in your schema, you need to decide how to keep your data consistent across multiple collections. For example, an e-commerce platform likely requires continuously up-to-date data to provide the real-time status of its product stock. On the other hand, applications that handle data for longer-term strategic decisions, such as social media analytics, can tolerate reading slightly stale data.

You can enforce data consistency in your application with any of the following methods:

-
[Embedding related data](/docs/manual/data-modeling/enforce-consistency/embed-data/#std-label-enforce-consistency-embedding)

-
[Transactions](/docs/manual/data-modeling/enforce-consistency/embed-data/#std-label-enforce-consistency-embedding)

-
[Atlas Database Triggers](https://www.mongodb.com/docs/atlas/atlas-ui/triggers/database-triggers/#std-label-atlas-database-trigger)

To learn more about each data consistency enforcement method, their use cases, and their performance tradeoffs, see [Data Consistency](/docs/manual/data-modeling/data-consistency/#std-label-data-modeling-data-consistency)[.](/docs/manual/data-modeling/data-consistency/#std-label-data-modeling-data-consistency)

## Enforce Schema with Validation Rules

Your schema validation needs depend on how your application organizes data. Schema validation is most useful for an established application with a defined data structure.

## Note

Schema validation rules are also flexible, so they don't need to cover every field in a document, unless your application requires that they do.

You can use schema validation in the following scenarios:

-
For an `events `collection, ensure that the `start_date `field stores only a date, not a string. Consistent types prevent unexpected values in connecting applications.

-
For a `store `collection, ensure that the `accepted_credit_cards `field contains only accepted card types, such as `["Visa", "MasterCard", "American Express"] `. This rule prevents users from entering unsupported values.

-
For a `students `collection, ensure that the `gpa `field is always a positive floating-point number. This rule prevents data entry errors.

To learn more, see [Schema Validation](/docs/manual/core/schema-validation/#std-label-schema-validation-overview)[.](/docs/manual/core/schema-validation/#std-label-schema-validation-overview)

## Index Commonly Queried Fields

When designing your data model, think about how you access and store your data. If you frequently query, filter, sort, or join specific fields, consider creating [indexes](/docs/manual/indexes/#std-label-indexes)on those fields. With indexes, MongoDB can:

-
Return query results faster

-
Sort results more efficiently

-
Optimize `$lookup `and `$group `operations

-
Reduce CPU and I/O usage

As your application grows, [monitor your deployment's index use](/docs/manual/tutorial/measure-index-use/#std-label-indexes-measuring-use)to ensure that your indexes still support relevant queries.

When you create indexes, consider the following index behaviors:

-
Each index requires at least 8 kB of data space.

-
Adding an index has some negative performance impact for write operations. For collections with high write-to-read ratio, indexes are expensive since each insert must also update any indexes.

-
Collections with high read-to-write ratio often benefit from additional indexes. Indexes do not affect un-indexed read operations.

-
When active, each index consumes disk space and memory. This usage can be significant and should be tracked for capacity planning, especially for concerns over working set size.

For more information on indexes, see [Indexing Strategies](/docs/manual/applications/indexes/#std-label-indexing-strategies)[.](/docs/manual/applications/indexes/#std-label-indexing-strategies)

## Additional Considerations

When developing a data model, analyze all of your application's [read and write operations](/docs/manual/crud/#std-label-crud)in conjunction with the following considerations.

### Atomicity

In MongoDB, a write operation is [atomic](/docs/manual/reference/glossary/#std-term-atomic-operation)on the level of a single document. This means that even if an update operation affects several sub-documents, either all of those sub-documents are updated, or the operation fails entirely and no updates occur.

A denormalized data model that uses embedded documents and arrays combines all related data in a single document instead of normalizing across multiple documents and collections. This data model allows atomic operations, in contrast to a normalized model where operations affect multiple documents and collections. For an example data model that provides atomic updates for a single document, see [Model Data for Atomic Operations](/docs/manual/tutorial/model-data-for-atomic-operations/#std-label-data-modeling-atomic-operation)[.](/docs/manual/tutorial/model-data-for-atomic-operations/#std-label-data-modeling-atomic-operation)

For data models that store references between related pieces of data, the application must issue separate read and write operations to retrieve and modify these related pieces of data.

For situations that require atomicity of reads and writes to multiple documents (in a single or multiple collections), MongoDB supports distributed transactions, including transactions on replica sets and sharded clusters.

For more information, see [Transactions](/docs/manual/core/transactions/#std-label-transactions)[.](/docs/manual/core/transactions/#std-label-transactions)

## Important

In most cases, a distributed transaction incurs a greater performance cost over single document writes, and the availability of distributed transactions should not be a replacement for effective schema design. For many scenarios, the [denormalized data model (embedded documents and arrays)](/docs/manual/data-modeling/embedding/#std-label-data-modeling-embedding)will continue to be optimal for your data and use cases. That is, for many scenarios, modeling your data appropriately will minimize the need for distributed transactions.

For additional transactions usage considerations (such as runtime limit and oplog size limit), see also [Production Considerations](/docs/manual/core/transactions-production-consideration/#std-label-production-considerations)[.](/docs/manual/core/transactions-production-consideration/#std-label-production-considerations)

### Data Lifecycle Management

Data lifecycle management refers to the process of managing data from creation and storage to archiving and deletion. To ensure schema cost-efficiency, performance, and security, consider data life cycle management when making data modeling decisions.

If your application requires some data to persist in the database for a limited period of time, consider using the [Time to Live or TTL feature](/docs/manual/tutorial/expire-data/#std-label-ttl-collections). For example, TTL collections could be useful for managing user login sessions on a web application, where sessions are set to automatically expire after 30 minutes of inactivity. This means that MongoDB automatically deletes the session documents after the specified time period.

Additionally, if your application only uses recently inserted documents, consider [Capped Collections](/docs/manual/core/capped-collections/#std-label-manual-capped-collection). Capped collections provide first-in-first-out (FIFO) management of inserted documents and efficiently support operations that insert and read documents based on insertion order.

### Hardware Constraints

When you design your schema, consider your deployment's hardware, especially the amount of available RAM. Larger documents use more RAM, which may cause your application to read from disk and degrade performance. When possible, design your schema so only relevant fields are returned by queries, ensuring that your application's [working set](/docs/manual/reference/glossary/#std-term-working-set)does not grow unnecessarily large.

### Small Documents

Each MongoDB document contains a certain amount of overhead. This overhead is normally insignificant but becomes significant if all documents are just a few bytes, as might be the case if the documents in your collection only have one or two fields.

Consider the following suggestions and strategies for optimizing storage utilization for these collections:

-
Use the `_id `field explicitly.

MongoDB clients automatically add an `_id `field to each document and generate a unique 12-byte [ObjectId](/docs/manual/reference/glossary/#std-term-ObjectId)for the `_id `field. Furthermore, MongoDB always indexes the `_id `field. For smaller documents, this may use a significant amount of space.

To optimize storage use, you can explicitly specify a value for the `_id `field when inserting documents into the collection. This allows applications to store a value in the `_id `field that would have occupied space in another portion of the document. This value must be unique, as the `_id `field uniquely identifies documents in a collection.

-
Use shorter field names.

## Note

While shortening field names can reduce BSON size in MongoDB, it's often more effective to modify the overall document model to reduce BSON size. Shortening field names might reduce expressiveness, and does not affect the size of indexes, as indexes have a predefined structure that does not incorporate field names.

MongoDB stores all field names in every document. For most documents, this represents a small fraction of the space used by a document; however, for small documents the field names may represent a proportionally large amount of space. Consider a collection of small documents that resemble the following:

```

{ last_name : "Smith", best_score: 3.9 }
```

If you shorten the field named `last_name `to `lname `and the field named `best_score `to `score `, as follows, you could save 9 bytes per document.

```

{ lname : "Smith", score : 3.9 }
```

-
Embed documents.

In some cases you may want to embed documents in other documents and save on the per-document overhead. See [Collections with a Large Number of Small Documents](/docs/manual/data-modeling/embedding/#std-label-faq-developers-embed-documents)[.](/docs/manual/data-modeling/embedding/#std-label-faq-developers-embed-documents)

## Learn More

To learn more about how to structure your documents and define your schema, see MongoDB University's [Data Modeling](https://learn.mongodb.com/learning-paths/data-modeling-for-mongodb)course.

[Back](/docs/manual/data-modeling/)

[Data Modeling](/docs/manual/data-modeling/)

[Next](/docs/manual/data-modeling/embedding/)

[Embedded Data](/docs/manual/data-modeling/embedding/)

Rate this page

On this page

- [Plan Your Schema Early and Iterate](#plan-your-schema-early-and-iterate)

- [Modify Your Data Model](#modify-your-data-model)

- [Link Related Data](#link-related-data)

- [Duplicate Data](#duplicate-data)

- [Enforce Data Consistency](#enforce-data-consistency)

- [Enforce Schema with Validation Rules](#enforce-schema-with-validation-rules)

- [Index Commonly Queried Fields](#index-commonly-queried-fields)

- [Additional Considerations](#additional-considerations)

- [Atomicity](#atomicity)

- [Data Lifecycle Management](#data-lifecycle-management)

- [Hardware Constraints](#hardware-constraints)

- [Small Documents](#small-documents)

- [Learn More](#learn-more)

On this page

- [Plan Your Schema Early and Iterate](#plan-your-schema-early-and-iterate)

- [Modify Your Data Model](#modify-your-data-model)

- [Link Related Data](#link-related-data)

- [Duplicate Data](#duplicate-data)

- [Enforce Data Consistency](#enforce-data-consistency)

- [Enforce Schema with Validation Rules](#enforce-schema-with-validation-rules)

- [Index Commonly Queried Fields](#index-commonly-queried-fields)

- [Additional Considerations](#additional-considerations)

- [Atomicity](#atomicity)

- [Data Lifecycle Management](#data-lifecycle-management)

- [Hardware Constraints](#hardware-constraints)

- [Small Documents](#small-documents)

- [Learn More](#learn-more)
