> Source: https://www.mongodb.com/docs/manual/tutorial/model-referenced-one-to-many-relationships-between-documents/
> Fetch method: direct_markdown

# Model One-to-Many Relationships with Document References

## Overview

This page describes a data model that uses [references](https://www.mongodb.com/docs/data-modeling/referencing/#std-label-data-modeling-referencing) between documents for one-to-many relationships.

## Pattern

The following example maps publisher and book relationships. It illustrates the advantage of referencing over embedding to avoid repeating the publisher information.

Embedding the publisher document inside the book document repeats the publisher data, as shown in the following example:

```javascript
{
   title: "MongoDB: The Definitive Guide",
   author: [ "Kristina Chodorow", "Mike Dirolf" ],
   published_date: ISODate("2010-09-24"),
   pages: 216,
   language: "English",
   publisher: {
              name: "O'Reilly Media",
              founded: 1980,
              location: "CA"
            }
}

{
   title: "50 Tips and Tricks for MongoDB Developer",
   author: "Kristina Chodorow",
   published_date: ISODate("2011-05-06"),
   pages: 68,
   language: "English",
   publisher: {
              name: "O'Reilly Media",
              founded: 1980,
              location: "CA"
            }
}
```

To avoid repeated publisher data, use *references* and keep the publisher information in a separate collection from the book collection.

The growth of the relationships determines where to store the reference. If the number of books per publisher is small with limited growth, store the book reference inside the publisher document. If the number of books per publisher is unbounded, this data model creates mutable, growing arrays, as in the following example:

```javascript
{
   name: "O'Reilly Media",
   founded: 1980,
   location: "CA",
   books: [123456789, 234567890, ...]
}

{
    _id: 123456789,
    title: "MongoDB: The Definitive Guide",
    author: [ "Kristina Chodorow", "Mike Dirolf" ],
    published_date: ISODate("2010-09-24"),
    pages: 216,
    language: "English"
}

{
   _id: 234567890,
   title: "50 Tips and Tricks for MongoDB Developer",
   author: "Kristina Chodorow",
   published_date: ISODate("2011-05-06"),
   pages: 68,
   language: "English"
}
```

To avoid mutable, growing arrays, store the publisher reference inside the book document:

```javascript
{
   _id: "oreilly",
   name: "O'Reilly Media",
   founded: 1980,
   location: "CA"
}

{
   _id: 123456789,
   title: "MongoDB: The Definitive Guide",
   author: [ "Kristina Chodorow", "Mike Dirolf" ],
   published_date: ISODate("2010-09-24"),
   pages: 216,
   language: "English",
   publisher_id: "oreilly"
}

{
   _id: 234567890,
   title: "50 Tips and Tricks for MongoDB Developer",
   author: "Kristina Chodorow",
   published_date: ISODate("2011-05-06"),
   pages: 68,
   language: "English",
   publisher_id: "oreilly"
}
```
