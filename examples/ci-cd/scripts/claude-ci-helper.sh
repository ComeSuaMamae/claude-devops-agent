#!/bin/bash

# Claude CI/CD Helper Script
# This script helps you interact with Claude for CI/CD tasks
# Usage: ./claude-ci-helper.sh "your prompt here"

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}Error: ANTHROPIC_API_KEY environment variable not set${NC}"
    echo "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

# Check if prompt is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: No prompt provided${NC}"
    echo "Usage: $0 \"your CI/CD question or request\""
    echo ""
    echo "Examples:"
    echo "  $0 \"Create a GitHub Actions workflow for a Python Django app\""
    echo "  $0 \"Help me debug this build error: [paste error]\""
    echo "  $0 \"Convert this Jenkins pipeline to GitLab CI: [paste pipeline]\""
    exit 1
fi

PROMPT="$1"

# Optional: Add context from files
CONTEXT=""
if [ -n "$2" ]; then
    CONTEXT_FILE="$2"
    if [ -f "$CONTEXT_FILE" ]; then
        CONTEXT="Here's the relevant file content:\n\n$(cat "$CONTEXT_FILE")\n\n"
    fi
fi

# Full prompt with context
FULL_PROMPT="${CONTEXT}${PROMPT}"

echo -e "${BLUE}Sending request to Claude...${NC}\n"

# Make API call to Claude
RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
    -H "Content-Type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "'"${FULL_PROMPT//\"/\\\"}"'"
            }
        ],
        "system": "You are an expert DevOps engineer helping with CI/CD pipelines. Provide practical, production-ready solutions. Include configuration files and explain your reasoning."
    }')

# Check for errors
if echo "$RESPONSE" | grep -q "error"; then
    echo -e "${RED}Error from API:${NC}"
    echo "$RESPONSE" | jq -r '.error.message' 2>/dev/null || echo "$RESPONSE"
    exit 1
fi

# Extract and display the response
echo -e "${GREEN}Claude's Response:${NC}\n"
echo "$RESPONSE" | jq -r '.content[0].text' 2>/dev/null || echo "$RESPONSE"

# Optional: Save response to file
if [ -n "$SAVE_TO_FILE" ]; then
    echo "$RESPONSE" | jq -r '.content[0].text' > "$SAVE_TO_FILE"
    echo -e "\n${GREEN}Response saved to: $SAVE_TO_FILE${NC}"
fi
