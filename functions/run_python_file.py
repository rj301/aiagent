"""
This module provides a function that runs a python file. A file is valid if it is within the working_directory. The
function is intended to be used by an AI agent via the Gemini API. The agent is restricted to only access files within
the working directory.
"""

import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=None):
    """
    Runs a python file with any additionally specified arguments.
    :param working_directory: Directory valid files must be located within
    :param file_path: Path to target file
    :param args: Additional arguments to call with python command
    :return: Result of running python file including stdout, stderr, and non-zero exit code
    """
    try:
        # Check for valid parameters
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_target_file = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        if not is_valid_target_file:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"

        if not os.path.isfile(target_file_path):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"

        if not target_file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"

        # Build command to pass into subprocess
        command = [sys.executable, target_file_path]
        if args:
            command.extend(args)

        # Run subprocess command
        result = subprocess.run(command, capture_output=True, cwd=working_dir_abs, text=True, timeout=30)

        # Build output string to describe subprocess result
        output = ""
        if result.returncode:
            output += f"Process exited with code {result.returncode}.\n"
        if (not result.stdout) and (not result.stderr):
            output += "No output produced.\n"
        else:
            output += f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        return output

    except UnicodeDecodeError as e:
        return f"Error: {e}"
    except FileNotFoundError as e:
        # This is expected to arise if teh working directory does not exist when subprocess is run
        return f"Error: The working directory does not exist{e}"
    except TypeError as e:
        return f"Error: {e}"
    except subprocess.TimeoutExpired:
        return f"Error: Maximum time for subprocess execution was exceeded"
    except Exception as e:
        return f"Error: executing Python file: {e}"
