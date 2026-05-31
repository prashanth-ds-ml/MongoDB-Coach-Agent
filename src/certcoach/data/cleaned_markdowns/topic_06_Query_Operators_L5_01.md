# Logical Query Predicate Operators

Logical operators return data based on boolean logic (and, or, and nor).

| Name | Description |
| --- | --- |
| `$and` | Joins query clauses with a logical `AND` and returns documents that match the conditions of all clauses. |
| `$nor` | Joins query clauses with a logical `NOR` and returns all documents that fail to match all clauses. |
| `$not` | Inverts the effect of a query predicate and returns documents that do *not* match the query predicate. |
| `$or` | Joins query clauses with a logical `OR` and returns all documents that match at least one clause. |

# $and (query predicate operator)

`$and`
`$and` performs a logical `AND` operation on an array of one or more expressions and selects the documents that satisfy all the expressions.

MongoDB provides an implicit `AND` operation when you specify a comma separated list of expressions.

## Syntax

The `$and` has the following syntax:

```javascript
{ $and: [ { <expression1> }, { <expression2> } , ... , { <expressionN> } ] }
```

## Behavior

`$and``false`When evaluating the clauses in the `$and` expression, MongoDB's query optimizer considers which indexes are available that could help satisfy clauses of the `$and` expression when selecting the best plan to execute.

To allow the query engine to optimize queries, `$and` handles errors as follows:

- If any expression supplied to `$and` would cause an error when evaluated alone, the `$and` containing the expression may cause an error but an error is not guaranteed.

- An expression supplied after the first expression supplied to `$and` may cause an error even if the first expression evaluates to `false`.

Most programming languages and drivers, including the MongoDB Shell (`mongosh`), do not allow the construction of objects with duplicate keys at the same object level. For example:

```javascript
db.inventory.find( { price: { $in: [ 7.99, 3.99 ], $in: [ 4.99, 1.99 ] } } )
```

The previous query is invalid because the field name `price` has duplicate operators at the same object level. The query sent to the server differs from the intent. To make the query work, use an explicit `AND`:

```javascript
db.inventory.find( {
   $and: [
      { price: { $in: [ 7.99, 3.99 ] } },
      { price: { $in: [ 4.99, 1.99 ] } }
   ]
} )
```

The previous query explicitly checks that both conditions are satisfied: the `price` array must include at least one value from each `$in` set. For more information, see Examples.

## Examples

The examples match multiple expressions on the same field.

Consider this query:

```javascript
db.inventory.find( { $and: [ { price: { $ne: 1.99 } }, { price: { $exists: true } } ] } )
```

The query selects all documents in the `inventory` collection where:

- the `price` field value is not equal to `1.99` **and**

- the `price` field exists.

You can simplify this query by combining the operator expressions for the `price` field into a single query object with a nested implicit `AND`:

```javascript
db.inventory.find( { price: { $ne: 1.99, $exists: true } } )
```

Rewrites are not always possible, particularly when duplicate conditions exist on the same field. For example:

```javascript
db.inventory.find( { status: { $ne: "closed", $ne: "archived" } } )
```

The previous query is invalid because it uses `$ne` more than once on the `status` field at the same object level. Use `$nin` instead:

```javascript
db.inventory.find( { status: { $nin: [ "closed", "archived" ] } } )
```

Rewrite the query based on your intent. Consider this query:

```javascript
db.inventory.find( {
   $and: [
      { status: "new" },
      { status: "processing" }
   ]
} )
```

To find documents where `status` is either `new` or `processing`, use `$in`:

```javascript
db.inventory.find( { status: { $in: [ "new", "processing" ] } } )
```

If your `status` field is an array `[ "new", "processing" ]` and you want to check if the document contains both `new` and `processing`, use `$all`:

```javascript
db.inventory.find( { status: { $all: [ "new", "processing" ] } } )
```

The previous query is semantically equivalent to `AND`, but `$all` is clearer when querying array fields.

Similar to duplicate field names, the same considerations apply for duplicate operators used in the query.
