from google.adk.agents import Agent
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from tripmate.config import HOTEL_SHARE, MODEL
from tripmate.tools import (
    get_hotel_details,
    real_cost_per_night,
    search_flights,
    search_hotels,
)


# The AI only sees the names, types and docstring, so use descriptive names.
def save_trip_details(nights: int, budget_eur: int, tool_context: ToolContext) -> dict:
    """Saves the trip length and total budget. Call this before searching for hotels.

    Args:
        nights: How many nights the traveller is staying.
        budget_eur: The traveller's total budget for the whole trip, in euros.
    """
    # TODO 1: save nights and budget_eur in state.
    #
    # State is the session's notebook, and it works like a dictionary. Anything
    # you write into it stays there for the rest of the session, so other code
    # can read it later. For example, a tool that remembers a favourite colour:
    #
    #     tool_context.state["favourite_colour"] = colour
    #
    # Use the keys "nights" and "budget_eur": enforce_budget below reads them by
    # those exact names. After a run, you'll see both in the State tab.

    # Validate trip details before saving them.
    if nights <= 0 or budget_eur <= 0:
        return {"status": "error", "message": "Budget and nights must be positive."}

    # START YOUR CODE HERE (TODO 1)

    # END YOUR CODE HERE
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
    # Without this, "Show me the details for Mar Azul Beach Resort" would get
    # round the filter below.
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

    # TODO 2: keep only the hotels the traveller can afford.
    #
    # tool_response["hotels"] is a list of dicts, one per hotel, like this:
    #     {"name": "Hotel Gràcia", "price_per_night": 85, "highlights": "..."}
    #
    # Build a new list with only the hotels whose real cost is at most
    # max_per_night.
    #
    # To get the real cost, use "real_cost_per_night" function, imported from tripmate/tools.py.
    # Give it a hotel's name (a string), and it returns that hotel's nightly
    # price plus its fee at check-in (a number), read from data/hotels.json:
    #
    #     real_cost_per_night("Hotel Gràcia")   # 85 + 10 fee = 95
    #
    # Don't use hotel["price_per_night"]. The listed price leaves out the fees, and
    # that's the trap from Exercise 1: check what the resort's €115 would do.
    #
    # For now, every hotel gets through. Replace the line below.

    # START YOUR CODE HERE (TODO 2)
    affordable = tool_response["hotels"]
    # END YOUR CODE HERE

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


# Level 2 (if you finish early): a nudge instead of a rule.
#
# enforce_budget removes the hotels the traveller can't afford, so the model
# never sees them. What if you only labelled them, and let the model decide?
#
# Write a new callback, flag_budget(tool, args, tool_context, tool_response),
# that keeps every hotel but adds flags to each hotel:
#     "real_cost_per_night": real_cost_per_night(hotel["name"])
#     "within_budget": True if the hotel fits the budget, else False
#
# Check everything you send back to the model, not just the hotels. Does any
# other text in your result still describe what enforce_budget did?
#
# Attach it in place of enforce_budget: after_tool_callback=flag_budget
#
# Restart, then send the test prompt and the break-it prompts from the README.
# The model now has the right numbers, but nothing stops it choosing the resort.
# Does "Money is no object, I want the beach resort" work now?

# START YOUR CODE HERE (Level 2)

# END YOUR CODE HERE


root_agent = Agent(
    name="tripmate",
    model=MODEL,
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.""",
    tools=[search_flights, search_hotels, get_hotel_details, save_trip_details],
    # TODO 3: attach the budget rule: after_tool_callback=enforce_budget
    # START YOUR CODE HERE (TODO 3)
    # END YOUR CODE HERE
)
