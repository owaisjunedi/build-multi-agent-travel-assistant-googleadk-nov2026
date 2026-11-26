# Exercise 4 (capstone): The front desk

**Goal:** build a front desk for TripMate, like a hotel reception. A main agent, the **concierge**, greets the traveller, answers simple questions itself and passes everything else to the right helper:

- trip plans go to the **trip planner** (your agents from Exercise 3),
- restaurant questions go to the **food guide**,
- transport questions go to **getting around**.

Trip plans must still stay within budget and respect the local news.

**You'll learn:** how one agent can pass a question to another. You list the helpers in `sub_agents=[...]` and give each one a short `description` of what it does. The concierge reads those descriptions to decide who should answer, just like the AI reads a tool's docstring.

There are no TODOs this time. `agent.py` has an outline, and `CHEATSHEET.md` in the repo root has every pattern you need. If you get stuck, see [Hints](#hints) below.

## What to build

```
concierge  (root_agent: answers quick questions, routes the rest)
 ├─ trip_planner     the Ex 3 SequentialAgent + a description
 │    ├─ local_insider   → state["local_notes"]
 │    └─ planner_agent   + budget rule from tripmate/budget.py
 ├─ food_guide       get_restaurants, reads {local_notes?} {budget_eur?} {nights?}
 └─ getting_around   (level 2) get_transport, reads {local_notes?}
```

| Agent | What it does |
|---|---|
| `trip_planner` | Plans the trip: local notes first, then flights, a hotel within budget and a day-by-day plan. |
| `food_guide` | Recommends places to eat. Skips anything closed and keeps prices sensible for the budget. |
| `getting_around` | Explains how to get around. Warns about strikes and closures and offers alternatives. |
| `concierge` | Greets travellers, answers simple questions itself, and hands off planning, food and transport. |

Give every specialist a clear `description`: that's what the concierge reads to decide who to call.

`agent.py` already imports every tool you need from `tripmate/tools.py`, the budget rule from `tripmate/budget.py` and `MODEL` from `tripmate/config.py`. When ready, restart `adk web workshop` and pick `ex4_front_desk`.

## Levels

- **Level 1:** `trip_planner`, `food_guide` and the `concierge`. Pass tests 1–4.
- **Level 2:** add `getting_around`. Pass test 5.
- **Extras:** a `budget_tracker` that answers "How much of my €600 is left?" with a Python tool, your own specialist (weather, packing list), or a guardrail from the cheat sheet.

## Acceptance tests

Run them in order, in one session. Use the **Traces** tab to see which agent answered.

| # | Traveller says | Answered by | Passes if |
|---|---|---|---|
| 1 | "Hi! What can you help me with?" | concierge | It introduces the specialists |
| 2 | The test prompt | trip_planner | Within budget, avoids closures and red flags |
| 3 | "How do I say thank you in Catalan?" | concierge | "Gràcies!", no hand-off |
| 4 | "Where should we eat on day 5? Nothing fancy." | food_guide | Affordable, not the Boqueria (closed that day) |
| 5 | "How do we get around on day 4?" | getting_around | Mentions the metro strike, suggests bikes or walking |

Test prompt:

> I'm flying from Amsterdam to Barcelona for 4 nights. My total budget is €600. I love the beach and I want to stay close by! Plan my trip with flights, a hotel and a day-by-day plan.

## Tips

- `{local_notes?}` with a `?` means "empty if not in state yet" instead of an error.
- No reply and no error in `adk web`? `root_agent` isn't defined yet.
- Wrong specialist answering? Improve the descriptions first.
- "Already has a parent" error? An agent can have only one parent, so list `trip_planner` in one place only.

## Hints

Three hints, in the order you build. Open only the ones you need: click a hint to unfold it. Each one goes into `agent.py`, between `# START YOUR CODE HERE` and `# END YOUR CODE HERE`.

If the hints don't fold in your editor, read this README on GitHub or in your editor's Markdown preview.

<details>
<summary><b>Hint 1: the trip-planning team (paste this)</b></summary>

This is Exercise 3 again, so there's nothing new to learn by retyping it. The only changes: the `SequentialAgent` is now called `trip_planner` instead of `root_agent`, and it has a `description` for the concierge to read.

```python
local_insider = Agent(
    name="local_insider",
    model=MODEL,
    description="Knows local closures, events, strikes and beach conditions.",
    instruction="""Find the destination in the traveller's message and call
get_local_notes for it. Reply with one short line per day.""",
    tools=[get_local_notes],
    output_key="local_notes",
)

planner_agent = Agent(
    name="planner_agent",
    model=MODEL,
    description="Plans trips: flights, a hotel within budget, and a day-by-day plan.",
    instruction="""You are TripMate, a friendly travel assistant.
Use the tools to find flights and hotels, then suggest a trip
with a day-by-day plan. Stay within the traveller's budget.

Local notes for the trip dates:
{local_notes}

Never schedule anything the local notes say is closed or unsafe.""",
    tools=[search_flights, search_hotels, get_hotel_details, save_trip_details],
    after_tool_callback=enforce_budget,
)

trip_planner = SequentialAgent(
    name="trip_planner",
    description="Plans a complete trip: checks local notes, then finds flights "
    "and a hotel within budget and writes a day-by-day plan.",
    sub_agents=[local_insider, planner_agent],
)
```

To check it on its own, add `root_agent = trip_planner` as the last line for now, restart, and send the test prompt. Replace that line when you build the concierge.

</details>

<details>
<summary><b>Hint 2: the food guide (fill in the gaps)</b></summary>

The state lines are done. Write the description and finish the instruction yourself.

```python
food_guide = Agent(
    name="food_guide",
    model=MODEL,
    description="...",  # one sentence: which questions should come here?
    instruction="""...tell it to recommend places to eat using get_restaurants...
Local notes: {local_notes?}
Total trip budget: {budget_eur?} euros for {nights?} nights.
...tell it what to do about closed places and prices...""",
    tools=[get_restaurants],
)
```

The `?` matters. A traveller might ask about food before planning a trip, and then `local_notes` isn't in state yet.

For level 2, `getting_around` has the same shape, with `get_transport` and `{local_notes?}`.

</details>

<details>
<summary><b>Hint 3: the concierge (fill in the gaps)</b></summary>

The concierge has no tools. It has `sub_agents`, and it reads their descriptions to decide who gets each question.

```python
root_agent = Agent(
    name="concierge",
    model=MODEL,
    instruction="""...who is it? What does it answer itself?
What does it hand to a specialist?...""",
    sub_agents=[trip_planner, food_guide],  # add getting_around for level 2
)
```

Two things to check if a test fails:

- **Test 3 hands off or re-plans:** say in the instruction that quick general questions, like a phrase in the local language, are answered by the concierge itself.
- **A question goes to the wrong specialist:** make that specialist's `description` more specific.

</details>

Still stuck? The full answer is in `solutions/ex4_front_desk/agent.py`.
