> Source: https://www.mongodb.com/docs/manual/reference/operator/query/
> Fetch method: html_fallback

# Query Predicates - Database Manual - MongoDB Docs Query Predicates

Query Predicates - Database Manual - MongoDB Docs

Make the MongoDB docs better! We value your opinion. Share your feedback for a chance to win $100.

Click here >

Docs Menu

Ask MongoDB AI

Docs Home/
Development/
Query Language

Docs Home/
Development/
Query Language

Docs Home/
Development/
Query Language

# Query Predicates

Copy page

Query predicates are expressions that return a boolean that indicates whether a document matches a specified query. For example, `{ name: { $eq: "Alice" } } `is a query predicate that returns documents where the value of the `"name" `field is the string `"Alice" `.

To match the correct documents, you can use the following types of operators in query predicates:

Operator Type

Description

Array Query Predicate Operators

Return data based on array conditions.

Bitwise Query Predicate Operators

Return data based on bit position conditions.

Comparison Query Predicate Operators

Return data based on value comparisons such as less than and greater than.

Data Type Query Predicate Operators

Return data based on field existence or data types.

Miscellaneous Query Predicate Operators

Perform specialized functions in query predicates.

Logical Query Predicate Operators

Return data based on boolean logic (and, or, and nor).

Geospatial Query Predicate Operators

Return data based on geospatial query predicates, such as containment within a region on the surface of the Earth.

## Alphabetical List of Operators

Name

Description

`$all`

Matches arrays that contain all elements specified in the query.

`$and`

Joins query clauses with a logical `AND `and returns documents that match the conditions of all clauses.

`$bitsAllClear`

Matches numeric or binary values in which a set of bit positions all have a value of `0 `.

`$bitsAllSet`

Matches numeric or binary values in which a set of bit positions all have a value of `1 `.

`$bitsAnyClear`

Matches numeric or binary values in which any bit from a set of bit positions has a value of `0 `.

`$bitsAnySet`

Matches numeric or binary values in which any bit from a set of bit positions has a value of `1 `.

`$elemMatch`

Selects documents if at least one element in the array field matches all the specified `$elemMatch`conditions.

`$eq`

Matches values that are equal to a specified value.

`$exists`

Matches documents that have the specified field.

`$expr`

Allows use of expressions in query predicates.

`$geoIntersects`

Selects geometries that intersect with a GeoJSONgeometry. The 2dsphereindex supports `$geoIntersects`.

`$geoWithin`

Selects geometries within a bounding GeoJSON geometry. The 2dsphereand 2dindexes support `$geoWithin`.

`$gt`

Matches values that are greater than a specified value.

`$gte`

Matches values that are greater than or equal to a specified value.

`$jsonSchema`

Validates documents against the given JSON Schema.

`$in`

Matches any of the values specified in an array.

`$lt`

Matches values that are less than a specified value.

`$lte`

Matches values that are less than or equal to a specified value.

`$mod`

Matches documents based on the result of a modulo operation on a field value.

`$ne`

Matches all values that are not equal to a specified value.

`$near`

Returns geospatial objects in proximity to a point. Requires a geospatial index. The `2dsphere `and `2d `indexes support `$near`.

`$nearSphere`

Returns geospatial objects in proximity to a point on a sphere. Requires a geospatial index. The `2dsphere `and `2d `indexes support `$nearSphere`.

`$nin`

Matches if the value is not equal to any of a given list of values.

`$nor`

Joins query clauses with a logical `NOR `and returns all documents that fail to match all clauses.

`$not`

Inverts the effect of a query predicate and returns documents that do not match the query predicate.

`$or`

Joins query clauses with a logical `OR `and returns all documents that match at least one clause.

`$regex`

Matches documents where values match a specified regular expression.

`$size`

Selects documents if the array field contains the specified number of elements.

`$type`

Matches documents if a field is of the specified type.

`$where`

Matches documents that satisfy a JavaScript expression.

Back

$vectorSearch

Next

Arrays

Rate this page

On this page

- Alphabetical List of Operators

On this page

- Alphabetical List of Operators
