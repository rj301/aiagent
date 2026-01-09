"""
Module to define a function that processes commands for the AI agent by creating calls to the Gemini API as until the
agent finishes calling functions or a maximum number of calls for a single query has occurred. Will print agent's final
response and return if the agent failed to generate a response.
"""

from config import MAX_API_CALLS
from google.genai import types
from functions.call_function import available_functions, call_function
from prompts import system_prompt


def get_agent_response(client, args):
    """
    Function that calls the Gemini API to generate a response until the response doesn't include function calls or a
    maximum number of API calls has occurred. Tracks total token usage and prints the final API call response and total
    token usage.
    :param client: Gemini API client object
    :param args: arguments declared when the program was run containing the user's prompt for the AI agent
    :return: string containing "success" if response was printed and "failure" if MAX_API_CALLS is reached
    """
    # Initialize list of conversation messages with initial user prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    total_prompt_tokens = 0
    total_response_tokens = 0

    for _ in range(MAX_API_CALLS):
        # Make a call to the Gemini API this creates a GenerateContentResponse object
        response_object = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                #temperature=0 #makes outputs less creative and more consistent
            ),
        )

        # Track token usage
        if not response_object.usage_metadata:
            raise RuntimeError("failed API request")

        # Add the Agen's responses to the conversation so it gets the full context on each call
        if response_object.candidates:
            messages.extend(response_object.candidates)

        prompt_tokens = response_object.usage_metadata.prompt_token_count
        response_tokens = response_object.usage_metadata.candidates_token_count
        total_prompt_tokens += prompt_tokens
        total_response_tokens += response_tokens

        # Print API response and token usage
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        func_responses = []
        if response_object.function_calls:

            for call in response_object.function_calls:
                func_call_result = call_function(call)

                if not func_call_result.parts:
                    # check if this is the right type of exception to raise
                    raise RuntimeError(f"Function call ({call}) returned types.Content object does not have .parts list")

                if not func_call_result.parts[0].function_response:
                    # check if this is the right type of exception to raise
                    raise RuntimeError(f"First item of function call's ({call}).parts list's .function_response is None")

                if not func_call_result.parts[0].function_response.response:
                    # check if this is the right type of exception to raise
                    raise RuntimeError(f"Function call {call} did not return a response (response was 'None')")

                func_responses.append(func_call_result.parts[0])

            if args.verbose:
                for result in func_responses:
                    print(f"-> {result.function_response.response}")

        else:
            print(f"TOKEN USAGE: {total_prompt_tokens} prompt tokens and {total_response_tokens} response tokens")
            print(response_object.text)
            return "success"

        # Add function responses to messages passed to Agent
        messages.append(types.Content(role="user", parts=func_responses))

    return "failure"
