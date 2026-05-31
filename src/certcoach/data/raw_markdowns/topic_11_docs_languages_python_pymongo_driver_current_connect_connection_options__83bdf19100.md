> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/
> Fetch method: direct_markdown

# Specify Connection Options

## Overview

This section describes the MongoDB connection and authentication options available in PyMongo. You can configure your connection by using either the connection URI or arguments to the `MongoClient` constructor.

### Using the Connection URI

If you pass a connection URI to the `MongoClient` constructor, you can include connection options in the string as `<name>=<value>` pairs. In the following example, the connection URI contains the `connectTimeoutMS` option with a value of `60000` and the `tls` option with a value of `true`. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
uri = "mongodb://<hostname>:<port>/?connectTimeoutMS=60000&tls=true"
client = pymongo.MongoClient(uri)
```

</Tab>

<Tab name="Asynchronous">

```python
uri = "mongodb://<hostname>:<port>/?connectTimeoutMS=60000&tls=true"
client = pymongo.AsyncMongoClient(uri)
```

</Tab>

</Tabs>

### Using a `MongoClient`

You can pass connection options as arguments to the `MongoClient` constructor instead of including them in your connection URI. Configuring the connection this way makes it easier to change settings at runtime and helps you catch errors during compilation. The following example shows how to use the `MongoClient` constructor to set connection options. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
uri = "mongodb://<hostname>:<port>"
client = pymongo.MongoClient(uri, connectTimeoutMS=60000, tls=True)
```

</Tab>

<Tab name="Asynchronous">

```python
uri = "mongodb://<hostname>:<port>"
client = pymongo.AsyncMongoClient(uri, connectTimeoutMS=60000, tls=True)
```

</Tab>

</Tabs>

## Connection Options

To learn about the connection options available in PyMongo, see the following sections:

- [Enable Authentication](https://www.mongodb.com/docs/languages/python/pymongo-driver/security/#std-label-pymongo-security)

- [Compress Network Traffic](https://www.mongodb.com/docs/languages/python/pymongo-driver/connect/connection-options/network-compression/#std-label-pymongo-network-compression)

- [Customize Server Selection](https://www.mongodb.com/docs/languages/python/pymongo-driver/connect/connection-options/server-selection/#std-label-pymongo-server-selection)

- [Stable API](https://www.mongodb.com/docs/languages/python/pymongo-driver/connect/connection-options/stable-api/#std-label-pymongo-stable-api)

- [Limit Server Execution Time](https://www.mongodb.com/docs/languages/python/pymongo-driver/connect/connection-options/csot/#std-label-pymongo-csot)

- [Connection Pools](https://www.mongodb.com/docs/languages/python/pymongo-driver/connect/connection-options/connection-pools/#std-label-pymongo-connection-pools)

- [Configure CRUD Operations](https://www.mongodb.com/docs/languages/python/pymongo-driver/crud/configure/#std-label-pymongo-configure-crud)

To learn how to enable TLS encryption and authentication in PyMongo, see [Configure Transport Layer Security (TLS)](https://www.mongodb.com/docs/languages/python/pymongo-driver/security/tls/#std-label-pymongo-tls) and [Authentication Mechanisms](https://www.mongodb.com/docs/languages/python/pymongo-driver/security/authentication/#std-label-pymongo-auth) in the Security section.

## API Documentation

To learn more about creating a `MongoClient` object in PyMongo, see the following API documentation:

- [MongoClient](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient)
