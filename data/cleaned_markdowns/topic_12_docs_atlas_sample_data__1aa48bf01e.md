> Source: https://www.mongodb.com/docs/atlas/sample-data/
> Fetch method: direct_markdown

# Sample Datasets

MongoDB provides sample data you can load into your deployments. You can use this data to quickly get started experimenting with data in MongoDB and using tools such as the Atlas UI and MongoDB Charts.

## Available Sample Datasets

The following table shows the sample datasets available. Click a sample dataset to learn more about it.

For instructions on loading this sample data into your deployment , see Load Sample Data Into Atlas.

| Dataset Name | Description |
| --- | --- |
| <a href="/docs/atlas/sample-data/sample-airbnb#std-label-sample-airbnb">Sample AirBnB Listings Dataset</a> | Contains details on<a href="https://www.airbnb.com">AirBnB</a> listings. |
| <a href="/docs/atlas/sample-data/sample-analytics#std-label-sample-analytics">Sample Analytics Dataset</a> | Contains training data for a mock financial services application. |
| <a href="/docs/atlas/sample-data/sample-geospatial#std-label-sample-geospatial">Sample Geospatial Dataset</a> | Contains shipwreck data. |
| <a href="/docs/atlas/sample-data/sample-guides#std-label-sample-guides">Sample Guides Dataset</a> | Contains planet data. |
| <a href="/docs/atlas/sample-data/sample-mflix#std-label-sample-mflix">Sample Mflix Dataset</a> | Contains movie data. Includes <a href="https://www.mongodb.com/docs/vector-search/tutorials/quick-start/#std-label-vector-search-quickstart-sample-data">vector embeddings.</a> |
| <a href="/docs/atlas/sample-data/sample-restaurants#std-label-sample-restaurants">Sample Restaurants Dataset</a> | Contains restaurant data. |
| <a href="/docs/atlas/sample-data/sample-supplies#std-label-sample-supplies">Sample Supply Store Dataset</a> | Contains data from a mock office supply store. |
| <a href="/docs/atlas/sample-data/sample-training#std-label-sample-training">Sample Training Dataset</a> | Contains MongoDB training services dataset. |
| <a href="/docs/atlas/sample-data/sample-weather#std-label-sample-weather">Sample Weather Dataset</a> | Contains detailed weather reports. |

## Sample Data Namespaces

When you load the sample data, MongoDB creates the following namespaces on your deployment:

**Warning:**

If any of these namespaces already exist on your cluster when you attempt to load the sample data, the operation will fail and no sample data will be loaded into your cluster.

| Database | Collection |
| --- | --- |
| <code>sample_airbnb</code> | <code>listingsAndReviews</code> |
| <code>sample_analytics</code> | <code>accounts</code> |
| <code>sample_analytics</code> | <code>customers</code> |
| <code>sample_analytics</code> | <code>transactions</code> |
| <code>sample_geospatial</code> | <code>shipwrecks</code> |
| <code>sample_guides</code> | <code>planets</code> |
| <code>sample_mflix</code> | <code>comments</code> |
| <code>sample_mflix</code> | <code>embedded_movies</code> |
| <code>sample_mflix</code> | <code>movies</code> |
| <code>sample_mflix</code> | <code>theaters</code> |
| <code>sample_mflix</code> | <code>users</code> |
| <code>sample_supplies</code> | <code>sales</code> |
| <code>sample_training</code> | <code>companies</code> |
| <code>sample_training</code> | <code>grades</code> |
| <code>sample_training</code> | <code>inspections</code> |
| <code>sample_training</code> | <code>posts</code> |
| <code>sample_training</code> | <code>routes</code> |
| <code>sample_training</code> | <code>trips</code> |
| <code>sample_training</code> | <code>zips</code> |
| <code>sample_weatherdata</code> | <code>data</code> |

## Tutorials Using Sample Data

### Atlas Tutorials

The Get Started tutorial walks through setting up an Atlas cluster and populating that cluster with sample data.

### MongoDB Charts Tutorials

The following MongoDB Charts tutorials guide you through visualizing sample data provided by Atlas:

Visualizing Order Data

Visualize the Sample Supply Store Dataset, which contains sales order data from a mock office supply company.

Visualizing Movie Details

Visualize the Sample Mflix Dataset, which contains data on movies and movie theaters.

**Tip:**

To visualize data in MongoDB Charts from the Atlas UI, click Visualize Your Data when viewing a specific database or collection. Charts loads the data source and you can start building a chart in the Charts view. For detailed steps, see Build Charts.

## MongoDB Courses that Use Sample Data

Instructor-led Training

Get quickly ramped on MongoDB with comprehensive private training programs for developers and operations teams.
