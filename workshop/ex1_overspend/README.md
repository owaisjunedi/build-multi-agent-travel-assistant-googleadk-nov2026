# Exercise 1: Build it, watch it overspend

**Goal:** build your first AI travel assistant, TripMate. It searches flights and hotels and plans a trip. Then you test it and find that it often goes over the traveller's budget.

**You'll learn:** how to make an agent from three things: a model (the AI), an instruction (what you want it to do) and tools (Python functions it can call, such as "search hotels"). You don't call the tools yourself: the AI decides when to use them.

## What to do

1. [Optional] Read `tripmate/tools.py` at the repo root to see the tools. The mock data is in `data/` at the repo root.
2. In `agent.py`, follow the TODO: create `root_agent`, using the weather example above it as a guide to the syntax. Give it a name, the model, an instruction and the three tools.
3. From the repo root, run `adk web workshop`, open http://localhost:8000, pick `ex1_overspend` and say hi.

## Break it

Send the test prompt 3 times, each in a new session:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach and I want to stay close by! Plan my trip with flights, a hotel and a day-by-day plan.

For each run:

- In the **Events** tab, which tools did it call? Did it check `get_hotel_details` for the hotel it picked?
- Look up the hotel's `fee_at_checkin` (per night) in `data/hotels.json`. Real total = `(price_per_night + fee_at_checkin) × nights + flight`.
- Did it stay within €600? Did it mention the fees?

## Think about

- We asked it to stay within budget. Why didn't it?
- Would "NEVER exceed the budget!!!" fix it? How sure would you be?

Stuck? See `solutions/ex1_overspend/agent.py`.
