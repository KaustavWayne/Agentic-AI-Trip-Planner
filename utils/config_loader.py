# config loader

import os 
from pathlib import Path
import yaml 
from dotenv import load_dotenv 

load_dotenv()

def load_config() -> dict:
    config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    with open(config_path) as f:
        config = yaml.safe_load(f) 

    # Inject API keys from environment variables
    config["api_keys"] = {
    'groq': os.getenv("GROQ_API_KEY"),
    "tavily": os.getenv("TAVILY_API_KEY"),
    "foursquare": os.getenv("FOURSQUARE_API_KEY"),
    "openweathermap": os.getenv("OPENWEATHERMAP_API_KEY"),
    "exchangerate": os.getenv("EXCHANGE_RATE_API_KEY"),
    "opentripmap": os.getenv("OPENTRIPMAP_API_KEY")
}
    return config