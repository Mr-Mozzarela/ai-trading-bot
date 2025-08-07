import os
from dotenv import load_dotenv
import httpx
from openai import OpenAI

load_dotenv()

proxy_url = "socks5h://127.0.0.1:10808"

http_client = httpx.Client(
    transport=httpx.HTTPTransport(proxy=proxy_url)
)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    http_client=http_client
)

def ask_gpt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",  # можно заменить на mistralai/mistral-7b-instruct
        messages=[
            {"role": "system", "content": "Ты торговый бот-советник. Отвечай чётко, кратко и по делу."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

