> Source: https://www.mongodb.com/docs/atlas/manage-clusters/
> Fetch method: direct_markdown

# Manage Clusters

Use the following resources to configure and manage Atlas clusters.

## Required Access

To view your clusters, you must have `Project Read Only` access or higher to the project.

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

To learn more about the syntax and parameters for the previous commands, see the Atlas CLI documentation for atlas clusters list and atlas clusters describe.

**See also: Related Links**

- Install the Atlas CLI

- Connect to the Atlas CLI

To return the advanced configuration settings details for the cluster you specify using the Atlas CLI, run the following command:

```sh

atlas clusters advancedSettings describe <clusterName> [options]

```

To learn more about the command syntax and parameters, see the Atlas CLI documentation for atlas clusters advancedSettings describe.

### Atlas UI

To view all clusters in the Atlas UI, see View All Cloud Clusters. To view the details for a cluster, see View Cluster Details.

## Select Cluster Tier

Select your preferred cluster tier. The cluster tier dictates the memory, storage, vCPUs, and IOPS (Input/Output Operations per Second) specification for each data-bearing server  in the cluster.

**Note:**

You might see different values depending on your selected cloud provider and region.

### Flex Clusters

Use Flex clusters as an economical way for getting started with MongoDB and for low-throughput applications. These clusters deploy to an environment with access to a subset of Atlas features. To learn more, see Limits on Atlas Cluster Types.

You can deploy one Free cluster (free sandbox replica set cluster) per Atlas project. You can upgrade a Free cluster to a Flex cluster at any time.

Flex clusters provide the following added features compared to Free clusters:

- Backups for your cluster data

- Increased storage

- API access

#### Considerations

Flex clusters don't have the full availability of features found in Dedicated clusters. To learn more, see Limits on Atlas Cluster Types.

### Dedicated Clusters for Low-Traffic Applications

`M10` and `M20` cluster tiers support development environments and production environments with low-traffic applications.

These clusters support replica set deployments only, but otherwise provide full access to Atlas features.

**Note:**

`M10` and `M20` cluster tiers use burstable performance infrastructure. Cloud providers cap CPU usage after burst periods, which can cause throttling under heavy load. To learn more, see How Atlas Scales Cluster Tier.

### Dedicated Clusters for High-Traffic Applications

`M30` and higher clusters are recommended for production environments.

These clusters support replica set and sharded cluster deployments with full access to Atlas features.

Some clusters have variants, denoted by the ❯ character. When you select these clusters, Atlas lists the variants and tags each cluster to distinguish their key characteristics.

### Sharded Clusters

You can use the Atlas Administration API to choose a different tier per shard in a sharded cluster. You can also select Analytics node tiers indepenently for each shard. The largest and smallest shard tiers must be within two tiers of each other. For example, if the largest shard is `M50`, the smallest shard can be `M30` or `M40`. If you change the cluster tier for a sharded cluster in the Atlas UI, Atlas changes the tier of all shards in the cluster.

You can also use the Atlas Administration API to choose different IOPS (Input/Output Operations per Second) per shard if the cluster is on AWS (Amazon Web Services) using AWS (Amazon Web Services) provisioned IOPS or the cluster is on Azure (Microsoft Azure) in regions that support Extended IOPS/storage.

To learn more, see Manage Cluster Sharding and the Update One Cluster in One Project endpoint in the Atlas Administration API documentation.

#### Limitations

Every shard must have an equal disk size on all nodes. NVMe (non-volatile memory express) clusters are not compatible with independent shard scaling.

NVMe (non-volatile memory express) instances can't be used in multi-cloud clusters.

### NVMe Storage

For applications hosted on AWS or  Azure that require low-latency and high-throughput I/O, Atlas offers storage options using locally attached ephemeral NVMe (non-volatile memory express) SSD (Solid State Disk)s.

A File Copy Based Initial Sync will always be used to sync all of the nodes of an NVME cluster whenever an initial sync is required.

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

| Azure Region | Location | Atlas Region |
| --- | --- | --- |
| <code>brazilsouth</code> | São Paulo, Brazil | <code>BRAZIL_SOUTH</code> |
| <code>canadacentral</code> | Toronto, ON | <code>CANADA_CENTRAL</code> |
| <code>centralus</code> | Iowa, USA | <code>US_CENTRAL</code> |
| <code>eastus</code> | Virginia (East US) | <code>US_EAST</code> |
| <code>eastus2</code> | Virginia, USA | <code>US_EAST_2</code> |
| <code>southcentralus</code> | Texas, USA | <code>US_SOUTH_CENTRAL</code> |
| <code>westus3</code> | El Mirage, Arizona | <code>US_WEST_3</code> |

### Europe

| Azure Region | Location | Atlas Region |
| --- | --- | --- |
| <code>francecentral</code> | Paris, France | <code>FRANCE_CENTRAL</code> |
| <code>northeurope</code> | Ireland | <code>EUROPE_NORTH</code> |
| <code>swedencentral</code> | Gävle, Sweden | <code>SWEDEN_CENTRAL</code> |
| <code>uksouth</code> | London, England, UK | <code>UK_SOUTH</code> |
| <code>westeurope</code> | Netherlands | <code>EUROPE_WEST</code> |

### Asia Pacific

| Azure Region | Location | Atlas Region |
| --- | --- | --- |
| <code>australiaeast</code> | New South Wales, Australia | <code>AUSTRALIA_EAST</code> |
| <code>centralindia</code> | Pune (Central India) | <code>INDIA_CENTRAL</code> |
| <code>japaneast</code> | Saitama, Tokyo, Japan | <code>JAPAN_EAST</code> |

The fixed-value storage space and RAM for an NVMe (non-volatile memory express) cluster corresponds to its cluster tier. To learn more, see Amazon Cluster Configuration Options and Azure Cluster Configuration Options.

Clusters with NVMe (non-volatile memory express) storage use Cloud Backups. You can't disable backup on NVMe (non-volatile memory express) clusters. If you want to use hourly backups, Atlas limits backups on NVMe (non-volatile memory express) clusters to once every 12 hours.

NVMe (non-volatile memory express) clusters use a hidden secondary node that consists of a provisioned volume with high throughput and IOPS (Input/Output Operations per Second) to facilitate backup.

You can't pause an NVMe (non-volatile memory express) cluster.

Scaling of clusters (including auto-scaling) that use the local NVMe (non-volatile memory express) SSD storage option requires an initial sync. Atlas NVMe (non-volatile memory express) clusters auto-scale to the next higher tier when 90% of the storage space is full. An initial sync takes longer to complete compared to subsequent syncs, and reduces the performance of the primary from which the data is read.

A File Copy Based Initial Sync will always be used to sync all of the nodes of an NVME cluster whenever an initial sync is required.

##### NVMe Availability Zones

NVMe (non-volatile memory express) clusters in the following Azure (Microsoft Azure) regions have two Availability Zones:

- `eastus2`

- `centralus`

- `southcentralus`

NVMe (non-volatile memory express) clusters in all other Azure (Microsoft Azure) regions that indicate Availability Zones have three Availability Zones.

### Free, Flex, and Dedicated Cluster Comparison

The following table highlights key differences between Free clusters, Flex clusters, and `M10+` dedicated clusters.

|  | Free Clusters | Flex Clusters | Dedicated Clusters |
| --- | --- | --- | --- |
| Storage (Data Size + Index Size) | 512 MB | 5 GB | 10 - 4000 GB |
| MongoDB Version Support | 8.0 | 8.0 | 7.0, and Latest Release |
| Metrics and Alerts | Limited | Limited | <a href="/docs/atlas/monitor-cluster-metrics#std-label-monitor-cluster-metrics">Full metrics</a>, including the <a href="/docs/atlas/real-time-performance-panel#std-label-real-time-metrics-status-tab">Real Time Performance Tab</a>, and full <a href="/docs/atlas/configure-alerts#std-label-configure-alerts">alert configuration options.</a> |
| VPC Peering | No | No | <a href="/docs/atlas/security-vpc-peering#std-label-vpc-peering">VPC Peering Connection wizard</a> |
| Global Region Selection | A subset of regions in AWS (Amazon Web Services), Google Cloud, and Azure. | A subset of regions in AWS (Amazon Web Services), Google Cloud, and Azure. | Atlas supports deploying clusters globally on <a href="/docs/atlas/reference/amazon-aws">Amazon Web Services</a>, <a href="/docs/atlas/reference/google-gcp">Google Cloud Platform</a>, and <a href="/docs/atlas/reference/microsoft-azure">Microsoft Azure.</a> |
| Cross-Region Deployments | No | No | Yes. Specify additional regions for high availability or local reads when <a href="/docs/atlas/tutorial/create-new-cluster">creating</a> or <a href="/docs/atlas/scale-cluster">scaling</a> a cluster. |
| Backups | No | Yes, <a href="/docs/atlas/backup/cloud-backup/flex-cluster-backup#std-label-flex-snapshots">daily backup snapshots</a> | Yes |
| Sharding | No | No | Yes, for clusters using an <code>M30+</code> tier |
| Dedicated Cluster | No, Free clusters run in a shared environment | No, Flex clusters run in a shared environment | Yes, <code>M10+</code> clusters deploy each <a href="https://www.mongodb.com/docs/manual/reference/program/mongod/#mongodb-binary-bin.mongod"><code>mongod</code></a> process to its own instance. |
| Performance Advisor | No | No | Yes |
| BI Connector for Atlas | No | No | Yes |

For a complete list of Free cluster limitations, see Atlas Free Cluster Limits.

To learn more, see Configure Auto-Scaling.

For replica sets, the data-bearing servers are the servers hosting the replica set nodes. For sharded clusters, the data-bearing servers are the servers hosting the shards. For sharded clusters, Atlas also deploys servers for the config servers; these are charged at a rate separate from the cluster costs.

## Take the Next Steps

You can manage clusters in the following ways:

| Action | Description |
| --- | --- |
| <a href="/docs/atlas/customize-storage">Customize Cluster Storage</a> | Customize the storage capacity of your cluster. Each cluster tier comes with a default set of resources. <code>M10+</code> clusters provide the ability to customize your storage capacity. |
| <a href="/docs/atlas/cluster-sharding">Manage Cluster Sharding</a> | Shard your cluster to scale horizontally. You can use the Atlas Cluster Builder UI, the latest version of the <a href="https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/group/endpoint-clusters">Atlas Admin API</a>, <a href="https://www.mongodb.com/docs/atlas/cli/current/">Atlas CLI</a>, or <a href="https://registry.terraform.io/providers/mongodb/mongodbatlas/latest">HashiCorp Terraform MongoDB Atlas Provider</a> to shard your cluster.<br>You can also use the latest version of the <a href="https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/group/endpoint-clusters">Atlas Admin API</a> to independently scale each shard in your cluster. |
| <a href="/docs/atlas/cluster-autoscaling#std-label-cluster-autoscaling">Configure Auto-Scaling</a> | Configure the cluster tier ranges that Atlas uses to automatically scale your cluster tier, storage capacity, or both in response to cluster usage. |
| <a href="/docs/atlas/cluster-blocking-writes#std-label-cluster-blocking-writes">Write-Blocking</a> | Learn about write-blocking and how to prevent it. Atlas blocks writes to your dedicated replica set cluster if the cluster's primary node exceeds write-blocking policy thresholds. |
| <a href="/docs/atlas/cluster-additional-settings">Configure Additional Settings</a> | Configure additional cluster settings such as MongoDB version, backup, and encryption options. |
| <a href="/docs/atlas/tags#std-label-configure-resource-tags">Resource Tags</a> | Use resource tags that you provide and manage to categorize resources by purpose, environment, team, or billing center. |
| <a href="/docs/atlas/scale-cluster">Modify a Cluster</a> | Reconfigure an existing cluster. Modify any of the available Atlas configuration options. |
| <a href="/docs/atlas/tutorial/major-version-change/">Upgrade Major MongoDB Version for a Cluster</a> | Manage major version upgrades for your cluster. Atlas enables you to upgrade the major version of an Atlas cluster at any time. |
| <a href="/docs/atlas/tutorial/cluster-maintenance-window/">Configure Maintenance Window</a> | Configure maintenance windows for your cluster. You can set the hour of the day that Atlas should start weekly maintenance on your cluster. |
| <a href="/docs/atlas/pause-terminate-cluster#std-label-pause-terminate-cluster">Pause, Resume, or Terminate a Cluster</a> | Pause, resume, or terminate an existing cluster. You can't change the configuration of a paused cluster. Also, you can't read data from or write data to a paused cluster. |
| <a href="/docs/atlas/cluster-config/multi-cloud-distribution">Configure High Availability and Workload Isolation</a> | Configure multi-cloud distribution for increased availability. Atlas offers options to improve the availability and workload balancing of your cluster. |
| <a href="/docs/atlas/reference/replica-set-tags#std-label-replica-set-tags">Query using Pre-Defined Replica Set Tags</a> | Use pre-defined replica set tags that Atlas provides to direct queries from specific applications to specific node types and regions. To use pre-defined replica set tags in your connection string and direct queries to specific nodes, set the tag in the <code>readPreferenceTags</code> connection string option. |
