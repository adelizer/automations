import os
from typing import List, Tuple
import csv


def parse_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def parse_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def parse_pdf_file(file_path):
    import pypdf

    content = ""
    with open(file_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            content += page.extract_text() + "\n"
    return content


def parse_csv_file(file_path):
    content = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            content.append(", ".join(row))
    return "\n".join(content)


def count_words(content):
    words = content.split()
    return len(words)


def get_files_in_directory(directory: str, recursive: bool = False):
    """
    Get a list of files in a directory.

    Args:
        directory (str): The directory path.
        recursive (bool): Whether to include subdirectories.

    Returns:
        List[str]: List of file paths.
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".txt", ".md", ".pdf", ".csv")):
                file_list.append(os.path.join(root, file))
        if not recursive:
            break
    return file_list


def parse_files(selected_files: List[str]) -> Tuple[int, int]:
    """
    Parse the selected files and count the total words.

    Args:
        selected_files (List[str]): List of selected file names to parse.

    Returns:
        Tuple[int, int]: Total word count and number of files parsed.
    """
    total_words = 0
    parsed_count = 0

    for file_name in selected_files:
        file_path = os.path.join(file_name)
        print(f"Parsing file: {file_name}")
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    total_words += len(content.split())
                    parsed_count += 1
            except Exception as e:
                print(f"Error parsing file {file_name}: {e}")

    return total_words, parsed_count
