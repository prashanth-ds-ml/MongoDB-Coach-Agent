> Source: https://www.mongodb.com/docs/atlas/atlas-ui/
> Fetch method: direct_markdown

# Interact with Your Data

## Overview

After loading your data or [our sample data](/docs/atlas/sample-data/load-sample-data#std-label-sample-data), you can use the Atlas UI to interact with the data in the following ways:

- [Manage Databases](/docs/atlas/atlas-ui/databases#std-label-atlas-ui-dbs) in your clusters.

- [Manage Collections](/docs/atlas/atlas-ui/collections#std-label-atlas-ui-collections) in your clusters.

- [Manage Documents](/docs/atlas/atlas-ui/documents#std-label-atlas-ui-docs) in your collections.

- [Manage Indexes](/docs/atlas/atlas-ui/indexes#std-label-atlas-ui-indexes) on your collections.

- [Create and run aggregation pipelines](/docs/atlas/atlas-ui/create-agg-pipeline#std-label-atlas-ui-agg-pipeline) to process data in your collections.

- [Shard Global Clusters](/docs/atlas/shard-global-collection#std-label-de-shard-collection-for-global-writes) to distribute large datasets evenly.

- [Build charts](https://www.mongodb.com/docs/charts/launch-charts/) to visualize data in your databases and collections.

## Required Roles

The following table describes the roles required to perform various actions on an Atlas cluster:

<table>
<thead>
<tr>
<th>Action</th>
<th>Required Roles</th>
</tr>
</thead>
<tbody>
<tr>
<td>Create Databases</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role.</td>
</tr>
<tr>
<td>View Databases</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Only"><code>Project Data Access Read Only</code></a> role.</td>
</tr>
<tr>
<td>Drop Databases</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role.</td>
</tr>
<tr>
<td>Create Collections</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role.</td>
</tr>
<tr>
<td>View Collections</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Only"><code>Project Data Access Read Only</code></a> role.</td>
</tr>
<tr>
<td>Drop Collections</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role.</td>
</tr>
<tr>
<td>Shard Collections</td>
<td>One of the following roles:<br><ul><li><a href="/docs/atlas/reference/user-roles#mongodb-authrole-Organization-Owner"><code>Organization Owner</code></a></li><li><a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Owner"><code>Project Owner</code></a></li></ul></td>
</tr>
<tr>
<td>Insert Documents</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role.</td>
</tr>
<tr>
<td>Delete Documents</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role.</td>
</tr>
<tr>
<td>Edit Documents</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role.</td>
</tr>
<tr>
<td>Create Indexes</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role.</td>
</tr>
<tr>
<td>Drop Indexes</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role.</td>
</tr>
<tr>
<td>Hide Indexes</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role.</td>
</tr>
<tr>
<td>View Indexes</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Only"><code>Project Data Access Read Only</code></a> role.</td>
</tr>
<tr>
<td>Create Aggregation Pipelines</td>
<td>At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role.</td>
</tr>
</tbody>
</table>

## Atlas UI Read Behavior

The Atlas UI reads from the primary unless the primary is unavailable. If the primary is unavailable, the Atlas UI reads from a non-hidden, non-delayed secondary member.

## Disable Atlas UI Data Interaction

To interact with your data in the Atlas UI as described in the [Overview section](/docs/atlas/atlas-ui#std-label-atlas-ui-overview), the Data
Explorer needs to be enabled. Disabling the Data Explorer will not prevent users from building [MongoDB Charts](https://www.mongodb.com/docs/charts/) in the Atlas UI.

**Important: Required Privileges**

To enable or disable Data Explorer for a project, you must have the [`Project Owner`](/docs/atlas/reference/user-roles#mongodb-authrole-Project-Owner)  role for the project or the [`Organization Owner`](/docs/atlas/reference/user-roles#mongodb-authrole-Organization-Owner) role on its parent organization.

Data Explorer is enabled by default. To disable Data Explorer:

1. In Atlas, go to the Project Settings page.

   If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

   If it's not already displayed, select your desired project from the Projects menu in the navigation bar.

   In the sidebar, click the  icon next to Project Overview.

   The [Project Settings](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fsettings%2FgroupSettings) page displays.

2. Set the Data Explorer toggle to Off.

**Important:**

When Data Explorer is disabled, you cannot:

- Terminate slow operations from the [Real-Time Performance Panel.](/docs/atlas/real-time-performance-panel#std-label-real-time-metrics-status-tab)

- Create indexes from the [Performance Advisor](/docs/atlas/performance-advisor#std-label-performance-advisor). You can still view Performance Advisor recommendations, but you must create those indexes from [`mongosh`.](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

- Use the [Search Tester](/docs/atlas/atlas-search/searching#std-label-atlas-search-queries) to run Search queries. You can still run Search queries using [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), [Compass](https://www.mongodb.com/try/download/compass), or [MongoDB drivers.](https://www.mongodb.com/docs/drivers/)

To enable Data Explorer, set the toggle to On.

## Troubleshoot

If you are experiencing issues connecting to your cluster on Data Explorer, see [Troubleshoot Data Explorer Issues.](/docs/atlas/atlas-ui/troubleshoot#std-label-atlas-ui-troubleshoot)
