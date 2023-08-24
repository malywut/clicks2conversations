import openai
from typing import List

from dotenv import load_dotenv, get_key

import openai
load_dotenv(dotenv_path=".env")
openai.api_key = get_key(dotenv_path="../.env", key_to_get="OPENAI_API_KEY")
openai.api_base = get_key(dotenv_path="../.env", key_to_get="OPENAI_API_BASE")
openai.api_type = get_key(dotenv_path="../.env", key_to_get="OPENAI_API_TYPE")
openai.api_version = get_key(dotenv_path="../.env", key_to_get="OPENAI_API_VERSION")


def generate(messages):
    response = openai.ChatCompletion.create(
        deployment_id= get_key(dotenv_path="../.env", key_to_get="OPENAI_DEPLOYMENT"),
        # Conversation as a list of messages.
        messages=messages,
        max_tokens=100
    )
    return response["choices"][0]["message"]["content"]