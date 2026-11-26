"""Smoke test: if this agent says hi back, your setup works."""

from google.adk.agents import Agent

from tripmate.config import MODEL

root_agent = Agent(
    name="hello",
    model=MODEL,
    instruction="Greet the traveller in one short, friendly sentence.",
)
