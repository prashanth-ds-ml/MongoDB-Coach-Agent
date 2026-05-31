> Source: https://www.mongodb.com/docs/manual/reference/method/cursor.sort/
> Fetch method: direct_markdown

# cursor.sort() (mongosh method)

## Definition

`cursor.sort(sort)`
This page documents a [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) method. This is *not* the documentation for a language-specific driver, such as Node.js.

For MongoDB API drivers, refer to the language-specific [MongoDB driver documentation](https://www.mongodb.com/docs/drivers/).

Specifies the order in which the query returns matching documents. You must apply [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) to the cursor before retrieving any documents from the database.

## Compatibility

This method is available in deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

This command is supported in all MongoDB Atlas clusters. For information on Atlas support for all commands, see [Unsupported Commands](https://www.mongodb.com/docs/atlas/unsupported-commands/).

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

The [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) method has the following parameter:

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
`sort`

</td>
<td headers="Type">
document

</td>
<td headers="Description">
A document that defines the sort order of the result set.

</td>
</tr>
</table>The `sort` parameter contains field and value pairs, in the following form:

```javascript
{ field: value }
```

The sort document can specify [ascending or descending sort on existing fields](https://www.mongodb.com/docs/reference/method/cursor.sort/#std-label-sort-asc-desc) or [sort on text score metadata](https://www.mongodb.com/docs/reference/method/cursor.sort/#std-label-sort-metadata).

## Behavior

### Limits

- You can sort on a maximum of 32 keys.

- Providing a sort pattern with duplicate fields causes an error.

### Sort Consistency

MongoDB does not store documents in a collection in a particular order. When sorting on a field which contains duplicate values, documents containing those values may be returned in any order.

The `$sort` operation is not a "stable sort," which means that documents with equivalent sort keys are not guaranteed to remain in the same relative order in the output as they were in the input.

If the field specified in the sort criteria does not exist in two documents, then the value on which they are sorted is the same. The two documents may be returned in any order.

If consistent sort order is desired, include at least one field in your sort that contains unique values. The easiest way to guarantee this is to include the `_id` field in your sort query.

Consider the following `restaurant` collection:

```js
db.restaurants.insertMany( [
   { _id: 1, name: "Central Park Cafe", borough: "Manhattan"},
   { _id: 2, name: "Rock A Feller Bar and Grill", borough: "Queens"},
   { _id: 3, name: "Empire State Pub", borough: "Brooklyn"},
   { _id: 4, name: "Stan's Pizzaria", borough: "Manhattan"},
   { _id: 5, name: "Jane's Deli", borough: "Brooklyn"},
] );
```

The following command uses the [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) method to sort on the `borough` field:

```js
db.restaurants.find().sort( { "borough": 1 } )
```

In this example, sort order may be inconsistent, since the `borough` field contains duplicate values for both `Manhattan` and `Brooklyn`. Documents are returned in alphabetical order by `borough`, but the order of those documents with duplicate values for `borough` might not be the same across multiple executions of the same sort. For example, here are the results from two different executions of the above command:

```js
{ _id: 3, name: "Empire State Pub", borough: "Brooklyn" }
{ _id: 5, name: "Jane's Deli", borough: "Brooklyn" }
{ _id: 1, name: "Central Park Cafe", borough: "Manhattan" }
{ _id: 4, name: "Stan's Pizzaria", borough: "Manhattan" }
{ _id: 2, name: "Rock A Feller Bar and Grill", borough: "Queens" }

{ _id: 5, name: "Jane's Deli", borough: "Brooklyn" }
{ _id: 3, name: "Empire State Pub", borough: "Brooklyn" }
{ _id: 4, name: "Stan's Pizzaria", borough: "Manhattan" }
{ _id: 1, name: "Central Park Cafe", borough: "Manhattan" }
{ _id: 2, name: "Rock A Feller Bar and Grill", borough: "Queens" }
```

While the values for `borough` are still sorted in alphabetical order, the order of the documents containing duplicate values for `borough` (i.e. `Manhattan` and `Brooklyn`) is not the same.

To achieve a *consistent sort*, add a field which contains exclusively unique values to the sort. The following command uses the [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) method to sort on both the `borough` field and the `_id` field:

```js
db.restaurants.find().sort( { "borough": 1, "_id": 1 } )
```

Since the `_id` field is always guaranteed to contain exclusively unique values, the returned sort order will always be the same across multiple executions of the same sort.

When sorting by a nonexistent field, MongoDB does not guarantee any particular output ordering. The behavior in these cases may change from version to version.

### Ascending/Descending Sort

Specify in the sort parameter the field or fields to sort by and a value of `1` or `-1` to specify an ascending or descending sort respectively.

The following operation sorts the documents first by the `age` field in descending order and then by the `posts` field in ascending order:

```javascript
db.users.find({ }).sort( { age : -1, posts: 1 } )
```

When comparing values of different [BSON types](https://www.mongodb.com/docs/reference/bson-types/#std-label-bson-types) in sort operations, MongoDB uses the following comparison order, from lowest to highest:

1. MinKey (internal type)

2. Null

3. Numbers (ints, longs, doubles, decimals)

4. Symbol, String

5. Object

6. Array

7. BinData

8. ObjectId

9. Boolean

10. Date

11. Timestamp

12. Regular Expression

13. JavaScript Code

14. JavaScript Code with Scope

15. MaxKey (internal type)

For details on the comparison/sort order for specific types, see [Comparison/Sort Order](https://www.mongodb.com/docs/reference/bson-type-comparison-order/#std-label-bson-types-comparison-order).

### Text Score Metadata Sort

`$text` provides text query capabilities for self-managed (non-Atlas) deployments. For data hosted on MongoDB, MongoDB also offers an improved full-text query solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/).

If you use [`$text`](https://www.mongodb.com/docs/reference/operator/query/text/#mongodb-query-op.-text), you can sort by descending relevance score using the [`{ $meta: "textScore" }`](https://www.mongodb.com/docs/reference/operator/aggregation/meta/#mongodb-expression-exp.-meta) expression.

The following sample document specifies a descending sort by the `"textScore"` metadata:

```javascript
db.users.find(
   { $text: { $search: "operating" } },
   { score: { $meta: "textScore" }}
).sort({ score: { $meta: "textScore" } })
```

The `"textScore"` metadata sorts in descending order.

For more information, see [`$meta`](https://www.mongodb.com/docs/reference/operator/aggregation/meta/#mongodb-expression-exp.-meta) for details.

### Sort by an Array Field

When MongoDB sorts documents by an array-value field, the [sort key](https://www.mongodb.com/docs/reference/glossary/#std-term-sort-key) depends on whether the sort is ascending or descending:

- In an ascending sort, the sort key is the lowest value in the array.

- In a descending sort, the sort key is the highest value in the array.

The query filter does not affect sort key selection.

For example, create a `shoes` collection with these documents:

```javascript
db.shoes.insertMany( [
   { _id: 'A', sizes: [ 7, 11 ] },
   { _id: 'B', sizes: [ 8, 9, 10 ] }
] )
```

The following queries sort the documents by the `sizes` field in ascending and descending order:

```javascript
// Ascending sort
db.shoes.find().sort( { sizes: 1 } )

// Descending sort
db.shoes.find().sort( { sizes: -1 } )
```

Both of the preceding queries return the document with `_id: 'A'` first because sizes `7` and `11` are the lowest and highest in the entries in the `sizes` array, respectively.

#### Filter and Sort by an Array Field

When you filter and sort by a field that contains an array, the filter does not affect the value used as the [sort key](https://www.mongodb.com/docs/reference/glossary/#std-term-sort-key). The sort always considers all array values as potential sort keys.

For example, the following query finds shoes with sizes greater than 9 and sorts the results by size in ascending order:

```javascript
db.shoes.find( { sizes: { $gt: 9 } } ).sort( { sizes: 1 } )
```

The sort is ascending, which means that the sort key is the lowest value in the `sizes` array:

- In document `_id: 'A'`, the lowest `sizes` element is `7`. This value is used as the sort key even though it does not match the filter `{ sizes: { $gt: 9 }`.

- In document `_id: 'B'`, the lowest `sizes` element is `8`. Similarly, this value is used as the sort key even though it does not match the filter.

The query returns the document with `_id: 'A'` first.

To only consider matched values as potential sort keys, you can generate a new field containing the matched values and sort on that field. For more information, see these pipeline stages and expressions:

- [`$addFields`](https://www.mongodb.com/docs/reference/operator/aggregation/addFields/#mongodb-pipeline-pipe.-addFields)

- [`$filter`](https://www.mongodb.com/docs/reference/operator/aggregation/filter/#mongodb-expression-exp.-filter)

- [`$sort`](https://www.mongodb.com/docs/reference/operator/aggregation/sort/#mongodb-pipeline-pipe.-sort)

### Sort and Index Use

MongoDB can obtain the results of a sort operation from an index which includes the sort fields. MongoDB *may* use multiple indexes to support a sort operation *if* the sort uses the same indexes as the query predicate.

If MongoDB cannot use an index or indexes to obtain the sort order, MongoDB must perform an in-memory sort operation on the data.

Sort operations that use an index often have better performance than in-memory sorts. For more information on creating indexes to support sort operations, see [Use Indexes to Sort Query Results](https://www.mongodb.com/docs/tutorial/sort-results-with-indexes/#std-label-sorting-with-indexes).

To check if MongoDB must perform an in-memory sort, append [`cursor.explain()`](https://www.mongodb.com/docs/reference/method/cursor.explain/#mongodb-method-cursor.explain) to the query and check the [explain results](https://www.mongodb.com/docs/reference/explain-results/#std-label-explain-results). If the query plan contains a `SORT` stage, then MongoDB must perform an in-memory sort operation.

To prevent in-memory sorts from consuming too much memory:

- Create an index to support the sort operation. See [Use Indexes to Sort Query Results](https://www.mongodb.com/docs/tutorial/sort-results-with-indexes/) for more information and examples.

- Limit the amount of data to sort by using [`cursor.limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) with [`cursor.sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort). See [Limit Results](https://www.mongodb.com/docs/reference/method/cursor.sort/#std-label-sort-limit-results) for more information and examples.

[Memory Limits on Sort Operations](https://www.mongodb.com/docs/reference/limits/#mongodb-limit-Sort-Operations)

### Limit Results

You can use [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) in conjunction with [`limit()`](https://www.mongodb.com/docs/reference/method/cursor.limit/#mongodb-method-cursor.limit) to return the first (in terms of the sort order) `k` documents, where `k` is the specified limit.

If MongoDB cannot obtain the sort order via an index scan, then MongoDB uses a top-k sort algorithm. This algorithm buffers the first `k` results (or last, depending on the sort order) seen so far by the underlying index or collection access. If at any point the memory footprint of these `k` results exceeds 100 megabytes, the query will fail *unless* the query specifies [`cursor.allowDiskUse()`](https://www.mongodb.com/docs/reference/method/cursor.allowDiskUse/#mongodb-method-cursor.allowDiskUse).

[Memory Limits on Sort Operations](https://www.mongodb.com/docs/reference/limits/#mongodb-limit-Sort-Operations)

### Interaction with Projection

When an operation both sorts *and* [projects](https://www.mongodb.com/docs/reference/glossary/#std-term-projection) with the same fields, MongoDB sorts on the original field values before applying the projection.

## Examples

A collection `orders` contain the following documents:

```javascript
db.orders.insertMany( [
   { _id: 1, item: { category: "cake", type: "chiffon" }, amount: 10 },
   { _id: 2, item: { category: "cookies", type: "chocolate chip" }, amount: 50 },
   { _id: 3, item: { category: "cookies", type: "chocolate chip" }, amount: 15 },
   { _id: 4, item: { category: "cake", type: "lemon" }, amount: 30 },
   { _id: 5, item: { category: "cake", type: "carrot" }, amount: 20 },
   { _id: 6, item: { category: "brownies", type: "blondie" }, amount: 10 }
] )
```

The following query, which returns all documents from the `orders` collection, does not specify a sort order:

```javascript
db.orders.find()
```

The query returns the documents in indeterminate order:

```javascript
{ _id: 1, item: { category: "cake", type: "chiffon" }, amount: 10 }
{ _id: 2, item: { category: "cookies", type: "chocolate chip" }, amount: 50 }
{ _id: 3, item: { category: "cookies", type: "chocolate chip" }, amount: 15 }
{ _id: 4, item: { category: "cake", type: "lemon" }, amount: 30 }
{ _id: 5, item: { category: "cake", type: "carrot" }, amount: 20 }
{ _id: 6, item: { category: "brownies", type: "blondie" }, amount: 10 }
```

The following query specifies a sort on the `amount` field in descending order.

```javascript
db.orders.find().sort( { amount: -1 } )
```

The query returns the following documents, in descending order of `amount`:

```javascript
{ _id: 2, item: { category: "cookies", type: "chocolate chip" }, amount: 50 }
{ _id: 4, item: { category: "cake", type: "lemon" }, amount: 30 }
{ _id: 5, item: { category: "cake", type: "carrot" }, amount: 20 }
{ _id: 3, item: { category: "cookies", type: "chocolate chip" }, amount: 15 }
{ _id: 1, item: { category: "cake", type: "chiffon" }, amount: 10 }
{ _id: 6, item: { category: "brownies", type: "blondie" }, amount: 10 }
```

The following query specifies the sort order using the fields from an embedded document `item`. The query sorts first by the `category` field in ascending order, and then within each `category`, by the `type` field in ascending order.

```javascript
db.orders.find().sort( { "item.category": 1, "item.type": 1 } )
```

The query returns the following documents, ordered first by the `category` field, and within each category, by the `type` field:

```javascript
{ _id: 6, item: { category: "brownies", type: "blondie" }, amount: 10 }
{ _id: 5, item: { category: "cake", type: "carrot" }, amount: 20 }
{ _id: 1, item: { category: "cake", type: "chiffon" }, amount: 10 }
{ _id: 4, item: { category: "cake", type: "lemon" }, amount: 30 }
{ _id: 2, item: { category: "cookies", type: "chocolate chip" }, amount: 50 }
{ _id: 3, item: { category: "cookies", type: "chocolate chip" }, amount: 15 }
```

## Return in Natural Order

The [`$natural`](https://www.mongodb.com/docs/reference/method/cursor.hint/#mongodb-operator-metaOp.-natural) parameter returns items according to their [natural order](https://www.mongodb.com/docs/reference/glossary/#std-term-natural-order) within the database. This ordering is an internal implementation feature, and you should not rely on any particular ordering of the documents.

Prior to MongoDB 7.0, [`$natural`](https://www.mongodb.com/docs/reference/method/cursor.hint/#mongodb-operator-metaOp.-natural) accepts incorrect type values, such as `0`, `NaN`, "X", and `-0.01`. After MongoDB 7.0, if you pass any value other than `1` and `-1` to [`$natural`](https://www.mongodb.com/docs/reference/method/cursor.hint/#mongodb-operator-metaOp.-natural), MongoDB returns an error.

### Index Use

Queries that include a sort by [`$natural`](https://www.mongodb.com/docs/reference/method/cursor.hint/#mongodb-operator-metaOp.-natural) order do **not** use indexes to fulfill the query predicate with the following exception: If the query predicate is an equality condition on the `_id` field `{ _id: <value> }`, then the query with the sort by [`$natural`](https://www.mongodb.com/docs/reference/method/cursor.hint/#mongodb-operator-metaOp.-natural) order can use the `_id` index.

[`$natural`](https://www.mongodb.com/docs/reference/method/cursor.hint/#mongodb-operator-metaOp.-natural)
