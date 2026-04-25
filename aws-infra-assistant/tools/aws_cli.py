import subprocess
import json
import logging
from typing import Optional, Dict, Any, List

class AWSCLIWrapper:
    """
    A utility class to execute AWS CLI commands and return structured data.
    """
    def __init__(self, profile: Optional[str] = None, region: Optional[str] = None):
        self.profile = profile
        self.region = region
        self.logger = logging.getLogger(__name__)

    def run(self, service: str, command: str, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Executes an AWS CLI command.
        Example: run("ec2", "describe-instances", ["--instance-ids", "i-12345"])
        """
        full_command = ["aws", service, command, "--output", "json"]
        
        if self.profile:
            full_command.extend(["--profile", self.profile])
        if self.region:
            full_command.extend(["--region", self.region])
        
        if args:
            full_command.extend(args)
            
        try:
            self.logger.info(f"Executing: {' '.join(full_command)}")
            result = subprocess.run(
                full_command, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            if not result.stdout.strip():
                return {"message": "Success (no output)"}
                
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"AWS CLI Error: {e.stderr}")
            return {"error": e.stderr.strip()}
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse JSON output: {result.stdout}")
            return {"error": "Failed to parse JSON result", "raw": result.stdout}
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Quick test
    wrapper = AWSCLIWrapper()
    print(wrapper.run("sts", "get-caller-identity"))
