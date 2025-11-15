# Quick Start Guide

Get up and running with Claude as a DevOps Agent in 5 minutes!

## Setup (2 minutes)

```bash
# 1. Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# 2. Install Python SDK
pip install anthropic boto3

# 3. Verify installation
python3 -c "import anthropic; print('Ready to go!')"
```

## Your First Task (3 minutes)

### Option 1: Generate a CI/CD Pipeline

```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": """Create a GitHub Actions workflow for a Python web app that:
        - Runs tests with pytest
        - Lints with flake8
        - Deploys to production on main branch"""
    }]
)

print(message.content[0].text)
```

### Option 2: Analyze Logs

```python
import anthropic
import os

# Your log content
logs = """
2024-01-15 14:30:01 ERROR Database connection timeout
2024-01-15 14:30:02 ERROR Database connection timeout
2024-01-15 14:30:05 WARN Retrying connection
"""

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Analyze these logs and identify issues:\n\n{logs}"
    }]
)

print(message.content[0].text)
```

### Option 3: Create Infrastructure

```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": """Create Terraform configuration for an AWS VPC with:
        - 3 public and 3 private subnets
        - NAT Gateway
        - Proper tags"""
    }]
)

print(message.content[0].text)
```

## Use the Helper Scripts

### Analyze Logs
```bash
cd examples/monitoring/scripts
python log-analyzer.py --log-file /var/log/app.log
```

### Optimize AWS Costs
```bash
cd examples/cloud-management/aws
python cost-optimizer.py --region us-east-1 --output report.txt
```

### Generate CI/CD Pipeline
```bash
cd examples/ci-cd/scripts
./claude-ci-helper.sh "Create a GitHub Actions workflow for Go application"
```

## Common Use Cases Cheat Sheet

### CI/CD
```
Prompt: "Create a [platform] pipeline for [language/framework] that [requirements]"
Examples:
- "Create a GitLab CI pipeline for Node.js that runs tests and deploys to AWS"
- "Create GitHub Actions for Python FastAPI with Docker and ECS deployment"
```

### Infrastructure
```
Prompt: "Create [IaC tool] configuration for [resource] with [requirements]"
Examples:
- "Create Terraform for AWS EKS cluster with managed node groups"
- "Create CloudFormation for serverless API with Lambda and API Gateway"
```

### Troubleshooting
```
Prompt: "I'm getting this error: [error]. Here's my config: [config]. Help me fix it."
Example:
- "Terraform apply failing with 'VPC not found'. Here's my VPC config: ..."
```

### Cost Optimization
```
Prompt: "Analyze my [cloud provider] usage and suggest cost optimizations: [usage data]"
Example:
- "Analyze my AWS bill and suggest savings. Top costs: EC2 $500, RDS $300, S3 $200"
```

### Security
```
Prompt: "Review this [config type] for security issues: [config]"
Example:
- "Review this IAM policy for least privilege: [policy JSON]"
```

## Best Practices Checklist

- ✅ Always review Claude's output before applying
- ✅ Test in dev/staging environments first
- ✅ Never share production secrets with Claude
- ✅ Provide detailed context in prompts
- ✅ Version control all generated code
- ✅ Document the prompts you used
- ✅ Validate security and compliance

## Next Steps

1. **Read the docs**: Start with [Getting Started](docs/getting-started/README.md)
2. **Try examples**: Explore [examples/](examples/) directory
3. **Learn best practices**: Read [BEST_PRACTICES.md](docs/BEST_PRACTICES.md)
4. **Pick a use case**:
   - [CI/CD Automation](docs/ci-cd/README.md)
   - [Infrastructure as Code](docs/infrastructure/README.md)
   - [Monitoring & Incident Response](docs/monitoring/README.md)
   - [Cloud Management](docs/cloud-management/README.md)

## Quick Tips

**Better Prompts = Better Results**
- Be specific about versions, requirements, and constraints
- Include context about your environment
- Ask for explanations along with code
- Iterate and refine based on output

**Safety First**
- Always review generated code
- Test in safe environments
- Use validation tools (terraform validate, etc.)
- Implement proper error handling

**Cost Efficient**
- Batch similar requests
- Cache common responses
- Monitor token usage
- Use appropriate max_tokens

---

**Ready to build?** Pick an example from the `examples/` directory and start experimenting!
