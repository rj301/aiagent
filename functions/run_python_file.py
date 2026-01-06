"""
This module provides a function that runs a python file. A file is valid if it is within the working_directory. The
function is intended to be used by an AI agent via the Gemini API. The agent is restricted to only access files within
the working directory.
"""

import os
import subprocess
import sys
from config import MAX_TIME
from google.genai import types


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
        result = subprocess.run(command, capture_output=True, cwd=working_dir_abs, text=True, timeout=MAX_TIME)

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


# Schema to describe run_python_file() to LLM
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Function that runs a python file with the structure '<python interpreter> <file.py> [additional args]",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to to the python file to be executed. File name must end in '.py'",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                # May need to improve the description of this
                description="Additional arguments to pass into the python file that is being called",
                # Describe the items held in the array
                items=types.Schema(
                    type=types.Type.STRING,
                )
            )
        },
        required=["file_path"]
    )
)
