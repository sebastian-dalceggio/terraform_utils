"""
Utility functions for interacting with Terraform, primarily for extracting
output values from Terraform state.
"""

from typing import Any
import subprocess
import json


def get_terraform_output(output_name: str) -> Any:
    """Retrieves a specific output value from Terraform's state.

    This function executes the 'terraform output -json' command, parses its JSON
    output, and then extracts the 'value' field for the specified output name.
    It handles various errors such as Terraform command not found, command
    execution failures, and JSON decoding issues, printing informative messages
    to stderr in case of an error.

    Args:
        output_name: The name of the Terraform output to retrieve.

    Returns:
        The value of the specified Terraform output if found. The type of the
        returned value depends on the Terraform output type (e.g., str, int,
        bool, list, dict). Returns None if the output is not found, or if any
        error occurs during the execution of the Terraform command or JSON
        parsing.
    """
    try:
        result = subprocess.run(
            ["terraform", "output", "-json"], capture_output=True, text=True, check=True
        )

        outputs = json.loads(result.stdout)

        if output_name in outputs:
            return outputs[output_name]["value"]
        else:
            print(f"Error: Output '{output_name}' not found in Terraform outputs.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error running Terraform command: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Terraform output: {e}")
        print(f"Output received:\n{result.stdout}")
        return None
    except FileNotFoundError:
        print(
            "Error: 'terraform' command not found. Is Terraform installed and in your PATH?"
        )
        return None
