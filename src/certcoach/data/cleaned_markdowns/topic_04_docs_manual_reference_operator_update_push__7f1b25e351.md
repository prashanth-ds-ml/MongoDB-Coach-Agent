> Source: https://www.mongodb.com/docs/manual/reference/operator/update/push/
> Fetch method: direct_markdown

# $push (update operator)

## Definition

`$push`
The `$push` operator appends a specified value to an array.

## Syntax

The `$push` operator has the form:

```javascript
{ $push: { <field1>: <value1>, ... } }
```

To specify a `<field>` in an embedded document or in an array, use dot notation.

## Behavior

Starting in MongoDB 5.0, update operators process document fields with string-based names in lexicographic order. Fields with numeric names are processed in numeric order. See Update Operators Behavior for details.

If the field is absent in the document to update, `$push` adds the array field with the value as its element.

If the field is **not** an array, the operation will fail.

If the value is an array, `$push` appends the whole array as a *single* element. To add each element of the value separately, use the `$each` modifier with `$push`. For an example, see Append a Value to Arrays in Multiple Documents. For a list of modifiers available for `$push`, see Modifiers.

Starting in MongoDB 5.0, `mongod` no longer raises an error when you use an update operator like `$push` with an empty operand expression ( `{ }` ). An empty update results in no changes and no oplog entry is created (meaning that the operation is a no-op).

## Modifiers

You can use the `$push` operator with the following modifiers:

| Modifier | Description |
| --- | --- |
| `$each` | Appends multiple values to the array field. |
| `$slice` | Limits the number of array elements. Requires the use of the `$each` modifier. |
| `$sort` | Orders elements of the array. Requires the use of the `$each` modifier. |
| `$position` | Specifies the location in the array at which to insert the new elements. Requires the use of the `$each` modifier. Without the `$position` modifier, the `$push` appends the elements to the end of the array. |
When used with modifiers, the `$push` operator has the form:

```javascript
{ $push: { <field1>: { <modifier1>: <value1>, ... }, ... } }
```

The processing of the `$push` operation with modifiers occur in the following order, regardless of the order in which the modifiers appear:

1. Update array to add elements in the correct position.

2. Apply sort, if specified.

3. Slice the array, if specified.

4. Store the array.

## Examples

Create the `students` collection:

```javascript
db.students.insertOne( { _id: 1, scores: [ 44, 78, 38, 80 ] } )
```

### Append a Value to an Array

The following example appends `89` to the `scores` array:

```javascript
db.students.updateOne(
   { _id: 1 },
   { $push: { scores: 89 } }
)
```

Example output:

```javascript
{ _id: 1, scores: [ 44, 78, 38, 80, 89 ] }
```

### Append a Value to Arrays in Multiple Documents

Add the following documents to the `students` collection:

```javascript
db.students.insertMany( [
   { _id: 2, scores: [ 45, 78, 38, 80, 89 ] } ,
   { _id: 3, scores: [ 46, 78, 38, 80, 89 ] } ,
   { _id: 4, scores: [ 47, 78, 38, 80, 89 ] }
] )
```

The following `$push` operation appends `95` to the `scores` array in each document:

```javascript
db.students.updateMany(
   { },
   { $push: { scores: 95 } }
)
```

To confirm that each `scores` array includes `95`, run the following operation:

```javascript
db.students.find()
```

The operation returns the following results:

```javascript
[
   { _id: 1, scores: [ 44, 78, 38, 80, 89, 95 ] },
   { _id: 2, scores: [ 45, 78, 38, 80, 89, 95 ] },
   { _id: 3, scores: [ 46, 78, 38, 80, 89, 95 ] },
   { _id: 4, scores: [ 47, 78, 38, 80, 89, 95 ] }
]
```

### Append Multiple Values to an Array

Use `$push` with the `$each` modifier to append multiple values to the array field.

The following example appends each element of `[ 90, 92, 85 ]` to the `scores` array for the document where the `name` field equals `joe`:

```javascript
db.students.updateOne(
   { name: "joe" },
   { $push: { scores: { $each: [ 90, 92, 85 ] } } }
)
```

### Use `$push` Operator with Multiple Modifiers

Add the following document to the `students` collection:

```javascript
db.students.insertOne(
   {
      "_id" : 5,
      "quizzes" : [
         { "wk": 1, "score" : 10 },
         { "wk": 2, "score" : 8 },
         { "wk": 3, "score" : 5 },
         { "wk": 4, "score" : 6 }
      ]
   }
)
```

The following `$push` operation uses:

- the `$each` modifier to add multiple documents to the `quizzes` array,

- the `$sort` modifier to sort all the elements of the modified `quizzes` array by the `score` field in descending order, and

- the `$slice` modifier to keep only the **first** three sorted elements of the `quizzes` array.

```javascript
db.students.updateOne(
   { _id: 5 },
   {
     $push: {
       quizzes: {
          $each: [ { wk: 5, score: 8 }, { wk: 6, score: 7 }, { wk: 7, score: 6 } ],
          $sort: { score: -1 },
          $slice: 3
       }
     }
   }
)
```

After the operation only the three highest scoring quizzes are in the array:

```javascript
{
  "_id" : 5,
  "quizzes" : [
     { "wk" : 1, "score" : 10 },
     { "wk" : 2, "score" : 8 },
     { "wk" : 5, "score" : 8 }
  ]
}
```

- `db.collection.updateMany()`

- `db.collection.findAndModify()`
