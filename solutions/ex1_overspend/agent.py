from google.adk.agents import Agent

from tripmate.config import MODEL
from tripmate.tools import get_hotel_details, search_flights, search_hotels

# Example: an agent with one tool. It's about the weather, not travel,
# so don't copy it as is. You hand the function to the agent,
# and the model decides when to call it.
#
#     def get_weather(city: str) -> dict:
#         """Gets today's weather for a city."""
#         return {"status": "success", "forecast": "sunny, 24°C"}
#
#     weather_agent = Agent(
#         name="weather_bot",
#         model=MODEL,
#         instruction="You answer questions about the weather. Use the get_weather tool.",
#         tools=[get_weather],
#     )


# TODO: create root_agent, this Agent should have:
#   - name: "tripmate"
#   - model: MODEL (imported above from tripmate/config.py)
#   - instruction: describe TripMate, a friendly travel assistant. Tell it to use
#     the tools to find flights and hotels, suggest a trip with a day-by-day plan,
#     and stay within the traveller's budget.
#   - tools: the three functions imported above
#
# The variable you assign your Agent to must be called root_agent, because
# that's the name adk web looks for when it loads this file.

# START YOUR CODE HERE
root_agent = Agent(
    name="tripmate",
    model=MODEL,
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.""",
    tools=[search_flights, search_hotels, get_hotel_details],
)
# END YOUR CODE HERE
