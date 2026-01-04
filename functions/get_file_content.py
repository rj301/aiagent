"""
This module provides a function that gets file content for a specified file. A file path is valid if it is within the
working_directory. The function is intended to be used by an AI agent via the Gemini API. The agent is restricted to
only access files within the working directory. This function confirms valid file path and returns the file's content as
one string.
"""

import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """
    Function that gets file content for a specified file
    :param working_directory: Directory valid files must be located within
    :param file_path: Path to target file
    :return: Success or failure of reading from target file
    """
    try:
        # Check for valid parameters
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
