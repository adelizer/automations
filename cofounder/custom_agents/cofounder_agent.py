import os
import asyncio
from agents import Agent, function_tool, Runner

from cofounder.custom_agents.planner_agent import (
    WebSearchItem,
    WebSearchPlan,
    planner_agent,
)
from cofounder.custom_agents.search_agent import search_agent
from cofounder.custom_agents.writer_agent import writer_agent


# create a function to save content to markdown file but to append to the file
def save_markdown(content: str, file_name: str):
    """
    Save markdown content to a file.

    Args:
        content (str): The markdown content to save.
        file_name (str): The name of the file to save the content to.
    """
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)


@function_tool
def save_markdown_to_file(content: str, file_name: str):
    """
    Save markdown content to a file.

    Args:
        content (str): The markdown content to save.
        file_name (str): The name of the file to save the content to.
    """
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


@function_tool
def create_new_directory(directory_name: str):
    """
    Create a new directory if it doesn't exist.


    Args:
        directory_name (str): The name of the directory to create.
    """
    directory_path = os.path.join(os.getcwd(), directory_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")


async def search(item: WebSearchItem) -> str | None:
    input = f"Search term: {item.query}\nReason for searching: {item.reason}"
    try:
        result = await Runner.run(
            search_agent,
            input,
        )
        return str(result.final_output)
    except Exception:
        return None


async def perform_searches(search_plan: WebSearchPlan) -> list[str]:
    num_completed = 0
    tasks = [asyncio.create_task(search(item)) for item in search_plan.searches]
    results = []
    for task in asyncio.as_completed(tasks):
        result = await task
        if result is not None:
            results.append(result)
        num_completed += 1
        print(f"Completed {num_completed}/{len(tasks)} searches.")
    return results


async def write_report(query: str, search_results: list[str]) -> str:
    """
    Write a report based on the search results.

    Args:
        query (str): The query for which the report is generated.
        search_results (list[str]): The search results to include in the report.

    Returns:
        str: The generated report.
    """
    input = f"Original query: {query}\nSummarized search results: {search_results}"
    report = await Runner.run(
        writer_agent,
        input,
    )
    return report


@function_tool
async def create_business_plan(query: str) -> str:
    """
    Create a business plan based on the provided initial idea.

    Args:
        query (str): The query to create a business plan for.

    Returns:
        str: The generated business plan.
    """
    search_plan = await Runner.run(
        planner_agent,
        f"Query: {query}",
    )

    search_results = await perform_searches(search_plan.final_output_as(WebSearchPlan))

    report = await write_report(query=query, search_results=search_results)
    print("\n\n=====REPORT=====\n\n")
    print(f"Report: {report.markdown_report}")
    print("\n\n=====FOLLOW UP QUESTIONS=====\n\n")
    follow_up_questions = "\n".join(report.follow_up_questions)
    print(f"Follow up questions: {follow_up_questions}")

    return report


cofounder_agent = Agent(
    name="CofounderAgent",
    instructions="You are an expert co-founder agent assistant. Your task is to help the user with their startup idea. ",
    tools=[create_business_plan, create_new_directory, save_markdown_to_file],
)
