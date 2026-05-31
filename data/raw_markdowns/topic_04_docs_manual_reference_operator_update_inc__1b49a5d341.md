> Source: https://www.mongodb.com/docs/manual/reference/operator/update/inc/
> Fetch method: direct_markdown

# $inc (update operator)

## Definition

`$inc`
The [`$inc`](https://www.mongodb.com/docs/reference/operator/update/inc/#mongodb-update-up.-inc) operator increments a field by a specified value.

## Compatibility

`$inc`You can use `$inc` for deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

- [MongoDB Enterprise](https://www.mongodb.com/docs/administration/install-enterprise/#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

- [MongoDB Community](https://www.mongodb.com/docs/administration/install-community/#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Syntax

The [`$inc`](https://www.mongodb.com/docs/reference/operator/update/inc/#mongodb-update-up.-inc) operator has the following form:

```javascript
{ $inc: { <field1>: <amount1>, <field2>: <amount2>, ... } }
```

To specify a `<field>` in an embedded document or in an array, use [dot notation](https://www.mongodb.com/docs/core/document/#std-label-document-dot-notation).

## Behavior

Starting in MongoDB 5.0, update operators process document fields with string-based names in lexicographic order. Fields with numeric names are processed in numeric order. See [Update Operators Behavior](https://www.mongodb.com/docs/reference/mql/update/#std-label-update-operators-processing-order) for details.

The [`$inc`](https://www.mongodb.com/docs/reference/operator/update/inc/#mongodb-update-up.-inc) operator accepts positive and negative values.

If the field does not exist, [`$inc`](https://www.mongodb.com/docs/reference/operator/update/inc/#mongodb-update-up.-inc) creates the field and sets the field to the specified value.

Use of the [`$inc`](https://www.mongodb.com/docs/reference/operator/update/inc/#mongodb-update-up.-inc) operator on a field with a null value will generate an error.

[`$inc`](https://www.mongodb.com/docs/reference/operator/update/inc/#mongodb-update-up.-inc) is an atomic operation within a single document.

Starting in MongoDB 5.0, [`mongod`](https://www.mongodb.com/docs/reference/program/mongod/#mongodb-binary-bin.mongod) no longer raises an error when you use an update operator like [`$inc`](https://www.mongodb.com/docs/reference/operator/update/inc/#mongodb-update-up.-inc) with an empty operand expression ( `{ }` ). An empty update results in no changes and no [oplog](https://www.mongodb.com/docs/reference/glossary/#std-term-oplog) entry is created (meaning that the operation is a no-op).

## Example

Create the `products` collection:

```javascript
db.products.insertOne(
   {
     _id: 1,
     sku: "abc123",
     quantity: 10,
     metrics: { orders: 2, ratings: 3.5 }
   }
)
```

The following [`updateOne()`](https://www.mongodb.com/docs/reference/method/db.collection.updateOne/#mongodb-method-db.collection.updateOne) operation uses the [`$inc`](https://www.mongodb.com/docs/reference/operator/update/inc/#mongodb-update-up.-inc) operator to:

- increase the `"metrics.orders"` field by 1

- increase the `quantity` field by -2 (which decreases `quantity`)

```javascript
db.products.updateOne(
   { sku: "abc123" },
   { $inc: { quantity: -2, "metrics.orders": 1 } }
)
```

The updated document would resemble:

```javascript
{
  _id: 1,
  sku: 'abc123',
  quantity: 8,
  metrics: { orders: 3, ratings: 3.5 }
}
```

- [`db.collection.updateMany()`](https://www.mongodb.com/docs/reference/method/db.collection.updateMany/#mongodb-method-db.collection.updateMany)

- [`db.collection.findAndModify()`](https://www.mongodb.com/docs/reference/method/db.collection.findAndModify/#mongodb-method-db.collection.findAndModify)
