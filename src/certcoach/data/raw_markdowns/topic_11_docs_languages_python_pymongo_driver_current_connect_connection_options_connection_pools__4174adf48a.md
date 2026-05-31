> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/connection-pools/
> Fetch method: direct_markdown

# Connection Pools

## Overview

In this guide, you can learn about how PyMongo uses connection pools to manage connections to a MongoDB deployment and how you can configure connection pool settings in your application.

A connection pool is a cache of open database connections maintained by PyMongo. When your application requests a connection to MongoDB, PyMongo seamlessly gets a connection from the pool, performs operations, and returns the connection to the pool for reuse.

Connection pools help reduce application latency and the number of times new connections are created by PyMongo.

## Configuring Connection Pools

You can specify the following connection pool settings in your `MongoClient` object or in your connection URI:

<table>
<tr>
<th id="Setting">
Setting

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Setting">
`connectTimeoutMS`

</td>
<td headers="Description">
The time that PyMongo waits when establishing a new connection before timing out.**Data Type**: `int`**Default**: `20000`**MongoClient Example**: `connectTimeoutMS = 40000`**Connection URI Example**: `connectTimeoutMS=40000`

</td>
</tr>
<tr>
<td headers="Setting">
`maxConnecting`

</td>
<td headers="Description">
The maximum number of connections that each pool can establish concurrently. If this limit is reached, further requests wait until a connection is established or another in-use connection is checked back into the pool.**Data Type**: `int`**Default**: `2`**MongoClient Example**: `maxConnecting = 3`**Connection URI Example**: `maxConnecting=3`

</td>
</tr>
<tr>
<td headers="Setting">
`maxIdleTimeMS`

</td>
<td headers="Description">
The maximum time that a connection can remain idle in the pool. When a connection exceeds this limit, PyMongo closes the connection and removes it from the pool. Set this value higher than your application's expected idle period but lower than firewall or proxy connection timeouts to prevent unexpected disconnections.**Data Type**: `int`**Default**: `None` (no limit)**MongoClient Example**: `maxIdleTimeMS = 60000`**Connection URI Example**: `maxIdleTimeMS=60000`

</td>
</tr>
<tr>
<td headers="Setting">
`maxPoolSize`

</td>
<td headers="Description">
The maximum number of concurrent connections that the pool maintains. If the maximum pool size is reached, further requests wait until a connection becomes available.**Data Type**: `int`**Default**: `100`**MongoClient Example**: `maxPoolSize = 150`**Connection URI Example**: `maxPoolSize=150`

</td>
</tr>
<tr>
<td headers="Setting">
`minPoolSize`

</td>
<td headers="Description">
The minimum number of concurrent connections that the pool maintains. If the number of open connections falls below this value due to network errors, PyMongo attempts to create new connections to maintain this minimum.**Data Type**: `int`**Default**: `0`**MongoClient Example**: `minPoolSize = 3`**Connection URI Example**: `minPoolSize=3`

</td>
</tr>
<tr>
<td headers="Setting">
`socketTimeoutMS`

</td>
<td headers="Description">
The length of time that PyMongo waits for a response from the server before timing out.**Data Type**: `int`**Default**: `None` (no timeout)**MongoClient Example**: `socketTimeoutMS = 100000`**Connection URI Example**: `socketTimeoutMS=100000`

</td>
</tr>
<tr>
<td headers="Setting">
`waitQueueTimeoutMS`

</td>
<td headers="Description">
How long a thread waits for a connection to become available in the connection pool before timing out.**Data Type**: `int`**Default**: `None` (no timeout)**MongoClient Example**: `waitQueueTimeoutMS = 100000`**Connection URI Example**: `waitQueueTimeoutMS=100000`

</td>
</tr>
</table>The following code creates a client with a maximum connection pool size of `50` by using the `maxPoolSize` parameter. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
client = MongoClient(host, port, maxPoolSize=50)
```

</Tab>

<Tab name="Asynchronous">

```python
client = AsyncMongoClient(host, port, maxPoolSize=50)
```

</Tab>

</Tabs>

The following code creates a client with the same configuration as the preceding example, but uses a connection URI:

<Tabs>

<Tab name="Synchronous">

```python
client = MongoClient(host, port, maxPoolSize=50)
```

</Tab>

<Tab name="Asynchronous">

```python
client = AsyncMongoClient(host, port, maxPoolSize=50)
```

</Tab>

</Tabs>

## Additional Information

To learn more about connection pools, see [Connection Pool Overview](https://www.mongodb.com/docs/manual/administration/connection-pool-overview/) in the MongoDB Server manual.

### API Documentation

To learn more about any of the methods or types discussed in this guide, see the following API documentation:

- [MongoClient](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient)
