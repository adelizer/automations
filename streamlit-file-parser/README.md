# Streamlit File Parser

This project is a Streamlit application that allows users to browse and select a folder, display all files in that folder with checkboxes for selection, and parse the selected files (text, markdown, or PDF). The application will indicate the success of the parsing operation by displaying the number of files parsed and the total word count.

## Project Structure

```
streamlit-file-parser
├── app
│   ├── main.py
│   └── utils
│       └── file_parser.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Create a Virtual Environment**

   To create a virtual environment, navigate to the project directory and run:

   ```
   python -m venv venv
   ```

2. **Activate the Virtual Environment**

   - On Windows:

     ```
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```
     source venv/bin/activate
     ```

3. **Install Dependencies**

   Install the required packages by running:

   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the Streamlit application, execute the following command in your terminal:

```
streamlit run app/main.py
```

This will start the Streamlit server and open the application in your default web browser.

## Dependencies

The following packages are required for this project:

- **streamlit**: For building the web application.
- **PyPDF2**: For parsing PDF files.
- **markdown**: For handling markdown files.
- **python-docx**: For parsing .docx files (if needed).
- **numpy**: Optional, for any numerical operations.

Make sure to install these packages in your virtual environment to ensure the application runs smoothly.