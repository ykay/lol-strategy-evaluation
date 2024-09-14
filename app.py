import chainlit as cl
import openai
import os
from dotenv import load_dotenv
import base64

from langsmith.wrappers import wrap_openai
from langsmith import traceable

import requests
from bs4 import BeautifulSoup

load_dotenv()

# Retrieve context from a blog post
url = "https://mobalytics.gg/blog/start-strong-league-legends/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
text = [p.text for p in soup.find_all("p")]
full_text = "\n".join(text)

# print(full_text)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
endpoint_url = "https://api.openai.com/v1"
client = wrap_openai(openai.AsyncClient(api_key=api_key, base_url=endpoint_url))
# https://platform.openai.com/docs/models/gpt-4o
model_kwargs = {"model": "gpt-4o", "temperature": 0.2, "max_tokens": 500}

# Pass in website text
# System prompt
system_msg = (
    f"You are a League of Legends expert who answers strategy-related questions in 2-3 sentences using this context: \n\n\n {full_text}"
)

@cl.on_message
@traceable
async def on_message(message: cl.Message):
    # Maintain an array of messages in the user session
    message_history = cl.user_session.get("message_history", [])

    # Provide the system prompt
    message_history.append({"role": "system", "content": system_msg})

    # Record the user's message in the history
    message_history.append({"role": "user", "content": message.content})

    response_message = cl.Message(content="")
    await response_message.send()

    # Pass in the full message history for each request
    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **model_kwargs
    )
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)

    await response_message.update()

    # Record the AI's response in the history
    message_history.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("message_history", message_history)
