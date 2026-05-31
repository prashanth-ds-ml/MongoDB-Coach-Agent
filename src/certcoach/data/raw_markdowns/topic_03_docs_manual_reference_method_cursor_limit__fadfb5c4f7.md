> Source: https://www.mongodb.com/docs/manual/reference/method/cursor.limit/
> Fetch method: direct_markdown

# cursor.limit() (mongosh method)

## Definition

`cursor.limit()`
This page documents a [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) method. This is *not* the documentation for a language-specific driver, such as Node.js.

For MongoDB API drivers, refer to the language-specific [MongoDB driver documentation](https://www.mongodb.com/docs/drivers/).

Use the [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) method on a cursor to specify the maximum number of documents the cursor will return. [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) is analogous to the `LIMIT` statement in a SQL database.

You must apply [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) to the cursor before retrieving any documents from the database.

Use [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) to maximize performance and prevent MongoDB from returning more results than required for processing.

The [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) method has the following prototype form:

```javascript
db.collection.find(<query>).limit(<number>)
```

## Compatibility

This method is available in deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

This command is supported in all MongoDB Atlas clusters. For information on Atlas support for all commands, see [Unsupported Commands](https://www.mongodb.com/docs/atlas/unsupported-commands/).

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Behavior

### Supported Values

The behavior of [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) is undefined for values less than -2 31 and greater than 2 31.

You must specify a numeric value for [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit).

### Zero Value

A [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) value of 0 (i.e. [`.limit(0)`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit)) is equivalent to setting no limit.

### Negative Values

A negative limit is similar to a positive limit but closes the cursor after returning a single [batch](https://www.mongodb.com/docs/core/cursors/#std-label-cursor-batches) of results. As such, with a negative limit, if the limited result set does not fit into a single batch, the number of documents received will be less than the specified limit. By passing a negative limit, the client indicates to the server that it will not ask for a subsequent batch via `getMore`.

### Using `limit()` with `sort()`

If using [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) with [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort), be sure to include at least one field in your sort that contains unique values, before passing results to [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit).

Sorting on fields that contain duplicate values may return an inconsistent sort order for those duplicate fields over multiple executions, especially when the collection is actively receiving writes.

The easiest way to guarantee sort consistency is to include the `_id` field in your sort query.

See [Consistent sorting with the sort() method](https://www.mongodb.com/docs/reference/method/cursor.sort/#std-label-sort-cursor-consistent-sorting) for more information.

### Using `limit()` with `skip()`

When you chain [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) and [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit), the method chaining order does not affect the results. The server always applies the skip operation based on the sort order before it applies the limit on how many documents to return.

The following code example shows different chaining orders for [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) and [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) that always produce the same query results for the same data set:

```javascript
db.myColl.find().sort({_id: 1}).skip(3).limit(6);

db.myColl.find().sort({_id: 1}).limit(6).skip(3);
```
