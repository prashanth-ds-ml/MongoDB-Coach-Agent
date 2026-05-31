> Source: https://www.mongodb.com/docs/atlas/manage-clusters/
> Fetch method: direct_markdown

# Manage Clusters

Use the following resources to configure and manage Atlas clusters.

## Required Access

To view your clusters, you must have [`Project Read Only`](/docs/atlas/reference/user-roles#mongodb-authrole-Project-Read-Only) access or higher to the project.

## View Your Clusters

### Atlas CLI

To list all clusters for your project using the Atlas CLI, run the following command:

```sh

atlas clusters list [options]

```

To return the details for the cluster you specify using the Atlas CLI, run the following command:

```sh

atlas clusters describe <clusterName> [options]

```

To learn more about the syntax and parameters for the previous commands, see the Atlas CLI documentation for [atlas clusters list](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-clusters-list/) and [atlas clusters describe.](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-clusters-describe/)

**See also: Related Links**

- [Install the Atlas CLI](https://www.mongodb.com/docs/atlas/cli/current/install-atlas-cli/)

- [Connect to the Atlas CLI](https://www.mongodb.com/docs/atlas/cli/current/connect-atlas-cli/)

To return the advanced configuration settings details for the cluster you specify using the Atlas CLI, run the following command:

```sh

atlas clusters advancedSettings describe <clusterName> [options]

```

To learn more about the command syntax and parameters, see the Atlas CLI documentation for [atlas clusters advancedSettings describe.](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-clusters-advancedSettings-describe/)

### Atlas UI

To view all clusters in the Atlas UI, see [View All Cloud Clusters](/docs/atlas/manage-database-deployments#std-label-view-all-database-deployments). To view the details for a cluster, see [View Cluster Details.](/docs/atlas/manage-database-deployments#std-label-view-cluster-details)

## Select Cluster Tier

Select your preferred cluster tier. The cluster tier dictates the memory, storage, vCPUs, and IOPS (Input/Output Operations per Second) specification for each data-bearing server  in the cluster.

**Note:**

You might see different values depending on your selected cloud provider and region.

### Flex Clusters

Use Flex clusters as an economical way for getting started with MongoDB and for low-throughput applications. These clusters deploy to an environment with access to a subset of Atlas features. To learn more, see [Limits on Atlas Cluster Types.](/docs/atlas/reference/limitations#std-label-limits)

You can deploy one Free cluster (free sandbox replica set cluster) per Atlas project. You can [upgrade](/docs/atlas/scale-cluster) a Free cluster to a Flex cluster at any time.

Flex clusters provide the following added features compared to Free clusters:

- [Backups](/docs/atlas/backup/cloud-backup/flex-cluster-backup#std-label-flex-snapshots) for your cluster data

- Increased storage

- [API access](/docs/atlas/api)

#### Considerations

Flex clusters don't have the full availability of features found in Dedicated clusters. To learn more, see [Limits on Atlas Cluster Types.](/docs/atlas/reference/limitations#std-label-limits)

### Dedicated Clusters for Low-Traffic Applications

`M10` and `M20` cluster tiers support development environments and production environments with low-traffic applications.

These clusters support replica set deployments only, but otherwise provide full access to Atlas features.

**Note:**

`M10` and `M20` cluster tiers use burstable performance infrastructure. Cloud providers cap CPU usage after burst periods, which can cause throttling under heavy load. To learn more, see [How Atlas Scales Cluster Tier.](/docs/atlas/cluster-autoscaling#std-label-howitworks-scale-cluster-tier)

### Dedicated Clusters for High-Traffic Applications

`M30` and higher clusters are recommended for production environments.

These clusters support replica set and sharded cluster deployments with full access to Atlas features.

Some clusters have variants, denoted by the ❯ character. When you select these clusters, Atlas lists the variants and tags each cluster to distinguish their key characteristics.

### Sharded Clusters

You can use the Atlas Administration API to choose a different tier per shard in a sharded cluster. You can also select [Analytics node](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-analytics-node) tiers indepenently for each shard. The largest and smallest shard tiers must be within two tiers of each other. For example, if the largest shard is `M50`, the smallest shard can be `M30` or `M40`. If you change the cluster tier for a sharded cluster in the Atlas UI, Atlas changes the tier of all shards in the cluster.

You can also use the Atlas Administration API to choose different IOPS (Input/Output Operations per Second) per shard if the cluster is on AWS (Amazon Web Services) using AWS (Amazon Web Services) provisioned IOPS or the cluster is on Azure (Microsoft Azure) in regions that support Extended IOPS/storage.

To learn more, see [Manage Cluster Sharding](/docs/atlas/cluster-sharding#std-label-atlas-cluster-sharding) and the [Update One Cluster in One Project](https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/operation/operation-updategroupcluster) endpoint in the Atlas Administration API documentation.

#### Limitations

Every shard must have an equal disk size on all nodes. NVMe (non-volatile memory express) clusters are not compatible with independent shard scaling.

NVMe (non-volatile memory express) instances can't be used in multi-cloud clusters.

### NVMe Storage

For applications hosted on [AWS](/docs/atlas/reference/amazon-aws#std-label-amazon-aws) or  [Azure](/docs/atlas/reference/microsoft-azure#std-label-microsoft-azure) that require low-latency and high-throughput I/O, Atlas offers storage options using locally attached ephemeral NVMe (non-volatile memory express) SSD (Solid State Disk)s.

[A File Copy Based Initial Sync](https://www.mongodb.com/docs/manual/core/replica-set-sync/#file-copy-based-initial-sync) will always be used to sync all of the nodes of an NVME cluster whenever an initial sync is required.

**Note:**

Atlas doesn't support NVMe (non-volatile memory express) clusters on Google Cloud. NVMe (non-volatile memory express) clusters are not compatible with independent shard scaling.

#### NVMe Considerations

The following cluster tiers support NVMe (non-volatile memory express) clusters on AWS (Amazon Web Services):

- `M40`

- `M50`

- `M60`

- `M80`

- `M200`

- `M400`

The following cluster tiers support NVMe (non-volatile memory express) clusters on Azure (Microsoft Azure):

- `M60`

- `M80`

- `M200`

- `M300`

- `M400`

- `M600`

Atlas supports NVMe (non-volatile memory express) clusters in the following Azure (Microsoft Azure) regions:

### Americas

<table>
<thead>
<tr>
<th>Azure Region</th>
<th>Location</th>
<th>Atlas Region</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>brazilsouth</code></td>
<td>São Paulo, Brazil</td>
<td><code>BRAZIL_SOUTH</code></td>
</tr>
<tr>
<td><code>canadacentral</code></td>
<td>Toronto, ON</td>
<td><code>CANADA_CENTRAL</code></td>
</tr>
<tr>
<td><code>centralus</code></td>
<td>Iowa, USA</td>
<td><code>US_CENTRAL</code></td>
</tr>
<tr>
<td><code>eastus</code></td>
<td>Virginia (East US)</td>
<td><code>US_EAST</code></td>
</tr>
<tr>
<td><code>eastus2</code></td>
<td>Virginia, USA</td>
<td><code>US_EAST_2</code></td>
</tr>
<tr>
<td><code>southcentralus</code></td>
<td>Texas, USA</td>
<td><code>US_SOUTH_CENTRAL</code></td>
</tr>
<tr>
<td><code>westus3</code></td>
<td>El Mirage, Arizona</td>
<td><code>US_WEST_3</code></td>
</tr>
</tbody>
</table>

### Europe

<table>
<thead>
<tr>
<th>Azure Region</th>
<th>Location</th>
<th>Atlas Region</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>francecentral</code></td>
<td>Paris, France</td>
<td><code>FRANCE_CENTRAL</code></td>
</tr>
<tr>
<td><code>northeurope</code></td>
<td>Ireland</td>
<td><code>EUROPE_NORTH</code></td>
</tr>
<tr>
<td><code>swedencentral</code></td>
<td>Gävle, Sweden</td>
<td><code>SWEDEN_CENTRAL</code></td>
</tr>
<tr>
<td><code>uksouth</code></td>
<td>London, England, UK</td>
<td><code>UK_SOUTH</code></td>
</tr>
<tr>
<td><code>westeurope</code></td>
<td>Netherlands</td>
<td><code>EUROPE_WEST</code></td>
</tr>
</tbody>
</table>

### Asia Pacific

<table>
<thead>
<tr>
<th>Azure Region</th>
<th>Location</th>
<th>Atlas Region</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>australiaeast</code></td>
<td>New South Wales, Australia</td>
<td><code>AUSTRALIA_EAST</code></td>
</tr>
<tr>
<td><code>centralindia</code></td>
<td>Pune (Central India)</td>
<td><code>INDIA_CENTRAL</code></td>
</tr>
<tr>
<td><code>japaneast</code></td>
<td>Saitama, Tokyo, Japan</td>
<td><code>JAPAN_EAST</code></td>
</tr>
</tbody>
</table>

The fixed-value storage space and RAM for an NVMe (non-volatile memory express) cluster corresponds to its cluster tier. To learn more, see [Amazon Cluster Configuration Options](/docs/atlas/reference/amazon-aws#std-label-amazon-aws-configuration-options) and [Azure Cluster Configuration Options.](/docs/atlas/reference/microsoft-azure#std-label-microsoft-azure-configuration-options)

Clusters with NVMe (non-volatile memory express) storage use [Cloud Backups](/docs/atlas/backup/cloud-backup/overview). You can't disable backup on NVMe (non-volatile memory express) clusters. If you want to use hourly backups, Atlas limits backups on NVMe (non-volatile memory express) clusters to once every 12 hours.

NVMe (non-volatile memory express) clusters use a [hidden secondary node](https://www.mongodb.com/docs/manual/core/replica-set-hidden-member/) that consists of a provisioned volume with high throughput and IOPS (Input/Output Operations per Second) to facilitate backup.

You can't [pause](/docs/atlas/pause-terminate-cluster#std-label-pause-cluster) an NVMe (non-volatile memory express) cluster.

Scaling of clusters (including [auto-scaling](/docs/atlas/cluster-autoscaling#std-label-cluster-autoscaling)) that use the local NVMe (non-volatile memory express) SSD storage option requires an [initial sync](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-initial-sync). Atlas NVMe (non-volatile memory express) clusters auto-scale to the next higher tier when 90% of the storage space is full. An [initial sync](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-initial-sync) takes longer to complete compared to subsequent syncs, and reduces the performance of the [primary](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-primary) from which the data is read.

[A File Copy Based Initial Sync](https://www.mongodb.com/docs/manual/core/replica-set-sync/#file-copy-based-initial-sync) will always be used to sync all of the nodes of an NVME cluster whenever an initial sync is required.

##### NVMe Availability Zones

NVMe (non-volatile memory express) clusters in the following Azure (Microsoft Azure) regions have two [Availability Zones:](/docs/atlas/reference/microsoft-azure#std-label-microsoft-azure-availability-zones)

- `eastus2`

- `centralus`

- `southcentralus`

NVMe (non-volatile memory express) clusters in all other Azure (Microsoft Azure) regions that [indicate Availability Zones](/docs/atlas/reference/microsoft-azure#std-label-microsoft-azure-supported-regions) have three Availability Zones.

### Free, Flex, and Dedicated Cluster Comparison

The following table highlights key differences between Free clusters, Flex clusters, and `M10+` dedicated clusters.

<table>
<thead>
<tr>
<th></th>
<th>Free Clusters</th>
<th>Flex Clusters</th>
<th>Dedicated Clusters</th>
</tr>
</thead>
<tbody>
<tr>
<td>Storage (Data Size + Index Size)</td>
<td>512 MB</td>
<td>5 GB</td>
<td>10 - 4000 GB</td>
</tr>
<tr>
<td>MongoDB Version Support</td>
<td>8.0</td>
<td>8.0</td>
<td>7.0, and Latest Release</td>
</tr>
<tr>
<td>Metrics and Alerts</td>
<td>Limited</td>
<td>Limited</td>
<td><a href="/docs/atlas/monitor-cluster-metrics#std-label-monitor-cluster-metrics">Full metrics</a>, including the <a href="/docs/atlas/real-time-performance-panel#std-label-real-time-metrics-status-tab">Real Time Performance Tab</a>, and full <a href="/docs/atlas/configure-alerts#std-label-configure-alerts">alert configuration options.</a></td>
</tr>
<tr>
<td>VPC Peering</td>
<td>No</td>
<td>No</td>
<td><a href="/docs/atlas/security-vpc-peering#std-label-vpc-peering">VPC Peering Connection wizard</a></td>
</tr>
<tr>
<td>Global Region Selection</td>
<td>A subset of regions in AWS (Amazon Web Services), Google Cloud, and Azure.</td>
<td>A subset of regions in AWS (Amazon Web Services), Google Cloud, and Azure.</td>
<td>Atlas supports deploying clusters globally on <a href="/docs/atlas/reference/amazon-aws">Amazon Web Services</a>, <a href="/docs/atlas/reference/google-gcp">Google Cloud Platform</a>, and <a href="/docs/atlas/reference/microsoft-azure">Microsoft Azure.</a></td>
</tr>
<tr>
<td>Cross-Region Deployments</td>
<td>No</td>
<td>No</td>
<td>Yes. Specify additional regions for high availability or local reads when <a href="/docs/atlas/tutorial/create-new-cluster">creating</a> or <a href="/docs/atlas/scale-cluster">scaling</a> a cluster.</td>
</tr>
<tr>
<td>Backups</td>
<td>No</td>
<td>Yes, <a href="/docs/atlas/backup/cloud-backup/flex-cluster-backup#std-label-flex-snapshots">daily backup snapshots</a></td>
<td>Yes</td>
</tr>
<tr>
<td>Sharding</td>
<td>No</td>
<td>No</td>
<td>Yes, for clusters using an <code>M30+</code> tier</td>
</tr>
<tr>
<td>Dedicated Cluster</td>
<td>No, Free clusters run in a shared environment</td>
<td>No, Flex clusters run in a shared environment</td>
<td>Yes, <code>M10+</code> clusters deploy each <a href="https://www.mongodb.com/docs/manual/reference/program/mongod/#mongodb-binary-bin.mongod"><code>mongod</code></a> process to its own instance.</td>
</tr>
<tr>
<td>Performance Advisor</td>
<td>No</td>
<td>No</td>
<td>Yes</td>
</tr>
<tr>
<td>BI Connector for Atlas</td>
<td>No</td>
<td>No</td>
<td>Yes</td>
</tr>
</tbody>
</table>

For a complete list of Free cluster limitations, see [Atlas Free Cluster Limits.](/docs/atlas/reference/free-shared-limitations#std-label-atlas-free-tier)

To learn more, see [Configure Auto-Scaling.](/docs/atlas/cluster-autoscaling#std-label-cluster-autoscaling)

For replica sets, the data-bearing servers are the servers hosting the replica set nodes. For sharded clusters, the data-bearing servers are the servers hosting the shards. For sharded clusters, Atlas also deploys servers for the [config servers](https://www.mongodb.com/docs/manual/core/sharded-cluster-config-servers/#std-label-sharding-config-server); these are charged at a rate separate from the cluster costs.

## Take the Next Steps

You can manage clusters in the following ways:

<table>
<thead>
<tr>
<th>Action</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="/docs/atlas/customize-storage">Customize Cluster Storage</a></td>
<td>Customize the storage capacity of your cluster. Each cluster tier comes with a default set of resources. <code>M10+</code> clusters provide the ability to customize your storage capacity.</td>
</tr>
<tr>
<td><a href="/docs/atlas/cluster-sharding">Manage Cluster Sharding</a></td>
<td>Shard your cluster to scale horizontally. You can use the Atlas Cluster Builder UI, the latest version of the <a href="https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/group/endpoint-clusters">Atlas Admin API</a>, <a href="https://www.mongodb.com/docs/atlas/cli/current/">Atlas CLI</a>, or <a href="https://registry.terraform.io/providers/mongodb/mongodbatlas/latest">HashiCorp Terraform MongoDB Atlas Provider</a> to shard your cluster.<br>You can also use the latest version of the <a href="https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/group/endpoint-clusters">Atlas Admin API</a> to independently scale each shard in your cluster.</td>
</tr>
<tr>
<td><a href="/docs/atlas/cluster-autoscaling#std-label-cluster-autoscaling">Configure Auto-Scaling</a></td>
<td>Configure the cluster tier ranges that Atlas uses to automatically scale your cluster tier, storage capacity, or both in response to cluster usage.</td>
</tr>
<tr>
<td><a href="/docs/atlas/cluster-blocking-writes#std-label-cluster-blocking-writes">Write-Blocking</a></td>
<td>Learn about write-blocking and how to prevent it. Atlas blocks writes to your dedicated replica set cluster if the cluster's primary node exceeds write-blocking policy thresholds.</td>
</tr>
<tr>
<td><a href="/docs/atlas/cluster-additional-settings">Configure Additional Settings</a></td>
<td>Configure additional cluster settings such as MongoDB version, backup, and encryption options.</td>
</tr>
<tr>
<td><a href="/docs/atlas/tags#std-label-configure-resource-tags">Resource Tags</a></td>
<td>Use resource tags that you provide and manage to categorize resources by purpose, environment, team, or billing center.</td>
</tr>
<tr>
<td><a href="/docs/atlas/scale-cluster">Modify a Cluster</a></td>
<td>Reconfigure an existing cluster. Modify any of the available Atlas configuration options.</td>
</tr>
<tr>
<td><a href="/docs/atlas/tutorial/major-version-change/">Upgrade Major MongoDB Version for a Cluster</a></td>
<td>Manage major version upgrades for your cluster. Atlas enables you to upgrade the major version of an Atlas cluster at any time.</td>
</tr>
<tr>
<td><a href="/docs/atlas/tutorial/cluster-maintenance-window/">Configure Maintenance Window</a></td>
<td>Configure maintenance windows for your cluster. You can set the hour of the day that Atlas should start weekly maintenance on your cluster.</td>
</tr>
<tr>
<td><a href="/docs/atlas/pause-terminate-cluster#std-label-pause-terminate-cluster">Pause, Resume, or Terminate a Cluster</a></td>
<td>Pause, resume, or terminate an existing cluster. You can't change the configuration of a paused cluster. Also, you can't read data from or write data to a paused cluster.</td>
</tr>
<tr>
<td><a href="/docs/atlas/cluster-config/multi-cloud-distribution">Configure High Availability and Workload Isolation</a></td>
<td>Configure multi-cloud distribution for increased availability. Atlas offers options to improve the availability and workload balancing of your cluster.</td>
</tr>
<tr>
<td><a href="/docs/atlas/reference/replica-set-tags#std-label-replica-set-tags">Query using Pre-Defined Replica Set Tags</a></td>
<td>Use pre-defined replica set tags that Atlas provides to direct queries from specific applications to specific node types and regions. To use pre-defined replica set tags in your connection string and direct queries to specific nodes, set the tag in the <code>readPreferenceTags</code> connection string option.</td>
</tr>
</tbody>
</table>
