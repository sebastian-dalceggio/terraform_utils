"""
Tests for the terraform_utils.utils module, specifically focusing on the
get_terraform_output function.
"""

import pytest
import json
from terraform_utils.utils import get_terraform_output
import subprocess


# Mock data for successful terraform output
MOCK_TERRAFORM_OUTPUT_SUCCESS = {
    "my_string_output": {"value": "hello_world", "type": "string"},
    "my_number_output": {"value": 123, "type": "number"},
    "my_bool_output": {"value": True, "type": "bool"},
    "my_list_output": {"value": ["item1", "item2"], "type": "list"},
    "my_map_output": {"value": {"key": "value"}, "type": "map"},
}


@pytest.mark.parametrize(
    "output_name, expected_value",
    [
        ("my_string_output", "hello_world"),
        ("my_number_output", 123),
        ("my_bool_output", True),
        ("my_list_output", ["item1", "item2"]),
        ("my_map_output", {"key": "value"}),
    ],
)
def test_get_terraform_output_success(mocker, output_name, expected_value):
    """Test successful retrieval of various Terraform output types."""
    mock_subprocess_run = mocker.patch("subprocess.run")
    mock_result = mocker.MagicMock(spec=subprocess.CompletedProcess)
    mock_result.stdout = json.dumps(MOCK_TERRAFORM_OUTPUT_SUCCESS)
    mock_result.stderr = ""
    mock_result.returncode = 0
    mock_subprocess_run.return_value = mock_result

    output = get_terraform_output(output_name)

    assert output == expected_value
    mock_subprocess_run.assert_called_once_with(
        ["terraform", "output", "-json"],
        capture_output=True,
        text=True,
        check=True,
        cwd=None,
    )


def test_get_terraform_output_with_cwd(mocker):
    """Test successful retrieval with a specified working directory."""
    mock_subprocess_run = mocker.patch("subprocess.run")
    mock_result = mocker.MagicMock(spec=subprocess.CompletedProcess)
    mock_result.stdout = json.dumps(MOCK_TERRAFORM_OUTPUT_SUCCESS)
    mock_result.stderr = ""
    mock_result.returncode = 0
    mock_subprocess_run.return_value = mock_result

    test_cwd = "/my/terraform/project"
    output = get_terraform_output("my_string_output", cwd=test_cwd)

    assert output == "hello_world"
    mock_subprocess_run.assert_called_once_with(
        ["terraform", "output", "-json"],
        capture_output=True,
        text=True,
        check=True,
        cwd=test_cwd,
    )


def test_get_terraform_output_not_found(mocker, capsys):
    """Test case where the requested output name is not found."""
    mock_subprocess_run = mocker.patch("subprocess.run")
    mock_result = mocker.MagicMock(spec=subprocess.CompletedProcess)
    mock_result.stdout = json.dumps(MOCK_TERRAFORM_OUTPUT_SUCCESS)
    mock_result.stderr = ""
    mock_result.returncode = 0
    mock_subprocess_run.return_value = mock_result

    output = get_terraform_output("non_existent_output")
    assert output is None
    captured = capsys.readouterr()
    assert (
        "Error: Output 'non_existent_output' not found in Terraform outputs."
        in captured.out
    )


def test_get_terraform_output_subprocess_error(mocker, capsys):
    """Test case where subprocess.run raises CalledProcessError."""
    mock_subprocess_run = mocker.patch("subprocess.run")
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=["terraform", "output", "-json"],
        output="stdout error message",
        stderr="stderr error message",
    )

    output = get_terraform_output("any_output")
    assert output is None
    captured = capsys.readouterr()
    assert "Error running Terraform command" in captured.out
    assert "STDOUT: stdout error message" in captured.out
    assert "STDERR: stderr error message" in captured.out


def test_get_terraform_output_json_decode_error(mocker, capsys):
    """Test case where JSON decoding fails."""
    mock_subprocess_run = mocker.patch("subprocess.run")
    mock_result = mocker.MagicMock(spec=subprocess.CompletedProcess)
    mock_result.stdout = "this is not valid json"
    mock_result.stderr = ""
    mock_result.returncode = 0
    mock_subprocess_run.return_value = mock_result

    output = get_terraform_output("any_output")
    assert output is None
    captured = capsys.readouterr()
    assert "Error decoding JSON from Terraform output" in captured.out
    assert "Output received:\nthis is not valid json" in captured.out


def test_get_terraform_output_file_not_found_error(mocker, capsys):
    """Test case where 'terraform' command is not found."""
    mock_subprocess_run = mocker.patch("subprocess.run")
    mock_subprocess_run.side_effect = FileNotFoundError(
        "No such file or directory: 'terraform'"
    )

    output = get_terraform_output("any_output")
    assert output is None
    captured = capsys.readouterr()
    assert (
        "Error: 'terraform' command not found. Is Terraform installed and in your PATH?"
        in captured.out
    )
