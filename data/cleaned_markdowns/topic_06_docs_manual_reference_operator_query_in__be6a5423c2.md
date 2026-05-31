> Source: https://www.mongodb.com/docs/manual/reference/operator/query/in/
> Fetch method: direct_markdown

# $in (query predicate operator)

`$in`
The `$in` operator selects the documents where the value of a field equals any value in the specified array.

## Syntax

The `$in` operator has the following form:

```javascript
{ field: { $in: [ <value1>, <value2>, ... <valueN> ] } }
```

For comparison of different BSON type values, see the specified BSON comparison order.

If `field` has an array, the `$in` operator selects the documents whose `field` has an array that contains at least one element that matches a value in the specified array. For example, `<value1>`, `<value2>`, and so on.

`$in` compares each parameter to each document in the collection, which can cause performance issues. To improve performance, create an index on the `field` you want to query. An index allows MongoDB to create bounds for each `$in` element and search more efficiently.

This document describes the `$in` query operator. For the `$in` aggregation operator, see $in (expression operator).

## Query Data on Atlas by Using MongoDB Search

in Operator`$in`For data stored in MongoDB Atlas, you can use the MongoDB Search in Operator operator when running `$search` queries. Running `$in` after `$search` is less performant than running `$search` with the in Operator operator.

To learn more about the MongoDB Search version of this operator, see the in Operator operator in the Atlas documentation.

## Examples

The examples on this page use data from the sample_mflix sample dataset. For details on how to load this dataset into your self-managed MongoDB deployment, see Load the sample dataset. If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

### Match Values

This query selects documents in the `movies` collection where the value of the `rated` field is `"G"` or `"TV-G"`:

```javascript
db.movies.find(
   { rated: { $in: ["G", "TV-G"] } },
   { _id: 0, title: 1 }
)

```

```
[
  { title: 'The Great Train Robbery' },
  { title: 'A Corner in Wheat' },
  { title: 'From Hand to Mouth' },
  { title: 'One Week' },
  { title: 'The Devil to Pay!' },
  { title: 'Footlight Parade' },
  { title: 'Gold Diggers of 1935' },
  { title: 'Naughty Marietta' },
  { title: 'Modern Times' },
  { title: 'Gone with the Wind' },
  { title: 'Fantasia' },
  { title: 'The Man Who Came to Dinner' },
  { title: 'National Velvet' },
  { title: 'Alice in Wonderland' },
  { title: 'The Member of the Wedding' },
  { title: 'Seven Brides for Seven Brothers' },
  { title: 'Around the World in Eighty Days' },
  { title: 'The King and I' },
  { title: 'A King in New York' },
  { title: 'Ben-Hur' }
]

```

Although you can write the query using the `$or` operator, use the `$in` operator rather than the `$or` operator when performing equality checks on the same field.

### Match Values in an Array

The following `updateMany()` operation sets the `familyFriendly` field to `true` when the `rated` array has at least one element that matches either `"G"` or `"TV-G"`:

```javascript
db.movies.updateMany(
   { rated: { $in: ["G", "TV-G"] } },
   { $set: { familyFriendly: true } }
)

```

```
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 536,
  modifiedCount: 536,
  upsertedCount: 0
}

```

For additional examples on querying arrays, see:

- Query an Array

- Query an Array of Embedded Documents

For additional examples on querying, see Query Documents.

### Use `$in` with a Regular Expression

The `$in` operator can select documents using regular expressions of the form `/pattern/`.

This query selects documents in the `movies` collection where the `plot` field either starts with `Alien` or contains `sci-fi`:

```javascript
db.movies.find(
   { plot: { $in: [ /^Alien/ , /sci-fi/ ] } },
   { _id: 0, title: 1, plot: 1 }
)

```

```
[
  {
    plot: 'Aliens come to Earth seeking scientists to help them in their war.',
    title: 'This Island Earth'
  },
  {
    plot: 'Censored by the Polish authorities, this film was reedited and new footage added. It begins with a sci-fi motif: abstract images and electronic music take the viewer from ruins of Lebanon ...',
    title: 'Rece do gèry'
  },
  {
    plot: 'An idyllic sci-fi future has one major drawback: life must end at 30.',
    title: "Logan's Run"
  },
  {
    plot: "Four horror/sci-fi segments directed by four famous directors which are their own versions of classic stories from Rod Serling's landmark television series.",
    title: 'Twilight Zone: The Movie'
  },
  {
    plot: 'Aliens who look like clowns come from outer space and terrorize a small town.',
    title: 'Killer Klowns from Outer Space'
  },
  ...
]

```
