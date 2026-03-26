import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastmcp import FastMCP
from utils.helpers import (
    search_web,
    get_weather,
    find_places,
    convert_currency,
    estimate_trip_expenses,
    generate_itinerary
)
from logger.logging import logger
from utils.config_loader import load_config

# Load config
config = load_config()

# Create MCP Server - Only pass 'name' (description is not supported anymore)
mcp = FastMCP(
    name=config["mcp"]["name"]
    # description removed - it causes error in current fastmcp
)

@mcp.tool
def web_research(query: str) -> str:
    """Perform comprehensive web research for trip planning (best time, visa, safety, tips, etc.)."""
    return search_web(query)

@mcp.tool
def get_city_weather(city: str) -> str:
    """Get current weather and short-term forecast for any city."""
    return get_weather(city)

@mcp.tool
def discover_places(city: str, category: str = "attractions") -> str:
    """Discover top attractions, restaurants, landmarks etc. using Foursquare."""
    return find_places(city, category)

@mcp.tool
def convert_money(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert currency for accurate budget planning."""
    return convert_currency(amount, from_currency, to_currency)

@mcp.tool
def estimate_expenses(
    destination: str,
    days: int,
    travelers: int = 1,
    budget_level: str = "moderate",
    currency: str = "INR"
) -> dict:
    """Estimate detailed trip expenses including total cost breakdown."""
    return estimate_trip_expenses(destination, days, travelers, budget_level, currency)

@mcp.tool
def create_itinerary(destination: str, days: int) -> str:
    """Generate a day-by-day travel itinerary."""
    return generate_itinerary(destination, days)


if __name__ == "__main__":
    logger.info("Starting Trip Planner MCP Server")
    mcp.run()