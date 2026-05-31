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

To learn more about the syntax and parameters for the previous commands, see the Atlas CLI documentation for atlas metrics disks describe and atlas metrics disks list.

**See also: Related Links**

- Install the Atlas CLI

- Connect to the Atlas CLI

### Atlas UI

The Clusters view displays all clusters in an Atlas project and features core metrics per cluster. You can also view a cluster's core metrics by clicking on it's name, which then displays the Overview tab. You can quickly view metrics in the available charts at a glance to assess cluster health. You can then click into other views and metrics to identify specific issues. To learn more about the Clusters view, see View All Cloud Clusters.

Monitor cluster metrics to identify performance issues and determine whether your current cluster meets your requirements. For more information on the metrics available to monitor your clusters, see Review Available Metrics.

## Available Charts

Atlas displays up to four of the following charts for each cluster in the project:

**Note: Monitoring Data Storage Granularity**

Atlas stores metrics data at increasing granularity levels. For more information, see Monitoring Data Storage Granularity.

| Chart | Data | Use Case |
| --- | --- | --- |
| Connections | The total number of active connections to the cluster<br>For a replica set, the chart shows the number of active connections to the primary.<br>For a sharded cluster, the chart shows the sum of all active connections to each primary in the cluster. | Monitor connections to determine whether the current connection limits are sufficient. If necessary, scale the cluster tier. |
| Disk IOPS<br><code>M10+</code> <em>Clusters Only</em> | The sum of read and write input/output operations per second (IOPS) for the cluster. | Monitor whether disk IOPS approaches the maximum provisioned IOPS. Determine whether the cluster can handle future workloads. |
| Disk Latency 1 | The latency, in milliseconds, of the disk partition used by MongoDB. | Monitor Disk Latency to determine the average amount of time to read from or write to disk. |
| Disk Usage<br><em>M10+ Clusters Only</em> | The total bytes of used disk space for the cluster.<br>For a replica set, the chart shows the disk usage of the primary host machine.<br>For a sharded cluster, the chart shows the sum of disk usage on each primary host in the cluster.<br>The line graph is green for less than 75% disk usage, yellow for 75%-89% disk usage, and red for 90% or more disk usage. | Monitor the combined size of your data and MongoDB operational data (buffer, journal, and log files) on the cluster.<br>IMPORTANT: The UI displays GB, but all disk usage metrics are in gibibytes (GiB). |
| Logical Size<br><em>Free and Flex Clusters Only</em> | Displays the sum of total bytes of the documents and index data across all databases in the cluster.<br>Logical size in the Atlas UI for time series collections represents the compressed data size after columnar compression.<br>The line graph is green for less than 75% of the max storage size, yellow for 75%-89% of the max storage size, and red for 90% or more of the max storage size. | Monitor the size of the documents and index data on the cluster. |
| Network<br><em>Free and Flex Clusters Only</em> | Displays the average rate of physical bytes or requests sent to/from this database server per second over the selected sample period. | Monitor network metrics to track network performance. |
| Operations | Displays the aggregated read (R) and write (W) operations on the cluster.<br>For a replica set, the chart shows operations for the <a href="https://www.mongodb.com/docs/manual/reference/glossary/#std-term-primary">primary.</a><br>For a <a href="https://www.mongodb.com/docs/manual/reference/glossary/#std-term-sharded-cluster">sharded cluster</a>, the chart shows the sum of the operations on each primary in the cluster. | Monitor performance issues related to high workloads. |

1 Clusters which use NVMe SSDs for storage display `Disk Latency` charts using the maximum value across the physical drives that make up the RAID (Redundant Array of Independent Disks). The following cluster tiers display RAID-based metrics if they use NVMe:

- `M80`

- `M200`

- `M400`
