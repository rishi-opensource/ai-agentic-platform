from langchain_core.tools import tool
from tools.aws_cli import AWSCLIWrapper
from typing import Optional, List

# Initialize AWS CLI Wrapper
aws = AWSCLIWrapper()

@tool
def describe_db_instances(db_instance_identifier: Optional[str] = None):
    """
    Describes RDS DB instances. Optionally filters by a specific database identifier.
    """
    args = []
    if db_instance_identifier:
        args.extend(["--db-instance-identifier", db_instance_identifier])
    
    return aws.run("rds", "describe-db-instances", args)

@tool
def describe_db_snapshots(db_instance_identifier: Optional[str] = None):
    """
    Lists RDS DB snapshots.
    """
    args = []
    if db_instance_identifier:
        args.extend(["--db-instance-identifier", db_instance_identifier])
    
    return aws.run("rds", "describe-db-snapshots", args)

# Export tools
RDS_TOOLS = [describe_db_instances, describe_db_snapshots]
