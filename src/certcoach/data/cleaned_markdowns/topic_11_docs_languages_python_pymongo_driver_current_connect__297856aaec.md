> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/
> Fetch method: direct_markdown

# Connect to MongoDB

## Overview

This page contains code examples that show how to connect your Python application to MongoDB with various settings.

To learn more about the connection options on this page, see the link provided in each section.

To use a connection example from this page, copy the code example into the sample application or your own application. Be sure to replace all placeholders in the code examples, such as `<hostname>`, with the relevant values for your MongoDB deployment.

### Sample Application

You can use the following sample application to test the code examples on this page. To use the sample application, perform the following steps:

1. Ensure you have PyMongo installed.

2. Copy the following code and paste it into a new `.py` file.

3. Copy a code example from this page and paste it on the specified lines in the file.

Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from pymongo import MongoClient

try:
    # start example code here

    # end example code here

    client.admin.command("ping")
    print("Connected successfully")

    # other application code

    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

```

</Tab>

<Tab name="Asynchronous">

```python
import asyncio
from pymongo import AsyncMongoClient

async def main():
    try:
        # start example code here

        # end example code here

        await client.admin.command("ping")
        print("Connected successfully")

        # other application code

        await client.close()

    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)

asyncio.run(main())
```

</Tab>

</Tabs>

## Connection

The following sections describe how to connect to different targets, such as a local instance of MongoDB or a cloud-hosted instance on Atlas.

### Local Deployment

The following code shows how to connect  the connection string to connect to a local MongoDB deployment. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
```

</Tab>

<Tab name="Asynchronous">

```python
uri = "mongodb://localhost:27017/"
client = AsyncMongoClient(uri)
```

</Tab>

</Tabs>

### Atlas

The following code shows the connection string to connect to a deployment hosted on Atlas. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
uri = "<Atlas connection string>"
client = MongoClient(uri, server_api=pymongo.server_api.ServerApi(
   version="1", strict=True, deprecation_errors=True))
```

</Tab>

<Tab name="Asynchronous">

```python
uri = "<Atlas connection string>"
client = AsyncMongoClient(uri, server_api=pymongo.server_api.ServerApi(
   version="1", strict=True, deprecation_errors=True))
```

</Tab>

</Tabs>

### Replica Set

The following code shows the connection string to connect to a replica set. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
uri = "mongodb://<replica set member>:<port>/?replicaSet=<replica set name>"
client = MongoClient(uri)
```

</Tab>

<Tab name="Asynchronous">

```python
uri = "mongodb://<replica set member>:<port>/?replicaSet=<replica set name>"
client = AsyncMongoClient(uri)
```

</Tab>

</Tabs>

## Network Compression

The following sections describe how to connect to MongoDB while specifying network compression algorithms.

### Compression Algorithms

The following tabs demonstrate how to specify all available compressors while connecting to MongoDB:

<Tabs>

<Tab name="MongoClient">

```python
client = pymongo.MongoClient("mongodb://<db_username>:<db_password>@<hostname>:<port>",
                             compressors = "snappy,zstd,zlib")
```

</Tab>

<Tab name="Connection String">

```python
uri = ("mongodb://<db_username>:<db_password>@<hostname>:<port>/?"
       "compressors=snappy,zstd,zlib")
client = pymongo.MongoClient(uri)
```

</Tab>

<Tab name="MongoClient (Asynchronous)">

```python
client = pymongo.AsyncMongoClient("mongodb://<db_username>:<db_password>@<hostname>:<port>",
                                  compressors = "snappy,zstd,zlib")
```

</Tab>

<Tab name="Connection String (Asynchronous)">

```python
uri = ("mongodb://<db_username>:<db_password>@<hostname>:<port>/?"
       "compressors=snappy,zstd,zlib")
client = pymongo.AsyncMongoClient(uri)
```

</Tab>

</Tabs>

To learn more about specifying compression algorithms, see Specify Compression Algorithms in the Network Compression guide.

### zlib Compression Level

The following tabs demonstrate how to specify a compression level for the `zlib` compressor:

<Tabs>

<Tab name="MongoClient">

```python
client = pymongo.MongoClient("mongodb://<db_username>:<db_password>@<hostname>:<port>",
   compressors = "zlib",
   zlibCompressionLevel=<zlib compression level>)
```

</Tab>

<Tab name="Connection String">

```python
uri = ("mongodb://<db_username>:<db_password>@<hostname>:<port>/?"
       "compressors=zlib"
       "zlibCompressionLevel=<zlib compression level>")
client = pymongo.MongoClient(uri)
```

</Tab>

<Tab name="MongoClient (Asynchronous)">

```python
client = pymongo.AsyncMongoClient("mongodb://<db_username>:<db_password>@<hostname>:<port>",
   compressors = "zlib",
   zlibCompressionLevel=<zlib compression level>)
```

</Tab>

<Tab name="Connection String (Asynchronous)">

```python
uri = ("mongodb://<db_username>:<db_password>@<hostname>:<port>/?"
   "compressors=zlib"
   "zlibCompressionLevel=<zlib compression level>")
client = pymongo.AsyncMongoClient(uri)
```

</Tab>

</Tabs>

To learn more about setting the zlib compression level, see Specify Compression Algorithms in the Network Compression guide.

## Server Selection

The following code shows a connection string that specifies a server selection function. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
client = pymongo.MongoClient("mongodb://<db_username>:<db_password>@<hostname>:<port>",
   server_selector=<selector function>)
```

</Tab>

<Tab name="Asynchronous">

```python
client = pymongo.AsyncMongoClient("mongodb://<db_username>:<db_password>@<hostname>:<port>",
   server_selector=<selector function>)
```

</Tab>

</Tabs>

To learn more about customizing server selection, see Customize Server Selection.

## Stable API

The following code shows how to specify Stable API settings for a connection.Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb://<db_username>:<db_password>@<hostname:<port>",
   server_api=ServerApi("<Stable API version>"))
```

</Tab>

<Tab name="Asynchronous">

```python
from pymongo.server_api import ServerApi

client = pymongo.AsyncMongoClient("mongodb://<db_username>:<db_password>@<hostname:<port>",
   server_api=ServerApi("<Stable API version>"))
```

</Tab>

</Tabs>

To learn more about the Stable API, see Stable API.

## Limit Server Execution Time

### timeout Block

The following code shows how to set a client-side timeout by using the `timeout()` method:

```python
with pymongo.timeout(<timeout length>):
   # perform operations here
```

To learn more about client-side timeouts, see Limit Server Execution Time.

### timeoutMS Connection Option

The following tabs demonstrate how to set a client-side timeout by using the `timeoutMS` connection option:

<Tabs>

<Tab name="MongoClient">

```python
client = pymongo.MongoClient("mongodb://<db_username>:<db_password>@<hostname@:<port>",
   timeoutMS=<timeout length>)
```

</Tab>

<Tab name="Connection String">

```python
uri = "mongodb://<db_username>:<db_password>@<hostname:<port>/?timeoutMS=<timeout length>"
client = pymongo.MongoClient(uri)
```

</Tab>

<Tab name="MongoClient (Asynchronous)">

```python
client = pymongo.AsyncMongoClient("mongodb://<db_username>:<db_password>@<hostname@:<port>",
   timeoutMS=<timeout length>)
```

</Tab>

<Tab name="Connection String (Asynchronous)">

```python
uri = "mongodb://<db_username>:<db_password>@<hostname:<port>/?timeoutMS=<timeout length>"
client = pymongo.AsyncMongoClient(uri)
```

</Tab>

</Tabs>

To learn more about client-side timeouts, see Limit Server Execution Time.
