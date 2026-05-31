> Source: https://www.mongodb.com/docs/manual/core/index-compound/
> Fetch method: html_fallback

# Compound Indexes - Database Manual - MongoDB Docs Compound Indexes

Compound Indexes - Database Manual - MongoDB Docs

Make the MongoDB docs better! We value your opinion. Share your feedback for a chance to win $100.

Click here >

Docs Menu

Ask MongoDB AI

Docs Home/
/
Types

Docs Home/
Development/
Indexes/
Types

Docs Home/
Development/
Indexes/
Types

# Compound Indexes

Copy page

Compound indexes collect and sort data from multiple field values from each document in a collection. You can use the compound index to query the first field or any prefix fields of the index. The order of fields in a compound index is very important. The B-tree created by a compound index stores the sorted data in the order that the index specifies the fields.

For example, the following image shows a compound index where documents are first sorted by `userid `in ascending order (alphabetically). Then, the `scores `for each `userid `are sorted in descending order:

To create a compound index, use the following prototype:

```

db.<collection>.createIndex( {
   <field1>: <sortOrder>,
<field2>: <sortOrder>,
...
<fieldN>: <sortOrder>
} )
```

You can create and manage compound indexes in the UIfor deployments hosted in MongoDB Atlas.

## Use Cases

If your application repeatedly runs a query that contains multiple fields, you can create a compound index to improve performance for that query. For example, a grocery store manager often needs to look up inventory items by name and quantity to determine which items are low stock. You can create a compound index on both the `item `and `quantity `fields to improve query performance.

## Get Started

To create a compound index, see Create a Compound Index.

## Details

This section describes technical details and limitations for compound indexes.

### Field Limit

A single compound index can contain up to 32 fields.

### Field Order

The order of the indexed fields impacts the effectiveness of a compound index. Compound indexes contain references to documents according to the order of the fields in the index. To create efficient compound indexes, follow the ESR (Equality, Sort, Range) guideline.

### Sort Order

Indexes store references to fields in either ascending ( `1 `) or descending ( `-1 `) sort order. For compound indexes, sort order can determine whether the index supports a sort operation. For more information, see Compound Index Sort Order.

### Hashed Index Fields

Compound indexes may contain a single hashed index field.

### Index Prefixes

Index prefixes are the beginning subsets of indexed fields. Compound indexes support queries on all fields included in the index prefix.

For example, consider this compound index:

```

{ "item": 1, "location": 1, "stock": 1 }
```

The index has these index prefixes:

-
`{ item: 1 } `

-
`{ item: 1, location: 1 } `

MongoDB can use the compound index to support queries on these field combinations:

-
`item `

-
`item `and `location `

-
`item `, `location `, and `stock `

MongoDB can also use the index to support a query on the `item `and `stock `fields, since the `item `field corresponds to a prefix. However, the index is not as efficient as `{ item: 1, stock: 1 } `.

For example, consider a query for `"item": "saccharomyces cerevisiae" `and `"stock": 60 `. If the collection contains 10000 documents matching `"item": "saccharomyces cerevisiae" `and only 100 of those documents match `"stock": 60 `, the query examines 10000 keys. In the `IXSCAN `stage, the query filters those keys by the `stock `field and only returns 100 results to the next stage.

MongoDB's indexing strategy eliminates any need to arrange exact match fields in a particular order. However, if the query does not specify an equality condition on an index prefix that precedes or overlaps with the sort specification, the operation will not efficiently use the index. For more information, see Sort and Non-prefix Subset of an Index.

MongoDB cannot use the compound index to support queries on these field combinations:

-
`location `

-
`stock `

-
`location `and `stock `

Without the `item `field, none of the preceding field combinations correspond to a prefix index.

## Tip

### Remove Redundant Indexes

If you have a collection that has both a compound index and an index on its prefix (for example, `{ a: 1, b: 1 } `and `{ a: 1 } `), if neither index has a sparseor uniqueconstraint, you can remove the index on the prefix ( `{ a: 1 } `). MongoDB uses the compound index in all of the situations that it would have used the prefix index.

### Sparse Compound Indexes

Compound indexes can contain different types of sparse indexes. The combination of index types determines how the compound index matches documents.

This table summarizes the behavior of a compound index that contains different types of sparse indexes:

Compound Index Components

Compound Index Behavior

Ascending indexes
Descending indexes

Only indexes documents that contain a value for at least one of the keys.

Ascending indexes
Descending indexes
Geospatial indexes

Only indexes a document when it contains a value for one of the `geospatial `fields. Does not index documents in the ascending or descending indexes.

Ascending indexes
Descending indexes
Text indexes

Only indexes a document when it matches one of the `text `fields. Does not index documents in the ascending or descending indexes.
