> Source: https://www.mongodb.com/docs/manual/tutorial/model-embedded-one-to-many-relationships-between-documents/
> Fetch method: direct_markdown

# Model One-to-Many Relationships with Embedded Documents

Use [embedded](https://www.mongodb.com/docs/data-modeling/embedding/#std-label-data-modeling-embedding) documents for one-to-many relationships. Embedding connected data in a single document reduces the number of read operations required to retrieve data. Structure your schema so your application receives all required information in a single read operation. For example, use the embedded one-to-many model for the following relationships:

- Country to major cities

- Author to books

- Student to classes

## Example

The example schema contains three entities, with `address one` and `address two` belonging to the same `patron`:

```javascript
// patron document
{
   _id: "joe",
   name: "Joe Bookreader"
}

// address one
{
   street: "123 Fake Street",
   city: "Faketon",
   state: "MA",
   zip: "12345"
}

// address two
{
   street: "1 Some Other Street",
   city: "Boston",
   state: "MA",
   zip: "12345"
}
```

### Embedded Document Pattern

In this example the application needs to display information for the `patron` and both `address` objects on a single page. To retrieve all necessary information with a single query, embed the `address one` and `address two` information inside the `patron` document:

```javascript
{
   _id: "joe",
   name: "Joe Bookreader",
   addresses: [
      {
         street: "123 Fake Street",
         city: "Faketon",
         state: "MA",
         zip: "12345"
      },
      {
         street: "1 Some Other Street",
         city: "Boston",
         state: "MA",
         zip: "12345"
      }
   ]
 }
```

## Learn More

- [Model One-to-One Relationships with Embedded Documents](https://www.mongodb.com/docs/tutorial/model-embedded-one-to-one-relationships-between-documents/#std-label-data-modeling-example-one-to-one)

- [Model One-to-Many Relationships with Document References](https://www.mongodb.com/docs/tutorial/model-referenced-one-to-many-relationships-between-documents/#std-label-data-modeling-publisher-and-books)
