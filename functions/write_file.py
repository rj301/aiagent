"""
This module provides a function that writes to a specified file. A file is valid if it is within the working_directory.
The function is intended to be used by an AI agent via the Gemini API. The agent is restricted to only access files
within the working directory. This function confirms valid file path and returns the file's content as one string.
"""

import os


def write_file(working_directory, file_path, content):
    """
    Write content to a file within the working directory. Will completely overwrite the contents of any existing file.
    :param working_directory: Directory valid files must be located within
    :param file_path: Path to target file
    :param content: String to write to target file
    :return: Success or failure of writing to target file
    """

    try:
        # Check for valid parameters
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_target_file = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        if not is_valid_target_file:
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"

        if os.path.isdir(target_file_path):
            return f"Error: Cannot write to \"{file_path}\" as it is a directory"

        # Create parent directories to the target file if they don't already exist
        parent_dir = os.path.dirname(target_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        # Write to file
        with open(target_file_path, "w") as file:
            chars_written = file.write(content)
            content_length = len(content)
            if chars_written != content_length:
                return f"Error: Unable to write entire provided content to \"{file_path}\". {chars_written} out of "\
                       f"{content_length} characters written"

        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"

    # TODO: create more clear error handling
    except Exception as e:
        return f"Error: {e}"
