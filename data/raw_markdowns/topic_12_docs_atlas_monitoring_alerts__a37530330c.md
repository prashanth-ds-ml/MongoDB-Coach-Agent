> Source: https://www.mongodb.com/docs/atlas/monitoring-alerts/
> Fetch method: direct_markdown

# Monitor Your Clusters

Atlas provides built-in tools, alerts, charts, integrations, and logs to help you monitor your clusters. Atlas provides the following ways to monitor your clusters and improve performance.

To learn about recommendations for monitoring and alerts, including important metrics to monitor and recommended alert configurations, see [Recommendations for Atlas Monitoring and Alerts](https://www.mongodb.com/docs/atlas/architecture/current/monitoring-alerts/#std-label-arch-center-monitoring-alerts-recs) in the Atlas Architecture Center.

## Slow Queries

To optimize your query performance, [review the best
practices for query performance](/docs/atlas/analyze-slow-queries#std-label-query-best-practices). You can also [analyze slow queries](/docs/atlas/analyze-slow-queries#std-label-analyze-slow-queries) and troubleshoot slow operations executed on your clusters.

Use the following built-in tools:

- [Monitor and improve slow queries](/docs/atlas/performance-advisor#std-label-performance-advisor) with the Performance Advisor.

- [Monitor collection-level query latency](/docs/atlas/namespace-insights#std-label-namespace-insights) with Namespace Insights.

- [Monitor query performance](/docs/atlas/tutorial/query-profiler#std-label-profile-database) with the Query Profiler.

- [Monitor real-time performance](/docs/atlas/real-time-performance-panel#std-label-real-time-metrics-status-tab) with the Real-Time Performance Panel.

## Schema Design

To optimize your schema design, review our frequently used [schema
design patterns](/docs/atlas/performance-advisor/schema-suggestions#std-label-schema-design-patterns). You can also [improve
your schema](/docs/atlas/performance-advisor/schema-suggestions#std-label-schema-suggestions). Improve your schema based on recommendations from the [Performance Advisor](/docs/atlas/performance-advisor#std-label-performance-advisor) and the [Atlas UI.](/docs/atlas/atlas-ui/databases#std-label-atlas-ui-dbs)

## Alerts

To trigger alerts based on [alert conditions](/docs/atlas/reference/alert-conditions#std-label-alert-conditions) and to help ensure cluster performance, [configure alerts and resolve them promptly](/docs/atlas/alerts#std-label-alerts). You can configure alerts based on specific conditions for your databases, users, accounts, and more. When you resolve alerts, you should fix the immediate problem, implement a long-term solution, and monitor your progress.

Before you get started with alerts, review the [Alert Basics.](/docs/atlas/alert-basics#std-label-alert-basics)

## Deployment Metrics

To monitor your cluster performance, [view
cluster metrics](/docs/atlas/monitor-cluster-metrics#std-label-monitor-cluster-metrics). View historical throughput, performance, and usage metrics for your databases. To learn more, [review the available metrics.](/docs/atlas/review-available-metrics#std-label-review-available-metrics)

## Third-Party Integrations

To receive Atlas alerts in various external monitoring services, [integrate with third-party monitoring services.](/docs/atlas/tutorial/third-party-service-integrations#std-label-third-party-integrations)

## MongoDB Logs

Atlas provides several methods for accessing your [log messages](https://www.mongodb.com/docs/manual/reference/log-messages/) and [system event audit messages.](https://www.mongodb.com/docs/manual/reference/audit-message/)

- [View and download your MongoDB logs](/docs/atlas/mongodb-logs#std-label-mongodb-logs) directly from the Atlas UI, API, or CLI for manual inspection and troubleshooting.

- [Export logs in near real-time](/docs/atlas/export-logs-external-sinks#std-label-export-logs-external-sinks) to AWS (Amazon Web Services) S3 (Simple Storage Service) buckets.

- Use the Atlas Administration API to [pull log data](https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/group/endpoint-monitoring-and-logs) every 5 minutes or [pull monitoring data.](https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/group/endpoint-monitoring-and-logs)

**Note:**

Atlas continues to support the following legacy methods for log and metric integration:

- Use the legacy [push-based log export](/docs/atlas/push-logs#std-label-mongodb-logs-push) feature to send logs to an AWS (Amazon Web Services) S3 (Simple Storage Service) bucket. For new S3 (Simple Storage Service) integrations, we recommend using [the Atlas export feature](/docs/atlas/export-logs-external-sinks#std-label-export-logs-external-sinks) instead.

- Configure push-based [monitoring integrations](/docs/atlas/tutorial/third-party-service-integrations/) for Atlas with Datadog to send metrics.

- Configure pull-based logging integrations with jSonar (which can push to other services like Splunk) and SumoLogic.
