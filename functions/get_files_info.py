"""
This module provides a function that gets file information for all files in a directory. A directory is valid if it is
within the working_directory. The function is intended to be used by an AI agent via the Gemini API. The agent is
restricted to only access files within the working directory. This function confirms valid target directory and returns
the files' information in the following format:
"
- FILENAME: file_size = SIZE, is_dir = BOOL
- FILENAME: file_size = SIZE, is_dir = BOOL
- FILENAME: file_size = SIZE, is_dir = BOOL
"
"""

import os


def get_files_info(working_directory, directory="."):
    """
    Gets information about all files in a given directory
    :param working_directory: The directory agent is allowed to access and work in
    :param directory: Relative file-path to target directory to get information about
    :return: String listing each file, its size, and if it is a directory
    """
    try:
        # Check for valid parameters
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        is_valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not is_valid_target_dir:
            return f"Error: Cannot list \"{directory}\" as it is outside permitted working directory"

        if not os.path.exists(target_dir):
            return f"Error: \"{target_dir}\" does not exist"

        if not os.path.isdir(target_dir):
            return f"Error: \"{directory}\" exists but it is not a directory"

        # Get information for all files in the directory
        files_info = list(map(_build_file_str(target_dir), os.listdir(target_dir)))

        return '\n'.join(files_info)

    except PermissionError as e:
        return f"Error: {e}"
    except TypeError as e:
        return f"Error: {e}"
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"


def _build_file_str(target_directory):
    """
    Helper function for get_files_info()
    Builds a string containing name, size, and is_dir information about a file. Curried the function to work with map
    and practice functional programming techniques.
    :param target_directory: The directory the file is in
    :return: String documenting file information
    """
    def inner(file):
        file_path = os.path.join(target_directory, file)
        return f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
    return inner
