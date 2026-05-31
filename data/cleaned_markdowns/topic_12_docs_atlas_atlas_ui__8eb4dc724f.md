> Source: https://www.mongodb.com/docs/atlas/atlas-ui/
> Fetch method: direct_markdown

# Interact with Your Data

## Overview

After loading your data or our sample data, you can use the Atlas UI to interact with the data in the following ways:

- Manage Databases in your clusters.

- Manage Collections in your clusters.

- Manage Documents in your collections.

- Manage Indexes on your collections.

- Create and run aggregation pipelines to process data in your collections.

- Shard Global Clusters to distribute large datasets evenly.

- Build charts to visualize data in your databases and collections.

## Required Roles

The following table describes the roles required to perform various actions on an Atlas cluster:

| Action | Required Roles |
| --- | --- |
| Create Databases | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role. |
| View Databases | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Only"><code>Project Data Access Read Only</code></a> role. |
| Drop Databases | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role. |
| Create Collections | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role. |
| View Collections | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Only"><code>Project Data Access Read Only</code></a> role. |
| Drop Collections | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role. |
| Shard Collections | One of the following roles:<br><ul><li><a href="/docs/atlas/reference/user-roles#mongodb-authrole-Organization-Owner"><code>Organization Owner</code></a></li><li><a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Owner"><code>Project Owner</code></a></li></ul> |
| Insert Documents | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role. |
| Delete Documents | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role. |
| Edit Documents | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role. |
| Create Indexes | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role. |
| Drop Indexes | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role. |
| Hide Indexes | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Admin"><code>Project Data Access Admin</code></a> role. |
| View Indexes | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Only"><code>Project Data Access Read Only</code></a> role. |
| Create Aggregation Pipelines | At least the <a href="/docs/atlas/reference/user-roles#mongodb-authrole-Project-Data-Access-Read-Write"><code>Project Data Access Read/Write</code></a> role. |

## Atlas UI Read Behavior

The Atlas UI reads from the primary unless the primary is unavailable. If the primary is unavailable, the Atlas UI reads from a non-hidden, non-delayed secondary member.

## Disable Atlas UI Data Interaction

To interact with your data in the Atlas UI as described in the Overview section, the Data
Explorer needs to be enabled. Disabling the Data Explorer will not prevent users from building MongoDB Charts in the Atlas UI.

**Important: Required Privileges**

To enable or disable Data Explorer for a project, you must have the `Project Owner`  role for the project or the `Organization Owner` role on its parent organization.

Data Explorer is enabled by default. To disable Data Explorer:

1. In Atlas, go to the Project Settings page.

   If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

   If it's not already displayed, select your desired project from the Projects menu in the navigation bar.

   In the sidebar, click the  icon next to Project Overview.

   The Project Settings page displays.

2. Set the Data Explorer toggle to Off.

**Important:**

When Data Explorer is disabled, you cannot:

- Terminate slow operations from the Real-Time Performance Panel.

- Create indexes from the Performance Advisor. You can still view Performance Advisor recommendations, but you must create those indexes from `mongosh`.

- Use the Search Tester to run Search queries. You can still run Search queries using `mongosh`, Compass, or MongoDB drivers.

To enable Data Explorer, set the toggle to On.

## Troubleshoot

If you are experiencing issues connecting to your cluster on Data Explorer, see Troubleshoot Data Explorer Issues.
