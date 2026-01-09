"""
Module that groups all of the functions available for the LLM agent to call
"""

from config import WORKING_DIRECTORY
from google.genai import types
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call, verbose=False):
    """
    Function that calls functions for the Agent
    :param function_call: The function the Agent is attempting to call
    :param verbose: Optional argument that enables detailed information about the function being called
    :return: types.Content object communicating failure or function result to the AI Agent
    """

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # Define mapping of functions to help define which function to call
    func_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    func_name = function_call.name or ""

    if not func_name in func_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}

    args["working_directory"] = WORKING_DIRECTORY

    func_result = func_map[func_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": func_result},
            )
        ],
    )
