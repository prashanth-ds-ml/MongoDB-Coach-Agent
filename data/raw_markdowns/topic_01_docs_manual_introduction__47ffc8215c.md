> Source: https://www.mongodb.com/docs/manual/introduction/
> Fetch method: direct_markdown

# Introduction to MongoDB

You can create a MongoDB database in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

To learn more about creating a MongoDB database with the Atlas UI, see [Get Started with Atlas](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started).

## Document Database

A record in MongoDB is a document, which is a data structure composed of field and value pairs. MongoDB documents are similar to JSON objects. The values of fields may include other documents, arrays, and arrays of documents.

The advantages of using documents are:

- Documents correspond to native data types in many programming languages.

- Embedded documents and arrays reduce need for expensive joins.

- Dynamic schema supports fluent polymorphism.

### Collections/Views/On-Demand Materialized Views

MongoDB stores documents in [collections](https://www.mongodb.com/docs/core/databases-and-collections/#std-label-collections). Collections are analogous to tables in relational databases.

In addition to collections, MongoDB supports:

- Read-only [Views](https://www.mongodb.com/docs/core/views/)

- [On-Demand Materialized Views](https://www.mongodb.com/docs/core/materialized-views/)

## Key Features

### High Performance

MongoDB provides high performance data persistence. In particular,

- Support for embedded data models reduces I/O activity on database system.

- Indexes support faster queries and can include keys from embedded documents and arrays.

### Query API

The MongoDB Query API supports [read and write operations (CRUD)](https://www.mongodb.com/docs/crud/#std-label-crud) as well as:

- [Data Aggregation](https://www.mongodb.com/docs/core/aggregation-pipeline/#std-label-aggregation-pipeline)

- [Text Search](https://www.mongodb.com/docs/text-search/#std-label-text-search) and [Geospatial Queries](https://www.mongodb.com/docs/tutorial/geospatial-tutorial/).

- [SQL to MongoDB Mapping Chart](https://www.mongodb.com/docs/reference/sql-comparison/)

- [SQL to Aggregation Mapping Chart](https://www.mongodb.com/docs/reference/sql-aggregation-comparison/)

### High Availability

MongoDB's replication facility, called [replica set](https://www.mongodb.com/docs/replication/), provides:

- *automatic* failover

- data redundancy.

A [replica set](https://www.mongodb.com/docs/replication/) is a group of MongoDB servers that maintain the same data set, providing redundancy and increasing data availability.

### Horizontal Scalability

MongoDB provides horizontal scalability as part of its *core* functionality:

- [Sharding](https://www.mongodb.com/docs/sharding/#std-label-sharding-introduction) distributes data across a cluster of machines.

- Starting in 3.4, MongoDB supports creating [zones](https://www.mongodb.com/docs/core/zone-sharding/#std-label-zone-sharding) of data based on the [shard key](https://www.mongodb.com/docs/reference/glossary/#std-term-shard-key). In a balanced cluster, MongoDB directs reads and writes covered by a zone only to those shards inside the zone. See the [Zones](https://www.mongodb.com/docs/core/zone-sharding/#std-label-zone-sharding) manual page for more information.

### Support for Multiple Storage Engines

MongoDB supports [multiple storage engines](https://www.mongodb.com/docs/core/storage-engines/):

- [WiredTiger Storage Engine](https://www.mongodb.com/docs/core/wiredtiger/) (including support for [Encryption at Rest](https://www.mongodb.com/docs/core/security-encryption-at-rest/))

- [In-Memory Storage Engine for Self-Managed Deployments](https://www.mongodb.com/docs/core/inmemory/).

In addition, MongoDB provides pluggable storage engine API that allows third parties to develop storage engines for MongoDB.
