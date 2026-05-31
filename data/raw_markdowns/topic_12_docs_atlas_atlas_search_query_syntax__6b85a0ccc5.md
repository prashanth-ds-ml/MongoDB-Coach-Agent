> Source: https://www.mongodb.com/docs/atlas/atlas-search/query-syntax/
> Fetch method: direct_markdown

# Choose the Aggregation Pipeline Stage

MongoDB Search queries run inside an [aggregation pipeline stage](https://www.mongodb.com/docs/manual/aggregation/), which is the preferred method for performing aggregations.

Aggregation operations process multiple documents and return computed results. You can use aggregation operations to:

- Group values from multiple documents together.

- Perform operations on the grouped data to return a single result.

- Analyze data changes over time.

You can use either the [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) or the [`$searchMeta`](/docs/atlas/atlas-search/aggregation-stages/searchMeta#mongodb-pipeline-pipe.-searchMeta) stage as the first stage in the aggregation pipeline.

<table>
<thead>
<tr>
<th>Aggregation Pipeline Stage</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search"><code>$search</code></a></td>
<td>Conducts full-text searches and returns an ordered list of documents along with additional search metadata. Use <a href="/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search"><code>$search</code></a> to retrieve matching documents with or without facets.</td>
</tr>
<tr>
<td><a href="/docs/atlas/atlas-search/aggregation-stages/searchMeta#mongodb-pipeline-pipe.-searchMeta"><code>$searchMeta</code></a></td>
<td>Conducts full-text searches and returns the metadata without fetching the documents. Use <a href="/docs/atlas/atlas-search/aggregation-stages/searchMeta#mongodb-pipeline-pipe.-searchMeta"><code>$searchMeta</code></a> to retrieve <strong>only</strong> the metadata about your search results, such as the total count of matching documents or facets.</td>
</tr>
</tbody>
</table>

After the [`$search`](/docs/atlas/atlas-search/aggregation-stages/search#mongodb-pipeline-pipe.-search) or the [`$searchMeta`](/docs/atlas/atlas-search/aggregation-stages/searchMeta#mongodb-pipeline-pipe.-searchMeta) stage completes, you can use additional aggregation stages to process documents further. For example, you can use one or more of the following stages, in addition to other stages:

<table>
<thead>
<tr>
<th>Aggregation Pipeline Stage</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/limit/#mongodb-pipeline-pipe.-limit"><code>$limit</code></a></td>
<td>Limits the number of documents passed to the next stage in the pipeline.</td>
</tr>
<tr>
<td><a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/skip/#mongodb-pipeline-pipe.-skip"><code>$skip</code></a></td>
<td>Skips documents that pass into the stage and passes the remaining documents to the next stage in the pipeline.</td>
</tr>
<tr>
<td><a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project"><code>$project</code></a></td>
<td>Passes along documents with the requested fields to the next stage in the pipeline.</td>
</tr>
<tr>
<td><a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/addFields/#mongodb-pipeline-pipe.-addFields"><code>$addFields</code></a></td>
<td>Adds new fields to documents.</td>
</tr>
<tr>
<td><a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/facet/#mongodb-pipeline-pipe.-facet"><code>$facet</code></a></td>
<td>Processes multiple aggregation pipelines within a single stage on the same set of input documents.</td>
</tr>
<tr>
<td><a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/#mongodb-pipeline-pipe.-match"><code>$match</code></a></td>
<td>Filters documents based on a specified query predicate and passes matched documents to the next pipeline stage.</td>
</tr>
<tr>
<td><a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group"><code>$group</code></a></td>
<td>Combines documents with the same fields or expression into a single document by a group key.</td>
</tr>
<tr>
<td><a href="https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/#mongodb-pipeline-pipe.-lookup"><code>$lookup</code></a></td>
<td>Performs a left outer join to a collection in the same database to filter in documents from the &quot;joined&quot; collection for processing.</td>
</tr>
</tbody>
</table>

When you add these stages to your aggregation pipeline, consider the potentially significant performance impact.

To improve performance, we recommend that you use [`$limit`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/limit/#mongodb-pipeline-pipe.-limit) for search results, [paginate](/docs/atlas/atlas-search/paginate-results#std-label-fts-paginate-results) through search results as needed, and [retrieve search results after a reference
point.](/docs/atlas/atlas-search/paginate-results#std-label-paginate-results-search-after)
