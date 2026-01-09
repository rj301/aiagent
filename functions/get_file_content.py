"""
This module provides a function that gets file content for a specified file. A file path is valid if it is within the
working_directory. The function is intended to be used by an AI agent via the Gemini API. The agent is restricted to
only access files within the working directory.
"""

import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    """
    Function that gets file content for a specified file
    :param working_directory: Directory valid files must be located within
    :param file_path: Path to target file
    :return: Content of file or failure of reading from target file
    """

    try:
        # Check for valid arguments
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_target_file = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        if not is_valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            if os.path.isdir(target_file_path):
                return f"Error: \"{file_path}\" is a directory instead of a file and cannot be read"
            return f"Error: \"{file_path}\" file not found"

        # Read from file and check if file continues beyond what is read
        with open(target_file_path, "r") as file:
            file_content = file.read(MAX_CHARS)
            if file.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content

    except PermissionError as e:
        return f"Error: {e}"
    except TypeError as e:
        return f"Error: {e}"
    except UnicodeEncodeError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"


# Schema to describe get_file_content() to LLM
# Only one 'parameter' because we pass the working dir so the LLM just needs to know to provide the other path
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Function that gets file content for a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to open the file that content is being retrieved from, relative to the " \
                            "working directory. e.g. './main.py'"
            )
        },
        required=["file_path"]
    )
)
