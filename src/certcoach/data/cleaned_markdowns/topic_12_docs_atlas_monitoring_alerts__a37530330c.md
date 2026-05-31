> Source: https://www.mongodb.com/docs/atlas/monitoring-alerts/
> Fetch method: direct_markdown

# Monitor Your Clusters

Atlas provides built-in tools, alerts, charts, integrations, and logs to help you monitor your clusters. Atlas provides the following ways to monitor your clusters and improve performance.

To learn about recommendations for monitoring and alerts, including important metrics to monitor and recommended alert configurations, see Recommendations for Atlas Monitoring and Alerts in the Atlas Architecture Center.

## Slow Queries

To optimize your query performance, review the best
practices for query performance. You can also analyze slow queries and troubleshoot slow operations executed on your clusters.

Use the following built-in tools:

- Monitor and improve slow queries with the Performance Advisor.

- Monitor collection-level query latency with Namespace Insights.

- Monitor query performance with the Query Profiler.

- Monitor real-time performance with the Real-Time Performance Panel.

## Schema Design

To optimize your schema design, review our frequently used schema
design patterns. You can also improve
your schema. Improve your schema based on recommendations from the Performance Advisor and the Atlas UI.

## Alerts

To trigger alerts based on alert conditions and to help ensure cluster performance, configure alerts and resolve them promptly. You can configure alerts based on specific conditions for your databases, users, accounts, and more. When you resolve alerts, you should fix the immediate problem, implement a long-term solution, and monitor your progress.

Before you get started with alerts, review the Alert Basics.

## Deployment Metrics

To monitor your cluster performance, view
cluster metrics. View historical throughput, performance, and usage metrics for your databases. To learn more, review the available metrics.

## Third-Party Integrations

To receive Atlas alerts in various external monitoring services, integrate with third-party monitoring services.

## MongoDB Logs

Atlas provides several methods for accessing your log messages and system event audit messages.

- View and download your MongoDB logs directly from the Atlas UI, API, or CLI for manual inspection and troubleshooting.

- Export logs in near real-time to AWS (Amazon Web Services) S3 (Simple Storage Service) buckets.

- Use the Atlas Administration API to pull log data every 5 minutes or pull monitoring data.

**Note:**

Atlas continues to support the following legacy methods for log and metric integration:

- Use the legacy push-based log export feature to send logs to an AWS (Amazon Web Services) S3 (Simple Storage Service) bucket. For new S3 (Simple Storage Service) integrations, we recommend using the Atlas export feature instead.

- Configure push-based monitoring integrations for Atlas with Datadog to send metrics.

- Configure pull-based logging integrations with jSonar (which can push to other services like Splunk) and SumoLogic.
