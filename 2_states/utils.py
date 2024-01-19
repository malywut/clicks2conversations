from typing import List

from dotenv import load_dotenv, get_key

import openai
load_dotenv(dotenv_path=".env")
openai.api_key = get_key(dotenv_path="../.env", key_to_get="OPENAI_API_KEY")
openai.api_base = get_key(dotenv_path="../.env", key_to_get="OPENAI_API_BASE")
openai.api_type = get_key(dotenv_path="../.env", key_to_get="OPENAI_API_TYPE")
openai.api_version = get_key(
    dotenv_path="../.env", key_to_get="OPENAI_API_VERSION")


def generate(messages):
    client = openai.OpenAI()
    response =  client.chat.completions.create(
        model=get_key(dotenv_path="../.env", key_to_get="OPENAI_MODEL"),
        # Conversation as a list of messages.
        messages=messages,
        max_tokens=100)

    model = response.get('model')
    usage = response.get('usage')
    created = response.get('created')

    # Write model usage in csv format to file
    with open("../monitoring.csv", "a") as f:
        f.write(
            f'"{created}","{model}","solution_2","{usage["prompt_tokens"]}","{usage["completion_tokens"]}"\n')

    return response["choices"][0]["message"]["content"]
