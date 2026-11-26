"""Settings shared by every exercise. Change a value here and it changes everywhere."""

from pathlib import Path

# The Gemini model every agent uses.
MODEL = "gemini-3.5-flash-lite"

# Hotels may use at most 80% of the total budget, which leaves room for the flight.
HOTEL_SHARE = 0.8

# The mock data: JSON files that imitate what travel APIs would return.
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
