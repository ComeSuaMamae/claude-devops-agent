# Infrastructure as Code with Claude

Learn how to leverage Claude to write, review, and manage Infrastructure as Code (IaC) across different platforms and tools.

## Table of Contents

1. [Introduction](#introduction)
2. [Supported IaC Tools](#supported-iac-tools)
3. [Common Use Cases](#common-use-cases)
4. [Getting Started](#getting-started)
5. [Best Practices](#best-practices)
6. [Examples](#examples)

## Introduction

Infrastructure as Code (IaC) is essential for modern DevOps, but it can be complex and error-prone. Claude can help you:

- **Generate IaC configurations** from requirements
- **Review code** for security vulnerabilities and best practices
- **Migrate** between different IaC tools (e.g., CloudFormation to Terraform)
- **Debug** configuration errors
- **Optimize** resource definitions for cost and performance
- **Document** infrastructure setup

## Supported IaC Tools

### Terraform
- **Strength**: Multi-cloud support, large ecosystem
- **Claude can help with**: Module creation, provider configuration, state management
- See: `examples/infrastructure/terraform/`

### AWS CloudFormation
- **Strength**: Deep AWS integration, native support
- **Claude can help with**: Template generation, nested stacks, parameter optimization
- See: `examples/infrastructure/cloudformation/`

### Pulumi
- **Strength**: Use real programming languages (Python, TypeScript, Go)
- **Claude can help with**: Infrastructure programs, testing, component design
- See: `examples/infrastructure/pulumi/`

### Ansible
- **Strength**: Configuration management and orchestration
- **Claude can help with**: Playbook creation, role design, inventory management
- See: `examples/infrastructure/ansible/`

### AWS CDK
- **Strength**: AWS infrastructure with TypeScript/Python
- **Claude can help with**: Construct creation, stack design, testing
- See: `examples/infrastructure/cdk/`

## Common Use Cases

### 1. Generate Infrastructure from Requirements

**Scenario**: You need to set up a 3-tier web application on AWS.

**Prompt to Claude**:
```
Create Terraform configuration for a 3-tier web application on AWS with:
- VPC with public and private subnets across 2 AZs
- Application Load Balancer in public subnets
- ECS Fargate for application tier
- RDS PostgreSQL in private subnets with Multi-AZ
- ElastiCache Redis for session storage
- S3 bucket for static assets
- CloudFront distribution
- Security groups with least privilege
- All resources should have appropriate tags
```

### 2. Review and Improve Existing IaC

**Prompt to Claude**:
```
Review this Terraform configuration for:
1. Security best practices
2. Cost optimization opportunities
3. High availability concerns
4. Missing error handling
5. Code organization improvements

[paste your Terraform code]
```

### 3. Migrate Between IaC Tools

**Prompt to Claude**:
```
Convert this CloudFormation template to Terraform:
[paste CloudFormation YAML]

Maintain the same functionality and resource dependencies.
```

### 4. Debug Configuration Errors

**Prompt to Claude**:
```
I'm getting this error when applying my Terraform configuration:
Error: [error message]

Here's my configuration:
[paste relevant code]

Help me understand what's wrong and how to fix it.
```

### 5. Implement Best Practices

**Prompt to Claude**:
```
Refactor this Terraform code to follow best practices:
- Use modules for reusability
- Implement proper variable validation
- Add comprehensive outputs
- Include lifecycle rules
- Setup remote state with locking

[paste code]
```

## Getting Started

### Prerequisites

```bash
# Install Terraform
brew install terraform

# Or install AWS CDK
npm install -g aws-cdk

# Or install Pulumi
brew install pulumi
```

### Basic Workflow with Claude

1. **Define Requirements**
   - Be specific about cloud provider, regions, resources needed
   - Include compliance requirements (HIPAA, PCI-DSS, etc.)
   - Specify environment (dev, staging, production)

2. **Generate Initial Configuration**
   - Provide detailed prompt to Claude
   - Review generated code
   - Ask for explanations of unfamiliar concepts

3. **Iterate and Refine**
   - Request modifications (e.g., "add monitoring", "increase redundancy")
   - Ask for cost optimization
   - Request security improvements

4. **Validate and Test**
   - Use `terraform plan` or equivalent
   - Ask Claude to review plan output
   - Test in non-production environment first

5. **Apply and Monitor**
   - Apply changes with appropriate safeguards
   - Set up monitoring and alerts
   - Document what was deployed

## Terraform Examples

### Creating a Complete AWS Environment

**Prompt**:
```
Create a production-ready Terraform module for an AWS environment with:
- VPC with CIDR 10.0.0.0/16
- 3 public subnets and 3 private subnets across 3 AZs
- NAT Gateways for private subnet internet access
- VPC Flow Logs to CloudWatch
- S3 VPC endpoint
- Proper tags for cost allocation
```

**Result**: See `examples/infrastructure/terraform/aws-vpc-module/`

### Kubernetes Cluster on AWS (EKS)

**Prompt**:
```
Generate Terraform configuration for AWS EKS cluster with:
- EKS 1.28
- 2 node groups (spot and on-demand)
- IRSA (IAM Roles for Service Accounts)
- EBS CSI driver
- Cluster autoscaler
- Managed node groups with proper security
```

**Result**: See `examples/infrastructure/terraform/eks-cluster/`

## CloudFormation Examples

### Serverless Application

**Prompt**:
```
Create CloudFormation template for serverless API:
- API Gateway REST API
- Lambda functions (NodeJS 20.x)
- DynamoDB table with GSI
- Cognito User Pool for authentication
- CloudWatch Logs with retention
- X-Ray tracing enabled
```

**Result**: See `examples/infrastructure/cloudformation/serverless-api.yaml`

## Security Best Practices

### 1. Use Claude to Review Security

**Prompt**:
```
Review this infrastructure code for security issues:
- Check for publicly accessible resources
- Verify encryption at rest and in transit
- Validate IAM permissions (least privilege)
- Check for hardcoded secrets
- Verify network segmentation

[paste code]
```

### 2. Implement Security Hardening

**Prompt**:
```
Harden this Terraform configuration:
- Enable all encryption options
- Implement VPC endpoints for AWS services
- Add WAF rules for Application Load Balancer
- Enable GuardDuty and Security Hub
- Setup AWS Config rules
- Implement backup strategies
```

### 3. Compliance Requirements

**Prompt**:
```
Modify this infrastructure to meet HIPAA compliance:
- Ensure encryption at rest and in transit
- Enable comprehensive audit logging
- Implement proper access controls
- Add backup and disaster recovery
- Document security controls

[paste current configuration]
```

## Cost Optimization

### Ask Claude to Optimize Costs

**Prompt**:
```
Analyze this infrastructure for cost optimization:
- Identify overprovisioned resources
- Suggest reserved instances or savings plans
- Recommend S3 lifecycle policies
- Find unused resources
- Suggest cheaper alternatives where appropriate

[paste Terraform/CloudFormation code]
```

## Advanced Techniques

### Multi-Environment Setup

**Prompt**:
```
Create a Terraform workspace structure for:
- Shared modules (VPC, ECS, RDS)
- Environment-specific configurations (dev, staging, prod)
- Different variable files per environment
- Remote state per environment
- Consistent naming conventions
```

### GitOps Workflow

**Prompt**:
```
Design a GitOps workflow for infrastructure using:
- Terraform Cloud or Atlantis
- GitHub for version control
- Automated plan on PR
- Protected main branch requiring approvals
- Automated apply on merge
- Drift detection
```

### Testing Infrastructure Code

**Prompt**:
```
Create tests for this Terraform module using Terratest:
[paste module code]

Include:
- Unit tests for variable validation
- Integration tests that deploy real resources
- Cleanup after tests
- Proper Go test structure
```

## Troubleshooting Common Issues

### State File Issues

**Problem**: Terraform state is locked or corrupted

**Prompt to Claude**:
```
I'm having Terraform state issues:
[describe the problem and error messages]

Current backend configuration:
[paste backend config]

How can I safely resolve this?
```

### Dependency Cycles

**Problem**: Circular dependencies in resources

**Prompt to Claude**:
```
I'm getting a cycle error in my Terraform configuration:
Error: Cycle: [cycle details]

Here's the relevant code:
[paste code]

How do I break this cycle while maintaining functionality?
```

### Provider Version Conflicts

**Problem**: Module version incompatibilities

**Prompt to Claude**:
```
I have version conflicts between modules:
[paste error]

Current version constraints:
[paste versions]

Help me resolve these conflicts.
```

## Integration with CI/CD

Combine IaC with CI/CD pipelines:

1. **Automated Plan on PR**
   ```
   Create a GitHub Actions workflow that:
   - Runs terraform plan on pull requests
   - Comments plan output on the PR
   - Validates formatting and security
   - Requires approval before apply
   ```

2. **Automated Apply on Merge**
   ```
   Create a pipeline that:
   - Runs terraform apply on merge to main
   - Notifies team of changes
   - Rolls back on failure
   - Updates documentation
   ```

See: [CI/CD Documentation](../ci-cd/README.md)

## Module Design Patterns

### Reusable Modules

**Prompt**:
```
Create a reusable Terraform module for RDS database with:
- Support for multiple engines (postgres, mysql, aurora)
- Optional read replicas
- Automated backups
- Parameter group customization
- Security group management
- Comprehensive outputs
- Input validation
```

### Composite Modules

**Prompt**:
```
Create a composite module that combines:
- VPC module
- ECS cluster module
- RDS module
- ALB module

Into a complete application stack with proper dependencies.
```

## Documentation Generation

Use Claude to document your infrastructure:

**Prompt**:
```
Generate comprehensive documentation for this Terraform module:
[paste module code]

Include:
- Overview and purpose
- Architecture diagram description
- Input variables table
- Output values table
- Usage examples
- Prerequisites
- Cost estimates
```

## Best Practices Checklist

When using Claude for IaC:

- ✅ Always review generated code before applying
- ✅ Test in non-production environment first
- ✅ Use version control for all IaC
- ✅ Implement remote state with locking
- ✅ Use modules for reusability
- ✅ Tag all resources consistently
- ✅ Implement proper IAM roles and policies
- ✅ Enable encryption by default
- ✅ Setup monitoring and alerting
- ✅ Document infrastructure decisions
- ✅ Regular security reviews
- ✅ Cost monitoring and optimization

## Resources

- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Infrastructure as Code Examples](../../examples/infrastructure/)

## Next Steps

- Explore [Monitoring & Incident Response](../monitoring/README.md)
- Learn about [Cloud Management](../cloud-management/README.md)
- Check [practical examples](../../examples/infrastructure/)

---

**Ready to start?** Check out the examples in `examples/infrastructure/` for working code!
