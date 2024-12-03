from fire import Fire
from dotenv import load_dotenv, get_key, set_key


def main(model):
    if model in {'gpt-4o-mini','4o-mini','mini'} :
        set_key(
            dotenv_path=".env", key_to_set="OPENAI_MODEL",
            value_to_set="gpt-4o-mini")
    elif model in {'gpt-4o','4o'}:
        set_key(dotenv_path=".env", key_to_set="OPENAI_MODEL", value_to_set="gpt-4o")
    else:
        # defaults to last value used
        pass


if __name__ == "__main__":
    Fire(main)
