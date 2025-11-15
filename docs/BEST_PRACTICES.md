# Best Practices for Using Claude as a DevOps Agent

This comprehensive guide covers best practices, patterns, and anti-patterns when using Claude for DevOps automation.

## Table of Contents

1. [Security Best Practices](#security-best-practices)
2. [Prompt Engineering](#prompt-engineering)
3. [Code Review and Validation](#code-review-and-validation)
4. [Cost Optimization](#cost-optimization)
5. [Error Handling](#error-handling)
6. [Team Collaboration](#team-collaboration)
7. [Documentation](#documentation)
8. [Testing](#testing)
9. [Common Pitfalls](#common-pitfalls)
10. [Advanced Patterns](#advanced-patterns)

## Security Best Practices

### 1. Never Share Secrets

**DON'T**:
```python
# ❌ NEVER DO THIS
prompt = f"""
Deploy to AWS using these credentials:
AWS_ACCESS_KEY_ID: AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
"""
```

**DO**:
```python
# ✅ USE PLACEHOLDERS
prompt = """
Deploy to AWS using credentials from environment variables:
- Use $AWS_ACCESS_KEY_ID from environment
- Use $AWS_SECRET_ACCESS_KEY from environment
"""

# Or reference secrets management
prompt = """
Deploy to AWS using credentials from AWS Secrets Manager:
- Secret name: prod/app/aws-credentials
"""
```

### 2. Sanitize Logs and Data

**Before sharing logs with Claude**:

```python
import re

def sanitize_log(log_content):
    """Remove sensitive data from logs"""
    # Remove email addresses
    log_content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', log_content)

    # Remove IP addresses (if sensitive)
    log_content = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', log_content)

    # Remove API keys
    log_content = re.sub(r'api[_-]?key["\']?\s*[:=]\s*["\']?[\w-]+', 'api_key=[REDACTED]', log_content, flags=re.IGNORECASE)

    # Remove tokens
    log_content = re.sub(r'token["\']?\s*[:=]\s*["\']?[\w.-]+', 'token=[REDACTED]', log_content, flags=re.IGNORECASE)

    return log_content

# Use before sending to Claude
sanitized_logs = sanitize_log(raw_logs)
```

### 3. Review Generated IAM Policies

**Always verify**:
- Principle of least privilege
- No wildcards on sensitive actions
- Proper resource restrictions
- Condition statements where appropriate

```python
# ✅ Good practice: Review before applying
iam_policy = get_policy_from_claude()
print("Review this policy before applying:")
print(json.dumps(iam_policy, indent=2))
response = input("Apply this policy? (yes/no): ")
if response.lower() == 'yes':
    apply_policy(iam_policy)
```

### 4. Secure API Key Storage

```bash
# ✅ Use environment variables
export ANTHROPIC_API_KEY="your-key"

# ✅ Or use a secrets manager
aws secretsmanager get-secret-value --secret-id anthropic-api-key

# ✅ Or use a .env file (add to .gitignore!)
echo "ANTHROPIC_API_KEY=your-key" > .env
echo ".env" >> .gitignore
```

### 5. Audit Trail

Keep records of what Claude generates:

```python
import json
from datetime import datetime

def log_claude_interaction(prompt, response, metadata=None):
    """Log all Claude interactions for audit"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'prompt': prompt,
        'response': response,
        'metadata': metadata or {}
    }

    with open('claude_audit.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
```

## Prompt Engineering

### 1. Be Specific and Detailed

**Poor Prompt**:
```
Create a CI/CD pipeline
```

**Good Prompt**:
```
Create a GitHub Actions workflow for a Python FastAPI application that:
- Runs on Python 3.11
- Executes pytest with coverage
- Performs linting with black and flake8
- Builds a Docker image
- Pushes to AWS ECR
- Deploys to ECS Fargate on main branch
- Includes security scanning with Snyk
- Sends Slack notifications on failure
- Uses secrets from GitHub Secrets
```

### 2. Provide Context

**Include**:
- Current environment (dev, staging, prod)
- Constraints (budget, compliance, performance)
- Existing architecture
- Team preferences
- Tool versions

```python
prompt = f"""
Context:
- Environment: Production
- Cloud: AWS (us-east-1)
- Compliance: HIPAA required
- Budget: $5000/month
- Team size: 5 developers
- Existing tools: Terraform, GitHub Actions, DataDog

Task:
Create infrastructure for a healthcare application...
"""
```

### 3. Ask for Explanations

```python
prompt = """
Create a Terraform module for AWS VPC.

Include:
1. The actual code
2. Explanation of each resource
3. Why these choices were made
4. Alternative approaches
5. Trade-offs to consider
"""
```

### 4. Iterate and Refine

**First Pass**:
```
Create a basic Kubernetes deployment for a web app
```

**Review, then refine**:
```
Based on the previous deployment, add:
- Horizontal Pod Autoscaling
- Readiness and liveness probes
- Resource limits and requests
- PodDisruptionBudget
- Network policies
```

### 5. Use Examples

```python
prompt = """
Create a CloudWatch alarm similar to this example:

Example:
{
  "AlarmName": "HighCPU",
  "MetricName": "CPUUtilization",
  "Threshold": 80
}

But for:
- Database connection pool exhaustion
- Threshold: 85% of max connections
- Evaluation periods: 2
- Actions: SNS notification
"""
```

## Code Review and Validation

### 1. Always Review Generated Code

**Review Checklist**:
- [ ] Syntax is correct
- [ ] Logic makes sense
- [ ] Security best practices followed
- [ ] No hardcoded values
- [ ] Error handling included
- [ ] Documentation present
- [ ] Tests included (if applicable)
- [ ] Follows team standards

### 2. Test in Non-Production First

```bash
# ✅ Development environment
terraform workspace select dev
terraform apply

# Verify it works
# Run tests
# Check logs

# ✅ Staging environment
terraform workspace select staging
terraform apply

# Full integration tests
# Performance tests

# ✅ Only then: Production
terraform workspace select prod
terraform apply
```

### 3. Use Validation Tools

```bash
# Terraform
terraform fmt
terraform validate
terraform plan
tflint

# CloudFormation
aws cloudformation validate-template --template-body file://template.yml
cfn-lint template.yml

# Python
black .
flake8 .
mypy .
pytest

# Shell scripts
shellcheck script.sh
```

### 4. Peer Review

Even for Claude-generated code:

```bash
# Create PR for review
git checkout -b claude-generated-pipeline
git add .github/workflows/deploy.yml
git commit -m "Add deployment pipeline (Claude-generated)"
git push origin claude-generated-pipeline

# Create PR and request reviews
gh pr create --title "Add deployment pipeline" \
  --body "Generated with Claude. Please review for security and best practices."
```

### 5. Automated Validation

```yaml
# .github/workflows/validate-claude-code.yml
name: Validate Generated Code

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Terraform Validate
        run: |
          terraform init
          terraform validate

      - name: Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: '.'

      - name: Cost Estimate
        uses: infracost/actions/setup@v2
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}
```

## Cost Optimization

### 1. Monitor API Usage

```python
import anthropic
from datetime import datetime

class CostTrackingClient:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.total_tokens = 0

    def create_message(self, **kwargs):
        message = self.client.messages.create(**kwargs)

        # Track tokens
        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        self.total_tokens += input_tokens + output_tokens

        # Estimate cost (example rates)
        input_cost = input_tokens * 0.003 / 1000  # $3 per MTok
        output_cost = output_tokens * 0.015 / 1000  # $15 per MTok
        total_cost = input_cost + output_cost

        print(f"Cost for this request: ${total_cost:.4f}")
        print(f"Total tokens so far: {self.total_tokens}")

        return message
```

### 2. Batch Similar Requests

**Instead of**:
```python
# ❌ Multiple separate requests
for log_file in log_files:
    analysis = analyze_log(log_file)
```

**Do**:
```python
# ✅ Batch them
combined_logs = "\n\n---\n\n".join([f"File: {f}\n{content}" for f, content in log_files.items()])
analysis = analyze_logs(combined_logs)
```

### 3. Use Caching

```python
import functools
import hashlib
import json

@functools.lru_cache(maxsize=100)
def get_cached_response(prompt_hash):
    """Cache responses for identical prompts"""
    # Implementation here
    pass

def analyze_with_cache(prompt):
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()

    # Check cache
    cached = get_cached_response(prompt_hash)
    if cached:
        return cached

    # If not cached, call Claude
    response = call_claude(prompt)
    get_cached_response.cache_clear()
    return response
```

### 4. Right-Size Token Limits

```python
# ✅ Adjust max_tokens based on expected output
simple_task = client.messages.create(
    max_tokens=500,  # Short responses
    messages=[...]
)

complex_task = client.messages.create(
    max_tokens=4096,  # Longer responses
    messages=[...]
)
```

## Error Handling

### 1. Implement Retry Logic

```python
import time
from anthropic import APIError, RateLimitError

def call_claude_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text

        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

        except APIError as e:
            print(f"API Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise
```

### 2. Validate Responses

```python
def validate_terraform_code(code):
    """Validate generated Terraform code"""
    # Check for required elements
    required = ['resource', 'provider']
    if not all(keyword in code for keyword in required):
        raise ValueError("Generated code missing required Terraform elements")

    # Check for dangerous patterns
    dangerous = ['rm -rf /', 'delete all', 'destroy']
    if any(pattern in code.lower() for pattern in dangerous):
        raise ValueError("Generated code contains dangerous operations")

    # Syntax check (basic)
    if code.count('{') != code.count('}'):
        raise ValueError("Unbalanced braces in generated code")

    return True

# Use it
terraform_code = get_code_from_claude(prompt)
if validate_terraform_code(terraform_code):
    apply_code(terraform_code)
```

### 3. Graceful Degradation

```python
def analyze_logs(logs):
    """Analyze logs with Claude, fallback to basic analysis"""
    try:
        # Try Claude first
        return claude_analysis(logs)
    except Exception as e:
        print(f"Claude analysis failed: {e}")
        print("Falling back to basic analysis...")
        # Fallback to simple pattern matching
        return basic_log_analysis(logs)
```

## Team Collaboration

### 1. Document Claude Usage

```python
"""
This script was generated with Claude AI assistance.

Prompt used:
"Create a Python script to analyze AWS CloudWatch logs and
identify error patterns"

Generated: 2024-01-15
Reviewed by: John Doe
Last modified: 2024-01-20
Modifications: Added retry logic and error handling
"""
```

### 2. Share Successful Prompts

Create a team knowledge base:

```
prompts/
├── ci-cd/
│   ├── github-actions-python.md
│   ├── gitlab-ci-nodejs.md
│   └── jenkins-java.md
├── infrastructure/
│   ├── aws-vpc-terraform.md
│   ├── azure-vnet-arm.md
│   └── gcp-network.md
└── monitoring/
    ├── cloudwatch-alarms.md
    └── datadog-dashboards.md
```

### 3. Code Review Process

```markdown
## PR Template for Claude-Generated Code

### Claude Assistance Details
- [ ] Prompt used is documented
- [ ] Response was reviewed before committing
- [ ] Code tested in development environment
- [ ] Security reviewed
- [ ] Follows team coding standards

### Testing
- [ ] Unit tests added/passing
- [ ] Integration tests passing
- [ ] Manual testing completed

### Documentation
- [ ] README updated
- [ ] Comments added for complex logic
- [ ] Runbook updated (if applicable)
```

## Documentation

### 1. Self-Documenting Code

Ask Claude to include documentation:

```python
prompt = """
Create a Python function to backup RDS snapshots.

Requirements:
- Comprehensive docstrings
- Type hints
- Inline comments for complex logic
- Usage examples
- Error handling documentation
"""
```

### 2. Generate README Files

```python
prompt = f"""
Create a comprehensive README for this project:

Project: {project_name}
Description: {description}
Tech stack: {stack}

Include:
- Project overview
- Prerequisites
- Installation steps
- Configuration
- Usage examples
- Troubleshooting
- Contributing guidelines
- License information
"""
```

### 3. Create Runbooks

```python
prompt = """
Create an incident response runbook for database connection pool exhaustion:

Include:
- Symptoms and detection
- Immediate mitigation steps (step-by-step)
- Diagnostic commands
- Root cause analysis procedure
- Long-term prevention measures
- Rollback procedures
- Post-incident tasks
- Communication templates
"""
```

## Testing

### 1. Ask for Tests

```python
prompt = """
Create a Python function to calculate AWS cost savings.

Include:
- The function implementation
- Unit tests using pytest
- Test cases for edge cases
- Mocking for AWS API calls
- Test fixtures
- Coverage should be >90%
"""
```

### 2. Test Generated Infrastructure

```bash
# Use Terratest for Terraform
prompt = """
For this Terraform VPC module, create Terratest tests that:
1. Verify VPC is created
2. Check subnet configuration
3. Validate security groups
4. Ensure tags are applied
5. Test in actual AWS (with cleanup)
"""
```

### 3. Validate in Stages

```python
# Stage 1: Syntax validation
terraform validate

# Stage 2: Plan review
terraform plan -out=plan.tfplan

# Ask Claude to review the plan
prompt = f"""
Review this Terraform plan for issues:
{plan_output}

Check for:
- Unexpected resource creation/deletion
- Security concerns
- Cost implications
"""

# Stage 3: Apply in dev
terraform apply plan.tfplan

# Stage 4: Automated tests
pytest tests/

# Stage 5: Manual verification
```

## Common Pitfalls

### 1. Over-Reliance on Claude

**Problem**: Blindly trusting all Claude output

**Solution**: Always review, understand, and validate

### 2. Insufficient Context

**Problem**: Vague prompts lead to generic solutions

**Solution**: Provide detailed requirements and constraints

### 3. Ignoring Updates

**Problem**: Cloud providers update services frequently

**Solution**: Verify generated code against current documentation

```python
prompt = """
Create an AWS Lambda function using Python 3.11 (latest available runtime as of 2024)

Check: What's the current latest Python runtime for AWS Lambda?
Then use that version.
"""
```

### 4. Not Testing Failure Scenarios

**Problem**: Only testing happy paths

**Solution**: Ask Claude to help with failure testing

```python
prompt = """
Create tests for this deployment script including:
- Network failures
- Authentication errors
- Resource limits
- Partial failures
- Rollback scenarios
"""
```

### 5. Mixing Environments

**Problem**: Testing in prod, or applying prod config to dev

**Solution**: Use workspaces and environment validation

```bash
# Add environment validation
if [ "$ENVIRONMENT" != "dev" ]; then
    echo "This script is for dev only!"
    exit 1
fi
```

## Advanced Patterns

### 1. Multi-Step Automation

```python
def complex_deployment_workflow():
    """Multi-step deployment using Claude for each phase"""

    # Phase 1: Generate infrastructure
    print("Phase 1: Generating infrastructure...")
    infra_code = claude_generate_infrastructure(requirements)
    validate_and_apply(infra_code)

    # Phase 2: Generate deployment pipeline
    print("Phase 2: Creating CI/CD pipeline...")
    pipeline = claude_generate_pipeline(app_details)
    validate_and_commit(pipeline)

    # Phase 3: Generate monitoring
    print("Phase 3: Setting up monitoring...")
    monitoring = claude_generate_monitoring(services)
    validate_and_apply(monitoring)

    # Phase 4: Generate documentation
    print("Phase 4: Creating documentation...")
    docs = claude_generate_docs(project_info)
    save_documentation(docs)
```

### 2. Feedback Loop

```python
def iterative_improvement(initial_code, requirements):
    """Use Claude to iteratively improve code"""

    current_code = initial_code

    for iteration in range(3):
        # Run tests
        test_results = run_tests(current_code)

        if test_results.success:
            return current_code

        # Ask Claude to fix failures
        prompt = f"""
        This code is failing tests:

        Code:
        {current_code}

        Test failures:
        {test_results.failures}

        Fix the code to pass all tests.
        """

        current_code = get_improved_code_from_claude(prompt)

    return current_code
```

### 3. Learning from Production

```python
def learn_from_incidents():
    """Use Claude to improve based on incidents"""

    # Get recent incidents
    incidents = get_incidents(days=30)

    for incident in incidents:
        prompt = f"""
        We had this incident:
        {incident.description}

        Root cause: {incident.root_cause}

        Current monitoring:
        {current_monitoring_config}

        Suggest:
        1. Additional monitoring to detect this earlier
        2. Automated remediation steps
        3. Prevention measures
        """

        improvements = get_suggestions_from_claude(prompt)
        review_and_implement(improvements)
```

## Summary

**Key Takeaways**:

1. **Security**: Never share secrets, always sanitize data
2. **Prompts**: Be specific, provide context, iterate
3. **Review**: Always human-review generated code
4. **Test**: Validate in non-prod environments first
5. **Document**: Keep records of prompts and decisions
6. **Cost**: Monitor usage, batch requests, cache when possible
7. **Team**: Share knowledge, maintain standards
8. **Iterate**: Refine and improve over time

**Remember**: Claude is a powerful assistant, but you are the engineer responsible for the final implementation.

---

**Next**: Apply these practices in your [next automation project](../getting-started/README.md)!
