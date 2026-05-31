> Source: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/atlas-search/
> Fetch method: direct_markdown

# MongoDB Search

## Overview

In this guide, you can learn how to query a MongoDB Search index and use advanced full-text search functionality in your PyMongo applications. You can query a search index by using a `$search` aggregation pipeline stage.

To learn more about the `$search` pipeline stage, see the $search guide in the MongoDB Server manual.

The `$search` aggregation-pipeline operator is available only for collections hosted on MongoDB Atlas clusters running MongoDB v4.2 or later that are covered by a MongoDB Search index. To learn more about the required setup and the functionality of this operator, see the MongoDB Search documentation.

### Sample Data

The examples in this guide use the `sample_mflix.movies` collection from the Atlas sample datasets. To learn how to create a free MongoDB Atlas cluster and load the sample datasets, see Get Started with PyMongo.

## Create a MongoDB Search Index

Before you can perform a search on an Atlas collection, you must first create a **MongoDB Search index** on the collection. A MongoDB Search index is a data structure that categorizes data in a searchable format. To learn how to create a MongoDB Search index, see MongoDB Search and Vector Search Indexes.

## Search Your Data

To use the `$search` aggregation pipeline stage, you must specify a MongoDB Search query operator that indicates the type of query you want to run. You can also optionally specify a collector that groups results by values or ranges. To view a table of all the operators and collectors available with MongoDB Search, see Use Operators and Collectors in MongoDB Search Queries.

The following example uses the `compound` operator to combine several operators into a single query. To learn more about the `compound` operator, see the Compound operator guide in the MongoDB Atlas documentation.

The query has the following search criteria:

- The `genres` field must not contain `Comedy`.

- The `title` field must contain the string `New York`.

The query also includes the following stages:

- `$limit`, to limit the output to 10 results.

- `$project`, to exclude all fields except `title` and add a field named `score`.

```python
client = pymongo.MongoClient("<connection-string>")
result = client["sample_mflix"]["movies"].aggregate([
         {
            "$search": {
              "index": "pymongoindex",
              "compound": {
              "mustNot": [
                  {
                      "text": {
                          "query": [
                              "Comedy"
                          ],
                          "path": "genres"
                      }
                  }
              ],
              "must": [
                  {
                      "text": {
                          "query": [
                              "New York"
                          ],
                          "path": "title"
                        }
                     }
                  ],
               }
            }
         },
         { "$limit": 10 },
         {
           "$project": {
           "_id": 0,
           "title": 1,
           "score": { "$meta": "searchScore" }
      }
    }
])

for i in result:
   print(i)
```

```none
{'title': 'New York, New York', 'score': 6.786379814147949}
{'title': 'New York', 'score': 6.258603096008301}
{'title': 'New York Doll', 'score': 5.381444931030273}
{'title': 'Escape from New York', 'score': 4.719935417175293}
{'title': 'Autumn in New York', 'score': 4.719935417175293}
{'title': 'Sleepless in New York', 'score': 4.719935417175293}
{'title': 'Gangs of New York', 'score': 4.719935417175293}
{'title': 'Sherlock Holmes in New York', 'score': 4.203253746032715}
{'title': 'New York: A Documentary Film', 'score': 4.203253746032715}
{'title': 'An Englishman in New York', 'score': 4.203253746032715}
```

## Additional Information

To learn more about the available MongoDB Search operators, see the Operators and Collectors guide in the MongoDB Atlas documentation.

For more information about MongoDB Search, and to view more query examples, see the MongoDB Search documentation.

If you'd like to perform vector searches on your data stored in Atlas, you must use MongoDB Vector Search. To learn more about MongoDB Vector Search, see the MongoDB Vector Search documentation.
