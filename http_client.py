import os

from openai import OpenAI

client = OpenAI(
    # Agentverse injects ASI1_API_KEY and ASI1_BASE_URL into every hosted agent.
    api_key=os.environ["ASI1_API_KEY"],
    base_url=os.environ["ASI1_BASE_URL"],
)


def ask_asi1(messages: list) -> str:
    """Send a chat message list to ASI:One and return the reply text."""
    completion = client.chat.completions.create(
        model="asi1",
        messages=messages,
        max_tokens=2048,
    )
    return completion.choices[0].message.content or ""
