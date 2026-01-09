from google.genai import types
from functions.call_function import available_functions, call_function
from prompts import system_prompt

# Loop call to AI model calls to create 'Agent Loop'
def get_agent_response(client, args):
    # Initialize list of conversation messages with initial user prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
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
            print(response_object.text)
            return "success"

        # Add function responses to messages passed to Agent
        # confirm to extend the candidates earlier but to append the func results
        messages.append(types.Content(role="user", parts=func_responses))

    return "failure"
