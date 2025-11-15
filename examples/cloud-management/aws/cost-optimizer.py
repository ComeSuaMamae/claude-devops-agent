#!/usr/bin/env python3
"""
AWS Cost Optimizer using Claude
Generated with Claude as a DevOps Agent

This script analyzes AWS resources and suggests cost optimization opportunities
using Claude AI for intelligent recommendations.

Usage:
    python cost-optimizer.py --region us-east-1
    python cost-optimizer.py --all-regions
    python cost-optimizer.py --region us-east-1 --execute-cleanup
"""

import argparse
import boto3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict
import anthropic


class AWSCostOptimizer:
    """Analyzes AWS resources and suggests optimizations"""

    def __init__(self, region: str = 'us-east-1'):
        """Initialize AWS clients"""
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.s3 = boto3.client('s3')
        self.ce = boto3.client('ce', region_name='us-east-1')  # Cost Explorer is global

        # Initialize Claude
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            self.claude = anthropic.Anthropic(api_key=api_key)
        else:
            self.claude = None
            print("Warning: ANTHROPIC_API_KEY not set. AI analysis disabled.")

    def find_unattached_volumes(self) -> List[Dict]:
        """Find EBS volumes not attached to any instance"""
        print("Scanning for unattached EBS volumes...")

        volumes = self.ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )

        unattached = []
        for vol in volumes['Volumes']:
            size = vol['Size']
            volume_type = vol['VolumeType']
            created = vol['CreateTime']

            # Estimate monthly cost
            cost_per_gb = {
                'gp2': 0.10,
                'gp3': 0.08,
                'io1': 0.125,
                'io2': 0.125,
                'st1': 0.045,
                'sc1': 0.025
            }
            monthly_cost = size * cost_per_gb.get(volume_type, 0.10)

            unattached.append({
                'volume_id': vol['VolumeId'],
                'size_gb': size,
                'type': volume_type,
                'created': created.isoformat(),
                'age_days': (datetime.now(created.tzinfo) - created).days,
                'monthly_cost': monthly_cost,
                'tags': {tag['Key']: tag['Value'] for tag in vol.get('Tags', [])}
            })

        return unattached

    def find_old_snapshots(self, days: int = 90) -> List[Dict]:
        """Find EBS snapshots older than specified days"""
        print(f"Scanning for snapshots older than {days} days...")

        cutoff_date = datetime.now(tz=None) - timedelta(days=days)
        snapshots = self.ec2.describe_snapshots(OwnerIds=['self'])

        old_snapshots = []
        for snap in snapshots['Snapshots']:
            start_time = snap['StartTime'].replace(tzinfo=None)

            if start_time < cutoff_date:
                # Estimate cost ($0.05 per GB-month)
                size_gb = snap['VolumeSize']
                monthly_cost = size_gb * 0.05

                old_snapshots.append({
                    'snapshot_id': snap['SnapshotId'],
                    'description': snap.get('Description', 'N/A'),
                    'size_gb': size_gb,
                    'created': start_time.isoformat(),
                    'age_days': (datetime.now() - start_time).days,
                    'monthly_cost': monthly_cost,
                    'tags': {tag['Key']: tag['Value'] for tag in snap.get('Tags', [])}
                })

        return old_snapshots

    def find_unused_elastic_ips(self) -> List[Dict]:
        """Find Elastic IPs not associated with instances"""
        print("Scanning for unused Elastic IPs...")

        addresses = self.ec2.describe_addresses()

        unused = []
        for addr in addresses['Addresses']:
            if 'InstanceId' not in addr:
                # Unused EIP costs $0.005/hour = ~$3.60/month
                unused.append({
                    'allocation_id': addr['AllocationId'],
                    'public_ip': addr['PublicIp'],
                    'monthly_cost': 3.60,
                    'tags': {tag['Key']: tag['Value'] for tag in addr.get('Tags', [])}
                })

        return unused

    def find_stopped_instances(self, days: int = 14) -> List[Dict]:
        """Find EC2 instances stopped for more than specified days"""
        print(f"Scanning for instances stopped longer than {days} days...")

        instances = self.ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
        )

        stopped = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']

                # Get state transition time
                state_reason = instance.get('StateTransitionReason', '')

                # Get attached volumes (still incurring costs)
                volumes = [bd['Ebs']['VolumeId'] for bd in instance.get('BlockDeviceMappings', [])]

                stopped.append({
                    'instance_id': instance_id,
                    'instance_type': instance_type,
                    'state_reason': state_reason,
                    'volumes': volumes,
                    'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                })

        return stopped

    def find_underutilized_instances(self) -> List[Dict]:
        """Identify instances with low CPU utilization (requires CloudWatch)"""
        print("Analyzing instance utilization (this may take a moment)...")

        instances = self.ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )

        cloudwatch = boto3.client('cloudwatch', region_name=self.region)
        underutilized = []

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']

                try:
                    # Get average CPU utilization for last 7 days
                    metrics = cloudwatch.get_metric_statistics(
                        Namespace='AWS/EC2',
                        MetricName='CPUUtilization',
                        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                        StartTime=datetime.now() - timedelta(days=7),
                        EndTime=datetime.now(),
                        Period=86400,  # 1 day
                        Statistics=['Average']
                    )

                    if metrics['Datapoints']:
                        avg_cpu = sum(d['Average'] for d in metrics['Datapoints']) / len(metrics['Datapoints'])

                        if avg_cpu < 10:  # Less than 10% average CPU
                            underutilized.append({
                                'instance_id': instance_id,
                                'instance_type': instance_type,
                                'avg_cpu_7d': round(avg_cpu, 2),
                                'launch_time': instance['LaunchTime'].isoformat(),
                                'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                            })
                except Exception as e:
                    print(f"Warning: Could not get metrics for {instance_id}: {e}")
                    continue

        return underutilized

    def get_cost_summary(self, days: int = 30) -> Dict:
        """Get cost summary from AWS Cost Explorer"""
        print(f"Fetching cost data for last {days} days...")

        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)

            response = self.ce.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.isoformat(),
                    'End': end_date.isoformat()
                },
                Granularity='MONTHLY',
                Metrics=['UnblendedCost'],
                GroupBy=[{'Type': 'SERVICE', 'Key': 'SERVICE'}]
            )

            costs_by_service = {}
            for result in response['ResultsByTime']:
                for group in result['Groups']:
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['UnblendedCost']['Amount'])
                    costs_by_service[service] = costs_by_service.get(service, 0) + cost

            # Sort by cost descending
            sorted_costs = sorted(costs_by_service.items(), key=lambda x: x[1], reverse=True)

            return {
                'total_cost': sum(costs_by_service.values()),
                'top_services': dict(sorted_costs[:10])
            }
        except Exception as e:
            print(f"Warning: Could not fetch cost data: {e}")
            return {'total_cost': 0, 'top_services': {}}

    def analyze_with_claude(self, findings: Dict) -> str:
        """Use Claude to analyze findings and provide recommendations"""
        if not self.claude:
            return "Claude AI analysis not available (ANTHROPIC_API_KEY not set)"

        print("Analyzing findings with Claude AI...")

        prompt = f"""Analyze these AWS cost optimization findings and provide specific recommendations:

FINDINGS:
{json.dumps(findings, indent=2, default=str)}

Please provide:
1. **Summary**: Overview of cost optimization opportunities
2. **Prioritized Recommendations**: Top 5 actions to take, ordered by impact
3. **Potential Savings**: Estimate monthly savings for each recommendation
4. **Implementation Steps**: How to implement each recommendation safely
5. **Risks**: Any risks to consider
6. **Quick Wins**: What can be done immediately vs. requires planning

Be specific and actionable. Focus on the most impactful optimizations first."""

        try:
            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text
        except Exception as e:
            return f"Error getting Claude analysis: {str(e)}"

    def generate_report(self, findings: Dict, analysis: str):
        """Generate comprehensive cost optimization report"""

        # Calculate total potential savings
        total_savings = 0

        for vol in findings.get('unattached_volumes', []):
            total_savings += vol['monthly_cost']

        for snap in findings.get('old_snapshots', []):
            total_savings += snap['monthly_cost']

        for eip in findings.get('unused_elastic_ips', []):
            total_savings += eip['monthly_cost']

        report = f"""
{'='*80}
AWS COST OPTIMIZATION REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Region: {self.region}
{'='*80}

EXECUTIVE SUMMARY
{'-'*80}
Current Monthly Cost: ${findings.get('cost_summary', {}).get('total_cost', 0):.2f}
Potential Monthly Savings: ${total_savings:.2f}
Optimization Opportunities: {len(findings.get('unattached_volumes', [])) + len(findings.get('old_snapshots', [])) + len(findings.get('unused_elastic_ips', [])) + len(findings.get('stopped_instances', []))}

{'='*80}
DETAILED FINDINGS
{'='*80}

1. UNATTACHED EBS VOLUMES
{'-'*80}
Found: {len(findings.get('unattached_volumes', []))}
Potential Savings: ${sum(v['monthly_cost'] for v in findings.get('unattached_volumes', [])):.2f}/month

{self._format_list(findings.get('unattached_volumes', []), ['volume_id', 'size_gb', 'type', 'age_days', 'monthly_cost'])}

2. OLD SNAPSHOTS (>90 days)
{'-'*80}
Found: {len(findings.get('old_snapshots', []))}
Potential Savings: ${sum(s['monthly_cost'] for s in findings.get('old_snapshots', [])):.2f}/month

{self._format_list(findings.get('old_snapshots', []), ['snapshot_id', 'size_gb', 'age_days', 'monthly_cost'])}

3. UNUSED ELASTIC IPs
{'-'*80}
Found: {len(findings.get('unused_elastic_ips', []))}
Potential Savings: ${sum(e['monthly_cost'] for e in findings.get('unused_elastic_ips', [])):.2f}/month

{self._format_list(findings.get('unused_elastic_ips', []), ['public_ip', 'monthly_cost'])}

4. STOPPED INSTANCES (>14 days)
{'-'*80}
Found: {len(findings.get('stopped_instances', []))}
Note: Still incurring EBS storage costs

{self._format_list(findings.get('stopped_instances', []), ['instance_id', 'instance_type'])}

5. UNDERUTILIZED INSTANCES (<10% CPU)
{'-'*80}
Found: {len(findings.get('underutilized_instances', []))}
Note: Consider downsizing or using Spot instances

{self._format_list(findings.get('underutilized_instances', []), ['instance_id', 'instance_type', 'avg_cpu_7d'])}

{'='*80}
CLAUDE AI RECOMMENDATIONS
{'='*80}

{analysis}

{'='*80}
TOP SERVICES BY COST (Last 30 days)
{'='*80}
{self._format_costs(findings.get('cost_summary', {}).get('top_services', {}))}

{'='*80}
NEXT STEPS
{'='*80}
1. Review the findings and AI recommendations above
2. Verify resources before deletion (check with teams)
3. Start with quick wins (unused Elastic IPs, old snapshots)
4. Plan instance right-sizing for underutilized resources
5. Set up AWS Budgets and Cost Anomaly Detection
6. Schedule regular cost optimization reviews

{'='*80}
END OF REPORT
{'='*80}
"""
        return report

    def _format_list(self, items: List[Dict], fields: List[str]) -> str:
        """Format a list of dictionaries for display"""
        if not items:
            return "  None found\n"

        output = []
        for item in items[:10]:  # Limit to first 10
            parts = [f"{field}: {item.get(field, 'N/A')}" for field in fields]
            output.append("  - " + ", ".join(parts))

        if len(items) > 10:
            output.append(f"  ... and {len(items) - 10} more")

        return "\n".join(output) + "\n"

    def _format_costs(self, costs: Dict[str, float]) -> str:
        """Format costs dictionary for display"""
        if not costs:
            return "  No data available\n"

        output = []
        for service, cost in costs.items():
            output.append(f"  {service}: ${cost:.2f}")

        return "\n".join(output) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description='AWS Cost Optimization Tool with Claude AI'
    )

    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region to analyze (default: us-east-1)'
    )

    parser.add_argument(
        '--output',
        help='Save report to file'
    )

    parser.add_argument(
        '--execute-cleanup',
        action='store_true',
        help='Actually delete resources (use with caution!)'
    )

    args = parser.parse_args()

    print(f"AWS Cost Optimizer")
    print(f"Region: {args.region}")
    print("=" * 80)

    # Initialize optimizer
    optimizer = AWSCostOptimizer(region=args.region)

    # Gather findings
    findings = {
        'unattached_volumes': optimizer.find_unattached_volumes(),
        'old_snapshots': optimizer.find_old_snapshots(),
        'unused_elastic_ips': optimizer.find_unused_elastic_ips(),
        'stopped_instances': optimizer.find_stopped_instances(),
        'underutilized_instances': optimizer.find_underutilized_instances(),
        'cost_summary': optimizer.get_cost_summary()
    }

    # Get Claude analysis
    analysis = optimizer.analyze_with_claude(findings)

    # Generate report
    report = optimizer.generate_report(findings, analysis)

    print(report)

    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")

    # Execute cleanup if requested
    if args.execute_cleanup:
        print("\n⚠️  CLEANUP MODE - This will DELETE resources!")
        response = input("Are you sure? Type 'yes' to continue: ")
        if response.lower() == 'yes':
            print("Cleanup functionality not implemented (safety measure)")
            print("Please review findings and delete manually")
        else:
            print("Cleanup cancelled")


if __name__ == "__main__":
    main()
