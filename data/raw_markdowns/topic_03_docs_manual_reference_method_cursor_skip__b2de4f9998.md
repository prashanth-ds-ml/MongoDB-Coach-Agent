> Source: https://www.mongodb.com/docs/manual/reference/method/cursor.skip/
> Fetch method: direct_markdown

# cursor.skip() (mongosh method)

## Definition

`cursor.skip(<offset>)`
This page documents a [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) method. This is *not* the documentation for a language-specific driver, such as Node.js.

For MongoDB API drivers, refer to the language-specific [MongoDB driver documentation](https://www.mongodb.com/docs/drivers/).

Call the [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) method on a cursor to control where MongoDB begins returning results. This approach may be useful in implementing paginated results.

You must apply [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) to the cursor before retrieving any documents from the database.

The [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) method has the following parameter:

<table>
<tr>
<th id="Parameter">
Parameter

</th>
<th id="Type">
Type

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Parameter">
`offset`

</td>
<td headers="Type">
number

</td>
<td headers="Description">
The number of documents to skip in the results set.

</td>
</tr>
</table>

## Compatibility

This method is available in deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

This command is supported in all MongoDB Atlas clusters. For information on Atlas support for all commands, see [Unsupported Commands](https://www.mongodb.com/docs/atlas/unsupported-commands/).

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Behavior

### Using `skip()` with `sort()`

If using [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) with [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort), be sure to include at least one field in your sort that contains unique values, before passing results to [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip).

Sorting on fields that contain duplicate values may return an inconsistent sort order for those duplicate fields over multiple executions, especially when the collection is actively receiving writes.

The easiest way to guarantee sort consistency is to include the `_id` field in your sort query.

See [Consistent sorting with the sort() method](https://www.mongodb.com/docs/reference/method/cursor.sort/#std-label-sort-cursor-consistent-sorting) for more information.

### Using `skip()` with `limit()`

When you chain [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) and [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit), the method chaining order does not affect the results. The server always applies the skip operation based on the sort order before it applies the limit on how many documents to return.

The following code example shows different chaining orders for [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) and [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) that always produce the same query results for the same data set:

```javascript
db.myColl.find().sort({_id: 1}).skip(3).limit(6);

db.myColl.find().sort({_id: 1}).limit(6).skip(3);
```

## Pagination Example

### Using `skip()`

The following JavaScript function uses [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) to paginate a collection by its `_id` field:

```javascript
function printStudents(pageNumber, nPerPage) {
  print( "Page: " + pageNumber );
  db.students.find()
             .sort( { _id: 1 } )
             .skip( pageNumber > 0 ? ( ( pageNumber - 1 ) * nPerPage ) : 0 )
             .limit( nPerPage )
             .forEach( student => {
               print( student.name );
             } );
}
```

The [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) method requires the server to scan from the beginning of the input results set before beginning to return results. As the offset increases, [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) will become slower.

### Using Range Queries

Range queries can use [indexes](https://www.mongodb.com/docs/indexes/#std-label-indexes) to avoid scanning unwanted documents, typically yielding better performance as the offset grows compared to using [`skip()`](https://www.mongodb.com/docs/reference/method/cursor.skip/#mongodb-method-cursor.skip) for pagination.

#### Descending Order

Use this procedure to implement pagination with range queries:

- Choose a field such as `_id` which generally changes in a consistent direction over time and has a [unique index](https://www.mongodb.com/docs/core/index-unique/#std-label-index-type-unique) to prevent duplicate values,

- Query for documents whose field is less than the start value using the [`$lt`](https://www.mongodb.com/docs/reference/operator/query/lt/#mongodb-query-op.-lt) and [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) operators, and

- Store the last-seen field value for the next query.

For example, the following function uses the above procedure to print pages of student names from a collection, sorted approximately in order of newest documents first using the `_id` field (that is, in *descending* order):

```javascript
function printStudents(startValue, nPerPage) {
  let endValue = null;
  db.students.find( { _id: { $lt: startValue } } )
             .sort( { _id: -1 } )
             .limit( nPerPage )
             .forEach( student => {
               print( student.name );
               endValue = student._id;
             } );

  return endValue;
}
```

You may then use the following code to print all student names using this pagination function, using [`MaxKey`](https://www.mongodb.com/docs/reference/mongodb-extended-json/#mongodb-bsontype-MaxKey) to start from the largest possible key:

```javascript
let currentKey = MaxKey;
while (currentKey !== null) {
  currentKey = printStudents(currentKey, 10);
}
```

While [ObjectId](https://www.mongodb.com/docs/reference/bson-types/#std-label-objectid) values should increase over time, they are not necessarily monotonic. This is because they:

- Only contain one second of temporal resolution, so [ObjectId](https://www.mongodb.com/docs/reference/bson-types/#std-label-objectid) values created within the same second do not have a guaranteed ordering, and

- Are generated by clients, which may have differing system clocks.

#### Ascending Order

Returning paginated results in ascending order is similar to the previous, but uses [`$gt`](https://www.mongodb.com/docs/reference/operator/query/gt/#mongodb-query-op.-gt) with an *ascending* sort order:

```javascript
function printStudents(startValue, nPerPage) {
  let endValue = null;
  db.students.find( { _id: { $gt: startValue } } )
             .sort( { _id: 1 } )
             .limit( nPerPage )
             .forEach( student => {
               print( student.name );
               endValue = student._id;
             } );

  return endValue;
}
```

Using this function is likewise similar, but with [`MinKey`](https://www.mongodb.com/docs/reference/mongodb-extended-json/#mongodb-bsontype-MinKey) as the starting key:

```javascript
let currentKey = MinKey;
while (currentKey !== null) {
  currentKey = printStudents(currentKey, 10);
}
```
