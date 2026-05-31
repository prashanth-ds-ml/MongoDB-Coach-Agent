> Source: https://www.mongodb.com/docs/atlas/atlas-ui/query/filter/
> Fetch method: direct_markdown

# Query Your Data

You can type MongoDB filter documents into the query bar to display only documents which match the specified criteria. To learn more about querying documents, see Query Documents in the MongoDB manual.

## Set Query Filter

1. In Atlas, go to the Data Explorer page for your project.

   If it's not already displayed, select the organization that contains your project from the  Organizations menu in the navigation bar.

   If it's not already displayed, select your project from the Projects menu in the navigation bar.

   In the sidebar, click Data Explorer under the Database heading.

   The Data Explorer displays.

   IMPORTANT: You can also click the name of a cluster to open the Cluster sidebar, and then click Data Explorer under the Shortcuts heading.

2. Set the query filter.

   Select the collection.

   In the Filter field, enter a filter document between the curly braces. You can use all the MongoDB query operators except the `$text` and `$expr` operators.

   **Example:**

   The following filter returns documents that have a `title` value of `Jurassic Park`:

   ```json
   { "title": "Jurassic Park" }
   ```

   Click Find to run the query and view the updated results.

   !Results of applying a query filter

## Examples

The examples on this page use a small example dataset. To import the sample data into your MongoDB deployment, perform the following steps:

1. Copy the following documents to your clipboard:

   ```JSON
   [
      {
         "name": "Andrea Le",
         "email": "andrea_le@fake-mail.com",
         "school": {
            "name": "Northwestern"
         },
         "version": 5,
         "scores": [ 85, 95, 75 ],
         "dateCreated": { "$date": "2003-03-26" }
      },
      {
         "email": "no_name@fake-mail.com",
         "version": 4,
         "scores": [ 90, 90, 70 ],
         "dateCreated": { "$date": "2001-04-15" }
      },
      {
         "name": "Greg Powell",
         "email": "greg_powell@fake-mail.com",
         "version": 1,
         "scores": [ 65, 75, 80 ],
         "dateCreated": { "$date": "1999-02-10" }
      }
   ]
   ```

2. In Atlas, use the left navigation panel to select the database and the collection you want to import the data to.

3. Click the Documents tab.

4. Click Add Data and select Insert Document.

5. Set the View to JSON (`{}`).

6. Paste the JSON documents from your clipboard into the modal.

7. Click Insert.

**Note:**

If you do not have a MongoDB deployment or if you want to query a larger sample data set, see Sample Data for Atlas Clusters for instructions on creating a free-tier cluster with sample data. The following example queries filter the sample documents provided on this page.

### Match by a Single Condition

The following query filter finds all documents where the value of `name` is "Andrea Le":

```shell
{ name: "Andrea Le" }
```

The query returns the following document:

```JSON
{
   "_id": { "$oid": "5e349915cebae490877d561d" },
   "name": "Andrea Le",
   "email": "andrea_le@fake-mail.com",
   "school": {
      "name": "Northwestern"
   },
   "version": 5,
   "scores": [ 85, 95, 75 ],
   "dateCreated": { "$date": "2003-03-26" }
}
```

### Match by Multiple Conditions ($and)

The following query filter finds all documents where `scores` array contains the value `75`, and the `name` is `Greg Powell`:

```shell
{ $and: [ { scores: 75, name: "Greg Powell" } ] }
```

The query returns the following document:

```JSON
{
   "_id": { "$oid":"5a9427648b0beebeb69579cf" },
   "name": "Greg Powell",
   "email": "greg_powell@fake-mail.com",
   "version": 1,
   "scores": [ 65, 75, 80 ],
   "dateCreated": { "$date": "1999-02-10" }
}
```

### Match by Multiple Possible Conditions ($or)

The following query filter uses the `$or` operator to find documents where `version` is `4`, or `name` is `Andrea Le`:

```shell
{ $or: [ { version: 4 }, { name: "Andrea Le" } ] }
```

The query returns the following documents:

```JSON
[
   {
      "_id": { "$oid": "5e349915cebae490877d561d" },
      "name": "Andrea Le",
      "email": "andrea_le@fake-mail.com",
      "school": {
         "name": "Northwestern"
      },
      "version": 5,
      "scores": [ 85, 95, 75 ],
      "dateCreated": { "$date": "2003-03-26" }
   },
   {
      "_id": { "$oid":"5e349915cebae490877d561e" },
      "email": "no_name@fake-mail.com",
      "version": 4,
      "scores": [ 90, 90, 70 ],
      "dateCreated": { "$date": "2001-04-15" }
   }
]
```

### Match by Exclusion ($not)

The following query filter uses the `$not` operator to find all documents where the value of the `name` field is **not** equal to "Andrea Le", or the `name` field does not exist:

```shell
{ name: { $not: { $eq: "Andrea Le" } } }
```

The query returns the following documents:

```JSON
[
   {
      "_id": { "$oid":"5e349915cebae490877d561e" },
      "email": "no_name@fake-mail.com",
      "version": 4,
      "scores": [ 90, 90, 70 ],
      "dateCreated": { "$date": "2001-04-15" }
   },
   {
      "_id": { "$oid":"5a9427648b0beebeb69579cf" },
      "name": "Greg Powell",
      "email": "greg_powell@fake-mail.com",
      "version": 1,
      "scores": [ 65, 75, 80 ],
      "dateCreated": { "$date": "1999-02-10" }
   }
]
```

**See also:**

For a complete list of logical query operators, see Logical Query Operators.

### Match with Comparison Operators

The following query filter uses the `$lte` operator to find all documents where `version` is less than or equal to `4`:

```shell
{ version: { $lte: 4 } }
```

The query returns the following documents:

```JSON
[
   {
      "_id": { "$oid":"5e349915cebae490877d561e" },
      "email": "no_name@fake-mail.com",
      "version": 4,
      "scores": [ 90, 90, 70 ],
      "dateCreated": { "$date": "2001-04-15" }
   },
   {
      "_id": { "$oid":"5a9427648b0beebeb69579cf" },
      "name": "Greg Powell",
      "email": "greg_powell@fake-mail.com",
      "version": 1,
      "scores": [ 65, 75, 80 ],
      "dateCreated": { "$date": "1999-02-10" }
   }
]
```

**See also:**

For a complete list of comparison operators, see Comparison Query Operators.

### Match by Date

The following query filter uses the `$gt` operator and `Date()` method to find all documents where the `dateCreated` field value is later than June 22nd, 2000:

```shell
{ dateCreated: { $gt: new Date('2000-06-22') } }
```

The query returns the following documents:

```JSON
[
   {
      "_id": { "$oid": "5e349915cebae490877d561d" },
      "name": "Andrea Le",
      "email": "andrea_le@fake-mail.com",
      "school": {
         "name": "Northwestern"
      },
      "version": 5,
      "scores": [ 85, 95, 75 ],
      "dateCreated": { "$date": "2003-03-26" }
   },
   {
      "_id": { "$oid": "5e349915cebae490877d561e" },
      "email": "no_name@fake-mail.com",
      "version": 4,
      "scores": [ 90, 90, 70 ],
      "dateCreated": { "$date": "2001-04-15" }
   }
]
```

### Match by Array Conditions

The following query filter uses the `$elemMatch` operator to find all documents where at least one value in the `scores` array is greater than `80` and less than `90`:

```shell
{ scores: { $elemMatch: { $gt: 80, $lt: 90 } } }
```

The query returns the following document because one of the values in the `scores` array is `85`:

```JSON
{
   "_id": { "$oid": "5e349915cebae490877d561d" },
   "name": "Andrea Le",
   "email": "andrea_le@fake-mail.com",
   "school": {
      "name": "Northwestern"
   },
   "version": 5,
   "scores": [ 85, 95, 75 ],
   "dateCreated": { "$date": "2003-03-26" }
}
```

For more query examples, see Query Documents in the MongoDB manual.

### Match by Substring

The following query filter uses the `$regex` operator to find all documents where the value of `email` includes the term "andrea\_le":

```shell
{ email: { $regex: "andrea_le" } }
```

The query returns the following document:

```JSON
{
   "_id": { "$oid": "5e349915cebae490877d561d" },
   "name": "Andrea Le",
   "email": "andrea_le@fake-mail.com",
   "school": {
      "name": "Northwestern"
   },
   "version": 5,
   "scores": [ 85, 95, 75 ],
   "dateCreated": { "$date": "2003-03-26" }
}
```

### Match by Embedded Field

The following query filter finds the document with the `school.name` subfield of "Northwestern":

```shell
{ "school.name": "Northwestern" }
```

The query returns the following document:

```JSON
{
   "_id": { "$oid": "5e349915cebae490877d561d" },
   "name": "Andrea Le",
   "email": "andrea_le@fake-mail.com",
   "school": {
      "name": "Northwestern"
   },
   "version": 5,
   "scores": [ 85, 95, 75 ],
   "dateCreated": { "$date": "2003-03-26" }
}
```

For more query examples, see Query Documents in the MongoDB manual.

## Supported Data Types in the Query Bar

The Atlas Filter supports using the `mongosh` representation of the MongoDB Extended JSON BSON data types.

**Example:**

The following filter returns documents where `start_date` is greater than than the BSON `Date` `2017-05-01`:

```javascript
{ "start_date": {$gt: new Date('2017-05-01')} }
```

By specifying the `Date` type in both `start_date` and the `$gt` comparison operator, Atlas performs the `greater
    than` comparison chronologically, returning documents with `start_date` later than `2017-05-01`.

Without the `Date` type specification, Atlas compares the `start_dates` as strings lexicographically, instead of comparing the values chronologically.

## Clear the Query

To clear the query bar and the results of the query, click Reset.

## How Does the Atlas Query Compare to MongoDB and SQL Queries?

`$filter` corresponds to the `WHERE` clause in a SQL (Structured Query Language) `SELECT` statement.

**Example:**

You have 3,235 articles. You would like to see all articles that Joe Bloggs wrote.

Atlas Filter Option

```javascript
{ author : { $eq : "Joe Bloggs" } }
```

MongoDB Aggregation

```javascript
db.article.aggregate( { $match: { "author": "Joe Bloggs" } } )
```

SQL

```sql
SELECT * FROM article
WHERE author = "Joe Bloggs";
```
