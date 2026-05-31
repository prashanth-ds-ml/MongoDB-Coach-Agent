> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/aggregation/
> Fetch method: direct_markdown

# Transform Your Data with Aggregation

## Overview

In this guide, you can learn how to use PyMongo to perform **aggregation operations**.

Aggregation operations process data in your MongoDB collections and return computed results. The MongoDB Aggregation framework, which is part of the Query API, is modeled on the concept of data processing pipelines. Documents enter a pipeline that contains one or more stages, and this pipeline transforms the documents into an aggregated result.

An aggregation operation is similar to a car factory. A car factory has an assembly line, which contains assembly stations with specialized tools to do specific jobs, like drills and welders. Raw parts enter the factory, and then the assembly line transforms and assembles them into a finished product.

The **aggregation pipeline** is the assembly line, **aggregation stages** are the assembly stations, and **operator expressions** are the specialized tools.

Python

You can find tutorials that provide detailed explanations of common aggregation tasks in the Complete Aggregation Pipeline Tutorials section of the Server manual. Select a tutorial, and then pick Python from the Select your language drop-down menu in the upper-right corner of the page.

### Aggregation Versus Find Operations

You can use find operations to perform the following actions:

- Select which documents to return

- Select which fields to return

- Sort the results

You can use aggregation operations to perform the following actions:

- Perform find operations

- Rename fields

- Calculate fields

- Summarize data

- Group values

### Limitations

Keep the following limitations in mind when using aggregation operations:

- Returned documents must not violate the BSON document size limit of 16 megabytes.

- Pipeline stages have a memory limit of 100 megabytes by default. You can exceed this limit by using the `allowDiskUse` keyword argument of the `aggregate()` method.

The $graphLookup stage has a strict memory limit of 100 megabytes and ignores the `allowDiskUse` parameter.

## Aggregation Example

This example uses the `sample_restaurants.restaurants` collection from the Atlas sample datasets. To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see Get Started with PyMongo.

To perform an aggregation, pass a list of aggregation stages to the `collection.aggregate()` method.

The following code example produces a count of the number of bakeries in each borough of New York. To do so, it uses an aggregation pipeline with the following stages:

- A $match stage to filter for documents whose `cuisine` field contains the value `"Bakery"`.

- A $group stage to group the matching documents by the `borough` field, accumulating a count of documents for each distinct value.

Select the Synchronous or Asynchronous tab to see the corresponding code:

<Tabs>

<Tab name="Synchronous">

```python
# Define an aggregation pipeline with a match stage and a group stage
pipeline = [
   { "$match": { "cuisine": "Bakery" } },
   { "$group": { "_id": "$borough", "count": { "$sum": 1 } } }
]

# Execute the aggregation
aggCursor = collection.aggregate(pipeline)

# Print the aggregated results
for document in aggCursor:
   print(document)
```

</Tab>

<Tab name="Asynchronous">

```python
# Define an aggregation pipeline with a match stage and a group stage
pipeline = [
   { "$match": { "cuisine": "Bakery" } },
   { "$group": { "_id": "$borough", "count": { "$sum": 1 } } }
]

# Execute the aggregation
aggCursor = await collection.aggregate(pipeline)

# Print the aggregated results
async for document in aggCursor:
   print(document)
```

</Tab>

</Tabs>

The preceding code example produces output similar to the following:

```javascript
{'_id': 'Bronx', 'count': 71}
{'_id': 'Brooklyn', 'count': 173}
{'_id': 'Missing', 'count': 2}
{'_id': 'Manhattan', 'count': 221}
{'_id': 'Queens', 'count': 204}
{'_id': 'Staten Island', 'count': 20}
```

### Explain an Aggregation

To view information about how MongoDB executes your operation, you can instruct MongoDB to **explain** it. When MongoDB explains an operation, it returns **execution plans** and performance statistics. An execution plan is a potential way MongoDB can complete an operation. When you instruct MongoDB to explain an operation, it returns both the plan MongoDB executed and any rejected execution plans.

To explain an aggregation operation, you can use either the PyMongoExplain library or a database command. Select the corresponding tab below to see an example of each method.

<Tabs>

<Tab name="PyMongoExplain">

Use pip to install the `pymongoexplain` library, as shown in the following example:

```sh
python3 -m pip install pymongoexplain
```

The following code example runs the preceding aggregation example and prints the explanation returned by MongoDB:

```python
# Define an aggregation pipeline with a match stage and a group stage
pipeline = [
   { "$match": { "cuisine": "Bakery" } },
   { "$group": { "_id": "$borough", "count": { "$sum": 1 } } }
]

# Execute the operation and print the explanation
result = ExplainableCollection(collection).aggregate(pipeline)
print(result)
```

```javascript
...
'winningPlan': {'queryPlan': {'stage': 'GROUP',
                                      'planNodeId': 3,
                                      'inputStage': {'stage': 'COLLSCAN',
                                                     'planNodeId': 1,
                                                     'filter': {'cuisine': {'$eq': 'Bakery'}},
                                                     'direction': 'forward'}},
                                                    ...
```

</Tab>

<Tab name="Database Command">

The following code example runs the preceding aggregation example and prints the explanation returned by MongoDB:

```python
# Define an aggregation pipeline with a match stage and a group stage
pipeline = [
   { $match: { cuisine: "Bakery" } },
   { $group: { _id: "$borough", count: { $sum: 1 } } }
]

# Execute the operation and print the explanation
result = database.command("aggregate", "collection", pipeline=pipeline, explain=True)
print(result)
```

```javascript
...
'command': {'aggregate': 'collection',
  'pipeline': [{'$match': {'cuisine': 'Bakery'}},
               {'$group': {'_id': '$borough',
                           'count': {'$sum': 1}}}],
  'explain': True,
...
```

</Tab>

</Tabs>

You can use Python's `pprint` module to make explanation results easier to read:

```python
import pprint
...
pprint.pp(result)
```

## Additional Information

### MongoDB Server Manual

For a full list of aggregation stages, see Aggregation Stages in the MongoDB Server manual.

To learn about assembling an aggregation pipeline and view examples, see Aggregation Pipeline.

To learn more about explaining MongoDB operations, see Explain Output and Query Plans.

### API Documentation

For more information about executing aggregation operations with PyMongo, see the following API documentation:

- aggregate()
