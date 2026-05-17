import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# set up environment variables
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

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

# send the request to google
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

metadata_stats = response.usage_metadata.__dict__

if metadata_stats is None:
    raise RuntimeError("Failed request. Please try again")

prompt_tokens = metadata_stats["prompt_token_count"]
output_tokens = metadata_stats["candidates_token_count"]

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {output_tokens}")

print(f"Response: {response.text}")
