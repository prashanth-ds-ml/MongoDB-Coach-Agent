> Source: https://www.mongodb.com/docs/atlas/tutorial/create-new-cluster/
> Fetch method: direct_markdown

# Create a Cluster

**Important:**

As of February 2025, you can create Flex clusters, and can no longer create `M2` and `M5` clusters or Serverless instances in the Atlas UI, Atlas CLI, Atlas Administration API, Atlas Kubernetes Operator, HashiCorp Terraform, or Atlas CloudFormation Resources.

As of January 22, 2026, Atlas no longer supports `M2` and `M5` clusters and Serverless instances. All existing `M2` and `M5` clusters were migrated to Flex clusters.

Atlas migrated Serverless instances to Free clusters, Flex clusters, or Dedicated clusters according to your usage. To see which tiers Atlas migrated your instances to, consult the [All Clusters](https://cloud.mongodb.com/v2#/clusters) page in the Atlas UI.

This tutorial takes you through the steps to create a new Atlas cluster. To learn how to modify an existing Atlas cluster, see [Modify a Cluster.](/docs/atlas/scale-cluster)

[Clusters](/docs/atlas/create-database-deployment#std-label-ref-deployment-types) can be either a [replica set](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-replica-set) or a [sharded cluster](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-sharded-cluster). This tutorial walks you through creating a replica set.

To learn about recommendations for clusters and high availability, see [Recommendations for Atlas Orgs, Projects, and Clusters](https://www.mongodb.com/docs/atlas/architecture/current/hierarchy/#std-label-arch-center-orgs-projects-clusters-recs) and [Recommendations for Atlas High Availability](https://www.mongodb.com/docs/atlas/architecture/current/high-availability/#std-label-arch-center-ha-recs), respectively, in the Atlas Architecture Center.

## Required Access

To create a cluster, you must have [`Organization Owner`](/docs/atlas/reference/user-roles#mongodb-authrole-Organization-Owner), [`Project Owner`](/docs/atlas/reference/user-roles#mongodb-authrole-Project-Owner), or [`Project Cluster Creator`](/docs/atlas/reference/user-roles#mongodb-authrole-Project-Cluster-Creator) access to the project.

## Considerations

- To minimize network latency and data transfer costs, and to increase overall stability and security, use the same cloud provider and region to host your application and cluster when possible.

- Clusters can span regions and cloud service providers. The total number of nodes in clusters spanning across regions has a specific constraint on a per-project basis.

  Atlas limits the total number of nodes in other regions in one project to a total of 40, **not** including:

  - Google Cloud regions communicating with each other

  - Free clusters

  - Flex clusters

  Sharded clusters include additional nodes. The electable nodes on the dedicated Config Server Replica Set (CSRS) count towards the total number of allowable nodes. Each sharded cluster has an additional electable node per region as part of the dedicated CSRS. To learn more, see [Replica Set Config Servers.](https://www.mongodb.com/docs/manual/core/sharded-cluster-config-servers/#std-label-replset-config-servers)

  The total number of nodes between any two regions must meet this constraint.

  **Example:**

  If an Atlas project has nodes in clusters spread across three regions:

  - 30 nodes in **Region A**

  - 10 nodes in **Region B**

  - 5 nodes in **Region C**

  You can only add 5 more nodes to **Region C** because:

  1. If you exclude Region C, Region A + Region B = 40.&#x20;

  2. If you exclude Region B, Region A + Region C = 35, \<= 40.&#x20;

  3. If you exclude Region A, Region B + Region C = 15, \<= 40.&#x20;

  4. Each combination of regions with the added 5 nodes still meets the per-project constraint:

     - Region A + B = 40&#x20;

     - Region A + C = 40&#x20;

     - Region B + C = 20&#x20;

  You can't create a multi-region cluster in a project if it has one or more clusters spanning 40 or more nodes in other regions.

  Contact Atlas [support](https://www.mongodb.com/docs/manual/support/) for questions or assistance with raising this limit.

- M30 and higher clusters are recommended for production environments. Clusters with sustained loads on M10 and M20 tiers may experience degraded performance over time.

- Each Atlas [project](/docs/atlas/organizations-projects#std-label-projects) supports up to 25 clusters. If you have questions or need assistance regarding the cluster limit, [contact support.](/docs/atlas/support#std-label-atlas-support)

- If your Atlas project contains a [custom role](/docs/atlas/security-add-mongodb-roles#std-label-mongodb-roles) that uses actions introduced in a specific MongoDB version, you must delete that role before creating clusters with an earlier MongoDB version.

- Atlas clusters created after July 2020 use TLS (Transport Layer Security) version 1.2 by default.

  **Important:**

  Beginning July 31st, 2025, Atlas will no longer support TLS (Transport Layer Security) 1.0 or 1.1 under any circumstance. Atlas will upgrade all clusters to reject attempts to connect with TLS (Transport Layer Security) 1.0 or 1.1.

  Any client connections configured for TLS (Transport Layer Security) 1.0 or 1.1 will undergo a service outage during this upgrade. To avoid this, set the minimum TLS (Transport Layer Security) version of your clusters to 1.2 at your earliest opportunity.

- When you create a cluster, Atlas creates a [network container](https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/operation/operation-creategroupcontainer) in the project for the cloud provider to which you deploy the cluster if one does not already exist.

- If you have a [Backup Compliance Policy enabled](/docs/atlas/backup/cloud-backup/backup-compliance-policy#std-label-backup-compliance-policy), all new and existing clusters have Cloud Backup automatically enabled and use the project-level Backup Compliance Policy. Atlas augments any preexisting cluster-level policies to meet the minimum requirements of the Backup Compliance Policy. All new clusters use the Backup Compliance Policy unless the mininum requirements of the [cluster-level backup policy](/docs/atlas/backup/cloud-backup/configure-backup-policy#std-label-configure-backup-policy) expand beyond the mininum requirements of the Backup Compliance Policy.

**Important:**

Do not choose Latest Version With Auto Upgrades. This option auto upgrades your cluster to the latest minor release. Some minor releases, such as MongoDB version 8.2, may not support Live Migration or Mongosync. When [upgrading](/docs/atlas/tutorial/major-version-change#std-label-major-version-upgrade-procedure), choose a major version to ensure compatibility with Live Migration and Mongosync.

## Procedure

### Atlas CLI

**Tip: AI Cluster Assistant**

MongoDB offers an AI Cluster Assistant you can use while creating or editing a cluster to answer natural-language questions about cluster configuration. The AI Cluster Assistant can recommend settings based on your workload and needs and apply those settings directly to your cluster.

To learn more about the AI Cluster Assistant, see [AI Cluster Assistant.](/docs/atlas/ai-cluster-assistant#std-label-atlas-ai-cluster-assistant)

To create one cluster in the specified project using the Atlas CLI, run the following command:

```sh

atlas clusters create [name] [options]

```

To watch for a specific cluster to become available using the Atlas CLI, run the following command:

```sh

atlas clusters watch <clusterName> [options]

```

To learn more about the syntax and parameters for the previous commands, see the Atlas CLI documentation for [atlas clusters create](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-clusters-create/) and [atlas clusters watch.](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-clusters-watch/)

**See also: Related Links**

- [Install the Atlas CLI](https://www.mongodb.com/docs/atlas/cli/current/install-atlas-cli/)

- [Connect to the Atlas CLI](https://www.mongodb.com/docs/atlas/cli/current/connect-atlas-cli/)

### View Available Regions

To list available regions that Atlas supports for new deployments using the Atlas CLI, run the following command:

```sh

atlas clusters availableRegions list [options]

```

To learn more about the command syntax and parameters, see the Atlas CLI documentation for [atlas clusters availableRegions list.](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-clusters-availableRegions-list/)

### Atlas UI

**Tip: AI Cluster Assistant**

MongoDB offers an AI Cluster Assistant you can use while creating or editing a cluster to answer natural-language questions about cluster configuration. The AI Cluster Assistant can recommend settings based on your workload and needs and apply those settings directly to your cluster.

To learn more about the AI Cluster Assistant, see [AI Cluster Assistant.](/docs/atlas/ai-cluster-assistant#std-label-atlas-ai-cluster-assistant)

When you create your first Atlas cluster using the Atlas UI, you can either:

- Use a template with preset advanced configuration options.

- Specify advanced configuration options.

Whether you use a template or specify advanced configuration, you can [modify all configuration options](/docs/atlas/scale-cluster) after you create the cluster.

**Note:**

The procedure for creating a new Atlas cluster in the Atlas UI differs depending on whether you already have one or more clusters in your project. The following steps apply to both, but you may see slightly different options in the UI.

### Use a Template

1. In Atlas, go to the Clusters page for your project.

   If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

   If it's not already displayed, select your desired project from the Projects menu in the navigation bar.

   In the sidebar, click Clusters under the Database heading.

   The [Clusters](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fclusters) page displays.

2. Open the Deploy your cluster page.

   If you already have one or more clusters, click Create to display the Deploy your cluster page.

   If this is your first cluster, click Build a Cluster to display the Deploy your cluster page.

3. Select a cluster type.

   You can deploy the following clusters from this page:

   M10

   The M10 tier is suitable for development environments and low-traffic applications, while higher tiers can handle large datasets and high-traffic applications. Dedicated clusters can be deployed into a single geographical region or multiple geographical regions.

   **Note:**

   To create Dedicated cluster tiers higher than M10, select Go to Advanced Configuration at the bottom of the page.

   Flex Clusters

   Flex clusters are low-cost cluster types suitable for teams who are learning MongoDB or developing small proof-of-concept applications. You can begin your project with an Atlas Flex cluster and upgrade to a production-ready Dedicated cluster tier at a future time.

   **Important:**

   As of February 2025, you can create Flex clusters, and can no longer create `M2` and `M5` clusters or Serverless instances in the Atlas UI, Atlas CLI, Atlas Administration API, Atlas Kubernetes Operator, HashiCorp Terraform, or Atlas CloudFormation Resources.

   As of January 22, 2026, Atlas no longer supports `M2` and `M5` clusters and Serverless instances. All existing `M2` and `M5` clusters were migrated to Flex clusters.

   Atlas migrated Serverless instances to Free clusters, Flex clusters, or Dedicated clusters according to your usage. To see which tiers Atlas migrated your instances to, consult the [All Clusters](https://cloud.mongodb.com/v2#/clusters) page in the Atlas UI.

   **Important:**

   All Serverless instances have been automatically migrated, based on current usage, to Free clusters, Flex clusters, or Dedicated clusters. The [All Clusters](https://cloud.mongodb.com/v2#/clusters) page in the Atlas UI shows which tiers your instances will be migrated to.

   Free clusters

   A Free cluster provides a free sandbox replica set. You can deploy one Free cluster per Atlas project. Free clusters are more limited than Atlas Flex and Dedicated clusters. For information on these limitations, refer to [Configuration Limits.](/docs/atlas/reference/free-shared-limitations#std-label-shared-limits-config)

4. Select your preferred Cloud Provider & Region.

   The choice of cloud provider and region affects the configuration options for the available cluster tiers, network latency for clients accessing your cluster, the geographic location of the nodes in your cluster, and the [cost of running the cluster.](/docs/atlas/billing#std-label-billing-overview)

   To learn more, see [Cloud Providers and Regions.](/docs/atlas/cloud-providers-regions#std-label-create-cluster-cloud-provider-region)

   **Note:**

   To deploy your cluster across multiple regions, or to deploy separate Search Nodes for workload isolation, select Go to Advanced Configuration at the bottom of the page.

5. Specify a name for the cluster in the Name box.

   This label identifies the cluster in Atlas.

   **Note:**

   Atlas creates your hostname based on your cluster name.

   You can't change the cluster name after Atlas deploys the cluster. Cluster names can't exceed 64 characters in length.

   IMPORTANT: Atlas truncates the cluster name to *23 characters* in its internal interactions. In practice, this means:

   - Cluster names shorter than 23 characters can't end with hyphen or dash (`-`).

   - Cluster names 23 characters or longer can't use a hyphen or dash (`-`) as its 23rd character.

   - The first 23 characters in a cluster name must be unique within a project.

   Don't include [sensitive information](/docs/atlas/production-notes#std-label-sensitive-info) in your cluster name.

6. Specify a tag key and value to apply to the cluster.

   To learn more, see [Apply a cluster Tag to a New Cluster from a Template.](/docs/atlas/database-deployment-tags#std-label-apply-tags-new-cluster-template)

   **Important:**

   Don't include sensitive information such as Personally Identifiable Information (PII) or Protected Health Information (PHI) in your resource tags. Other MongoDB services, such as Billing, can access resource tags. MongoDB also sends cluster resource tags to DataDog and Prometheus integrations. Resource tags are *not* intended for private and sensitive data. To learn more, see [Sensitive Information.](/docs/atlas/production-notes#std-label-sensitive-info)

7. Deploy your cluster.

   Click Create.

   **Important:**

   Each Atlas [project](/docs/atlas/organizations-projects#std-label-projects) supports up to 25 clusters. If you have questions or need assistance regarding the cluster limit, [contact support.](/docs/atlas/support#std-label-atlas-support)

8. Update your Billing Address details as needed.

   <table>
   <thead>
   <tr>
   <th>Field</th>
   <th>Necessity</th>
   <th>Action</th>
   </tr>
   </thead>
   <tbody>
   <tr>
   <th>Billing Email Address</th>
   <td>Optional</td>
   <td>Type the email address to which Atlas should send <a href="/docs/atlas/reference/alert-conditions#std-label-billing-alerts">billing alerts.</a><br>By default, Atlas sends billing alerts to the Organization Owners and Billing Admins.<br><ul><li>If you leave the Billing Email Address blank, Atlas sends billing alerts to the Organization Owners and Billing Admins.</li><li>If you specify a billing email address and uncheck Only
   send invoice emails to the Billing Email
   Address, Atlas sends billing alerts to the billing email address, Organization Owners, and Billing Admins.</li><li>If you specify a billing email address and check the box for Only
   send invoice emails to the Billing Email
   Address, Atlas send billing alerts to the billing email address only.</li></ul></td>
   </tr>
   <tr>
   <th>Company Name</th>
   <td>Optional</td>
   <td>Type the name of the company for your billing address.</td>
   </tr>
   <tr>
   <th>Country</th>
   <td>Required</td>
   <td>Select the country for your billing address. You can also start typing the name of the country and then select it from the filtered list of countries.</td>
   </tr>
   <tr>
   <th>Street Address</th>
   <td>Required</td>
   <td>Type the street address for your billing address.</td>
   </tr>
   <tr>
   <th>Apt/Suite/Floor</th>
   <td>Optional</td>
   <td>Type an the apartment, suite, or floor for your billing address.</td>
   </tr>
   <tr>
   <th>City</th>
   <td>Required</td>
   <td>Type the name of the city for your billing address.</td>
   </tr>
   <tr>
   <th>State/Province/Region</th>
   <td>Required</td>
   <td>Type or select the political subdivision in which your billing address exists. The label and field change depending on what you selected as your <strong>Country</strong>:<br><ul><li>If you select <strong>United States</strong> as your <strong>Country</strong>, this label changes to <strong>State</strong>. The field changes to a dropdown menu of U.S. states. You can also start typing the name of the state and then select it from the filtered list of states.</li><li>If you select <strong>Canada</strong> as your <strong>Country</strong>, this label changes to <strong>Province</strong>. The field changes to a dropdown menu of Canadian provinces. You can also start typing the name of the province and then select it from the filtered list of provinces.</li><li>If you select any other country as your <strong>Country</strong>, this label changes to <strong>State/Province/Region</strong>. The field changes to a text box. Type the name of your province, state, or region in this box.</li></ul></td>
   </tr>
   <tr>
   <th>ZIP or Postal Code</th>
   <td>Required</td>
   <td>Type the ZIP (U.S.) or Postal Code (other countries) for your billing address.</td>
   </tr>
   <tr>
   <th>VAT Number</th>
   <td>Conditional</td>
   <td>Atlas displays the VAT ID field if you select a country other than the United States.<br>To learn more about VAT, see <a href="/docs/atlas/billing/international-usage#std-label-vat-id-number">VAT ID.</a><br>If your company's billing address is in a country other than the United States (USA), Atlas typically charges VAT (Value Added Tax) if you do not enter a valid <code>VAT ID Number</code> on your <a href="/docs/atlas/billing#std-label-atlas-billing-profile">billing profile.</a><br>IMPORTANT: If your billing address is in Ireland or certain Canadian provinces, Atlas always charges VAT (Value Added Tax), even with a valid <code>VAT ID Number</code>.<br>To learn more about VAT (Value Added Tax) by region, see <a href="/docs/atlas/billing/international-usage#std-label-atlas-international-tax">International Usage and Taxation.</a></td>
   </tr>
   </tbody>
   </table>

9. Update your Payment Method details as needed.

   Click the radio button for Credit Card or Paypal.

   - If you selected Credit Card, type values for the following fields:

     <table>
     <thead>
     <tr>
     <th>Field</th>
     <th>Necessity</th>
     <th>Action</th>
     </tr>
     </thead>
     <tbody>
     <tr>
     <th>Name on Card</th>
     <td>Required</td>
     <td>Type the name that appears on your credit card.</td>
     </tr>
     <tr>
     <th>Card Number</th>
     <td>Required</td>
     <td>Type the 16-digit number that appears on your credit card. American Express uses a 15-digit number.</td>
     </tr>
     <tr>
     <th>Expiration Date</th>
     <td>Required</td>
     <td>Type the expiration date for your credit card in the two-digit month and two-digit year format.</td>
     </tr>
     <tr>
     <th>CVC (Card Verification Code)</th>
     <td>Required</td>
     <td>Type the three-digit number on the back of your credit card. American Express uses a 4-digit number found on the front of the credit card.</td>
     </tr>
     </tbody>
     </table>

   - If you selected PayPal:

     Click Pay with PayPal.

     Complete the actions on the PayPal website.

   **Note:**

   All projects within your organization share the same billing settings, including payment method.

10. Review project's cost.

    Under the Cart section, review the following:

    <table>
    <thead>
    <tr>
    <th>Field</th>
    <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <th>Cluster Tier</th>
    <td>Displays cost for your selected cluster tier and configuration details. To learn more, see <a href="/docs/atlas/billing/cluster-configuration-costs#std-label-region-costs">Cloud Service Provider and Region</a> and <a href="/docs/atlas/billing/cluster-configuration-costs#std-label-instance-size-costs">Cluster Tier.</a></td>
    </tr>
    <tr>
    <th>Included Features</th>
    <td>Displays features included with your selected cluster configuration.</td>
    </tr>
    <tr>
    <th>Additional Settings</th>
    <td>Displays additional settings that you enabled, such as cloud backups, sharding, <a href="https://www.mongodb.com/docs/bi-connector/current/">BI Connector</a>, and more. To learn more, see <a href="/docs/atlas/billing/cluster-configuration-costs#std-label-billing-backup-cloud-provider-snapshots">Cloud Backups.</a></td>
    </tr>
    </tbody>
    </table>

11. Deploy your cluster.

    Click Confirm and Deploy Cluster.

    **Important:**

    Each Atlas [project](/docs/atlas/organizations-projects#std-label-projects) supports up to 25 clusters. If you have questions or need assistance regarding the cluster limit, [contact support.](/docs/atlas/support#std-label-atlas-support)

### Use Advanced Settings

1. In Atlas, go to the Clusters page for your project.

   If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

   If it's not already displayed, select your desired project from the Projects menu in the navigation bar.

   In the sidebar, click Clusters under the Database heading.

   The [Clusters](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fclusters) page displays.

2. Open the Deploy your cluster page.

   If you already have one or more clusters, click Create to display the Deploy your cluster page.

   If this is your first cluster, click Build a Cluster to display the Deploy your cluster page.

3. Open Advanced Configuration.

   - Navigate to the bottom of the page and click Go to Advanced Configuration.

4. Select a cluster type.

   You can deploy the following clusters from this page:

   Flex Clusters

   Flex clusters are low-cost cluster types suitable for teams who are learning MongoDB or developing small proof-of-concept applications. You can begin your project with an Atlas Flex cluster and upgrade to a production-ready Dedicated cluster tier at a future time. Flex clusters are more limited than Dedicated clusters. For information on these limitations, refer to [Configuration Limits.](/docs/atlas/reference/flex-limitations#std-label-flex-limits-config)

   **Important:**

   As of February 2025, you can create Flex clusters, and can no longer create `M2` and `M5` clusters or Serverless instances in the Atlas UI, Atlas CLI, Atlas Administration API, Atlas Kubernetes Operator, HashiCorp Terraform, or Atlas CloudFormation Resources.

   As of January 22, 2026, Atlas no longer supports `M2` and `M5` clusters and Serverless instances. All existing `M2` and `M5` clusters were migrated to Flex clusters.

   Atlas migrated Serverless instances to Free clusters, Flex clusters, or Dedicated clusters according to your usage. To see which tiers Atlas migrated your instances to, consult the [All Clusters](https://cloud.mongodb.com/v2#/clusters) page in the Atlas UI.

   **Important:**

   All Serverless instances have been automatically migrated, based on current usage, to Free clusters, Flex clusters, or Dedicated clusters. The [All Clusters](https://cloud.mongodb.com/v2#/clusters) page in the Atlas UI shows which tiers your instances will be migrated to.

   Dedicated clusters

   Dedicated clusters include M10 and higher tiers. The M10 and M20 tiers are suitable for development environments and low-traffic applications, while higher tiers can handle large datasets and high-traffic applications. Dedicated clusters can be deployed into a single geographical region or multiple geographical regions.

   **Note:**

   If you choose to create a Dedicated cluster, you also have the option to Create a Global Cluster. For more information, refer to [Manage Global Clusters.](/docs/atlas/global-clusters#std-label-global-clusters)

   Free clusters

   A Free cluster provides a free sandbox replica set. You can deploy one Free cluster per Atlas project. Free clusters are more limited than Atlas Flex and Dedicated clusters. For information on these limitations, refer to [Configuration Limits.](/docs/atlas/reference/free-shared-limitations#std-label-shared-limits-config)

5. Select your preferred Cloud Provider & Region.

   The choice of cloud provider and region affects the configuration options for the available cluster tiers, network latency for clients accessing your cluster, the geographic location of the nodes in your cluster, and the [cost of running the cluster.](/docs/atlas/billing#std-label-billing-overview)

   To learn more about selecting a provider and region, refer to [Cloud Providers and Regions.](/docs/atlas/cloud-providers-regions#std-label-create-cluster-cloud-provider-region)

   From the Cloud Provider & Region section, you can also choose Multi-Cloud, Multi-Region & Workload Isolation. Multi-region clusters can better withstand data center outages and may contain dedicated geographic regions for localized reads, thereby improving performance. To learn how to deploy a multi-region cluster, see [Configure High Availability and Workload Isolation.](/docs/atlas/cluster-config/multi-cloud-distribution#std-label-create-cluster-multi-region)

   If you choose Multi-Cloud, Multi-Region & Workload Isolation, you can also choose to configure:

   - Electable nodes

   - Read-only nodes

   - Analytics nodes

   - Search nodes

   For information on these settings, see [Configure High Availability and Workload Isolation.](/docs/atlas/cluster-config/multi-cloud-distribution#std-label-create-cluster-multi-region)

6. Select the Cluster Tier.

   The selected tier dictates the memory, storage, vCPUs, and IOPS (Input/Output Operations per Second) specification for each data-bearing server  in the cluster.

   Dedicated clusters support [Cluster Auto-Scaling](/docs/atlas/cluster-autoscaling#std-label-cluster-autoscaling). Cluster tier Auto-scaling is enabled by default when you create new clusters in the user interface. It is disabled by defaut if you create new clusters in the API. With auto-scaling enabled, Atlas automatically scales your cluster tier, storage capacity, or both in response to cluster usage. Auto-scaling allows your cluster to adapt to your current workload and reduce the need to make manual optimizations.

   - [Cluster storage scaling](/docs/atlas/cluster-autoscaling#std-label-howitworks-scale-cluster-storage) automatically increases your cluster storage capacity when 90% of disk capacity is used. This setting is enabled by default to help ensure that your cluster can always support sudden influxes of data. To opt out of cluster storage scaling, un-check the Storage Scaling checkbox in the Auto-scale section.

   - [Cluster tier scaling](/docs/atlas/cluster-autoscaling#std-label-howitworks-scale-cluster-tier) automatically scales your cluster tier up or down in response to various cluster metrics. To opt out of cluster tier auto-scaling, un-check the Cluster Tier Scaling checkbox in the Auto-scale section.

     To control how Atlas should auto-scale your cluster, you set:

     - The maximum cluster tier to which your cluster can automatically scale up. By default, this setting is set to the next cluster tier compared to your current cluster tier.

     - The minimum cluster tier to which your cluster can scale down. By default, this setting is set to the current cluster tier.

   For more information on how to select an appropriate cluster tier and storage settings for your workload, see [Select Cluster Tier](/docs/atlas/manage-clusters#std-label-create-cluster-instance) and [Customize Cluster Storage.](/docs/atlas/customize-storage#std-label-create-cluster-storage)

   You can [select a cluster tier](/docs/atlas/manage-clusters#std-label-create-cluster-instance) appropriately sized for your analytics workload. To learn more, see [Analytics Nodes for Workload Isolation.](/docs/atlas/cluster-config/multi-cloud-distribution#std-label-deploy-analytics-nodes)

   You can also select a different tier for your Search Nodes. To learn more about the available tiers for your Search Nodes, see [Search Tier.](/docs/atlas/cluster-config/multi-cloud-distribution#std-label-select-tiers-for-search-nodes)

7. Select any Additional Settings.

   From the Additional Settings section, you can:

   - [Select the MongoDB Version of the Cluster](/docs/atlas/cluster-additional-settings#std-label-create-cluster-version)

   - [Configure Backup Options for the Cluster](/docs/atlas/cluster-additional-settings#std-label-create-cluster-backups)

   - [Termination Protection](/docs/atlas/cluster-additional-settings#std-label-create-cluster-termination-protection)

   - [Deploy a Sharded Cluster](/docs/atlas/cluster-additional-settings#std-label-create-cluster-sharding)

   - [Configure the Number of Shards](/docs/atlas/cluster-additional-settings#std-label-create-cluster-shardNum)

   - [Enable BI Connector for Atlas](/docs/atlas/cluster-additional-settings#std-label-create-cluster-enable-bi)

   - [Manage Your Own Encryption Keys](/docs/atlas/cluster-additional-settings#std-label-create-cluster-enable-encryption)

   - [Configure Additional Options](/docs/atlas/cluster-additional-settings#std-label-create-cluster-more-configuration-options)

8. Specify the Cluster Details.

   From the Cluster Details section, you can:

   - Specify the Cluster Name.

     This label identifies the cluster in Atlas.

     **Note:**

     Atlas creates your hostname based on your cluster name.

     You can't change the cluster name after Atlas deploys the cluster. Cluster names can't exceed 64 characters in length.

     IMPORTANT: Atlas truncates the cluster name to *23 characters* in its internal interactions. In practice, this means:

     - Cluster names shorter than 23 characters can't end with hyphen or dash (`-`).

     - Cluster names 23 characters or longer can't use a hyphen or dash (`-`) as its 23rd character.

     - The first 23 characters in a cluster name must be unique within a project.

     Don't include [sensitive information](/docs/atlas/production-notes#std-label-sensitive-info) in your cluster name.

   - [Apply tags to the cluster.](/docs/atlas/database-deployment-tags#std-label-apply-tags-new-cluster)

     **Important:**

     Don't include sensitive information such as Personally Identifiable Information (PII) or Protected Health Information (PHI) in your resource tags. Other MongoDB services, such as Billing, can access resource tags. MongoDB also sends cluster resource tags to DataDog and Prometheus integrations. Resource tags are *not* intended for private and sensitive data. To learn more, see [Sensitive Information.](/docs/atlas/production-notes#std-label-sensitive-info)

9. Proceed to checkout.

   Click Create Cluster below the form and complete the billing information only if it doesn't already exist. If your organization already has the billing information, Atlas deploys your cluster.

10. Update your Billing Address details as needed.

    <table>
    <thead>
    <tr>
    <th>Field</th>
    <th>Necessity</th>
    <th>Action</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <th>Billing Email Address</th>
    <td>Optional</td>
    <td>Type the email address to which Atlas should send <a href="/docs/atlas/reference/alert-conditions#std-label-billing-alerts">billing alerts.</a><br>By default, Atlas sends billing alerts to the Organization Owners and Billing Admins.<br><ul><li>If you leave the Billing Email Address blank, Atlas sends billing alerts to the Organization Owners and Billing Admins.</li><li>If you specify a billing email address and uncheck Only
    send invoice emails to the Billing Email
    Address, Atlas sends billing alerts to the billing email address, Organization Owners, and Billing Admins.</li><li>If you specify a billing email address and check the box for Only
    send invoice emails to the Billing Email
    Address, Atlas send billing alerts to the billing email address only.</li></ul></td>
    </tr>
    <tr>
    <th>Company Name</th>
    <td>Optional</td>
    <td>Type the name of the company for your billing address.</td>
    </tr>
    <tr>
    <th>Country</th>
    <td>Required</td>
    <td>Select the country for your billing address. You can also start typing the name of the country and then select it from the filtered list of countries.</td>
    </tr>
    <tr>
    <th>Street Address</th>
    <td>Required</td>
    <td>Type the street address for your billing address.</td>
    </tr>
    <tr>
    <th>Apt/Suite/Floor</th>
    <td>Optional</td>
    <td>Type an the apartment, suite, or floor for your billing address.</td>
    </tr>
    <tr>
    <th>City</th>
    <td>Required</td>
    <td>Type the name of the city for your billing address.</td>
    </tr>
    <tr>
    <th>State/Province/Region</th>
    <td>Required</td>
    <td>Type or select the political subdivision in which your billing address exists. The label and field change depending on what you selected as your <strong>Country</strong>:<br><ul><li>If you select <strong>United States</strong> as your <strong>Country</strong>, this label changes to <strong>State</strong>. The field changes to a dropdown menu of U.S. states. You can also start typing the name of the state and then select it from the filtered list of states.</li><li>If you select <strong>Canada</strong> as your <strong>Country</strong>, this label changes to <strong>Province</strong>. The field changes to a dropdown menu of Canadian provinces. You can also start typing the name of the province and then select it from the filtered list of provinces.</li><li>If you select any other country as your <strong>Country</strong>, this label changes to <strong>State/Province/Region</strong>. The field changes to a text box. Type the name of your province, state, or region in this box.</li></ul></td>
    </tr>
    <tr>
    <th>ZIP or Postal Code</th>
    <td>Required</td>
    <td>Type the ZIP (U.S.) or Postal Code (other countries) for your billing address.</td>
    </tr>
    <tr>
    <th>VAT Number</th>
    <td>Conditional</td>
    <td>Atlas displays the VAT ID field if you select a country other than the United States.<br>To learn more about VAT, see <a href="/docs/atlas/billing/international-usage#std-label-vat-id-number">VAT ID.</a><br>If your company's billing address is in a country other than the United States (USA), Atlas typically charges VAT (Value Added Tax) if you do not enter a valid <code>VAT ID Number</code> on your <a href="/docs/atlas/billing#std-label-atlas-billing-profile">billing profile.</a><br>IMPORTANT: If your billing address is in Ireland or certain Canadian provinces, Atlas always charges VAT (Value Added Tax), even with a valid <code>VAT ID Number</code>.<br>To learn more about VAT (Value Added Tax) by region, see <a href="/docs/atlas/billing/international-usage#std-label-atlas-international-tax">International Usage and Taxation.</a></td>
    </tr>
    </tbody>
    </table>

11. Update your Payment Method details as needed.

    Click the radio button for Credit Card or Paypal.

    - If you selected Credit Card, type values for the following fields:

      <table>
      <thead>
      <tr>
      <th>Field</th>
      <th>Necessity</th>
      <th>Action</th>
      </tr>
      </thead>
      <tbody>
      <tr>
      <th>Name on Card</th>
      <td>Required</td>
      <td>Type the name that appears on your credit card.</td>
      </tr>
      <tr>
      <th>Card Number</th>
      <td>Required</td>
      <td>Type the 16-digit number that appears on your credit card. American Express uses a 15-digit number.</td>
      </tr>
      <tr>
      <th>Expiration Date</th>
      <td>Required</td>
      <td>Type the expiration date for your credit card in the two-digit month and two-digit year format.</td>
      </tr>
      <tr>
      <th>CVC (Card Verification Code)</th>
      <td>Required</td>
      <td>Type the three-digit number on the back of your credit card. American Express uses a 4-digit number found on the front of the credit card.</td>
      </tr>
      </tbody>
      </table>

    - If you selected PayPal:

      Click Pay with PayPal.

      Complete the actions on the PayPal website.

    **Note:**

    All projects within your organization share the same billing settings, including payment method.

12. Review project's cost.

    Under the Cart section, review the following:

    <table>
    <thead>
    <tr>
    <th>Field</th>
    <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <th>Cluster Tier</th>
    <td>Displays cost for your selected cluster tier and configuration details. To learn more, see <a href="/docs/atlas/billing/cluster-configuration-costs#std-label-region-costs">Cloud Service Provider and Region</a> and <a href="/docs/atlas/billing/cluster-configuration-costs#std-label-instance-size-costs">Cluster Tier.</a></td>
    </tr>
    <tr>
    <th>Included Features</th>
    <td>Displays features included with your selected cluster configuration.</td>
    </tr>
    <tr>
    <th>Additional Settings</th>
    <td>Displays additional settings that you enabled, such as cloud backups, sharding, <a href="https://www.mongodb.com/docs/bi-connector/current/">BI Connector</a>, and more. To learn more, see <a href="/docs/atlas/billing/cluster-configuration-costs#std-label-billing-backup-cloud-provider-snapshots">Cloud Backups.</a></td>
    </tr>
    </tbody>
    </table>

13. Deploy your cluster. Click Confirm and Deploy Cluster.

    **Important:**

    Each Atlas [project](/docs/atlas/organizations-projects#std-label-projects) supports up to 25 clusters. If you have questions or need assistance regarding the cluster limit, [contact support.](/docs/atlas/support#std-label-atlas-support)

For replica sets, the data-bearing servers are the servers hosting the replica set nodes. For sharded clusters, the data-bearing servers are the servers hosting the shards. For sharded clusters, Atlas also deploys servers for the [config servers](https://www.mongodb.com/docs/manual/core/sharded-cluster-config-servers/#std-label-sharding-config-server); these are charged at a rate separate from the cluster costs.
