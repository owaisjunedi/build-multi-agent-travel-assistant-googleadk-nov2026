# Exercise 3: A team with a fixed order

**Goal:** make TripMate's plan respect what's happening in Barcelona that week. Sagrada Família is closed on day 2, the beaches have a jellyfish warning (red flag) on days 3 and 4, and there's a metro strike on day 4. A single agent often forgets to check, so you split TripMate into two agents that always run in the same order:

1. **Local Insider:** checks the local news.
2. **Planner:** plans the trip using that news.

**You'll learn:**
- **`SequentialAgent`:** runs agents one after another, always in the order you choose. Your code decides the order, not the AI.
- **`output_key`:** saves an agent's answer in state (the notebook from Exercise 2). Writing `{local_notes}` in another agent's instruction pastes that answer in.

## What to do

Your work is in `agent.py`. You now also import `get_local_notes` from `tripmate/tools.py`, and the budget rule from Exercise 2 from `tripmate/budget.py`.

1. **TODO 1:** create `local_insider`, an agent that looks up the local notes and saves its reply with `output_key`.
2. **TODO 2** (bottom of the file): make `root_agent` a `SequentialAgent` that runs `local_insider`, then `planner_agent`.
3. **TODO 3** (inside `planner_agent`): put `{local_notes}` in the planner's instruction and tell it what to do with them.

Restart `adk web workshop` and pick `ex3_fixed_order`.

## Check it

Send the test prompt in 3 new sessions:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach and I want to stay close by! Plan my trip with flights, a hotel and a day-by-day plan.

- No Sagrada Família on day 2, no beach on days 3 and 4, no metro on day 4.
- Still within budget.
- **Traces** tab: does `local_insider` run first every time?
- **State** tab: is `local_notes` there?

## Think about

- What would happen if you swapped the order?
- The order is guaranteed by code. Is following the notes guaranteed too?

Stuck? See `solutions/ex3_fixed_order/agent.py`.
