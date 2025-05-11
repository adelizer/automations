import asyncio

from pydantic import BaseModel

from agents import Agent, Runner, trace

properties = """
- Idea Name
- Description
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

product_stratgist = Agent(
    name="Product Strategist and Researcher",
    instructions=f"You are an expert product strategist and researcher. Your task is to analyze potential ideas for a SaaS application. Focus on identifying pain points, unmet needs, feature requests, inefficiencies, or trends. For the given idea, fill out the following properties in JSON format {properties}",
    tools=[],
)
