"""The budget rule from Exercise 2, used from Exercise 3 on. Nothing to change here."""

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from .config import HOTEL_SHARE
from .tools import real_cost_per_night


def save_trip_details(nights: int, budget_eur: int, tool_context: ToolContext) -> dict:
    """Saves the trip length and total budget. Call this before searching for hotels.

    Args:
        nights: How many nights the traveller is staying.
        budget_eur: The traveller's total budget for the whole trip, in euros.
    """
    # Validate trip details before saving them.
    if nights <= 0 or budget_eur <= 0:
        return {"status": "error", "message": "Budget and nights must be positive."}

    tool_context.state["nights"] = nights
    tool_context.state["budget_eur"] = budget_eur
    return {"status": "saved"}


def enforce_budget(
    tool: BaseTool, args: dict, tool_context: ToolContext, tool_response: dict
) -> dict | None:
    """Runs after every tool call. Hides hotels the traveller can't afford,
    in search results and in hotel details.

    It checks the real cost from our data, not the prices the model saw.

    Returning None keeps the tool's result as it is.
    Returning a dict replaces what the model sees.
    """
    hotel_tools = ("search_hotels", "get_hotel_details")
    if tool.name not in hotel_tools or tool_response.get("status") != "success":
        return None  # leave other tools, and errors, alone

    budget = tool_context.state.get("budget_eur")
    nights = tool_context.state.get("nights")
    if not budget or not nights:
        return {
            "status": "error",
            "message": "Ask for the budget and number of nights, "
            "then call save_trip_details.",
        }

    max_per_night = budget * HOTEL_SHARE / nights

    # get_hotel_details can reach the same data, so it needs the same rule.
    if tool.name == "get_hotel_details":
        hotel_name = tool_response["hotel"]["name"]
        hotel_cost = real_cost_per_night(hotel_name)
        if hotel_cost > max_per_night:
            return {
                "status": "error",
                "message": f"{hotel_name} costs €{hotel_cost:.0f}/night incl. fees, "
                f"over this trip's limit of €{max_per_night:.0f}/night. "
                "Tell the traveller, and suggest a hotel from search_hotels instead.",
            }
        return None

    affordable = [
        hotel
        for hotel in tool_response["hotels"]
        if real_cost_per_night(hotel["name"]) <= max_per_night
    ]

    # Add the real nightly cost, so the model's sums include the fees.
    affordable = [
        {**hotel, "real_cost_per_night": real_cost_per_night(hotel["name"])}
        for hotel in affordable
    ]

    return {
        "status": "success",
        "hotels": affordable,
        "note": f"Only hotels up to €{max_per_night:.0f}/night incl. fees are shown. "
        "Use real_cost_per_night for totals: it includes the fees.",
    }
