import re
import requests
from tavily import TavilyClient

from utils.config_loader import load_config
from exception.exceptionhandling import APICallFailed
from logger.logging import logger


config = load_config()
tavily_client = TavilyClient(api_key=config["api_keys"]["tavily"])


def get_currency_from_city(city: str) -> str:
    """
    Detect currency automatically using OpenTripMap + REST Countries API
    """

    try:
        api_key = config["api_keys"]["opentripmap"]

        geo_url = "https://api.opentripmap.com/0.1/en/places/geoname"

        geo_resp = requests.get(
            geo_url,
            params={"name": city, "apikey": api_key},
            timeout=10
        )

        geo_resp.raise_for_status()

        data = geo_resp.json()

        country_code = data.get("country")

        if not country_code:
            return "USD"

        # Get currency from REST Countries
        rest_url = f"https://restcountries.com/v3.1/alpha/{country_code}"

        rest_resp = requests.get(rest_url, timeout=10)

        rest_resp.raise_for_status()

        rest_data = rest_resp.json()

        currency = list(rest_data[0]["currencies"].keys())[0]

        return currency

    except Exception as e:
        logger.error(f"Currency detection failed for {city}: {e}")
        return "USD"
    
def get_currency_from_city(city: str) -> str:
    """
    Detect currency automatically using OpenTripMap + REST Countries API
    """

    try:
        api_key = config["api_keys"]["opentripmap"]

        geo_url = "https://api.opentripmap.com/0.1/en/places/geoname"

        geo_resp = requests.get(
            geo_url,
            params={"name": city, "apikey": api_key},
            timeout=10
        )

        geo_resp.raise_for_status()

        data = geo_resp.json()

        country_code = data.get("country")

        if not country_code:
            return "USD"

        # Get currency from REST Countries
        rest_url = f"https://restcountries.com/v3.1/alpha/{country_code}"

        rest_resp = requests.get(rest_url, timeout=10)

        rest_resp.raise_for_status()

        rest_data = rest_resp.json()

        currency = list(rest_data[0]["currencies"].keys())[0]

        return currency

    except Exception as e:
        logger.error(f"Currency detection failed for {city}: {e}")
        return "USD"
    
print(get_currency_from_city("Tokyo"))
print(get_currency_from_city("Paris"))
print(get_currency_from_city("Kolkata"))