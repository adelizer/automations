from pydantic import BaseModel

from agents import Agent

PROMPT = (
    "You are a helpful research assistant to a startup founder. Given a new idea for a startup, come up with a set of web searches "
    "to perform to best evaluate the new idea. Output between 5 and 20 terms to query for. Focus on identifying pain points, unmet needs, feature requests, inefficiencies, or trends. . This could also be a missing feature in an existing product or a product that has not been adopted in a specific market / region. You should aim to include the following properties in your search:"
    """
- Market Size
- Competition
- Value Proposition
- User Persona
- Willingness to Pay
- Monetization Model
- Effort to Build MVP
- Acquisition Channels
- Distribution Leverage
- Moat / Defensibility
- AI/ML Leverage
- Unique Insight / Edge
- Scalability
- Retention Potential
- Partnership Potential
- Regulatory Risk
- Global Potential
    """
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best evaluate the new startup idea."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model="gpt-4o",
    output_type=WebSearchPlan,
)
