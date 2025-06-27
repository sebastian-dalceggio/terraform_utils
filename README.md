# terraform_utils

## Overview

`terraform_utils` is a lightweight Python package designed to simplify programmatic interaction with Terraform outputs. It provides utility functions to easily retrieve specific output values from your Terraform state, making it ideal for scripting, automation, or integrating Terraform outputs into other applications.

## Why use `terraform_utils`?

When working with Terraform, you often define outputs to expose important values (e.g., IP addresses, resource IDs, connection strings) from your infrastructure. While `terraform output` command is useful, parsing its raw output in scripts can be cumbersome. `terraform_utils` abstracts away the complexities of running `subprocess` commands and JSON parsing, providing a clean Python interface to access these values.

This package is particularly useful for:
*   **CI/CD Pipelines**: Fetching dynamic infrastructure values to configure subsequent deployment steps.
*   **Automation Scripts**: Using Terraform outputs as inputs for other automation tools or scripts.
*   **Local Development**: Quickly retrieving specific outputs for testing or local application configuration.

## Installation

To install `terraform_utils` and its dependencies, you can use `uv` (or `pip`):

```bash
# Ensure you have uv installed (https://astral.sh/uv/install)
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

The primary utility function is `get_terraform_output`, which allows you to retrieve a named output from your Terraform state.

**Example:**

Assuming you have a `main.tf` with an output defined like this:

```terraform
output "web_app_url" {
  value       = "http://example.com/my-app"
  description = "The URL of the web application"
}

output "database_port" {
  value       = 5432
  description = "The database port"
}
```

You can retrieve these outputs in your Python script:

```python
from terraform_utils.utils import get_terraform_output

# Make sure you are in the directory where your Terraform state exists
# or specify the working directory for terraform commands if needed.

web_app_url = get_terraform_output("web_app_url")
if web_app_url is not None:
    print(f"Web App URL: {web_app_url}")
else:
    print("Failed to retrieve web_app_url.")

database_port = get_terraform_output("database_port")
if database_port is not None: # Use 'is not None' as 0 or False are valid outputs
    print(f"Database Port: {database_port}")
else:
    print("Failed to retrieve database_port.")

# Example of a non-existent output
non_existent = get_terraform_output("non_existent_output")
if non_existent is None:
    print("As expected, 'non_existent_output' was not found.")
```

## Development and Contributing

This project uses `uv` for dependency management and `pre-commit` hooks for code quality.

*   **Pre-commit Hooks**:
    *   `mypy`: For type checking.
    *   `ruff`: For linting and formatting.
    These are configured in `.pre-commit-config.yaml`.

*   **Testing**:
    Tests are written using `pytest`. You can run them with:
    ```bash
    uv run pytest tests/
    ```

*   **CI/CD**:
    A GitHub Actions workflow (`.github/workflows/pull_request_to_main.yaml`) is configured to run tests on pull requests to the `main` branch.
