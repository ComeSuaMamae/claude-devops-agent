# Getting Started with Claude as a DevOps Agent

Welcome! This guide will help you start using Claude as an intelligent DevOps agent for automation, troubleshooting, and optimization.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Your First Automation](#your-first-automation)
4. [Best Practices](#best-practices)
5. [Common Workflows](#common-workflows)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

## Prerequisites

### Required

- **Claude API Access**: Get your API key from [Anthropic Console](https://console.anthropic.com/)
- **Basic DevOps Knowledge**: Understanding of cloud platforms, CI/CD, and infrastructure
- **Command Line Familiarity**: Comfortable using terminal/bash

### Recommended

- Cloud Platform Account (AWS, Azure, or GCP)
- Git and version control knowledge
- Basic scripting skills (Python, Bash, or similar)
- Familiarity with at least one IaC tool (Terraform, CloudFormation, etc.)

## Setup

### 1. Get Your API Key

1. Sign up at [Anthropic Console](https://console.anthropic.com/)
2. Navigate to API Keys section
3. Create a new API key
4. Save it securely (you'll need it in the next step)

### 2. Configure Environment

```bash
# Set your API key as an environment variable
export ANTHROPIC_API_KEY="your-api-key-here"

# Add to your shell profile for persistence
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or ~/.zshrc
```

### 3. Install Required Tools

```bash
# Install Python (if not already installed)
# macOS
brew install python3

# Linux (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install python3 python3-pip

# Install Anthropic Python SDK
pip install anthropic

# Optional: Install AWS CLI (for cloud management examples)
pip install awscli boto3

# Optional: Install Terraform (for IaC examples)
brew install terraform  # macOS
# or download from https://www.terraform.io/downloads
```

### 4. Verify Setup

```bash
# Test Python and Anthropic SDK
python3 -c "import anthropic; print('Anthropic SDK installed successfully')"

# Test API key is set
echo $ANTHROPIC_API_KEY

# Test basic Claude interaction (optional)
python3 << EOF
import anthropic
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(message.content[0].text)
EOF
```

## Your First Automation

Let's create a simple script that uses Claude to analyze system logs.

### Step 1: Create the Script

```python
# save as: test_claude.py
import anthropic
import os

def analyze_log(log_content):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Analyze this log and identify any issues:\n\n{log_content}"
        }]
    )

    return message.content[0].text

# Test with sample log
sample_log = """
2024-01-15 14:30:00 INFO Starting application
2024-01-15 14:30:01 ERROR Database connection failed: Connection timeout
2024-01-15 14:30:02 ERROR Database connection failed: Connection timeout
2024-01-15 14:30:05 ERROR Database connection failed: Connection timeout
2024-01-15 14:30:10 WARN Retrying database connection
2024-01-15 14:30:11 INFO Database connection established
"""

print("Analyzing logs with Claude...")
analysis = analyze_log(sample_log)
print("\nAnalysis:")
print(analysis)
```

### Step 2: Run It

```bash
python3 test_claude.py
```

### Step 3: Review Output

Claude will analyze the logs and provide insights like:
- Identifying the database connection timeout issues
- Suggesting the retry mechanism worked
- Recommending investigation of network or database configuration

## Best Practices

### 1. Start Simple

Begin with straightforward tasks:
- ✅ Generate basic CI/CD configurations
- ✅ Analyze individual log files
- ✅ Create simple infrastructure templates

Avoid initially:
- ❌ Complex multi-cloud architectures
- ❌ Production-critical automation
- ❌ Large-scale system redesigns

### 2. Provide Context

Claude works best with complete information:

**Good Prompt**:
```
Create a GitHub Actions workflow for a Node.js application that:
- Runs on Node.js 18 and 20
- Includes linting (ESLint) and testing (Jest)
- Deploys to AWS S3 on merge to main
- Uses caching for faster builds
- Environment: Production web application
```

**Poor Prompt**:
```
Create a CI/CD pipeline
```

### 3. Iterate and Refine

Break complex tasks into steps:

```
Step 1: "Create basic VPC with public subnets"
Review output...

Step 2: "Add private subnets and NAT gateway to the VPC"
Review output...

Step 3: "Add VPC endpoints for S3 and DynamoDB"
Review output...
```

### 4. Always Review and Test

**Critical**: Never apply Claude's suggestions directly to production without:
- ✅ Reviewing the code/configuration
- ✅ Testing in a dev/staging environment
- ✅ Understanding what it does
- ✅ Validating security implications
- ✅ Checking for compliance requirements

### 5. Version Control Everything

```bash
# Initialize git repository
git init

# Save all Claude-generated code
git add .
git commit -m "Add CI/CD pipeline generated with Claude"

# Document your prompts
echo "Prompt: Create GitHub Actions workflow for Node.js app..." > .prompts/pipeline.md
```

## Common Workflows

### Workflow 1: Generate CI/CD Pipeline

```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

prompt = """
Create a complete GitHub Actions workflow for a Python FastAPI application that:
1. Runs tests with pytest
2. Checks code quality with black and flake8
3. Builds Docker image
4. Pushes to Docker Hub
5. Deploys to AWS ECS on main branch
"""

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}]
)

# Save to file
with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(message.content[0].text)

print("Pipeline created! Review .github/workflows/deploy.yml")
```

### Workflow 2: Analyze Infrastructure

```python
import anthropic
import os

# Read your existing Terraform configuration
with open('main.tf', 'r') as f:
    terraform_code = f.read()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

prompt = f"""
Review this Terraform configuration for:
1. Security best practices
2. Cost optimization opportunities
3. High availability concerns
4. Missing error handling

Configuration:
{terraform_code}
"""

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}]
)

print(message.content[0].text)
```

### Workflow 3: Troubleshoot Issues

```python
import anthropic
import os
import subprocess

# Capture error output
result = subprocess.run(
    ['terraform', 'apply'],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    error_output = result.stderr

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""
    I'm getting this error when running terraform apply:

    {error_output}

    Help me:
    1. Understand what's wrong
    2. Provide specific fix
    3. Explain how to prevent this in the future
    """

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    print("Error Analysis:")
    print(message.content[0].text)
```

## Troubleshooting

### Issue: API Key Not Found

**Error**: `Error: ANTHROPIC_API_KEY environment variable not set`

**Solution**:
```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# If not set, add it
export ANTHROPIC_API_KEY="your-key-here"

# Make it permanent
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: Rate Limits

**Error**: `Rate limit exceeded`

**Solution**:
- Space out your requests
- Implement retry logic with exponential backoff
- Consider batching similar requests
- Upgrade your API plan if needed

### Issue: Response Too Large

**Error**: Output is truncated or incomplete

**Solution**:
- Increase `max_tokens` in your API call
- Break complex prompts into smaller pieces
- Ask for summaries instead of complete details

### Issue: Claude Provides Incorrect Code

**Cause**: Insufficient context or outdated information

**Solution**:
- Provide more context (versions, environment, constraints)
- Specify the exact tool versions you're using
- Review and test all generated code
- Iterate with more specific prompts

## Next Steps

### Learn More

1. **CI/CD Automation**
   - Read: [CI/CD Documentation](../ci-cd/README.md)
   - Try: Generate a pipeline for your project
   - Examples: `examples/ci-cd/`

2. **Infrastructure as Code**
   - Read: [Infrastructure Documentation](../infrastructure/README.md)
   - Try: Create a VPC with Terraform
   - Examples: `examples/infrastructure/`

3. **Monitoring & Incident Response**
   - Read: [Monitoring Documentation](../monitoring/README.md)
   - Try: Analyze your application logs
   - Examples: `examples/monitoring/`

4. **Cloud Management**
   - Read: [Cloud Management Documentation](../cloud-management/README.md)
   - Try: Optimize your cloud costs
   - Examples: `examples/cloud-management/`

### Practice Projects

Start with these beginner-friendly projects:

1. **Simple Pipeline**: Create a GitHub Actions workflow for a personal project
2. **Log Analyzer**: Use Claude to analyze your application logs
3. **Cost Review**: Analyze your AWS bill and identify savings
4. **Documentation**: Generate runbooks for your services
5. **IaC Review**: Have Claude review your Terraform code

### Join the Community

- Share your experiences and learn from others
- Contribute examples to this repository
- Report issues and suggest improvements

## Tips for Success

1. **Be Specific**: More detailed prompts = better results
2. **Iterate**: Don't expect perfect output on the first try
3. **Learn**: Understand what Claude generates, don't just copy-paste
4. **Test**: Always test in safe environments first
5. **Document**: Save your successful prompts for reuse
6. **Security**: Never share production secrets with Claude
7. **Review**: Always human-review automated changes

## Resources

- [Anthropic Documentation](https://docs.anthropic.com/)
- [API Reference](https://docs.anthropic.com/claude/reference/getting-started)
- [Best Practices](https://docs.anthropic.com/claude/docs/best-practices)
- [Project Examples](../../examples/)

---

**Ready to dive deeper?** Choose a use case from the docs and start building!

**Questions?** Review the specific documentation for each area:
- [CI/CD](../ci-cd/README.md)
- [Infrastructure](../infrastructure/README.md)
- [Monitoring](../monitoring/README.md)
- [Cloud Management](../cloud-management/README.md)
