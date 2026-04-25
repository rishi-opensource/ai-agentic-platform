from langchain_core.tools import tool
from tools.aws_cli import AWSCLIWrapper
from typing import Optional, List

# Initialize AWS CLI Wrapper
aws = AWSCLIWrapper()

@tool
def list_functions():
    """
    Lists all Lambda functions in the current region.
    """
    return aws.run("lambda", "list-functions")

@tool
def get_function_configuration(function_name: str):
    """
    Gets the configuration for a specific Lambda function.
    """
    return aws.run("lambda", "get-function-configuration", ["--function-name", function_name])

# Export tools
LAMBDA_TOOLS = [list_functions, get_function_configuration]
