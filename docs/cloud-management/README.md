# Cloud Management with Claude

Learn how to use Claude as an intelligent agent for managing cloud resources across AWS, Azure, and GCP.

## Table of Contents

1. [Introduction](#introduction)
2. [Cloud Platforms](#cloud-platforms)
3. [Common Use Cases](#common-use-cases)
4. [Resource Management](#resource-management)
5. [Cost Optimization](#cost-optimization)
6. [Security and Compliance](#security-and-compliance)
7. [Multi-Cloud Management](#multi-cloud-management)
8. [Best Practices](#best-practices)

## Introduction

Cloud management involves provisioning, configuring, monitoring, and optimizing cloud resources. Claude can help you:

- **Provision resources** using infrastructure as code
- **Optimize costs** by analyzing usage patterns
- **Improve security** through automated audits
- **Manage compliance** with regulatory requirements
- **Automate operations** with intelligent scripts
- **Troubleshoot issues** across cloud services
- **Design architectures** following best practices

## Cloud Platforms

### AWS (Amazon Web Services)

**Strengths**: Comprehensive service catalog, mature ecosystem, global reach

**Claude can help with**:
- EC2, ECS, EKS, Lambda management
- S3, RDS, DynamoDB operations
- VPC networking and security groups
- IAM policy creation and review
- CloudFormation/Terraform templates
- Cost analysis with Cost Explorer
- Security audits with AWS Config

See: `examples/cloud-management/aws/`

### Azure

**Strengths**: Enterprise integration, hybrid cloud, Microsoft ecosystem

**Claude can help with**:
- Virtual Machines, AKS, Functions
- Storage, Cosmos DB, SQL Database
- Virtual Networks and NSGs
- Azure AD and RBAC
- ARM templates and Bicep
- Cost Management analysis
- Security Center recommendations

See: `examples/cloud-management/azure/`

### GCP (Google Cloud Platform)

**Strengths**: Big data, ML/AI services, Kubernetes (GKE)

**Claude can help with**:
- Compute Engine, GKE, Cloud Functions
- Cloud Storage, BigQuery, Cloud SQL
- VPC and firewall rules
- IAM and service accounts
- Deployment Manager templates
- Billing analysis
- Security Command Center

See: `examples/cloud-management/gcp/`

## Common Use Cases

### 1. Resource Provisioning

**Scenario**: Set up a complete application environment.

**Prompt to Claude**:
```
Create AWS resources for a production web application:
- Auto Scaling group with ALB
- RDS PostgreSQL Multi-AZ
- ElastiCache Redis cluster
- S3 bucket for static assets
- CloudFront distribution
- Route53 hosted zone
- All with proper security and monitoring

Provide as Terraform or CloudFormation.
```

### 2. Cost Analysis and Optimization

**Scenario**: Reduce cloud spending.

**Prompt to Claude**:
```
Analyze my AWS Cost and Usage Report:
[paste cost data or summary]

Identify:
1. Top 10 cost drivers
2. Underutilized resources
3. Opportunities for Reserved Instances/Savings Plans
4. Unnecessary data transfer costs
5. Storage optimization (S3 lifecycle, EBS cleanup)
6. Specific action items with estimated savings
```

### 3. Security Audit

**Scenario**: Review cloud security posture.

**Prompt to Claude**:
```
Audit my AWS environment for security issues:

Current setup:
- S3 buckets: [list with configs]
- Security groups: [list with rules]
- IAM policies: [list with details]
- EC2 instances: [list with details]

Check for:
- Publicly accessible resources
- Overly permissive IAM policies
- Unencrypted data
- Missing MFA
- Compliance with CIS AWS Foundations Benchmark
```

### 4. Disaster Recovery Planning

**Scenario**: Design a DR strategy.

**Prompt to Claude**:
```
Design a disaster recovery strategy for:
- Application: E-commerce platform
- Primary region: us-east-1
- RTO: 4 hours
- RPO: 1 hour
- Stack: EC2, RDS, S3, ElastiCache

Provide:
1. DR architecture
2. Backup strategy
3. Failover procedures
4. Cost estimate
5. Terraform/CloudFormation code
```

### 5. Migration Planning

**Scenario**: Migrate from on-premises to cloud.

**Prompt to Claude**:
```
Plan migration of on-premises application to AWS:

Current environment:
- 10 VMs (Windows Server, Linux)
- SQL Server database (500GB)
- File server (2TB)
- Load balancer

Requirements:
- Minimal downtime
- Cost-effective
- Improve resilience

Provide migration strategy and AWS architecture.
```

## Resource Management

### EC2 Instance Management

**Prompt**:
```
Create a Python script using boto3 to:
1. List all EC2 instances
2. Identify stopped instances older than 7 days
3. Find instances without tags
4. Calculate monthly costs per instance
5. Generate CSV report
6. Send email summary
```

See: `examples/cloud-management/aws/ec2-management.py`

### S3 Bucket Operations

**Prompt**:
```
Create a script to manage S3 buckets:
1. Audit all buckets for public access
2. Check encryption settings
3. Verify lifecycle policies
4. Calculate storage costs by bucket
5. Identify old or unused buckets
6. Suggest optimizations
```

### RDS Database Management

**Prompt**:
```
Build an RDS management tool that:
1. Lists all RDS instances
2. Checks backup configurations
3. Identifies Multi-AZ status
4. Analyzes performance metrics
5. Suggests right-sizing based on CloudWatch
6. Estimates cost savings
```

## Cost Optimization

### Compute Optimization

**Prompt**:
```
Analyze my EC2 fleet and suggest optimizations:

Current instances:
[paste instance details with utilization metrics]

Consider:
- Right-sizing (smaller instance types)
- Reserved Instances vs On-Demand
- Spot instances for suitable workloads
- Graviton (ARM) instances
- Scheduled shutdowns for non-prod

Calculate potential monthly savings.
```

### Storage Optimization

**Prompt**:
```
Optimize S3 storage costs:

Current usage:
- Total data: 500TB
- Storage class distribution: [details]
- Access patterns: [details]

Suggest:
1. S3 Intelligent-Tiering opportunities
2. Lifecycle policies for infrequent access
3. Compression opportunities
4. Delete old versions/incomplete uploads
5. Cross-region replication optimization
```

### Database Cost Reduction

**Prompt**:
```
Reduce RDS costs for:
[paste RDS instance details and CloudWatch metrics]

Consider:
- Aurora Serverless v2 for variable workloads
- Reserved Instances
- Right-sizing based on actual usage
- Read replica optimization
- Snapshot retention policies
- Stop databases during non-business hours (dev/test)
```

### Network Cost Optimization

**Prompt**:
```
Reduce AWS data transfer costs:

Current data transfer:
[paste data transfer metrics from Cost Explorer]

Analyze:
- Inter-AZ traffic that could be reduced
- NAT Gateway usage vs VPC endpoints
- CloudFront vs direct S3 access
- Cross-region traffic patterns
- Opportunities for consolidation
```

## Security and Compliance

### IAM Policy Generation

**Prompt**:
```
Create IAM policy for developer access that:
- Allows EC2 read/write in specific VPC
- Allows S3 access to specific buckets only
- Allows RDS describe/modify for tagged databases
- Denies production resource deletion
- Enforces MFA for sensitive operations
- Follows least privilege principle
```

### Security Group Audit

**Prompt**:
```
Audit these security groups for issues:
[paste security group rules]

Check for:
- 0.0.0.0/0 on non-standard ports
- Overly permissive rules
- Unused security groups
- Better organization opportunities
- Missing egress restrictions
```

### Compliance Automation

**Prompt**:
```
Create AWS Config rules to enforce:
- All S3 buckets encrypted
- All EBS volumes encrypted
- No public RDS instances
- CloudTrail enabled
- MFA on root account
- No unused IAM users (90+ days)

Provide as CloudFormation template.
```

### Vulnerability Management

**Prompt**:
```
Create a security scanning pipeline that:
1. Scans EC2 instances for vulnerabilities
2. Checks for missing OS patches
3. Audits installed software
4. Generates compliance report
5. Creates remediation tickets
6. Sends alerts for critical findings
```

## Multi-Cloud Management

### Cross-Cloud Architecture

**Prompt**:
```
Design a multi-cloud architecture:
- Primary: AWS (us-east-1)
- Secondary: Azure (East US)
- Requirements: Active-Active for HA

Services needed:
- Compute (containers)
- Database (PostgreSQL)
- Object storage
- Load balancing
- DNS failover

Provide architecture diagram description and IaC for both clouds.
```

### Cloud Cost Comparison

**Prompt**:
```
Compare costs for this workload across AWS, Azure, and GCP:

Requirements:
- 10 VMs (4 vCPU, 16GB RAM)
- 2TB managed PostgreSQL
- 5TB object storage
- Load balancer
- 1TB/month data transfer

Provide monthly cost estimates with breakdown.
```

### Unified Monitoring

**Prompt**:
```
Design a unified monitoring strategy for:
- AWS resources
- Azure resources
- On-premises servers

Using:
- Open source tools (Prometheus, Grafana)
- Or cloud-native (CloudWatch + Azure Monitor)

Include:
- Metrics collection
- Log aggregation
- Alerting
- Dashboards
```

## Automation Scripts

### AWS Resource Cleanup

**Prompt**:
```
Create a Python script for AWS cleanup:
1. Find unattached EBS volumes (>30 days)
2. Find old snapshots (>90 days)
3. Find unused Elastic IPs
4. Find stopped instances (>14 days)
5. Estimate monthly savings
6. Optionally delete with confirmation
7. Send cleanup report via email
```

See: `examples/cloud-management/aws/resource-cleanup.py`

### Auto-Scaling Based on Custom Metrics

**Prompt**:
```
Create Lambda function that:
1. Monitors custom application metric
2. Calculates scaling decision
3. Updates Auto Scaling group desired capacity
4. Logs actions to CloudWatch
5. Sends notifications for scale events
```

### Backup Automation

**Prompt**:
```
Automate backup strategy:
1. EBS snapshot creation (daily, weekly, monthly)
2. RDS automated backups verification
3. S3 versioning audit
4. Backup retention enforcement
5. Disaster recovery testing
6. Compliance reporting
```

## Best Practices

### 1. Use Tags Consistently

**Prompt to Claude**:
```
Design a tagging strategy for AWS resources:
- Cost allocation by team/project/environment
- Automation tags
- Compliance tags
- Owner/contact information

Provide:
1. Tag schema
2. Enforcement mechanisms (AWS Config, Lambda)
3. Cost allocation report setup
```

### 2. Implement Security in Layers

- Network security (VPC, security groups, NACLs)
- Identity and access (IAM, least privilege)
- Data protection (encryption at rest and in transit)
- Monitoring and logging (CloudTrail, VPC Flow Logs)
- Incident response (automated remediation)

### 3. Design for Resilience

**Prompt**:
```
Review this architecture for resilience:
[paste architecture description]

Check for:
- Single points of failure
- Multi-AZ deployment
- Backup and recovery
- Auto-scaling configuration
- Health checks and monitoring
- Graceful degradation
```

### 4. Optimize for Cost

- Right-size resources based on actual usage
- Use Reserved Instances/Savings Plans for steady workloads
- Leverage Spot instances for fault-tolerant workloads
- Implement auto-scaling
- Use lifecycle policies for data
- Regular cost reviews and optimization

### 5. Automate Everything

**Ask Claude to help**:
```
What manual cloud operations should I automate first?

Current manual tasks:
[list your regular cloud management tasks]

Prioritize by:
- Time saved
- Error reduction
- Cost impact
- Implementation effort
```

## Infrastructure as Code

Combine cloud management with IaC:

**Prompt**:
```
Convert my existing AWS resources to Terraform:
- VPC with current configuration
- EC2 instances with Auto Scaling
- RDS databases
- S3 buckets with policies
- IAM roles and policies

Provide modular Terraform code with best practices.
```

See: [Infrastructure as Code Documentation](../infrastructure/README.md)

## Monitoring and Alerting

**Prompt**:
```
Set up comprehensive monitoring for AWS:
1. CloudWatch dashboards for key metrics
2. Alarms for resource utilization
3. Budget alerts
4. Security finding alerts (GuardDuty, Security Hub)
5. Health check monitoring
6. Cost anomaly detection

Provide as CloudFormation/Terraform.
```

See: [Monitoring Documentation](../monitoring/README.md)

## Real-World Examples

### Startup Environment

**Prompt**:
```
Design a cost-optimized AWS environment for a startup:
- Budget: $500-1000/month
- Traffic: 10,000 users/month
- Stack: Web app + API + database
- Needs: Dev + Production environments

Provide:
- Architecture
- Cost breakdown
- Terraform code
- CI/CD pipeline
```

### Enterprise Migration

**Prompt**:
```
Plan AWS landing zone for enterprise:
- 50+ AWS accounts
- Multiple business units
- Compliance: SOC2, HIPAA
- Hybrid connectivity required

Design:
- AWS Organizations structure
- Networking (Transit Gateway)
- Security (GuardDuty, Security Hub, Config)
- Cost allocation
- Service Catalog
```

## Resources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Azure Cloud Adoption Framework](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/)
- [GCP Architecture Framework](https://cloud.google.com/architecture/framework)
- [Cloud Management Examples](../../examples/cloud-management/)

## Next Steps

- Review [Infrastructure as Code](../infrastructure/README.md)
- Explore [Monitoring & Incident Response](../monitoring/README.md)
- Check [practical examples](../../examples/cloud-management/)

---

**Ready to optimize your cloud?** Check out the examples in `examples/cloud-management/` for working scripts!
