> Source: https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/
> Fetch method: direct_markdown

# `$search`

The [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) stage performs a full-text search on the specified field or fields. The field or fields must be covered by an MongoDB Search [index.](/docs/atlas/atlas-search/index-definitions#std-label-ref-index-definitions)

## Compatibility

The `$search` stage is available in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas/)

- [MongoDB Enterprise](https://www.mongodb.com/docs/manual/administration/install-enterprise/#std-label-install-mdb-enterprise) deployments running version 8.2 or later with the [Kubernetes Operator.](https://www.mongodb.com/docs/kubernetes/current/#std-label-k8s-operator)

- [MongoDB Community](https://www.mongodb.com/docs/manual/administration/install-community/#std-label-install-mdb-community-edition) deployments running version 8.2 or later

## Syntax

A `$search` pipeline stage has the following prototype form:

```json
{
  $search: {
    "index": "<index-name>",
    "<operator-name>"|"<collector-name>": {
      <operator-specification>|<collector-specification>
    },
    "highlight": {
      <highlight-options>
    },
    "concurrent": true | false,
    "count": {
      <count-options>
    },
    "searchAfter"|"searchBefore": "<encoded-token>",
    "scoreDetails": true| false,
    "sort": {
      <fields-to-sort>: 1 | -1
    },
    "returnScope": {
      "path": "<embedded-documents-field-to-retrieve>"
    },
    "returnStoredSource": true | false,
    "searchNodePreference": {
      "key": <preference-string>
    }
  }
}
```

## Fields

The `$search` stage takes a document with the following fields:

<table>
<thead>
<tr>
<th>Field</th>
<th>Type</th>
<th>Necessity</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>&lt;collector-name&gt;</code></td>
<td>object</td>
<td>Conditional</td>
<td>Name of the <a href="/docs/atlas/atlas-search/operators-and-collectors#std-label-collectors-ref">collector</a> to use with the query. You can provide a document that contains the collector-specific options as the value for this field. Either this or <code>&lt;operator-name&gt;</code> is required.</td>
</tr>
<tr>
<td><code>concurrent</code></td>
<td>boolean</td>
<td>Optional</td>
<td>Parallelize search across segments on <a href="/docs/atlas/atlas-search/about/deployment-options#std-label-what-is-search-node">dedicated search
nodes</a>. If you don't have separate search nodes on your cluster, MongoDB Search ignores this flag. If omitted, defaults to <code>false</code>. To learn more, see <a href="/docs/atlas/atlas-search/concurrent-query#std-label-concurrent-ref">Parallelize Query Execution Across Segments.</a></td>
</tr>
<tr>
<td><code>count</code></td>
<td>object</td>
<td>Optional</td>
<td>Document that specifies the <a href="/docs/atlas/atlas-search/counting#std-label-count-ref">count</a> options for retrieving a count of the results. To learn more, see <a href="/docs/atlas/atlas-search/counting#std-label-count-ref">Count MongoDB Search Results.</a></td>
</tr>
<tr>
<td><code>highlight</code></td>
<td>object</td>
<td>Optional</td>
<td>Document that specifies the <a href="/docs/atlas/atlas-search/highlighting#std-label-highlight-ref">highlighting</a> options for displaying search terms in their original context.</td>
</tr>
<tr>
<td><code>index</code></td>
<td>string</td>
<td>Optional</td>
<td>Name of the MongoDB Search index to use. If omitted, defaults to <code>default</code>.<br>If you name your index <code>default</code>, you don't need to specify an <code>index</code> parameter in the <a href="/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search"><code>$search</code></a> pipeline stage. If you give a custom name to your index, you must specify this name in the <code>index</code> parameter.<br>MongoDB Search doesn't return results if you misspell the index name or if the specified index doesn't already exist on the cluster.</td>
</tr>
<tr>
<td><code>&lt;operator-name&gt;</code></td>
<td>object</td>
<td>Conditional</td>
<td>Name of the <a href="/docs/atlas/atlas-search/operators-and-collectors#std-label-operators-ref">operator</a> to search with. You can provide a document that contains the operator-specific options as the value for this field. Either this or <code>&lt;collector-name&gt;</code> is required. Use the <a href="/docs/atlas/atlas-search/operators-collectors/compound#std-label-compound-ref">compound</a> operator to run a compound query with multiple operators.</td>
</tr>
<tr>
<td><code>returnScope</code></td>
<td>Object</td>
<td>Optional</td>
<td>Object that sets the context of the query to the specified embedded document field. You must also specify <code>returnStoredSource</code> and set it to <code>true</code>.</td>
</tr>
<tr>
<td><code>returnStoredSource</code></td>
<td>boolean</td>
<td>Conditional</td>
<td>Flag that specifies whether to perform a full document lookup on the backend database or return only stored source fields directly from MongoDB Search. If omitted, defaults to <code>false</code>. Must be <code>true</code> if you specify <code>returnScope</code>.<br>To learn more, see <a href="/docs/atlas/atlas-search/return-stored-source#std-label-fts-return-stored-source-option">Return Stored Source Fields.</a></td>
</tr>
<tr>
<td><code>searchAfter</code></td>
<td>string</td>
<td>Optional</td>
<td>Reference point for retrieving results. <code>searchAfter</code> returns documents starting immediately following the specified reference point. The reference point must be a Base64-encoded token generated by the <a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/meta/#mongodb-expression-exp.-meta"><code>$meta</code></a> keyword <code>searchSequenceToken</code>. To learn more, see <a href="/docs/atlas/atlas-search/paginate-results#std-label-fts-paginate-results">Paginate the Results</a>. This field is mutually exclusive with the <code>searchBefore</code> field.</td>
</tr>
<tr>
<td><code>searchBefore</code></td>
<td>string</td>
<td>Optional</td>
<td>Reference point for retrieving results. <code>searchBefore</code> returns documents starting immediately before the specified reference point. The reference point must be a Base64-encoded token generated by the <a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/meta/#mongodb-expression-exp.-meta"><code>$meta</code></a> keyword <code>searchSequenceToken</code>. To learn more, see <a href="/docs/atlas/atlas-search/paginate-results#std-label-fts-paginate-results">Paginate the Results</a>. This field is mutually exclusive with the <code>searchAfter</code> field.</td>
</tr>
<tr>
<td><code>searchNodePreference</code></td>
<td>object</td>
<td>Optional</td>
<td>Document that enables preferential routing for this query. If you set a value for this field, Atlas executes this query against the same search node each time as long as that value remains the same, overriding the <a href="/docs/atlas/atlas-search/query-ref#std-label-about-mongot">default query routing</a> behavior.<br>This document contains a key-value pair where the value of <code>key</code> is an arbitrary string.<br>IMPORTANT: Enabling this setting can improve the consistency of your search results, but doesn't guarantee perpetual consistency. Changes to your data set, index structure, cluster topology, or preferred node availability might still cause inconsistencies.</td>
</tr>
<tr>
<td><code>scoreDetails</code></td>
<td>boolean</td>
<td>Optional</td>
<td>Flag that specifies whether to retrieve a detailed breakdown of the score for the documents in the results. If omitted, defaults to <code>false</code>. To view the details, you must use the <a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/meta/">$meta</a> expression in the <a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project"><code>$project</code></a> stage. To learn more, see <a href="/docs/atlas/atlas-search/score/get-details#std-label-fts-score-details">Return the Score Details.</a></td>
</tr>
<tr>
<td><code>sort</code></td>
<td>object</td>
<td>Optional</td>
<td>Document that specifies the fields to sort the MongoDB Search results by in ascending or descending order. You can sort by date, number (integer, float, and double values), and string values. To learn more, see <a href="/docs/atlas/atlas-search/sort#std-label-sort-ref">Sort MongoDB Search Results.</a></td>
</tr>
</tbody>
</table>

## Behavior

[`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) must be the first stage of any pipeline it appears in. [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) cannot be used in:

- a [view definition](https://www.mongodb.com/docs/manual/core/views/)

- a [`$facet`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/facet/#mongodb-pipeline-pipe.-facet) pipeline stage

## Aggregation Variable

[`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) returns only the results of your query. The metadata results of your [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) query are saved in the `$$SEARCH_META` aggregation variable. You can use the `$$SEARCH_META` variable to view the metadata results for your [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) query.

The `$$SEARCH_META` aggregation variable can be used anywhere after a [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) stage in any pipeline, but it can't be used after the [`$lookup`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/#mongodb-pipeline-pipe.-lookup) or [`$unionWith`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/unionWith/#mongodb-pipeline-pipe.-unionWith) stage in any pipeline. The `$$SEARCH_META` aggregation variable can't be used in any subsequent stage after a [`$searchMeta`](/docs/atlas/atlas-search/aggregation-stages/searchMeta#mongodb-pipeline-pipe.-searchMeta) stage.

**Example:**

Suppose the following index on the `sample_mflix.movies` collection.

```json
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "released": {
        "type": "date"
      }
    }
  }
}
```

The following query searches for movies released near September 01, 2011 using the [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) stage. The query includes a:

- [`$project`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project) stage to exclude all fields in the documents except `title` and `released`.

- [`$facet`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/facet/#mongodb-pipeline-pipe.-facet) stage that outputs a:

  - `docs` field with an array of the top `5` search results

  - `meta` field with the value of `$$SEARCH_META` variable

```json
db.movies.aggregate([
  {
    "$search": {
      "near": {
        "path": "released",
        "origin": ISODate("2011-09-01T00:00:00.000+00:00"),
        "pivot": 7776000000
      }
    }
  },
  {
    $project: {
      "_id": 0,
      "title": 1,
      "released": 1
    }
  },
  { "$limit": 5 },
  {
    "$facet": {
      "docs": [],
      "meta": [
        {"$replaceWith": "$$SEARCH_META"},
        {"$limit": 1}
      ]
    }
  }
])
```

**Output:**

```json
{
  "docs" : [
    {
      "title" : "Submarino",
      "released" : ISODate("2011-09-01T00:00:00Z")
    },
    {
      "title" : "Devil's Playground",
      "released" : ISODate("2011-09-01T00:00:00Z")
    },
    {
      "title" : "Bag It",
      "released" : ISODate("2011-09-01T00:00:00Z")
    },
    {
      "title" : "Dos",
      "released" : ISODate("2011-09-01T00:00:00Z")
    },
    {
      "title" : "We Were Here",
      "released" : ISODate("2011-09-01T00:00:00Z")
    }
  ],
  "meta" : [
    { "count" : { "lowerBound" : NumberLong(17373) } }
  ]
}
```

To learn more about the `$$SEARCH_META` variable and its usage, see:

- [facet](/docs/atlas/atlas-search/operators-collectors/facet#std-label-fts-facet-aggregation-variable)

- [count](/docs/atlas/atlas-search/counting#std-label-fts-count-aggregation-variable)

## Troubleshooting

If you are experiencing issues with your MongoDB Search [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) queries, see [Troubleshoot Queries.](/docs/atlas/atlas-search/query-ref#std-label-fts-troubleshooting)
