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

- Enable Authentication

- Compress Network Traffic

- Customize Server Selection

- Stable API

- Limit Server Execution Time

- Connection Pools

- Configure CRUD Operations

To learn how to enable TLS encryption and authentication in PyMongo, see Configure Transport Layer Security (TLS) and Authentication Mechanisms in the Security section.

## API Documentation

To learn more about creating a `MongoClient` object in PyMongo, see the following API documentation:

- MongoClient
