> Source: https://www.mongodb.com/docs/manual/reference/operator/update/unset/
> Fetch method: direct_markdown

# $unset (update operator)

## Definition

The following page refers to the update operator [`$unset`](https://www.mongodb.com/docs/reference/operator/update/unset/#mongodb-update-up.-unset). For the aggregation stage, see [`$unset`](https://www.mongodb.com/docs/reference/operator/aggregation/unset/#mongodb-pipeline-pipe.-unset).

`$unset`
The [`$unset`](https://www.mongodb.com/docs/reference/operator/update/unset/#mongodb-update-up.-unset) operator deletes a particular field.

## Compatibility

`$unset`You can use `$unset` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

Consider the following syntax:

```javascript
{ $unset: { <field1>: "", ... } }
```

The specified value in the [`$unset`](https://www.mongodb.com/docs/reference/operator/update/unset/#mongodb-update-up.-unset) expression (i.e. `""`) does not impact the operation.

To specify a `<field>` in an embedded document or in an array, use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation).

## Behavior

Starting in MongoDB 5.0, update operators process document fields with string-based names in lexicographic order. Fields with numeric names are processed in numeric order. See [Update Operators Behavior](https://www.mongodb.com/docs/reference/mql/update/#std-label-update-operators-processing-order) for details.

If the field does not exist, then [`$unset`](https://www.mongodb.com/docs/reference/operator/update/unset/#mongodb-update-up.-unset) does nothing (i.e. no operation).

When used with [`$`](https://www.mongodb.com/docs/reference/operator/update/positional/#mongodb-update-up.-) to match an array element, [`$unset`](https://www.mongodb.com/docs/reference/operator/update/unset/#mongodb-update-up.-unset) replaces the matching element with `null` rather than removing the matching element from the array. This behavior keeps consistent the array size and element positions.

Starting in MongoDB 5.0, [`mongod`](https://www.mongodb.com/docs/reference/program/mongod/#mongodb-binary-bin.mongod) no longer raises an error when you use an update operator like [`$unset`](https://www.mongodb.com/docs/reference/operator/update/unset/#mongodb-update-up.-unset) with an empty operand expression ( `{ }` ). An empty update results in no changes and no [oplog](https://www.mongodb.com/docs/reference/glossary/#std-term-oplog) entry is created (meaning that the operation is a no-op).

## Example

Create the `products` collection:

```javascript
db.products.insertMany( [
   { "item": "chisel", "sku": "C001", "quantity": 4, "instock": true },
   { "item": "hammer", "sku": "unknown", "quantity": 3, "instock": true },
   { "item": "nails", "sku": "unknown", "quantity": 100, "instock": true }
] )
```

Update the *first* document in the `products` collection where the value of `sku` is `unknown`:

```javascript
db.products.updateOne(
   { sku: "unknown" },
   { $unset: { quantity: "", instock: "" } }
)
```

[`updateOne()`](https://www.mongodb.com/docs/reference/method/db.collection.updateOne/#mongodb-method-db.collection.updateOne) uses the [`$unset`](https://www.mongodb.com/docs/reference/operator/update/unset/#mongodb-update-up.-unset) operator to:

- remove the `quantity` field

- remove the `instock` field

```javascript
{
  item: 'chisel',
  sku: 'C001',
  quantity: 4,
  instock: true
},
{
  item: 'hammer',
  sku: 'unknown'
},
{
  item: 'nails',
  sku: 'unknown',
  quantity: 100,
  instock: true
}
```

[`db.collection.updateMany()`](https://www.mongodb.com/docs/reference/method/db.collection.updateMany/#mongodb-method-db.collection.updateMany)
[`db.collection.findAndModify()`](https://www.mongodb.com/docs/reference/method/db.collection.findAndModify/#mongodb-method-db.collection.findAndModify)
