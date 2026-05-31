> Source: https://www.mongodb.com/docs/manual/reference/operator/query/
> Fetch method: html_fallback

# Query Predicates - Database Manual - MongoDB Docs Query Predicates

Query Predicates - Database Manual - MongoDB Docs

[Make the MongoDB docs better! We value your opinion. Share your feedback for a chance to win $100.](https://research.rallyuxr.com/recruit/clf9wl0m50006e31jbdt7hn51/study/cmobv8cnk2hpei2l3h8qw9zax?channel=share)

[Click here >](https://research.rallyuxr.com/recruit/clf9wl0m50006e31jbdt7hn51/study/cmobv8cnk2hpei2l3h8qw9zax?channel=share)

Docs Menu

Ask MongoDB AI

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Query Language](/docs/manual/reference/mql)

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Query Language](/docs/manual/reference/mql)

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Query Language](/docs/manual/reference/mql)

# Query Predicates

Copy page

Query predicates are expressions that return a boolean that indicates whether a document matches a specified query. For example, `{ name: { $eq: "Alice" } } `is a query predicate that returns documents where the value of the `"name" `field is the string `"Alice" `.

To match the correct documents, you can use the following types of operators in query predicates:

Operator Type

Description

[Array Query Predicate Operators](/docs/manual/reference/mql/query-predicates/arrays/#std-label-query-selectors-arrays)

Return data based on array conditions.

[Bitwise Query Predicate Operators](/docs/manual/reference/mql/query-predicates/bitwise/#std-label-query-selectors-bitwise)

Return data based on bit position conditions.

[Comparison Query Predicate Operators](/docs/manual/reference/mql/query-predicates/comparison/#std-label-query-selectors-comparison)

Return data based on value comparisons such as less than and greater than.

[Data Type Query Predicate Operators](/docs/manual/reference/mql/query-predicates/data-type/#std-label-query-selectors-data-type)

Return data based on field existence or data types.

[Miscellaneous Query Predicate Operators](/docs/manual/reference/mql/query-predicates/misc/#std-label-query-selectors-misc)

Perform specialized functions in query predicates.

[Logical Query Predicate Operators](/docs/manual/reference/mql/query-predicates/logical/#std-label-query-selectors-logical)

Return data based on boolean logic (and, or, and nor).

[Geospatial Query Predicate Operators](/docs/manual/reference/mql/query-predicates/geospatial/#std-label-query-selectors-geospatial)

Return data based on geospatial query predicates, such as containment within a region on the surface of the Earth.

## Alphabetical List of Operators

Name

Description

`[$all](/docs/manual/reference/operator/query/all/#mongodb-query-op.-all)`

Matches arrays that contain all elements specified in the query.

`[$and](/docs/manual/reference/operator/query/and/#mongodb-query-op.-and)`

Joins query clauses with a logical `AND `and returns documents that match the conditions of all clauses.

`[$bitsAllClear](/docs/manual/reference/operator/query/bitsAllClear/#mongodb-query-op.-bitsAllClear)`

Matches numeric or binary values in which a set of bit positions all have a value of `0 `.

`[$bitsAllSet](/docs/manual/reference/operator/query/bitsAllSet/#mongodb-query-op.-bitsAllSet)`

Matches numeric or binary values in which a set of bit positions all have a value of `1 `.

`[$bitsAnyClear](/docs/manual/reference/operator/query/bitsAnyClear/#mongodb-query-op.-bitsAnyClear)`

Matches numeric or binary values in which any bit from a set of bit positions has a value of `0 `.

`[$bitsAnySet](/docs/manual/reference/operator/query/bitsAnySet/#mongodb-query-op.-bitsAnySet)`

Matches numeric or binary values in which any bit from a set of bit positions has a value of `1 `.

`[$elemMatch](/docs/manual/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch)`

Selects documents if at least one element in the array field matches all the specified `[$elemMatch](/docs/manual/reference/operator/query/elemMatch/#mongodb-query-op.-elemMatch)`conditions.

`[$eq](/docs/manual/reference/operator/query/eq/#mongodb-query-op.-eq)`

Matches values that are equal to a specified value.

`[$exists](/docs/manual/reference/operator/query/exists/#mongodb-query-op.-exists)`

Matches documents that have the specified field.

`[$expr](/docs/manual/reference/operator/query/expr/#mongodb-query-op.-expr)`

Allows use of expressions in query predicates.

`[$geoIntersects](/docs/manual/reference/operator/query/geoIntersects/#mongodb-query-op.-geoIntersects)`

Selects geometries that intersect with a [GeoJSON](/docs/manual/reference/glossary/#std-term-GeoJSON)geometry. The [2dsphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere/#std-label-2dsphere-index)index supports `[$geoIntersects](/docs/manual/reference/operator/query/geoIntersects/#mongodb-query-op.-geoIntersects)`[.](/docs/manual/reference/operator/query/geoIntersects/#mongodb-query-op.-geoIntersects)

`[$geoWithin](/docs/manual/reference/operator/query/geoWithin/#mongodb-query-op.-geoWithin)`

Selects geometries within a bounding [GeoJSON geometry](/docs/manual/reference/geojson/#std-label-geospatial-indexes-store-geojson). The [2dsphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere/#std-label-2dsphere-index)and [2d](/docs/manual/core/indexes/index-types/geospatial/2d/#std-label-2d-index)indexes support `[$geoWithin](/docs/manual/reference/operator/query/geoWithin/#mongodb-query-op.-geoWithin)`[.](/docs/manual/reference/operator/query/geoWithin/#mongodb-query-op.-geoWithin)

`[$gt](/docs/manual/reference/operator/query/gt/#mongodb-query-op.-gt)`

Matches values that are greater than a specified value.

`[$gte](/docs/manual/reference/operator/query/gte/#mongodb-query-op.-gte)`

Matches values that are greater than or equal to a specified value.

`[$jsonSchema](/docs/manual/reference/operator/query/jsonSchema/#mongodb-query-op.-jsonSchema)`

Validates documents against the given JSON Schema.

`[$in](/docs/manual/reference/operator/query/in/#mongodb-query-op.-in)`

Matches any of the values specified in an array.

`[$lt](/docs/manual/reference/operator/query/lt/#mongodb-query-op.-lt)`

Matches values that are less than a specified value.

`[$lte](/docs/manual/reference/operator/query/lte/#mongodb-query-op.-lte)`

Matches values that are less than or equal to a specified value.

`[$mod](/docs/manual/reference/operator/query/mod/#mongodb-query-op.-mod)`

Matches documents based on the result of a modulo operation on a field value.

`[$ne](/docs/manual/reference/operator/query/ne/#mongodb-query-op.-ne)`

Matches all values that are not equal to a specified value.

`[$near](/docs/manual/reference/operator/query/near/#mongodb-query-op.-near)`

Returns geospatial objects in proximity to a point. Requires a geospatial index. The `2dsphere `and `2d `indexes support `[$near](/docs/manual/reference/operator/query/near/#mongodb-query-op.-near)`[.](/docs/manual/reference/operator/query/near/#mongodb-query-op.-near)

`[$nearSphere](/docs/manual/reference/operator/query/nearSphere/#mongodb-query-op.-nearSphere)`

Returns geospatial objects in proximity to a point on a sphere. Requires a geospatial index. The `2dsphere `and `2d `indexes support `[$nearSphere](/docs/manual/reference/operator/query/nearSphere/#mongodb-query-op.-nearSphere)`[.](/docs/manual/reference/operator/query/nearSphere/#mongodb-query-op.-nearSphere)

`[$nin](/docs/manual/reference/operator/query/nin/#mongodb-query-op.-nin)`

Matches if the value is not equal to any of a given list of values.

`[$nor](/docs/manual/reference/operator/query/nor/#mongodb-query-op.-nor)`

Joins query clauses with a logical `NOR `and returns all documents that fail to match all clauses.

`[$not](/docs/manual/reference/operator/query/not/#mongodb-query-op.-not)`

Inverts the effect of a query predicate and returns documents that do not match the query predicate.

`[$or](/docs/manual/reference/operator/query/or/#mongodb-query-op.-or)`

Joins query clauses with a logical `OR `and returns all documents that match at least one clause.

`[$regex](/docs/manual/reference/operator/query/regex/#mongodb-query-op.-regex)`

Matches documents where values match a specified regular expression.

`[$size](/docs/manual/reference/operator/query/size/#mongodb-query-op.-size)`

Selects documents if the array field contains the specified number of elements.

`[$type](/docs/manual/reference/operator/query/type/#mongodb-query-op.-type)`

Matches documents if a field is of the specified type.

`[$where](/docs/manual/reference/operator/query/where/#mongodb-query-op.-where)`

Matches documents that satisfy a JavaScript expression.

[Back](/docs/manual/reference/operator/aggregation/vectorSearch/)

[$vectorSearch](/docs/manual/reference/operator/aggregation/vectorSearch/)

[Next](/docs/manual/reference/mql/query-predicates/arrays/)

[Arrays](/docs/manual/reference/mql/query-predicates/arrays/)

Rate this page

On this page

- [Alphabetical List of Operators](#alphabetical-list-of-operators)

On this page

- [Alphabetical List of Operators](#alphabetical-list-of-operators)
