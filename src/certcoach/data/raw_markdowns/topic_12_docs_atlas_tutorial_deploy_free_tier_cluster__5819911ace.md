> Source: https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/
> Fetch method: direct_markdown

# Deploy a Free Cluster

*Estimated completion time: 3 minutes*

Atlas Free clusters (formerly known as `M0`) provide a small-scale development environment to host your data. Free clusters never expire, and provide access to a [subset](/docs/atlas/reference/free-shared-limitations#std-label-atlas-free-tier) of Atlas features and functionality.

Paid clusters provide full access to Atlas features, configuration options, and operational capabilities. For more information on paid clusters, including deployment instructions, see [Create a Cluster.](/docs/atlas/tutorial/create-new-cluster)

**Note:**

You can deploy only one Free cluster per Atlas project.

## Procedure

You can create Free clusters through the [Atlas CLI](https://www.mongodb.com/docs/atlas/cli/current/), Atlas User Interface, and Atlas Administration API. Select the appropriate tab based on how you would like to create the Free clusters.

### Atlas CLI

To create one cluster, load sample data, add your IP address to your project IP access list, and create a MongoDB user for your cluster using the Atlas CLI, run the following command:

```sh

atlas setup [options]

```

To learn more about the command syntax and parameters, see the Atlas CLI documentation for [atlas setup.](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-setup/)

For step-by-step instructions on using this command, see [Create and Configure an Atlas Cluster using the Atlas CLI.](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-quickstart/)

### Atlas Administration API

To create a free cluster using the Atlas Administration API, send a `POST` request to the `clusters` endpoint with the `instanceSize` set to `M0` (the cluster tier for Free clusters). To learn more about the resource and parameters, see [Create.](https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/operation/operation-creategroupcluster)

### Atlas UI

To create a free cluster through the Atlas UI:

**Important:**

The following procedure applies to creating your very first cluster in the Atlas UI.

1. Log in to Atlas.

   Complete any welcome prompts. If you're logging in for the first time, Atlas sometimes skips the next two steps.

2. Go to the Project Overview page for your project.

   If it is not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

   If it is not already displayed, select your desired project from the Projects menu in the navigation bar.

   If the [Overview](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Foverview) page is not already displayed, click Project Overview in the sidebar.

3. Create a cluster.

   Click the Create button to create a cluster.

4. Select the M0 option.

   Free clusters are free forever and suitable for users learning MongoDB or developing small proof-of-concept applications.

5. Select your preferred Provider.

   Atlas supports Free clusters on [Amazon Web Services (AWS)](/docs/atlas/reference/amazon-aws#std-label-amazon-aws), [Google Cloud Platform (GCP)](/docs/atlas/reference/google-gcp#std-label-google-gcp), and [Microsoft Azure.](/docs/atlas/reference/microsoft-azure#std-label-microsoft-azure)

6. Select your preferred Region.

   Atlas displays only the cloud provider regions that support Free clusters.

7. Specify a name for your cluster in the Name box.

   You can specify any name for your cluster. The cluster name can contain ASCII letters, numbers, and hyphens.

   You can't change the cluster name after Atlas deploys the cluster. Cluster names can't exceed 64 characters in length.

8. Click Create to deploy the cluster.

   The Security Quickstart wizard appears.

   To learn more about the security features available, see [Configure Security Features for Clusters.](/docs/atlas/setup-cluster-security#std-label-setup-cluster-security)

   Once you deploy your free Atlas cluster, it takes less than 15 seconds for it to become ready to use.

9. Create a database user.

   Specify a Username for your database user.

   Specify a Password or copy the secure password that Atlas suggests.

   Click Create Database User.

10. Add your IP address to the IP access list.

    Click Add My Current IP Address.

    Click Finish and Close.

    Click Go to Overview.

## Next Steps

Now that your cluster is provisioned, proceed to [Manage the Database Users for Your Cluster.](/docs/atlas/tutorial/create-mongodb-user-for-cluster#std-label-gswa-user)
