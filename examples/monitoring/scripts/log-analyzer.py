#!/usr/bin/env python3
"""
Intelligent Log Analyzer using Claude
Generated with Claude as a DevOps Agent

This script analyzes log files and uses Claude to identify issues,
patterns, and suggest remediation steps.

Usage:
    python log-analyzer.py --log-file /var/log/application.log
    python log-analyzer.py --log-file /var/log/nginx/error.log --last-hours 24
    python log-analyzer.py --watch /var/log/app.log --interval 300
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any
import anthropic


class LogAnalyzer:
    """Analyzes logs using Claude for intelligent insights"""

    def __init__(self, api_key: str):
        """Initialize the analyzer with Anthropic API key"""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-5-20250929"

    def read_log_file(
        self, file_path: str, last_hours: int = None, max_lines: int = 1000
    ) -> List[str]:
        """Read log file, optionally filtering by time"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            if last_hours:
                # Filter by time (assumes logs have timestamps)
                cutoff_time = datetime.now() - timedelta(hours=last_hours)
                filtered_lines = []

                for line in lines:
                    # Try to extract timestamp (common formats)
                    timestamp = self._extract_timestamp(line)
                    if timestamp and timestamp >= cutoff_time:
                        filtered_lines.append(line)

                lines = filtered_lines

            # Limit to max_lines (most recent)
            if len(lines) > max_lines:
                print(f"Note: Analyzing last {max_lines} lines out of {len(lines)} total")
                lines = lines[-max_lines:]

            return lines

        except FileNotFoundError:
            print(f"Error: Log file not found: {file_path}")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied reading: {file_path}")
            sys.exit(1)

    def _extract_timestamp(self, line: str) -> datetime:
        """Extract timestamp from log line (supports common formats)"""
        # ISO 8601: 2024-01-15T14:30:00
        iso_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
        if iso_match:
            try:
                return datetime.fromisoformat(iso_match.group(1))
            except ValueError:
                pass

        # Common log format: 15/Jan/2024:14:30:00
        clf_match = re.search(r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})', line)
        if clf_match:
            try:
                return datetime.strptime(clf_match.group(1), "%d/%b/%Y:%H:%M:%S")
            except ValueError:
                pass

        return None

    def get_basic_stats(self, lines: List[str]) -> Dict[str, Any]:
        """Extract basic statistics from logs"""
        stats = {
            "total_lines": len(lines),
            "error_keywords": Counter(),
            "log_levels": Counter(),
            "ip_addresses": Counter(),
        }

        # Common error keywords
        error_keywords = [
            'error', 'exception', 'fail', 'fatal', 'critical',
            'timeout', 'refused', 'denied', 'unable'
        ]

        # Log levels
        log_levels = ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL', 'FATAL']

        for line in lines:
            line_lower = line.lower()

            # Count error keywords
            for keyword in error_keywords:
                if keyword in line_lower:
                    stats["error_keywords"][keyword] += 1

            # Count log levels
            for level in log_levels:
                if level in line.upper():
                    stats["log_levels"][level] += 1
                    break

            # Extract IP addresses
            ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
            ips = re.findall(ip_pattern, line)
            for ip in ips:
                stats["ip_addresses"][ip] += 1

        return stats

    def analyze_with_claude(self, logs: List[str], context: str = "") -> str:
        """Send logs to Claude for analysis"""

        # Create a concise log summary for efficiency
        log_sample = ''.join(logs[:500])  # First 500 lines or less

        prompt = f"""Analyze these application logs and provide:

1. **Summary**: What's happening in these logs?
2. **Issues Identified**: List any errors, warnings, or concerning patterns
3. **Root Cause Analysis**: What appears to be causing any issues?
4. **Timeline**: When did issues start? Are they ongoing or resolved?
5. **Impact Assessment**: How severe are the issues?
6. **Remediation Steps**: Specific actions to resolve issues (prioritized)
7. **Prevention**: How to prevent similar issues in the future

{context}

Logs:
```
{log_sample}
```

Provide your analysis in a clear, structured format. Be specific and actionable."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

        except Exception as e:
            return f"Error analyzing logs with Claude: {str(e)}"

    def generate_report(
        self, logs: List[str], stats: Dict[str, Any], analysis: str, output_file: str = None
    ):
        """Generate a comprehensive analysis report"""

        report = f"""
{'='*80}
LOG ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

BASIC STATISTICS
{'-'*80}
Total Log Lines: {stats['total_lines']}

Log Levels:
{self._format_counter(stats['log_levels'])}

Error Keywords:
{self._format_counter(stats['error_keywords'])}

Top IP Addresses:
{self._format_counter(stats['ip_addresses'], limit=10)}

{'='*80}
CLAUDE AI ANALYSIS
{'='*80}

{analysis}

{'='*80}
END OF REPORT
{'='*80}
"""

        # Print to console
        print(report)

        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"\nReport saved to: {output_file}")

        return report

    def _format_counter(self, counter: Counter, limit: int = None) -> str:
        """Format a Counter object for display"""
        if not counter:
            return "  None found"

        items = counter.most_common(limit)
        return '\n'.join([f"  {k}: {v}" for k, v in items])


def main():
    parser = argparse.ArgumentParser(
        description='Analyze log files using Claude AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze entire log file
  python log-analyzer.py --log-file /var/log/app.log

  # Analyze last 24 hours only
  python log-analyzer.py --log-file /var/log/app.log --last-hours 24

  # Save report to file
  python log-analyzer.py --log-file /var/log/app.log --output report.txt

  # Provide additional context
  python log-analyzer.py --log-file /var/log/app.log --context "Deployment happened at 14:00"
        """
    )

    parser.add_argument(
        '--log-file',
        required=True,
        help='Path to log file to analyze'
    )

    parser.add_argument(
        '--last-hours',
        type=int,
        help='Only analyze logs from last N hours'
    )

    parser.add_argument(
        '--max-lines',
        type=int,
        default=1000,
        help='Maximum number of log lines to analyze (default: 1000)'
    )

    parser.add_argument(
        '--output',
        help='Save report to file'
    )

    parser.add_argument(
        '--context',
        default='',
        help='Additional context for analysis (e.g., recent changes, deployment info)'
    )

    args = parser.parse_args()

    # Get API key from environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    # Initialize analyzer
    print(f"Initializing log analyzer...")
    analyzer = LogAnalyzer(api_key)

    # Read logs
    print(f"Reading logs from: {args.log_file}")
    logs = analyzer.read_log_file(
        args.log_file,
        last_hours=args.last_hours,
        max_lines=args.max_lines
    )

    if not logs:
        print("No logs found to analyze")
        sys.exit(0)

    print(f"Analyzing {len(logs)} log lines...")

    # Get basic statistics
    stats = analyzer.get_basic_stats(logs)

    # Analyze with Claude
    print("Sending logs to Claude for analysis...")
    analysis = analyzer.analyze_with_claude(logs, args.context)

    # Generate report
    print("\n")
    analyzer.generate_report(logs, stats, analysis, args.output)


if __name__ == "__main__":
    main()
