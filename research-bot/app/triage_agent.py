import os
from agents import Agent, ItemHelpers, Runner, function_tool


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


orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="You are an expert orchestrator agent assistant. Your task is to help the user...",
    tools=[create_new_directory, save_markdown_to_file],
)
