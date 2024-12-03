from typing import List

from dotenv import load_dotenv, get_key

load_dotenv(dotenv_path=".env")
import openai
client = openai.OpenAI(api_key = get_key(dotenv_path="../.env", key_to_get="OPENAI_API_KEY"))

def generate(messages):
    response = client.chat.completions.create(
        model=get_key(dotenv_path="../.env", key_to_get="OPENAI_MODEL"),
        messages=messages,
        max_tokens=100
    )
    model=response.model
    usage=response.usage
    created=response.created

    # Write model usage in csv format to file
    with open("../monitoring.csv", "a") as f:
        f.write(f'"{created}","{model}","solution_1","{usage.prompt_tokens}","{usage.completion_tokens}"\n')

    return response.choices[0].message.content