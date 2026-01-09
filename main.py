"""
Guided project from Boot.dev to create an AI agent using Gemini API, python, and functional programming
"""


import argparse
import os
from dotenv import load_dotenv  # import environmental variables
from google import genai        # import google's genai library
from functions.get_agent_response import get_agent_response


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

    if get_agent_response(client, args) == "failure":
        print("Failed to get agent response")
        exit(1)

    exit(0)


if __name__ == "__main__":
    main()
