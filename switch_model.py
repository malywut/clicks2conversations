from fire import Fire
from dotenv import load_dotenv, get_key, set_key


def main(model):
    if model == 'gpt-3.5' or model == 3.5:
        set_key(
            dotenv_path="../.env", key_to_set="MODEL",
            value_to_set="gpt-35-turbo")
        set_key(
            dotenv_path="../.env", key_to_set="OPENAI_DEPLOYMENT",
            value_to_set=get_key(
                dotenv_path="../.env", key_to_get="OPENAI_DEPLOYMENT_3.5"))
    elif model == 'gpt-4' or model == 4:
        set_key(dotenv_path="../.env", key_to_set="MODEL", value_to_set="gpt-4")
        set_key(
            dotenv_path="../.env", key_to_set="OPENAI_DEPLOYMENT",
            value_to_set=get_key(
                dotenv_path="../.env", key_to_get="OPENAI_DEPLOYMENT_4"))
    else:
        # defaults to last value used
        pass


if __name__ == "__main__":
    Fire(main)
