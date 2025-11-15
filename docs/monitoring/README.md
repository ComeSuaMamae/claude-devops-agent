# Monitoring & Incident Response with Claude

Learn how to leverage Claude for intelligent monitoring, log analysis, incident response, and automated remediation.

## Table of Contents

1. [Introduction](#introduction)
2. [Use Cases](#use-cases)
3. [Log Analysis](#log-analysis)
4. [Incident Response](#incident-response)
5. [Automated Remediation](#automated-remediation)
6. [Alerting and Notifications](#alerting-and-notifications)
7. [Best Practices](#best-practices)
8. [Examples](#examples)

## Introduction

Monitoring and incident response are critical for maintaining reliable systems. Claude can act as an intelligent DevOps agent to:

- **Analyze logs** and identify patterns, anomalies, and root causes
- **Diagnose issues** by correlating metrics, logs, and events
- **Suggest fixes** based on error messages and system state
- **Generate runbooks** for common incidents
- **Automate responses** to known issues
- **Create dashboards** and alerts
- **Perform RCA** (Root Cause Analysis)

## Use Cases

### 1. Log Analysis and Pattern Recognition

**Scenario**: You have application error logs and need to identify the root cause.

**Prompt to Claude**:
```
Analyze these application logs and identify:
1. What is causing the errors
2. When did the issue start
3. Pattern of failures
4. Suggested remediation steps

[paste logs]
```

### 2. Performance Degradation Analysis

**Scenario**: Application response time has increased.

**Prompt to Claude**:
```
Our API response time has increased from 200ms to 2000ms. Here are:
- Recent CloudWatch metrics: [paste metrics]
- Application logs: [paste logs]
- Database slow query log: [paste queries]

Help me diagnose the performance issue and suggest solutions.
```

### 3. Incident Response Automation

**Scenario**: Create automated response to common incidents.

**Prompt to Claude**:
```
Create a Python script that:
1. Monitors CloudWatch metrics for high CPU usage
2. When CPU > 80% for 5 minutes:
   - Captures diagnostics (top, ps, netstat)
   - Analyzes running processes
   - Sends alert with analysis
   - Suggests remediation
3. Optionally auto-scale if needed
```

### 4. Creating Runbooks

**Scenario**: Document incident response procedures.

**Prompt to Claude**:
```
Create a runbook for responding to database connection pool exhaustion including:
- Symptoms and detection
- Immediate mitigation steps
- Diagnostic commands
- Root cause analysis steps
- Long-term prevention
- Rollback procedures
```

## Log Analysis

### Application Logs

Claude can analyze various log formats and identify issues:

**Example Prompt**:
```
Analyze these nginx access logs and identify:
- Unusual traffic patterns
- Potential security issues (SQL injection, XSS attempts)
- Performance bottlenecks
- Error rate trends
- Top error URLs

[paste logs]
```

**Claude's Analysis Can Include**:
- Error rate calculations
- Pattern identification
- Timeline of events
- Correlation between different error types
- Specific problematic requests

### System Logs

**Example Prompt**:
```
Review these Linux system logs (syslog/journald):
[paste logs]

Identify:
- System errors or warnings
- Resource exhaustion indicators
- Security concerns
- Hardware issues
- Service failures
```

### Kubernetes Logs

**Example Prompt**:
```
Analyze these Kubernetes pod logs and events:
[kubectl logs output]
[kubectl describe pod output]

Diagnose:
- Why is the pod crashing
- CrashLoopBackOff root cause
- Resource constraints
- Configuration issues
```

### Structured Log Analysis

**Example Prompt**:
```
Parse and analyze this JSON log data:
[paste structured logs]

Create:
1. Summary of error types and frequency
2. Timeline of issues
3. Correlation between errors
4. Affected services/endpoints
5. Suggested fixes prioritized by impact
```

## Incident Response

### Incident Diagnosis

**During an Active Incident**:

```
We're experiencing an outage. Current symptoms:
- 500 errors on API endpoint /api/users
- Error rate: 45% of requests
- Started: 2024-01-15 14:30 UTC
- Recent deployments: [describe]

Logs:
[paste recent logs]

Metrics:
[paste relevant metrics]

Help me:
1. Identify root cause
2. Immediate mitigation steps
3. Recovery procedure
```

### Multi-Signal Correlation

**Prompt**:
```
Correlate these signals to diagnose the issue:

Application Metrics:
- Request rate: normal
- Error rate: 15% (up from 0.1%)
- Response time: 3000ms (up from 200ms)

Database Metrics:
- Connection pool: 95% utilized
- Query time: 2500ms average
- Slow query log: [paste]

Infrastructure:
- CPU: 45% (normal)
- Memory: 78% (slightly high)
- Disk I/O: normal

What's the root cause and how do I fix it?
```

### Creating Incident Reports

**Prompt**:
```
Generate a post-incident report for:

Incident: Database connection pool exhaustion
Duration: 2 hours
Impact: 15% error rate on API
Root cause: Leaked connections from new feature
Resolution: Rolled back deployment

Include:
- Executive summary
- Timeline
- Root cause analysis
- Impact assessment
- Remediation steps
- Prevention measures
- Action items
```

## Automated Remediation

### Auto-Healing Scripts

**Example: Disk Space Cleanup**

**Prompt**:
```
Create a Python script that:
1. Monitors disk usage
2. When usage > 85%:
   - Identifies old log files
   - Compresses logs older than 7 days
   - Deletes logs older than 30 days
   - Sends notification with actions taken
3. Runs safely without breaking running services
```

See: `examples/monitoring/scripts/disk-cleanup.py`

### Service Recovery

**Prompt**:
```
Create a bash script that:
1. Monitors a service health endpoint
2. If 3 consecutive failures:
   - Captures diagnostics (logs, metrics)
   - Attempts graceful restart
   - Verifies service recovery
   - Sends detailed alert
3. If restart fails, escalates to on-call
```

See: `examples/monitoring/scripts/service-monitor.sh`

### Database Connection Management

**Prompt**:
```
Write a script to prevent database connection leaks:
1. Monitor connection pool usage
2. Identify long-running connections
3. Warn when connections near limit
4. Optionally kill idle connections
5. Log all actions for audit
```

## Alerting and Notifications

### Intelligent Alert Generation

**Prompt**:
```
Review our current alerting setup:
[paste alert definitions]

Improve it by:
1. Reducing false positives
2. Adding context to alerts
3. Suggesting automatic remediation where possible
4. Grouping related alerts
5. Adding severity levels
```

### Alert Analysis

**Prompt**:
```
We're getting this alert repeatedly:
Alert: High memory usage
Threshold: 85%
Frequency: Every 5 minutes for 3 hours

Recent logs:
[paste logs]

System metrics:
[paste metrics]

Is this a real issue or a false positive? How should we adjust the alert?
```

### Creating Meaningful Alerts

**Prompt**:
```
Create CloudWatch alarms for:
1. API latency > 1s for 5 minutes
2. Error rate > 5% for 2 minutes
3. Database connection pool > 80% for 3 minutes

Include:
- Proper thresholds
- Actionable notifications
- Suggested remediation in alert message
- Runbook links
```

## Monitoring Tools Integration

### CloudWatch Integration

**Prompt**:
```
Create a Python script using boto3 to:
1. Query CloudWatch metrics for last hour
2. Analyze for anomalies
3. Generate a report
4. Send to Slack if issues found

Metrics to check:
- Lambda errors and duration
- API Gateway 4xx/5xx rates
- DynamoDB throttled requests
```

See: `examples/monitoring/cloudwatch/anomaly-detector.py`

### Prometheus/Grafana

**Prompt**:
```
Create PromQL queries to:
1. Detect request rate anomalies
2. Identify slow endpoints (p95 latency)
3. Track error budgets (SLO monitoring)
4. Alert on saturation metrics

Then create a Grafana dashboard JSON for visualization.
```

### ELK Stack Integration

**Prompt**:
```
Create an Elasticsearch query to:
1. Find error rate trends over last 24 hours
2. Group by error type
3. Identify affected users/endpoints
4. Export results for analysis
```

## Performance Monitoring

### APM Analysis

**Prompt**:
```
Review this APM trace data:
[paste trace information]

Identify:
1. Bottlenecks in the request path
2. Slow database queries
3. N+1 query problems
4. External service latency
5. Optimization opportunities
```

### Resource Usage Trends

**Prompt**:
```
Analyze these resource usage trends:

Past 30 days:
- CPU: Gradually increasing from 40% to 75%
- Memory: Stable at 60%
- Disk: Increasing 2GB per day
- Network: Normal

What's happening and what should I do?
```

## Creating Dashboards

### Monitoring Dashboard Design

**Prompt**:
```
Design a comprehensive monitoring dashboard for a microservices architecture with:
- Overview panel (system health)
- Service-level metrics (latency, errors, throughput)
- Infrastructure metrics (CPU, memory, disk)
- Business metrics (users, transactions)
- Alert summary

Suggest tools and implementation approach.
```

### Custom Metrics

**Prompt**:
```
Create CloudWatch custom metrics for:
1. Business KPIs (orders/min, revenue/hour)
2. Application-specific metrics
3. User experience metrics
4. Resource utilization

Include Python code to publish metrics.
```

## Best Practices

### 1. Provide Complete Context

When asking Claude to analyze issues:
- ✅ Include all relevant logs (not just error messages)
- ✅ Provide metrics and trends
- ✅ Include recent changes (deployments, config updates)
- ✅ Specify environment (production, staging)
- ✅ Include system architecture context

### 2. Sanitize Sensitive Data

Before sharing with Claude:
- ❌ Remove API keys, passwords, tokens
- ❌ Mask customer PII (emails, names, IDs)
- ❌ Redact internal IP addresses if sensitive
- ✅ Keep error messages and stack traces
- ✅ Keep timestamps and patterns

### 3. Iterative Analysis

Complex issues require iteration:
```
First: "Analyze these logs for errors"
Then: "Focus on the database timeout errors"
Then: "What queries are causing timeouts?"
Then: "Suggest optimizations for these queries"
```

### 4. Verify Suggestions

Always:
- Test remediation in non-production first
- Validate automated scripts before deployment
- Review generated queries before running
- Confirm understanding of root cause

### 5. Build Knowledge Base

Use Claude to:
- Document recurring issues
- Create runbooks
- Build troubleshooting guides
- Maintain incident history

## SRE and SLO Monitoring

### Defining SLIs/SLOs

**Prompt**:
```
Help me define SLIs and SLOs for an e-commerce API:
- Service: Product catalog API
- Users: Mobile app, website
- Critical user journeys: Browse products, search, view details

Suggest:
1. Appropriate SLIs (latency, availability, etc.)
2. Realistic SLO targets
3. How to measure them
4. Alert thresholds (error budgets)
```

### Error Budget Monitoring

**Prompt**:
```
Create a script to track error budget:
- SLO: 99.9% availability (43 minutes downtime/month)
- Current month: 15 minutes downtime
- Days remaining: 12

Calculate:
1. Remaining error budget
2. Burn rate
3. Predicted month-end status
4. Alert if budget at risk
```

## Advanced Use Cases

### Predictive Analysis

**Prompt**:
```
Analyze these resource trends and predict:
1. When will we hit capacity
2. Do we need to scale
3. Cost implications
4. Recommended actions

Data:
[paste historical metrics]
```

### Security Incident Detection

**Prompt**:
```
Analyze these logs for security incidents:
- Unusual access patterns
- Potential data exfiltration
- Brute force attempts
- Privilege escalation
- Suspicious API calls

[paste logs]
```

### Cost Optimization from Monitoring

**Prompt**:
```
Review our monitoring data and suggest cost optimizations:
- Underutilized resources
- Over-provisioned instances
- Expensive operations
- Resource waste

[paste CloudWatch/Datadog metrics]
```

## Integration Patterns

### 1. Slack Bot for Incident Response

Create a bot that:
- Receives alerts
- Uses Claude to analyze
- Posts analysis and suggestions in Slack
- Allows team to ask follow-up questions

See: `examples/monitoring/integrations/slack-incident-bot/`

### 2. Automated Log Analyzer

Pipeline that:
- Streams logs to S3
- Lambda triggered on new logs
- Sends to Claude for analysis
- Stores insights in DynamoDB
- Alerts on critical issues

See: `examples/monitoring/integrations/log-analyzer-pipeline/`

### 3. Runbook Generator

System that:
- Learns from past incidents
- Generates runbooks using Claude
- Keeps documentation updated
- Suggests improvements

## Resources

- [SRE Book](https://sre.google/books/)
- [AWS CloudWatch Best Practices](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html)
- [Monitoring Examples](../../examples/monitoring/)

## Next Steps

- Explore [Cloud Management](../cloud-management/README.md)
- Review [CI/CD Integration](../ci-cd/README.md)
- Check [practical examples](../../examples/monitoring/)

---

**Ready to improve your monitoring?** Check out the examples in `examples/monitoring/` for working scripts!
