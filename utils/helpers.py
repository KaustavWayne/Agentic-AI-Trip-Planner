import re
import requests
from tavily import TavilyClient

from utils.config_loader import load_config
from exception.exceptionhandling import APICallFailed
from logger.logging import logger


config = load_config()
tavily_client = TavilyClient(api_key=config["api_keys"]["tavily"])


# --------------------------------------------------
# WEB SEARCH
# --------------------------------------------------
def search_web(query: str) -> str:
    """Perform web search using Tavily."""

    try:
        response = tavily_client.search(
            query=query,
            max_results=config["tools"]["tavily_max_results"]
        )

        results = response.get("results", [])

        formatted = []

        for i, r in enumerate(results, 1):
            formatted.append(
                f"{i}. {r.get('title')}\n"
                f"{r.get('url')}\n"
                f"{r.get('content','')[:200]}\n"
            )

        return "\n".join(formatted)

    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        raise APICallFailed("Web search failed") from e


# --------------------------------------------------
# WEATHER
# --------------------------------------------------
def get_weather(city: str) -> str:
    """Get current weather summary."""

    try:
        url = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={config['api_keys']['openweathermap']}"
            f"&units={config['tools']['weather_units']}"
        )

        resp = requests.get(url, timeout=15)
        resp.raise_for_status()

        data = resp.json()
        forecast = data.get("list", [])[0]

        temp = forecast["main"]["temp"]
        humidity = forecast["main"]["humidity"]
        desc = forecast["weather"][0]["description"]

        return "\n".join([
            f"City: {city}",
            f"Temperature: {temp}°C",
            f"Humidity: {humidity}%",
            f"Weather: {desc}"
        ])

    except Exception as e:
        logger.error(f"Weather API failed for {city}: {e}")
        raise APICallFailed("Weather fetch failed") from e


# --------------------------------------------------
# PLACES
# --------------------------------------------------
def find_places(city: str, category: str = "attractions") -> str:
    """Discover top tourist attractions using OpenTripMap."""

    try:
        api_key = config["api_keys"]["opentripmap"]

        # Step 1 — get city coordinates
        geo_url = "https://api.opentripmap.com/0.1/en/places/geoname"

        geo_resp = requests.get(
            geo_url,
            params={"name": city, "apikey": api_key},
            timeout=10
        ).json()

        lat = geo_resp["lat"]
        lon = geo_resp["lon"]

        # Step 2 — search attractions
        places_url = "https://api.opentripmap.com/0.1/en/places/radius"

        resp = requests.get(
            places_url,
            params={
                "radius": 10000,
                "lon": lon,
                "lat": lat,
                "limit": 20,
                "rate": 2,   # Only popular places
                "kinds": "interesting_places,cultural,architecture,museums",
                "apikey": api_key
            },
            timeout=10
        ).json()

        places = []

        for p in resp.get("features", []):

            props = p.get("properties", {})
            name = props.get("name", "").strip()

            # Filter bad names
            if not name:
                continue

            if len(name) < 3:
                continue

            if name.lower() in ["fountain", "statue", "wall", "tower"]:
                continue

            places.append(name)

        # remove duplicates
        places = list(dict.fromkeys(places))

        if not places:
            return "No attractions found"

        # return top 10
        return "\n".join(places[:10])

    except Exception as e:
        logger.error(f"OpenTripMap failed for {city}: {e}")
        raise APICallFailed("Places search failed")

# Get Currency from countries

import pycountry
import requests

def get_currency_and_symbol(city: str) -> dict:
    """
    Dynamically detect currency code AND symbol using OpenTripMap + REST Countries.
    Returns: {"code": "JPY", "symbol": "¥"}
    """
    # Default fallbacks
    fallback = {"code": "USD", "symbol": "$"}

    try:
        api_key = config["api_keys"]["opentripmap"]
        geo_url = "https://api.opentripmap.com/0.1/en/places/geoname"

        geo_resp = requests.get(geo_url, params={"name": city, "apikey": api_key}, timeout=10)
        geo_resp.raise_for_status()
        
        country_code = geo_resp.json().get("country")

        # Hit REST Countries to get dynamic currency data
        if country_code:
            rest_url = f"https://restcountries.com/v3.1/alpha/{country_code.upper()}"
        else:
            # Fallback directly to city name if OpenTripMap doesn't know the country
            rest_url = f"https://restcountries.com/v3.1/name/{city}"

        rest_resp = requests.get(rest_url, timeout=10)
        rest_resp.raise_for_status()
        rest_data = rest_resp.json()

        currencies = rest_data[0].get("currencies", {})
        if not currencies:
            return fallback

        # Extract the key (e.g., "JPY") and the symbol (e.g., "¥") dynamically
        currency_code = list(currencies.keys())[0]
        currency_symbol = currencies[currency_code].get("symbol", "")

        return {
            "code": currency_code,
            "symbol": currency_symbol
        }

    except Exception as e:
        logger.error(f"Dynamic currency lookup failed for {city}: {e}")
        return fallback
    
# Resolve destination using LLM and generate itinerary
from groq import Groq


def resolve_destination_with_llm(destination: str):
    """
    Detect if destination is a country or city.
    If country → return top tourist cities
    If city → return the same city
    """

    client = Groq(api_key=config["api_keys"]["groq"])

    prompt = f"""
You are a travel expert.

If the input is a COUNTRY return top 3 tourist cities.
If the input is already a CITY return the same city.

Return ONLY comma separated city names.

Examples:
India -> Kolkata, Delhi, Agra, Jaipur
France -> Paris, Nice, Lyon
Japan -> Tokyo, Kyoto, Osaka
England -> London, Manchester, Liverpool
Italy -> Rome, Venice, Florence
France -> Paris, Nice, Lyon

Destination: {destination}
"""

    response = client.chat.completions.create(
        model=config["llm"]["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=50
    )

    cities = response.choices[0].message.content.strip()

    return [c.strip() for c in cities.split(",")]

# Generate itinerary based on discovered places
# --------------------------------------------------
# GENERATE ITINERARY
# --------------------------------------------------
def generate_itinerary(destination: str, days: int) -> str:
    """Generate smart travel itinerary using Groq LLM."""
    try:
        client = Groq(api_key=config["api_keys"]["groq"])

        # 1. Resolve destination
        cities = resolve_destination_with_llm(destination)
        destination = cities[0]

        # 2. Detect local currency & symbol dynamically
        currency_info = get_currency_and_symbol(destination)
        currency_code = currency_info["code"]
        currency_symbol = currency_info["symbol"]

        # 3. Get tourist attractions
        places_raw = find_places(destination)

        filtered_places = [
            p for p in places_raw.split("\n")
            if len(p) > 4
            and "memorial" not in p.lower()
            and "plaque" not in p.lower()
            and "stone" not in p.lower()
            and "wall" not in p.lower()
            and "tower" not in p.lower()
        ]
        places = "\n".join(filtered_places[:10])

        # 4. Weather information
        weather = get_weather(destination)

        # 5. Budget estimation
        budget_data = estimate_trip_expenses(
            destination,
            days,
            currency=currency_code
        )

        total_local = budget_data.get("total_estimate_local", 0)
        total_usd = budget_data.get("total_estimate_usd", 0)

        budget_text = f"{currency_symbol}{total_local:,.0f} {currency_code} (≈ ${round(total_usd,2)} USD)"

        # 6. Extra web research
        research = search_web(f"top tourist attractions in {destination}")

        prompt = f"""
You are a professional travel planner.

Create a {days}-day travel itinerary for {destination}.

Cities included in the trip:
{", ".join(cities)}

Use the following information.

Weather:
{weather}

Top Tourist Attractions:
{places}

Travel Research:
{research}

Budget Information:
{budget_text}

IMPORTANT RULES:
- You MUST show the exact budget above
- DO NOT create a new budget
- DO NOT convert currencies yourself
- Always display both currencies exactly as written

Instructions:
- Plan exactly 2 attractions per day
- Provide short descriptions
- If multiple cities exist, distribute days logically
- Use markdown headings
"""

        response = client.chat.completions.create(
            model=config["llm"]["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Itinerary generation failed for {destination}: {e}")
        raise APICallFailed("Itinerary generation failed")

# --------------------------------------------------
# CURRENCY
# --------------------------------------------------
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert currency using ExchangeRate API."""

    try:
        api_key = config["api_keys"]["exchangerate"]

        url = (
            f"https://v6.exchangerate-api.com/v6/"
            f"{api_key}/pair/{from_currency}/{to_currency}/{amount}"
        )

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":
            raise ValueError(data.get("error-type"))

        return float(data["conversion_result"])

    except Exception as e:
        logger.error(f"Currency conversion failed: {e}")
        raise APICallFailed("Currency conversion failed") from e


# --------------------------------------------------
# EXPENSE ESTIMATOR
# --------------------------------------------------
def estimate_trip_expenses(
    destination: str,
    days: int,
    travelers: int = 1,
    budget_level: str = "moderate",
    currency: str = "INR"
) -> dict:
    """Estimate trip expenses."""

    try:

        daily_cost = {
            "budget": 60,
            "moderate": 130,
            "luxury": 300
        }

        avg_daily_usd = daily_cost.get(budget_level.lower(), 130)

        total_usd = avg_daily_usd * days * travelers
        total_local = convert_currency(total_usd, "USD", currency)

        return {
            "destination": destination,
            "days": days,
            "travelers": travelers,
            "budget_level": budget_level,
            "daily_estimate_usd": avg_daily_usd,
            "total_estimate_usd": total_usd,
            "total_estimate_local": round(total_local, 2),
            "currency": currency
        }

    except Exception as e:
        logger.error(f"Expense estimation failed for {destination}: {e}")
        raise APICallFailed("Expense estimation failed") from e