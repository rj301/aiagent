import os
from dotenv import load_dotenv  # import environmental variables
from google import genai        # import google's genai library


def main():
    # load environmental variables and get API key from os
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Confirm API key exists
    if not api_key:
        raise Exception("API key not found")

    # Create an instance of a Gemini client
    client = genai.Client(api_key=api_key)

    # Make a call to the Gemini API this creates a GenerateContentResponse object
    response_object = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )

    # Access the text from the Gemini API call's response object
    print(response_object.text)


if __name__ == "__main__":
    main()
