import asyncio

from pydantic import BaseModel

from agents import Agent, Runner, trace

product_stratgist = Agent(
    name="Product Strategist",
    instructions="You are an expert product strategist. Your task is to analyze the following content and extract potential ideas for a SaaS application. Focus on identifying pain points, unmet needs, feature requests, inefficiencies, or trends. This could also be a missing feature in an existing product or a product that has not been adopted in a specific market / region. Provide a list of ideas with a brief description for each.",
)


async def run_agent(content: str):
    with trace("Deterministic Product Strategist Agent"):
        # Create a new agent
        agent = product_stratgist

        # Generate initial list of ideas
        initial_ideas = await Runner.run(agent, content)
        print("Initial Ideas:", initial_ideas)
    return initial_ideas
