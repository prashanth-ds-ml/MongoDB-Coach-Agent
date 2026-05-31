> Source: https://www.mongodb.com/docs/atlas/review-all-cluster-metrics/
> Fetch method: direct_markdown

# Review Project Overview

### Atlas CLI

You can view select project metrics using the Atlas CLI.

## View Disk Metrics

To return the metrics for a disk partition on a specified host using the Atlas CLI, run the following command:

```sh

atlas metrics disks describe <hostname:port> <diskName> [options]

```

To list available disks or disk partitions on a specified host using the Atlas CLI, run the following command:

```sh

atlas metrics disks list <hostname:port> [options]

```

To learn more about the syntax and parameters for the previous commands, see the Atlas CLI documentation for [atlas metrics disks describe](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-metrics-disks-describe/) and [atlas metrics disks list.](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-metrics-disks-list/)

**See also: Related Links**

- [Install the Atlas CLI](https://www.mongodb.com/docs/atlas/cli/current/install-atlas-cli/)

- [Connect to the Atlas CLI](https://www.mongodb.com/docs/atlas/cli/current/connect-atlas-cli/)

### Atlas UI

The Clusters view displays all clusters in an Atlas [project](/docs/atlas/organizations-projects#std-label-projects) and features core metrics per cluster. You can also view a cluster's core metrics by clicking on it's name, which then displays the Overview tab. You can quickly view metrics in the available charts at a glance to assess cluster health. You can then click into other views and metrics to identify specific issues. To learn more about the Clusters view, see [View All Cloud Clusters.](/docs/atlas/manage-database-deployments#std-label-view-all-database-deployments)

Monitor cluster metrics to identify performance issues and determine whether your current cluster meets your requirements. For more information on the metrics available to monitor your clusters, see [Review Available Metrics.](/docs/atlas/review-available-metrics#std-label-review-available-metrics)

## Available Charts

Atlas displays up to four of the following charts for each cluster in the project:

**Note: Monitoring Data Storage Granularity**

Atlas stores metrics data at increasing granularity levels. For more information, see [Monitoring Data Storage Granularity.](/docs/atlas/monitor-cluster-metrics#std-label-monitoring-storage-granularity)

<table>
<thead>
<tr>
<th>Chart</th>
<th>Data</th>
<th>Use Case</th>
</tr>
</thead>
<tbody>
<tr>
<td>Connections</td>
<td>The total number of active connections to the cluster<br>For a replica set, the chart shows the number of active connections to the primary.<br>For a sharded cluster, the chart shows the sum of all active connections to each primary in the cluster.</td>
<td>Monitor connections to determine whether the current connection limits are sufficient. If necessary, scale the cluster tier.</td>
</tr>
<tr>
<td>Disk IOPS<br><code>M10+</code> <em>Clusters Only</em></td>
<td>The sum of read and write input/output operations per second (IOPS) for the cluster.</td>
<td>Monitor whether disk IOPS approaches the maximum provisioned IOPS. Determine whether the cluster can handle future workloads.</td>
</tr>
<tr>
<td>Disk Latency 1</td>
<td>The latency, in milliseconds, of the disk partition used by MongoDB.</td>
<td>Monitor Disk Latency to determine the average amount of time to read from or write to disk.</td>
</tr>
<tr>
<td>Disk Usage<br><em>M10+ Clusters Only</em></td>
<td>The total bytes of used disk space for the cluster.<br>For a replica set, the chart shows the disk usage of the primary host machine.<br>For a sharded cluster, the chart shows the sum of disk usage on each primary host in the cluster.<br>The line graph is green for less than 75% disk usage, yellow for 75%-89% disk usage, and red for 90% or more disk usage.</td>
<td>Monitor the combined size of your data and MongoDB operational data (buffer, journal, and log files) on the cluster.<br>IMPORTANT: The UI displays GB, but all disk usage metrics are in gibibytes (GiB).</td>
</tr>
<tr>
<td>Logical Size<br><em>Free and Flex Clusters Only</em></td>
<td>Displays the sum of total bytes of the documents and index data across all databases in the cluster.<br>Logical size in the Atlas UI for time series collections represents the compressed data size after columnar compression.<br>The line graph is green for less than 75% of the max storage size, yellow for 75%-89% of the max storage size, and red for 90% or more of the max storage size.</td>
<td>Monitor the size of the documents and index data on the cluster.</td>
</tr>
<tr>
<td>Network<br><em>Free and Flex Clusters Only</em></td>
<td>Displays the average rate of physical bytes or requests sent to/from this database server per second over the selected sample period.</td>
<td>Monitor network metrics to track network performance.</td>
</tr>
<tr>
<td>Operations</td>
<td>Displays the aggregated read (R) and write (W) operations on the cluster.<br>For a replica set, the chart shows operations for the <a href="https://www.mongodb.com/docs/manual/reference/glossary/#std-term-primary">primary.</a><br>For a <a href="https://www.mongodb.com/docs/manual/reference/glossary/#std-term-sharded-cluster">sharded cluster</a>, the chart shows the sum of the operations on each primary in the cluster.</td>
<td>Monitor performance issues related to high workloads.</td>
</tr>
</tbody>
</table>

1 Clusters which use [NVMe SSDs](/docs/atlas/manage-clusters#std-label-nvme-storage) for storage display `Disk Latency` charts using the maximum value across the physical drives that make up the RAID (Redundant Array of Independent Disks). The following [cluster tiers](/docs/atlas/manage-clusters#std-label-create-cluster-instance) display RAID-based metrics if they use [NVMe:](/docs/atlas/manage-clusters#std-label-nvme-storage)

- `M80`

- `M200`

- `M400`
