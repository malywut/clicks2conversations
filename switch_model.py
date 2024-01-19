from fire import Fire
from dotenv import load_dotenv, get_key, set_key


def main(model):
    if model == 'gpt-3.5' or model == 3.5:
        set_key(
            dotenv_path=".env", key_to_set="OPENAI_MODEL",
            value_to_set="gpt-3.5-turbo")
        
        # If the OPENAI API used is Azure, then the deployment id is needed
        # If the OPENAI API used is OpenAI, then the model is needed
        if get_key(dotenv_path=".env", key_to_get="OPENAI_API_TYPE") == "azure":
            set_key(
                dotenv_path=".env", key_to_set="OPENAI_DEPLOYMENT",
                value_to_set=get_key(
                    dotenv_path=".env", key_to_get="OPENAI_DEPLOYMENT_3.5"))
    elif model == 'gpt-4' or model == 4:
        set_key(dotenv_path=".env", key_to_set="OPENAI_MODEL", value_to_set="gpt-4")
        if get_key(dotenv_path=".env", key_to_get="OPENAI_API_TYPE") == "azure":
            set_key(
                dotenv_path=".env", key_to_set="OPENAI_DEPLOYMENT",
                value_to_set=get_key(
                    dotenv_path=".env", key_to_get="OPENAI_DEPLOYMENT_4"))
    else:
        # defaults to last value used
        pass


if __name__ == "__main__":
    Fire(main)
