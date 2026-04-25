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

    def run(self, service: str, command: str, args: Optional[List[str]] = None, timeout: int = 30) -> Dict[str, Any]:
        """
        Executes an AWS CLI command with timeout and basic retry logic.
        """
        full_command = ["aws", service, command, "--output", "json"]
        
        if self.profile:
            full_command.extend(["--profile", self.profile])
        if self.region:
            full_command.extend(["--region", self.region])
        
        if args:
            full_command.extend(args)
            
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                self.logger.info(f"Executing (Attempt {attempt+1}): {' '.join(full_command)}")
                result = subprocess.run(
                    full_command, 
                    capture_output=True, 
                    text=True, 
                    check=True,
                    timeout=timeout
                )
                
                if not result.stdout.strip():
                    return {"message": "Success (no output)"}
                    
                return json.loads(result.stdout)
            except subprocess.TimeoutExpired:
                self.logger.error(f"Command timed out after {timeout} seconds")
                if attempt < max_retries:
                    continue
                return {"error": f"Command timed out after {timeout} seconds"}
            except subprocess.CalledProcessError as e:
                self.logger.error(f"AWS CLI Error: {e.stderr}")
                return {"error": e.stderr.strip()}
            except json.JSONDecodeError:
                self.logger.error(f"Failed to parse JSON output")
                return {"error": "Failed to parse JSON result", "raw": result.stdout}
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                return {"error": str(e)}

if __name__ == "__main__":
    # Quick test
    wrapper = AWSCLIWrapper()
    print(wrapper.run("sts", "get-caller-identity"))
