> Source: https://www.mongodb.com/docs/manual/reference/operator/query/size/
> Fetch method: direct_markdown

# $size (query predicate operator)

`$size`
The `$size` operator matches any array with the number of elements specified by the argument.

## Syntax

A `$size` expression has the following syntax:

```javascript
{
   <field>: {
      $size: <number>
   }
}
```

## Additional Examples

For additional examples on querying arrays, see:

- Query an Array

- Query an Array of Embedded Documents

For additional examples on querying, see Query Documents.

`db.collection.find()`
