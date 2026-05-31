> Source: https://www.mongodb.com/docs/atlas/sample-data/
> Fetch method: direct_markdown

# Sample Datasets

MongoDB provides sample data you can load into your deployments. You can use this data to quickly get started experimenting with data in MongoDB and using tools such as the [Atlas UI](/docs/atlas/atlas-ui#std-label-atlas-ui) and [MongoDB Charts.](https://www.mongodb.com/docs/charts/)

## Available Sample Datasets

The following table shows the sample datasets available. Click a sample dataset to learn more about it.

For instructions on loading this sample data into your deployment , see [Load Sample Data Into Atlas.](/docs/atlas/sample-data/load-sample-data#std-label-load-sample-data)

<table>
<thead>
<tr>
<th>Dataset Name</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="/docs/atlas/sample-data/sample-airbnb#std-label-sample-airbnb">Sample AirBnB Listings Dataset</a></td>
<td>Contains details on<a href="https://www.airbnb.com">AirBnB</a> listings.</td>
</tr>
<tr>
<td><a href="/docs/atlas/sample-data/sample-analytics#std-label-sample-analytics">Sample Analytics Dataset</a></td>
<td>Contains training data for a mock financial services application.</td>
</tr>
<tr>
<td><a href="/docs/atlas/sample-data/sample-geospatial#std-label-sample-geospatial">Sample Geospatial Dataset</a></td>
<td>Contains shipwreck data.</td>
</tr>
<tr>
<td><a href="/docs/atlas/sample-data/sample-guides#std-label-sample-guides">Sample Guides Dataset</a></td>
<td>Contains planet data.</td>
</tr>
<tr>
<td><a href="/docs/atlas/sample-data/sample-mflix#std-label-sample-mflix">Sample Mflix Dataset</a></td>
<td>Contains movie data. Includes <a href="https://www.mongodb.com/docs/vector-search/tutorials/quick-start/#std-label-vector-search-quickstart-sample-data">vector embeddings.</a></td>
</tr>
<tr>
<td><a href="/docs/atlas/sample-data/sample-restaurants#std-label-sample-restaurants">Sample Restaurants Dataset</a></td>
<td>Contains restaurant data.</td>
</tr>
<tr>
<td><a href="/docs/atlas/sample-data/sample-supplies#std-label-sample-supplies">Sample Supply Store Dataset</a></td>
<td>Contains data from a mock office supply store.</td>
</tr>
<tr>
<td><a href="/docs/atlas/sample-data/sample-training#std-label-sample-training">Sample Training Dataset</a></td>
<td>Contains MongoDB training services dataset.</td>
</tr>
<tr>
<td><a href="/docs/atlas/sample-data/sample-weather#std-label-sample-weather">Sample Weather Dataset</a></td>
<td>Contains detailed weather reports.</td>
</tr>
</tbody>
</table>

## Sample Data Namespaces

When you load the sample data, MongoDB creates the following namespaces on your deployment:

**Warning:**

If any of these namespaces already exist on your cluster when you attempt to load the sample data, the operation will fail and no sample data will be loaded into your cluster.

<table>
<thead>
<tr>
<th>Database</th>
<th>Collection</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>sample_airbnb</code></td>
<td><code>listingsAndReviews</code></td>
</tr>
<tr>
<td><code>sample_analytics</code></td>
<td><code>accounts</code></td>
</tr>
<tr>
<td><code>sample_analytics</code></td>
<td><code>customers</code></td>
</tr>
<tr>
<td><code>sample_analytics</code></td>
<td><code>transactions</code></td>
</tr>
<tr>
<td><code>sample_geospatial</code></td>
<td><code>shipwrecks</code></td>
</tr>
<tr>
<td><code>sample_guides</code></td>
<td><code>planets</code></td>
</tr>
<tr>
<td><code>sample_mflix</code></td>
<td><code>comments</code></td>
</tr>
<tr>
<td><code>sample_mflix</code></td>
<td><code>embedded_movies</code></td>
</tr>
<tr>
<td><code>sample_mflix</code></td>
<td><code>movies</code></td>
</tr>
<tr>
<td><code>sample_mflix</code></td>
<td><code>theaters</code></td>
</tr>
<tr>
<td><code>sample_mflix</code></td>
<td><code>users</code></td>
</tr>
<tr>
<td><code>sample_supplies</code></td>
<td><code>sales</code></td>
</tr>
<tr>
<td><code>sample_training</code></td>
<td><code>companies</code></td>
</tr>
<tr>
<td><code>sample_training</code></td>
<td><code>grades</code></td>
</tr>
<tr>
<td><code>sample_training</code></td>
<td><code>inspections</code></td>
</tr>
<tr>
<td><code>sample_training</code></td>
<td><code>posts</code></td>
</tr>
<tr>
<td><code>sample_training</code></td>
<td><code>routes</code></td>
</tr>
<tr>
<td><code>sample_training</code></td>
<td><code>trips</code></td>
</tr>
<tr>
<td><code>sample_training</code></td>
<td><code>zips</code></td>
</tr>
<tr>
<td><code>sample_weatherdata</code></td>
<td><code>data</code></td>
</tr>
</tbody>
</table>

## Tutorials Using Sample Data

### Atlas Tutorials

The [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) tutorial walks through setting up an Atlas cluster and populating that cluster with sample data.

### MongoDB Charts Tutorials

The following [MongoDB Charts](https://www.mongodb.com/docs/charts/) tutorials guide you through visualizing sample data provided by Atlas:

[Visualizing Order Data](https://www.mongodb.com/docs/charts/tutorial/order-data/order-data-tutorial-overview/)

Visualize the [Sample Supply Store Dataset](/docs/atlas/sample-data/sample-supplies#std-label-sample-supplies), which contains sales order data from a mock office supply company.

[Visualizing Movie Details](https://www.mongodb.com/docs/charts/tutorial/movie-details/movie-details-tutorial-overview/)

Visualize the [Sample Mflix Dataset](/docs/atlas/sample-data/sample-mflix#std-label-sample-mflix), which contains data on movies and movie theaters.

**Tip:**

To visualize data in MongoDB Charts from the Atlas UI, click Visualize Your Data when viewing a specific database or collection. Charts loads the data source and you can start building a chart in the Charts view. For detailed steps, see [Build Charts.](https://www.mongodb.com/docs/charts/build-charts/)

## MongoDB Courses that Use Sample Data

[Instructor-led Training](https://www.mongodb.com/services/training)

Get quickly ramped on MongoDB with comprehensive private training programs for developers and operations teams.
