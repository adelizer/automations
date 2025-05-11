"""
# streamlit-file-parser/app/main.py

This is a Streamlit application that allows users to select and parse files from a specified directory.
The application supports parsing text, markdown, PDF, and CSV files.

"""

import asyncio
import csv
from datetime import datetime

import streamlit as st
from deterministic_agent import run_agent
from utils.file_parser import (get_files_in_directory, parse_csv_file,
                               parse_markdown_file, parse_pdf_file,
                               parse_text_file)

PARENT_DIR = "/Users/mohamedadelabdelhady/workspace/automations/data"

def append_to_csv(file_name, file_path, word_count, summary):
    csv_file = "file_summary.csv"
    entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([file_name, file_path, entry_date, word_count, summary])

async def main():
    st.title("Idea Discovery Agent")

    # Directory selection
    directory = st.text_input("Enter the directory path:", value=PARENT_DIR)
    recursive = st.checkbox("Include subdirectories", value=False)

    if st.button("Load Files"):
        if directory:
            files = get_files_in_directory(directory, recursive)
            st.session_state["files"] = files
        else:
            st.error("Please enter a directory path.")

    # File selection
    if "files" in st.session_state:
        selected_files = st.multiselect("Select files to parse:", st.session_state["files"], default=st.session_state["files"], format_func=lambda x: x.split("/")[-1])

        if st.button("Parse Files"):
            parsed_content = {}
            # loop through selected files and parse them
            for file in selected_files:
                if file.endswith(".txt"):
                    content = parse_text_file(file)
                elif file.endswith(".md"):
                    content = parse_markdown_file(file)
                elif file.endswith(".pdf"):
                    content = parse_pdf_file(file)
                elif file.endswith(".csv"):
                    content = parse_csv_file(file)
                else:
                    content = "Unsupported file type."
        
                if content != "Unsupported file type.":
                    parsed_content[file] = content

            st.session_state["parsed_content"] = parsed_content
            
        # Display parsed content
    if "parsed_content" in st.session_state:
        file_to_view = st.selectbox("Select a file to view content:", list(st.session_state["parsed_content"].keys()))
        st.text_area("File Content:", st.session_state["parsed_content"][file_to_view], height=300)

    # Add a button for summarizing and updating the CSV
    if st.button("Summarize and Save to CSV"): 
        if "parsed_content" in st.session_state:
            for file, content in st.session_state["parsed_content"].items():
                if content != "Unsupported file type.":
                    word_count = len(content.split())
                    summary = await run_agent(content)
                    append_to_csv(file, file, word_count, summary)
            st.success("Summary saved to CSV.")
        else:
            st.error("No parsed content available to summarize.")


if __name__ == "__main__":
    asyncio.run(main())