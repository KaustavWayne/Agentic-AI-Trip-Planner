# model loader

from langchain_groq import ChatGroq
from utils.config_loader import load_config

config = load_config()


def get_llm():

    return ChatGroq(
        model=config["llm"]["model"],          # ✅ correct key
        temperature=config["llm"]["temperature"],
        max_tokens=config["llm"]["max_tokens"],
        api_key=config["api_keys"]["groq"]
    )