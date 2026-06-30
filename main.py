import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No API Key found.")

parser = argparse.ArgumentParser()
parser.add_argument("user_prompt", type=str)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

for _ in range(20):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

    if response.function_calls:
        tool_parts = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if not function_call_result.parts:
                raise Exception("Empty parts in function result")

            part = function_call_result.parts[0]

            if part.function_response is None:
                raise Exception("Missing function_response")

            if part.function_response.response is None:
                raise Exception("Missing function response value")

            if args.verbose:
                print(f"-> {part.function_response.response}")

            tool_parts.append(part)

        messages.append(types.Content(
            role="user",
            parts=tool_parts
        ))

        continue

    print(response.text)
    break


if _ == 19:
    print("Max iterations reached without final response")
    exit(1)
