from langchain_core.tools import tool
from tools.aws_cli import AWSCLIWrapper
from typing import Optional, List

# Initialize AWS CLI Wrapper
aws = AWSCLIWrapper()

@tool
def describe_instances(instance_ids: Optional[List[str]] = None):
    """
    Lists EC2 instances. Optionally filters by a list of instance IDs.
    """
    args = []
    if instance_ids:
        args.extend(["--instance-ids"] + instance_ids)
    
    return aws.run("ec2", "describe-instances", args)

@tool
def describe_vpcs(vpc_ids: Optional[List[str]] = None):
    """
    Lists VPCs in the current region. Optionally filters by a list of VPC IDs.
    """
    args = []
    if vpc_ids:
        args.extend(["--vpc-ids"] + vpc_ids)
    
    return aws.run("ec2", "describe-vpcs", args)

@tool
def get_ec2_status(instance_id: str):
    """
    Gets the status of a specific EC2 instance.
    """
    return aws.run("ec2", "describe-instance-status", ["--instance-ids", instance_id])

# Export tools
EC2_TOOLS = [describe_instances, describe_vpcs, get_ec2_status]
