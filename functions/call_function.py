from google import genai        # import google's genai library
from google.genai import types
from functions.get_files_info import schema_get_files_info


available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)
