"""Simple DeepSeek API test script for Assignment 3.

Before running this script, set the API key in PowerShell:

    $env:DEEPSEEK_API_KEY="your_api_key_here"

Then run:

    python deepseek_agent.py
"""

import os
import urllib.request
import json


API_URL = "https://api.deepseek.com/chat/completions"


def ask_deepseek(question: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("Please set the DEEPSEEK_API_KEY environment variable.")

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful coding assistant.",
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        "stream": False,
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    answer = ask_deepseek("Explain what a Python unit test is in one paragraph.")
    print(answer)
