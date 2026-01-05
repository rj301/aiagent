"""
Guided project from Boot.dev to create an AI agent using Gemini API, python, and functional programming
"""


import argparse
import os
from dotenv import load_dotenv  # import environmental variables
from google import genai        # import google's genai library
from google.genai import types
from prompts import system_prompt


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="AI agent code assistant")
    parser.add_argument("user_prompt", type=str, help="user prompt for Gemini")
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()

    # Load environmental variables and get API key from os
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Confirm API key exists
    if not api_key:
        raise RuntimeError("API key not found")

    # Create an instance of a Gemini client
    client = genai.Client(api_key=api_key)

    # Initialize list of conversation messages with initial user prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Make a call to the Gemini API this creates a GenerateContentResponse object
    response_object = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0
        ),
    )

    # Track token usage
    if not response_object.usage_metadata:
        raise RuntimeError("failed API request")
    prompt_tokens = response_object.usage_metadata.prompt_token_count
    response_tokens = response_object.usage_metadata.candidates_token_count

    # Print API response and token usage
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print(response_object.text)


if __name__ == "__main__":
    main()
