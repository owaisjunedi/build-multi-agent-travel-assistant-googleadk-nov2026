"""Loads the mock data from the data/ folder once, for every exercise."""

import json

from .config import DATA_DIR


def load_dataset(name: str) -> dict:
    """Reads data/<name>.json and returns its contents."""
    return json.loads((DATA_DIR / f"{name}.json").read_text(encoding="utf-8"))


FLIGHTS = load_dataset("flights")
HOTELS = load_dataset("hotels")
LOCAL_NOTES = load_dataset("local_notes")
RESTAURANTS = load_dataset("restaurants")
TRANSPORT = load_dataset("transport")
