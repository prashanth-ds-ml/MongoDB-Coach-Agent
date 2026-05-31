> Source: https://www.mongodb.com/docs/manual/core/databases-and-collections/
> Fetch method: direct_markdown

# Databases and Collections in MongoDB

MongoDB stores data records as documents (BSON documents) in collections. A database holds one or more collections.

You can manage databases and collections using the Atlas UI, `mongosh`, or MongoDB Compass. This page covers Atlas UI procedures. For self-managed deployments, use `mongosh` or MongoDB Compass.

Select your client:

<Tabs>

<Tab name="Atlas UI">

</Tab>

<Tab name="mongosh">

The MongoDB Shell, `mongosh`, is a JavaScript and Node.js REPL (Read Eval Print Loop) environment for interacting with MongoDB deployments. To learn more, see mongosh.

</Tab>

<Tab name="MongoDB Compass">

MongoDB Compass is a powerful GUI for querying, aggregating, and analyzing your MongoDB data in a visual environment. To learn more, see MongoDB Compass.

</Tab>

</Tabs>

## Databases

<Tabs>

<Tab name="Atlas UI">

Log in to Atlas and go to the Data Explorer page for your project.

### Select your organization and project

- If it's not already displayed, select the organization that contains your project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

### Open the Data Explorer

In the sidebar, click Data Explorer under the Database heading.

The Data Explorer displays.

</Tab>

<Tab name="mongosh">

Issue the `use <db>` statement:

```javascript
use myDB
```

</Tab>

<Tab name="MongoDB Compass">

### Start MongoDB Compass and connect to your cluster.

To learn more, see Connect to MongoDB.

### Select Databases.

The Databases tab lists the existing databases for your deployment.

</Tab>

</Tabs>

### Create a Database

<Tabs>

<Tab name="Atlas UI">

#### In MongoDB Atlas, go to the Data Explorer page for your project

- If it's not already displayed, select the organization that contains your project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Data Explorer under the Database heading.

  The Data Explorer displays.

#### Open the Create Database dialog box

In the Connections sidebar, select or hover over your cluster and click the  icon to open the Create Database dialog box.

#### Enter the Database Name and the Collection Name

Enter the Database Name and the Collection Name to create the database and its first collection.

If you want to use custom collation on the collection, select the Use Custom Collation checkbox and select the desired collation settings.

Don't include sensitive information in your database and collection names.

For more information on MongoDB database names and collection names, see Naming Restrictions.

#### Optional. Specify a time series collection

Select whether the collection is a time series collection. If you select to create a time series collection, specify the time field and granularity. You can optionally specify the meta field and the time for old data in the collection to expire.

#### Click Create Database

Upon successful creation, the database and the collection appears in the Connections sidebar.

</Tab>

<Tab name="mongosh">

MongoDB creates the database when you first store data for it. Switch to a non-existent database and run:

```javascript
use myNewDB

db.myNewCollection1.insertOne( { x: 1 } )
```

`insertOne()` creates both the database `myNewDB` and the collection `myNewCollection1` if they do not already exist. Be sure that both names follow MongoDB Naming Restrictions.

</Tab>

<Tab name="MongoDB Compass">

#### Open the Databases tab.

#### Click Create database.

#### Enter the database and collection names.

#### Click Create Database.

</Tab>

</Tabs>

## Collections

MongoDB stores documents in collections. Collections are analogous to tables in relational databases.

### Create a Collection

If a collection does not exist, MongoDB creates the collection when you first store data for that collection.

<Tabs>

<Tab name="Atlas">

#### In MongoDB Atlas, go to the Data Explorer page for your project

- If it's not already displayed, select the organization that contains your project from the  Organizations menu in the navigation bar.

- If it's not already displayed, select your project from the Projects menu in the navigation bar.

- In the sidebar, click Data Explorer under the Database heading.

  The Data Explorer displays.

#### Open the Create Collection dialog box.

Select or hover over the database, and click the  icon to open the Create Collection dialog box.

#### Enter the Collection Name.

In the Create Collection dialog box, enter the name of the collection you want to create.

MongoDB Atlas also provides Additional preferences. You can choose from the following options:

- Create a Clustered Collection

- Create a Collection with Collation

Don't include sensitive information in your collection name.

For more information on MongoDB collection names, see Naming Restrictions.

#### Optional. Specify a time series collection.

Select whether the collection is a time series collection. If you select to create a time series collection, specify the time field and granularity. You can optionally specify the meta field and the time for old data in the collection to expire.

#### Click Create Collection.

Upon successful creation, the collection appears underneath the database in the Connections sidebar.

</Tab>

<Tab name="mongosh">

```javascript
db.myNewCollection2.insertOne( { x: 1 } )
db.myNewCollection3.createIndex( { y: 1 } )
```

Both `insertOne()` and `createIndex()` create their respective collection if it does not already exist. Be sure the collection name follows MongoDB Naming Restrictions.

</Tab>

<Tab name="MongoDB Compass">

#### In the left navigation, click the database name.

#### Click + next to the database name.

#### Enter a name in Create Collection.

#### Click Create Collection.

</Tab>

</Tabs>

<Tabs>

<Tab name="Atlas">

</Tab>

<Tab name="mongosh">

#### Explicit Creation

Use `db.createCollection()` to explicitly create a collection with options such as maximum size or validation rules. Without these options, MongoDB automatically creates collections when you first store data.

To modify these collection options, see `collMod`.

</Tab>

<Tab name="MongoDB Compass">

#### Explicit creation

##### In the left navigation, click the database name.

##### Click Create collection.

##### Enter the collection name and optional preferences.

##### Click Create Collection.

MongoDB Compass supports the following additional preferences:

- Create a Capped Collection

- Create a Clustered Collection

- Create a Collection with Collation

- Create a Collection with Encrypted Field

- Create a Time Series Collection

</Tab>

</Tabs>

### Schema Validation

By default, documents in a collection do not share a schema. Fields and data types can vary across documents.

You can enforce schema validation rules during insert and update operations.

For MongoDB Atlas deployments, the Performance Advisor and the MongoDB Atlas UI detect common schema design issues and suggest modifications that follow MongoDB best practices. To learn more, see Schema Suggestions.

### Modifying Document Structure

To add, remove, or retype fields in a collection's documents, update the existing documents.

### Unique Identifiers

Collections are assigned an immutable UUID (Universally unique identifier) that remains consistent across all replica set members and shards.

<Tabs>

<Tab name="Atlas">

</Tab>

<Tab name="mongosh">

To retrieve the UUID for a collection, run either the listCollections command or the `db.getCollectionInfos()` method.

</Tab>

<Tab name="MongoDB Compass">

</Tab>

</Tabs>
