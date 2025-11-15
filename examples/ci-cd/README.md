# CI/CD Examples

This directory contains practical, working examples of CI/CD pipelines generated and optimized with Claude's assistance.

## Directory Structure

```
ci-cd/
├── github-actions/       # GitHub Actions workflows
├── gitlab-ci/           # GitLab CI configurations
├── jenkins/             # Jenkins pipelines
├── scripts/             # Helper scripts
└── troubleshooting/     # Common issues and solutions
```

## Quick Start

Each subdirectory contains:
- **README.md**: Explanation of the example
- **Configuration files**: Ready-to-use pipeline configs
- **Prompts used**: The prompts given to Claude to generate the examples

## Examples Overview

### GitHub Actions

1. **Node.js Web Application** (`github-actions/nodejs-webapp.yml`)
   - Multi-version testing
   - Docker build and push
   - Automated deployment

2. **Python FastAPI** (`github-actions/fastapi-deployment.yml`)
   - Testing with pytest
   - Code quality checks
   - Security scanning
   - AWS ECS deployment

3. **Go Microservice** (`github-actions/go-microservice.yml`)
   - Cross-platform builds
   - Integration tests
   - Kubernetes deployment

### GitLab CI

1. **React Application** (`gitlab-ci/react-app.yml`)
   - Build optimization
   - S3 and CloudFront deployment
   - Multi-environment setup

2. **Monorepo Pipeline** (`gitlab-ci/monorepo.yml`)
   - Selective testing
   - Parallel jobs
   - DAG pipeline structure

### Jenkins

1. **Declarative Pipeline** (`jenkins/declarative-pipeline.groovy`)
   - Multi-stage build
   - Parallel execution
   - Post-build actions

2. **Scripted Pipeline** (`jenkins/scripted-pipeline.groovy`)
   - Dynamic stages
   - Complex logic
   - Custom notifications

## Using These Examples

### 1. Copy and Customize

```bash
# Copy an example to your project
cp github-actions/nodejs-webapp.yml ../../../.github/workflows/deploy.yml

# Edit for your needs
vim ../../../.github/workflows/deploy.yml
```

### 2. Learn the Patterns

Study how Claude structured the pipelines:
- Caching strategies
- Security practices
- Error handling
- Environment management

### 3. Extend with Claude

Use the examples as a starting point and ask Claude to extend them:

```
Based on examples/ci-cd/github-actions/nodejs-webapp.yml,
add a stage that:
1. Runs Lighthouse CI for performance testing
2. Comments results on pull requests
3. Fails the build if performance scores drop below 90
```

## Common Patterns

### Caching

All examples use intelligent caching:
```yaml
# GitHub Actions example
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Security Scanning

Examples include security checks:
```yaml
- name: Run security scan
  run: |
    npm audit
    npx snyk test
```

### Multi-Environment Deployment

Examples show environment-specific deployments:
```yaml
deploy-production:
  if: github.ref == 'refs/heads/main'
  environment: production
```

## Helper Scripts

### `scripts/claude-ci-helper.sh`

A bash script that sends CI/CD questions to Claude:

```bash
./scripts/claude-ci-helper.sh "Generate a GitHub Actions workflow for Django"
```

### `scripts/pipeline-validator.py`

Validates pipeline syntax before committing:

```bash
python scripts/pipeline-validator.py .github/workflows/deploy.yml
```

## Troubleshooting Examples

The `troubleshooting/` directory contains:

1. **Common build failures** and how Claude helped solve them
2. **Performance issues** and optimization strategies
3. **Security problems** and remediation steps

Each troubleshooting case includes:
- Original error/issue
- Prompt given to Claude
- Claude's analysis
- Solution implemented
- Results

## Contributing Your Own Examples

If you've created useful pipelines with Claude's help:

1. Add your example to the appropriate directory
2. Include a `PROMPT.md` file with the prompts you used
3. Document any customizations needed
4. Update this README

## Testing Examples Locally

Many examples can be tested locally:

### GitHub Actions (with act)
```bash
brew install act
act -W github-actions/nodejs-webapp.yml
```

### GitLab CI (with gitlab-runner)
```bash
gitlab-runner exec docker test
```

## Advanced Examples

Coming soon:
- Matrix builds with dynamic configuration
- Monorepo selective execution
- Cross-repository workflows
- Custom GitHub Actions/GitLab components
- Pipeline-as-a-Service integration

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI Documentation](https://docs.gitlab.com/ee/ci/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [CI/CD Best Practices Guide](../../docs/ci-cd/README.md)

---

**Tip**: Start with the simplest example that matches your stack, then gradually add complexity!
