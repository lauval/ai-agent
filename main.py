import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import FunctionResponse
from functions.call_functions import callable_functions, call_function

# set up environment variables
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
max_iterations = 40


def main():

    # read in system prompt
    with open(file="system_prompt.md", mode="r") as f:
        system_prompt = f.read()

    # create argument parser
    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # set up role tracking
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # initiate the agent loop
    for iter_val in range(max_iterations):
        # send the request to google
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[callable_functions], system_instruction=system_prompt
            ),
        )

        # track model responses so far
        if response.candidates:
            for prev_response in response.candidates:
                messages.append(prev_response.content)

        # collect stats (token counts) for logging to console
        metadata_stats = response.usage_metadata.__dict__

        prompt_tokens = metadata_stats["prompt_token_count"]
        output_tokens = metadata_stats["candidates_token_count"]

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {output_tokens}")

        # break condition. If no new responses, exit agent loop
        if response.function_calls is None:
            print(f"Response: {response.text}")
            return

        else:
            for function_call in response.function_calls:
                result = call_function(function_call, verbose=args.verbose)

                # append function call results to messages list
                messages.append(result)

                if not bool(result.parts):
                    raise Exception("Function call does not contain a .parts attribute")

                elif type(result.parts[0].function_response) is not FunctionResponse:
                    raise Exception("Function call did not return a FunctionResponse object")

                elif result.parts[0].function_response.response is None:
                    raise Exception("Function response is empty")

                if args.verbose:
                    print(f"-> ({result.parts[0].function_response.response})")

        # as a final check, if we've reached the max num of iterations and there's
        # still no response, exit with code 1
        if iter_val == max_iterations - 1:
            print("\nMaximum number of iterations reached, exiting with sys code 1")
            sys.exit(1)


if __name__ == "__main__":
    main()
