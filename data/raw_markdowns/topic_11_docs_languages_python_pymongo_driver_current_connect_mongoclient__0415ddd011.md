> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/mongoclient/
> Fetch method: direct_markdown

# Create a MongoClient

## Overview

To connect to a MongoDB deployment, you need two things:

- A **connection URI**, also known as a *connection string*, which tells PyMongo which MongoDB deployment to connect to.

- A **MongoClient** object, which creates the connection to the MongoDB deployment and lets you perform operations on it.

You can also use either of these components to customize the way PyMongo behaves while connected to MongoDB.

This guide shows you how to create a connection string and use a `MongoClient` object to connect to MongoDB.

## Connection URI

A standard connection string includes the following components:

<table>
<tr>
<th id="Component">
Component

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Component">
`mongodb://`

</td>
<td headers="Description">
Required. A prefix that identifies this as a string in the standard connection format.

</td>
</tr>
<tr>
<td headers="Component">
`username:password`

</td>
<td headers="Description">
Optional. Authentication credentials. If you include these, the client authenticates the user against the database specified in `authSource`. For more information about the `authSource` connection option, see [Authentication Mechanisms](https://www.mongodb.com/docs/languages/python/pymongo-driver/security/authentication/#std-label-pymongo-auth).

</td>
</tr>
<tr>
<td headers="Component">
`host[:port]`

</td>
<td headers="Description">
Required. The host and optional port number where MongoDB is running. If you don't include the port number, the driver uses the default port, `27017`.

</td>
</tr>
<tr>
<td headers="Component">
`/defaultauthdb`

</td>
<td headers="Description">
Optional. The authentication database to use if the connection string includes `username:password@` authentication credentials but not the `authSource` option. If you don't include this component, the client authenticates the user against the `admin` database.

</td>
</tr>
<tr>
<td headers="Component">
`?<options>`

</td>
<td headers="Description">
Optional. A query string that specifies connection-specific options as `<name>=<value>` pairs. See [Specify Connection Options](https://www.mongodb.com/docs/languages/python/pymongo-driver/connect/connection-options/#std-label-pymongo-connection-options) for a full description of these options.

</td>
</tr>
</table>For more information about creating a connection string, see [Connection Strings](https://www.mongodb.com/docs/manual/reference/connection-string/) in the MongoDB Server documentation.

## MongoClient

To create a connection to MongoDB, pass a connection URI as a string to the `MongoClient` constructor. In the following example, the driver uses a sample connection URI to connect to a MongoDB instance on port `27017` of `localhost`:

```python
from pymongo import MongoClient

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
```

If you are working with an asynchronous application, use the `AsyncMongoClient` class. The following example shows how to create an `AsyncMongoClient` object:

```python
from pymongo import AsyncMongoClient

uri = "mongodb://localhost:27017/"
client = AsyncMongoClient(uri)
```

The following table describes the positional parameters that the `MongoClient()` constructor accepts. All parameters are optional.

<table>
<tr>
<th id="Parameter">
Parameter

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Parameter">
`host`

</td>
<td headers="Description">
The hostname, IP address, or Unix domain socket path of the MongoDB deployment. If your application connects to a replica set or sharded cluster, you can specify multiple hostnames or IP addresses in a Python list.

If you pass a literal IPv6 address, you must enclose the address in square brackets (`[ ]`). For example, pass the value `[::1]` to connect to localhost.

PyMongo doesn't support [multihomed](https://en.wikipedia.org/wiki/Multihoming) and [round-robin DNS](https://en.wikipedia.org/wiki/Round-robin_DNS) addresses.

**Data type:** `Union[str, Sequence[str]]` | **Default value:** `"localhost"`

</td>
</tr>
<tr>
<td headers="Parameter">
`port`

</td>
<td headers="Description">
The port number MongoDB Server is running on.

You can include the port number in the `host` argument instead of using this parameter.

**Data type:** `int` | **Default value:** `27017`

</td>
</tr>
<tr>
<td headers="Parameter">
`document_class`

</td>
<td headers="Description">
The default class that the client uses to decode BSON documents returned by queries. This parameter accepts the following types:

- `bson.raw_bson.RawBSONDocument`. To learn more about the `RawBSONDocument` class, see [Work with Raw BSON Data](https://www.mongodb.com/docs/languages/python/pymongo-driver/data-formats/bson/#std-label-pymongo-bson-raw).

- A subclass of the `collections.abc.Mapping` type, such as `OrderedDict`. Depending on the strictness of your type-checking rules, you might also need to specify types for the key and value, as shown in the following example:

  ```python
  client = MongoClient(document_class=OrderedDict[str, int])
  ```

- A subclass of the `TypedDict` type. To pass a `TypedDict` subclass for this parameter, you must also include the class in a type hint for your `MongoClient` object, as shown in the following example:

  ```python
  client: MongoClient[MyTypedDict] = MongoClient()
  ```

  The [TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict) class is in the `typing` module, which is available only in Python 3.8 and later. To use the `TypedDict` class in earlier versions of Python, install the [typing_extensions](https://pypi.org/project/typing-extensions/) package.

**Data type:** `Type[_DocumentType]`
**Default:** `dict`

</td>
</tr>
<tr>
<td headers="Parameter">
`tz_aware`

</td>
<td headers="Description">
If this parameter is `True`, the client treats `datetime` values as aware. Otherwise, it treats them as naive.

For more information about aware and naive `datetime` values, see [datetime](https://docs.python.org/3/library/datetime.html) in the Python documentation.

**Data type:** `bool`

</td>
</tr>
<tr>
<td headers="Parameter">
`connect`

</td>
<td headers="Description">
If this parameter is `True`, the client begins connecting to MongoDB in the background immediately after you create it. If this parameter is `False`, the client connects to MongoDB when it performs the first database operation.

If your application is running in a [function-as-a-service (FaaS)](https://en.wikipedia.org/wiki/Function_as_a_service) environment, the default value is `False`. Otherwise, the default value is `True`.

**Data type:** `bool`

</td>
</tr>
<tr>
<td headers="Parameter">
`type_registry`

</td>
<td headers="Description">
An instance of the `TypeRegistry` class to enable encoding and decoding of custom types. For more information about encoding and decoding custom types, see the [Custom Types](https://www.mongodb.com/docs/languages/python/pymongo-driver/data-formats/custom-types/serialization/#std-label-pymongo-serialization) section.

**Data type:** [TypeRegistry](https://pymongo.readthedocs.io/en/4.17.0/api/bson/codec_options.html#bson.codec_options.TypeRegistry)

</td>
</tr>
</table>You can also pass keyword arguments to the `MongoClient()` constructor to specify optional parameters. For a complete list of keyword arguments, see the [MongoClient](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient) class in the API documentation.

## Concurrent Execution

The following sections describe PyMongo's support for concurrent execution mechanisms.

### Multithreading

PyMongo is thread-safe and provides built-in connection pooling for threaded applications. Because each `MongoClient` object represents a pool of connections to the database, most applications require only a single instance of `MongoClient`, even across multiple requests.

### Multiple Forks

PyMongo supports calling the `fork()` method to create a new process. However, if you fork a process, you must create a new `MongoClient` instance in the child process.

If you use the `fork()` method to create a new process, don't pass an instance of the `MongoClient` class from the parent process to the child process. This creates a high probability of deadlock among `MongoClient` instances in the child process. PyMongo tries to issue a warning if this deadlock might occur.

For more information about deadlock in forked processes, see [Forking a Process Causes a Deadlock](https://www.mongodb.com/docs/languages/python/pymongo-driver/connect/mongoclient/#std-label-pymongo-fork-deadlock).

### Multiprocessing

PyMongo supports the Python `multiprocessing` module. However, on Unix systems, the multiprocessing module spawns processes by using the `fork()` method. This carries the same risks described in [Multiple Forks](https://www.mongodb.com/docs/languages/python/pymongo-driver/connect/mongoclient/#std-label-pymongo-forks).

To use multiprocessing with PyMongo, write code similar to the following example:

```python
# Each process creates its own instance of MongoClient.
def func():
    db = pymongo.MongoClient().mydb
    # Do something with db.

proc = multiprocessing.Process(target=func)
proc.start()
```

Do not copy an instance of the `MongoClient` class from the parent process to a child process.

## Type Hints

If your application uses Python 3.5 or later, you can add *type hints*, as described in [PEP 484](https://peps.python.org/pep-0484/), to your code. Type hints denote the data types of variables, parameters, and function return values, and the structure of documents. Some IDEs can use type hints to check your code for type errors and suggest appropriate options for code completion.

To use type hints in your PyMongo application, you must add a type annotation to your `MongoClient` object, as shown in the following example. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from pymongo import MongoClient

client: MongoClient = MongoClient()
```

</Tab>

<Tab name="Asynchronous">

```python
from pymongo import AsyncMongoClient

client: AsyncMongoClient = AsyncMongoClient()
```

</Tab>

</Tabs>

For more accurate type information, you can include the generic document type `Dict[str, Any]` in your type annotation. This data type matches all documents in MongoDB. The following example shows how to include this data type in your type annotation. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from pymongo import MongoClient
from typing import Any, Dict

client: MongoClient[Dict[str, Any]] = MongoClient()
```

</Tab>

<Tab name="Asynchronous">

```python
from pymongo import AsyncMongoClient
from typing import Any, Dict

client: AsyncMongoClient[Dict[str, Any]] = AsyncMongoClient()
```

</Tab>

</Tabs>

If all the documents that you are working with correspond to a single custom type, you can specify the custom type as a type hint for your `MongoClient` object. This provides more accurate type information than the generic `Dict[str, Any]` type.

The following example shows how to specify the `Movie` type as a type hint for a `MongoClient` object. Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int

client: MongoClient[Movie] = MongoClient()
```

</Tab>

<Tab name="Asynchronous">

```python
from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int

client: AsyncMongoClient[Movie] = AsyncMongoClient()
```

</Tab>

</Tabs>

## Closing a MongoClient

During garbage collection, PyMongo automatically cleans up application-side resources used by a `MongoClient` instance. However, PyMongo does not guarantee the closure of server-side resources such as open cursors or sessions. You can ensure that PyMongo closes these resources by calling the `close()` method on your `MongoClient` instance when you are done using it, as shown in the following example:

```python
client.close()
```

You can also instantiate the client in a `with` statement, as shown in the following example. The client automatically closes when the block terminates.

```python
with MongoClient("mongodb://localhost:27017/") as client:
   db = client.get_database("mydatabase")
    # Perform further client operations here
```

Calling `close()` from a `__del__` method causes a deadlock.

To avoid a deadlock, use a `with` statement, as shown in the preceding example, or call `close()` in your application's shutdown logic.

## Troubleshooting

### MongoClient Fails ConfigurationError

Providing invalid keyword argument names causes the driver to raise this error.

Ensure that the keyword arguments that you specify exist and are spelled correctly.

### Forking a Process Causes a Deadlock

A `MongoClient` instance spawns multiple threads to run background tasks, such as monitoring connected servers. These threads share state that is protected by instances of the `threading.Lock` class, which are themselves [not fork-safe](http://bugs.python.org/issue6721). PyMongo is subject to the same limitations as any other multithreaded code that uses the `threading.Lock` class, or any mutexes.

One of these limitations is that the locks become useless after calling the `fork()` method. When `fork()` executes, the driver copies all the parent process's locks to the child process in the same state as they were in the parent. If they are locked in the parent process, they are also locked in the child process. The child process created by `fork()` has only one thread, so any locks created by other threads in the parent process are never released in the child process. The next time the child process attempts to acquire one of these locks, deadlock occurs.

Starting in PyMongo version 4.3, after you call the `os.fork()` method, the driver uses the `os.register_at_fork()` method to reset its locks and other shared state in the child process. Although this reduces the likelihood of a deadlock, PyMongo depends on libraries that aren't fork-safe in multithreaded applications, including OpenSSL and [getaddrinfo(3).](https://man7.org/linux/man-pages/man3/gai_strerror.3.html) Therefore, a deadlock can still occur.

The Linux manual page for [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html) also imposes the following restriction:

After a `fork()`  in a multithreaded program, the child can safely call only async-signal-safe functions (see [signal-safety(7)](https://man7.org/linux/man-pages/man7/signal-safety.7.html)) until such time as it calls [execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html).

Because PyMongo relies on functions that are *not* async-signal-safe, it can cause deadlocks or crashes when running in a child process.

For an example of a deadlock in a child process, see [PYTHON-3406](https://jira.mongodb.org/browse/PYTHON-3406) in Jira.

For more information about the problems caused by Python locks in multithreaded contexts with `fork()`, see [Issue 6721](http://bugs.python.org/issue6721) in the Python Issue Tracker.

#### Client Type Annotations

If you don't add a type annotation for your `MongoClient` object, your type checker might show an error similar to the following:

```python
from pymongo import MongoClient
client = MongoClient()  # error: Need type annotation for "client"
```

The solution is to annotate the `MongoClient` object as `client: MongoClient` or `client: MongoClient[Dict[str, Any]]`.

#### Incompatible Type

If you specify `MongoClient` as a type hint but don't include data types for the document, keys, and values, your type checker might show an error similar to the following:

```python
error: Dict entry 0 has incompatible type "str": "int";
expected "Mapping[str, Any]": "int"
```

The solution is to add the following type hint to your `MongoClient` object:

```python
client: MongoClient[Dict[str, Any]]
```

## API Documentation

To learn more about creating a `MongoClient` object in PyMongo, see the following API documentation:

- [MongoClient](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient)

- [AsyncMongoClient](https://pymongo.readthedocs.io/en/4.17.0/api/pymongo/asynchronous/mongo_client.html#pymongo.asynchronous.mongo_client.AsyncMongoClient)
