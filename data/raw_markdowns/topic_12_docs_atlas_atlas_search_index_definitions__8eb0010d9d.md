> Source: https://www.mongodb.com/docs/atlas/atlas-search/index-definitions/
> Fetch method: direct_markdown

# Index Reference

A MongoDB Search index is a data structure that maps documents from your cluster to the terms that are extracted from those documents. MongoDB Search indexes enable efficient full-text searches of your database.

When you define a MongoDB Search index, you can use [static or dynamic
mappings](/docs/atlas/atlas-search/define-field-mappings#std-label-fts-field-mappings) to specify which fields or field types you want to index in your collection. You can also use [analyzers](/docs/atlas/atlas-search/analyzers#std-label-analyzers-ref) to define how MongoDB Search extracts searchable tokens from `string` fields or query strings. Finally, you can apply additional configuration options in your index definition to improve the performance and accuracy of your MongoDB Search query, including options to [store source fields in your index](/docs/atlas/atlas-search/stored-source-definition#std-label-fts-stored-source-definition), or [define synonym mappings.](/docs/atlas/atlas-search/define-field-mappings#std-label-fts-field-mappings)

To learn how to define a MongoDB Search index according to your query requirements, see [Manage MongoDB Search Indexes](/docs/atlas/atlas-search/manage-indexes#std-label-ref-create-index). Once you define your MongoDB Search index, you can add the index to your cluster with the [Create
a MongoDB Search Index](/docs/atlas/atlas-search/tutorial#std-label-create-fts-index) tutorial. To learn how to view, edit, update, or delete your MongoDB Search index, see [Supported Clients.](/docs/atlas/atlas-search/manage-indexes#std-label-fts-manage-indexes)

This page describes the JSON (Javascript Object Notation) syntax and definition options for a MongoDB Search index.

## Syntax

### Basic

```json
{ 
  "mappings": { 
    "dynamic": <boolean> | { <field-types-definition> } , 
    "fields": { <field-definition> } 
  }
}
  
```

### Expanded

```json
{
  "analyzer": "<analyzer-for-index>", 
  "searchAnalyzer": "<analyzer-for-query>", 
  "mappings": { 
    "dynamic": <boolean> | { 
      "typeSet": "<typeSet-name>" 
    } , 
    "fields": { 
      <field-definition> 
    } 
  },
  "numPartitions": <integer>,
  "analyzers": [ <custom-analyzer> ],
  "storedSource": <boolean> | {
    <stored-source-definition>
  },
  "synonyms": [
    {
      <synonym-mapping-definition>
    }
  ],
  "typeSets": [
    {
      "types": [
        {<field-types-definition>}
      ]
    }
  ]
}
```

## Options

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
<td><code>analyzer</code></td>
<td>String</td>
<td>Optional</td>
<td>Specifies the <a href="/docs/atlas/atlas-search/analyzers#std-label-analyzers-ref">analyzer</a> to apply to string fields when indexing.<br>If you set this only at the top and do not specify an analyzer for the fields in the index definition, MongoDB Search applies this analyzer to all the fields. To use a different analyzer for each field, you must specify a different analyzer for the field.<br>If omitted, defaults to <a href="/docs/atlas/atlas-search/analyzers/standard#std-label-ref-standard-analyzer">Standard Analyzer.</a></td>
</tr>
<tr>
<td><code>analyzers</code></td>
<td>Array of <a href="/docs/atlas/atlas-search/analyzers/custom#std-label-custom-analyzers">Custom Analyzers</a></td>
<td>Optional</td>
<td>Specifies the <a href="/docs/atlas/atlas-search/analyzers/custom#std-label-custom-analyzers">Custom Analyzers</a> to use in this index.</td>
</tr>
<tr>
<td><code>mappings</code></td>
<td>Object</td>
<td>Required</td>
<td>Specifies how to index fields at different paths for this index.</td>
</tr>
<tr>
<td><code>mappings.</code><code>dynamic</code></td>
<td>Boolean or Object</td>
<td>Optional</td>
<td>Enables dynamic mapping of field types or configures fields individually for this index.<br>Value must be one of the following:<br><ul><li>boolean - set to <code>true</code> to recursively index all indexable field types or set to <code>false</code> to not dynamically index any of the indexable field types.</li><li>object - specify the <code>typeSet</code> to use for recursively indexing all indexable field types. To learn more, see <code>mappings.dynamic.typeSet</code>.</li></ul><br>If omitted, defaults to <code>false</code>. If set to <code>false</code>, you must define the individual fields to statically index using <code>mappings.fields</code>.<br>You can also configure fields individually to override default settings using <code>mappings.fields</code>. Settings for fields in <code>mappings.fields</code> override default settings.<br>IMPORTANT: MongoDB Search automatically indexes all dynamically indexable field types in a <code>document</code>. MongoDB Search also recursively indexes all nested documents under the <code>document</code>, unless you explicitly override by setting <code>dynamic</code> to <code>false</code>. You can also configure dynamic indexing to only index specified field types using <code>typeSets</code>.<br>To learn about the field types that you can enable for dynamic mappings, see <a href="/docs/atlas/atlas-search/define-field-mappings#std-label-bson-data-types">MongoDB Search Field Types.</a><br>For example index configurations, see <a href="/docs/atlas/atlas-search/define-field-mappings#std-label-index-config-example">Examples</a></td>
</tr>
<tr>
<td><code>mappings.</code><code>dynamic.</code><code>typeSet</code></td>
<td>String</td>
<td>Optional</td>
<td>References the name of the <code>typeSets</code> object that contains the list of field types to automatically and recursively index.<br>Mutually exclusive with <code>mappings.dynamic</code> boolean flag.</td>
</tr>
<tr>
<td><code>mappings.</code><code>fields</code></td>
<td>Object</td>
<td>Conditional</td>
<td>Specifies the fields that you want to index. Required only if dynamic mapping is <code>false</code>.<br>You can't index fields that contain the dollar (<code>$</code>) sign at the start of the field name.<br>To learn more, see <a href="/docs/atlas/atlas-search/define-field-mappings#std-label-fts-field-mappings">Define Field Mappings.</a></td>
</tr>
<tr>
<td><code>searchAnalyzer</code></td>
<td>String</td>
<td>Optional</td>
<td>Specifies the <a href="/docs/atlas/atlas-search/analyzers#std-label-analyzers-ref">analyzer</a> to apply to query text before searching with it.<br>If omitted, defaults to the analyzer that you specify for the <code>analyzer</code> option. If you omit both the <code>searchAnalyzer</code> and the <code>analyzer</code> options, defaults to the <a href="/docs/atlas/atlas-search/analyzers/standard#std-label-ref-standard-analyzer">Standard Analyzer.</a></td>
</tr>
<tr>
<td><code>numPartitions</code></td>
<td>Integer</td>
<td>Optional</td>
<td>Specifies the number of sub-indexes to create if the document count exceeds two billion. The following values are valid: <code>1</code>, <code>2</code>, <code>4</code>. If omitted, defaults to <code>1</code>.<br>To use index partitions, you must have search nodes deployed in your cluster.</td>
</tr>
<tr>
<td><code>storedSource</code></td>
<td>Boolean or <a href="/docs/atlas/atlas-search/stored-source-definition#std-label-fts-stored-source-definition">Stored Source Definition</a></td>
<td>Optional</td>
<td>Specifies fields in the documents to store for query-time look-ups using the <a href="/docs/atlas/atlas-search/return-stored-source#std-label-fts-return-stored-source-option">returnedStoredSource</a> option. You can store fields of all <a href="/docs/atlas/atlas-search/define-field-mappings#std-label-bson-data-chart">MongoDB Search Field Types</a> on MongoDB Search. Value can be one of the following:<br><ul><li><code>true</code>, to store all fields</li><li><code>false</code>, to not store any fields</li><li><a href="/docs/atlas/atlas-search/stored-source-definition#std-label-fts-stored-source-document">Object</a> that specifies the fields to <code>include</code> or <code>exclude</code> from storage</li></ul><br><code>storedSource</code> is only available on clusters running MongoDB 7.0+.<br>If omitted, defaults to <code>false</code>.<br>To learn more, see <a href="/docs/atlas/atlas-search/stored-source-definition#std-label-fts-stored-source-definition">Define Stored Source Fields in Your MongoDB Search Index.</a></td>
</tr>
<tr>
<td><code>synonyms</code></td>
<td>Array of <a href="/docs/atlas/atlas-search/synonyms#std-label-synonyms-ref">Synonym Mapping Definition</a></td>
<td>Optional</td>
<td>Specifies the synonym mappings to use in your index.<br>An index definition can have only one <a href="/docs/atlas/atlas-search/synonyms#std-label-synonyms-ref">synonym mapping.</a><br>To learn more, see <a href="/docs/atlas/atlas-search/synonyms#std-label-synonyms-ref">Define Synonym Mappings in Your MongoDB Search Index.</a></td>
</tr>
<tr>
<td><code>typeSets</code></td>
<td>Array of objects</td>
<td>Optional</td>
<td>Specifies the <a href="/docs/atlas/atlas-search/define-field-mappings#std-label-fts-configure-dynamic-mappings">typeSets</a> to use in this index for dynamic mappings.</td>
</tr>
<tr>
<td><code>typeSets.</code><code>[n].name</code></td>
<td>String</td>
<td>Required</td>
<td>Specifies the name of the <code>typeSet</code> configuration.</td>
</tr>
<tr>
<td><code>typeSets.</code><code>[n].types</code></td>
<td>Array of objects</td>
<td>Required</td>
<td>Specifies the field types, one per object, to index automatically using dynamic mappings.</td>
</tr>
<tr>
<td><code>typeSets.</code><code>[n].types.</code><code>[n].type</code></td>
<td>String</td>
<td>Required</td>
<td>Specifies the field type to automatically index. To learn more about the field types that you can configure for dynamic mapping, see <a href="/docs/atlas/atlas-search/define-field-mappings#std-label-fts-configure-dynamic-mappings">Configure a <code>typeSet</code>.</a></td>
</tr>
</tbody>
</table>

## Troubleshoot Indexes

### `mongot` Process Not Installed or Running

The following error is returned if you run `$search` queries when the MongoDB Search `mongot` process isn't installed or running:

```shell
MongoError: Remote error from mongot :: caused by :: Error connecting to localhost:28000.
```

The `mongot` process is installed only when the first MongoDB Search index is defined. If you don't have any MongoDB Search index in your cluster, create at least one MongoDB Search index to resolve this error.

## Learn More

To learn how to define a MongoDB Search index to meet your MongoDB Search query needs, see [Manage MongoDB Search Indexes.](/docs/atlas/atlas-search/manage-indexes#std-label-ref-create-index)

To learn how to add an index to your cluster, see [Create a MongoDB Search Index.](/docs/atlas/atlas-search/tutorial#std-label-create-fts-index)

To learn more about the available index configuration options, see the following reference pages:

- [Process Data with Analyzers](/docs/atlas/atlas-search/analyzers#std-label-analyzers-ref)

- [Define Field Mappings](/docs/atlas/atlas-search/define-field-mappings#std-label-fts-field-mappings)

- [Define Stored Source Fields in Your MongoDB Search Index](/docs/atlas/atlas-search/stored-source-definition#std-label-fts-stored-source-definition)

- [Define Synonym Mappings in Your MongoDB Search Index](/docs/atlas/atlas-search/synonyms#std-label-synonyms-ref)
