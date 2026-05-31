> Source: https://www.mongodb.com/docs/manual/reference/operator/query/size/
> Fetch method: direct_markdown

# $size (query predicate operator)

`$size`
The [`$size`](https://www.mongodb.com/docs/reference/operator/query/size/#mongodb-query-op.-size) operator matches any array with the number of elements specified by the argument.

## Compatibility

`$size`You can use `$size` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

Consider the following examples:

```javascript
db.collection.find( { field: { $size: 2 } } );
```

This query returns all documents in `collection` where `field` is an array with 2 elements. For instance, the above expression will return `{ field: [ red, green ] }` and `{ field: [ apple, lime ] }` but *not* `{ field: fruit }` or `{ field: [ orange, lemon, grapefruit ] }`. To match fields with only one element within an array use [`$size`](https://www.mongodb.com/docs/reference/operator/query/size/#mongodb-query-op.-size) with a value of 1, as follows:

```javascript
db.collection.find( { field: { $size: 1 } } );
```

[`$size`](https://www.mongodb.com/docs/reference/operator/query/size/#mongodb-query-op.-size) does not accept ranges of values. To select documents based on fields with different numbers of elements, create a counter field that you increment when you add elements to a field.

Queries cannot use indexes for the [`$size`](https://www.mongodb.com/docs/reference/operator/query/size/#mongodb-query-op.-size) portion of a query, although the other portions of a query can use indexes if applicable.

## Syntax

A `$size` expression has the following syntax:

```javascript
{
   <field>: {
      $size: <number>
   }
}
```

## Additional Examples

For additional examples on querying arrays, see:

- [Query an Array](https://www.mongodb.com/docs/tutorial/query-arrays/#std-label-read-operations-arrays)

- [Query an Array of Embedded Documents](https://www.mongodb.com/docs/tutorial/query-array-of-documents/#std-label-array-match-embedded-documents)

For additional examples on querying, see [Query Documents](https://www.mongodb.com/docs/tutorial/query-documents/#std-label-read-operations-query-document).

[`db.collection.find()`](https://www.mongodb.com/docs/reference/method/db.collection.find/#mongodb-method-db.collection.find)
