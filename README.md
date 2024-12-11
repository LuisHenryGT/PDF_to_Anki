# Anki Deck Generator from PDF

## Overview

This project is a Flask-based web application that allows you to upload a PDF file (e.g., lecture notes, study guides, etc..) and automatically generate a set of flashcards in an Anki-compatible `.apkg` deck format. By leveraging a large language model (openAI API) for text analysis and card generation, this tool aims to streamline your study process: simply upload your notes as a PDF, and the app will produce flashcards you can instantly import into Anki, making your study sessions more effective and efficient.

**how it works:**
- **Upload PDF Notes:** The simple web interface allows users to upload a PDF document.
- **Text Extraction & Cleaning:** The app extracts text from the uploaded PDF and remove noise, excessive whitespace, and artifacts like page headers and footers.
- **Language Model Integration:** Using a prompt from `prompt.txt` and an API key from `apikey.txt`, the application calls a language model (OpenAI’s API) to transform the cleaned text into a set of flashcards in JSON format.
- **Anki Deck Creation:** The JSON-formatted flashcards are converted into an Anki deck file (`.apkg`), ready for you to download and import into your Anki desktop or mobile application.

## Project Structure

The project’s directory layout is as follows:

```
project_folder/
├─ static/
│  ├─ pdf-logo.svg
│  ├─ anki-logo.svg
│
├─ templates/
│  └─ index.html
│
├─ app.py
├─ helpers.py
├─ prompt.txt
├─ apikey.txt
└─ README.md
```

### File & Folder Details

1. **`static/` folder:**  
   This directory contains `pdf-logo.svg` and `anki-logo.svg`, used in the header of the web interface.

2. **`templates/` folder:**  
   Contains the HTML templates for the index page, which includes:
   - A header section displaying the PDF and Anki logos.
   - A simple form to upload a PDF file.
   
   Flask’s `render_template` function uses this file to return the main page to the user.

3. **`app.py`:**  
   This is the main Flask application file. It:
   - Initializes the Flask app.
   - Handles the `/` route (the main page), which allows the user to upload a PDF.
   - On form submission (POST request), it processes the PDF file, generates flashcards, and returns an `.apkg` file for download.
   
   Key points in `app.py`:
   - Checks if the uploaded file is indeed a PDF by verifying the file extension.
   - Calls functions from `helpers.py` to extract text, clean it, and run flashcard generation and deck creation.
   - Uses `return send_file(...)` to provide the generated Anki deck file as a downloadable response.

4. **`helpers.py`:**  
   This file encapsulates the core logic behind text extraction, transformation, and deck generation. It includes functions to:
   - **`extract_text_from_pdf(pdf_path)`:** Uses `pdfplumber` to open and extract text from each page of the uploaded PDF.
   - **`clean_extracted_text(text)`:** Cleans the extracted text by removing extra spaces, page numbers, and other non-useful artifacts.
   - **`read_file(filename)`:** A utility function to read content from a file (used to read prompts and API keys).
   - **`run_flashcard_generation(cleaned_text)`:** Uses the OpenAI API (or another language model provider) to send the cleaned text along with a system prompt and gets back JSON-formatted flashcards.
   - **`run_deck_creation(json_file, deck_name)`:** Takes the generated flashcards (in JSON) and creates an Anki deck file using `genanki`. This involves:
     - Defining a model (template) for the cards.
     - Creating an Anki deck object and adding notes for each flashcard.
     - Writing the deck out as a `.apkg` file.

   Dependencies:
   - `pdfplumber` for PDF text extraction.
   - `openai` for calling the language model API.
   - `genanki` to create the Anki deck.
   - `re` for regular expressions to clean text.
   
   The `run_flashcard_generation` function expects the language model to return JSON containing flashcards. For example, the JSON might look like this:
   ```json
   [
       {"front": "What is the definition of photosynthesis?", "back": "Photosynthesis is..."},
       {"front": "Name the three states of matter.", "back": "Solid, liquid, and gas."}
   ]
   ```
   
   These are then turned into Anki notes and compiled into a `.apkg` deck.

5. **`prompt.txt`:**  
   A text file containing the system prompt given to the language model. This prompt can instruct the model on how to structure the flashcards. By modifying this file, you can change the style, format, or complexity of the generated flashcards without altering your code.

6. **`apikey.txt`:**  
   A text file that stores your secret API key for the language model API. Storing it separately keeps your code clean and helps prevent you from accidentally sharing your keys. In a production environment, consider using environment variables or more secure methods of storing secrets.

7. **`index.html`:**  
   An HTML template that provides the user interface. It uses Bootstrap for simple styling and includes:
   - A header with logos.
   - A file upload form where users can submit their PDF.
   - A "Generate Flashcards" button that triggers the server-side logic in `app.py`.

## Running the Project

### Prerequisites

- **Python 3.8+** recommended.
- **Python Packages:** Make sure you have installed the required packages:
  ```bash
  pip install flask pdfplumber genanki openai requests
  ```
  
  Adjust this command if you already have some dependencies. `requests` may be required for certain API calls, and `openai` is needed to interact with the OpenAI API.

### Steps to Run Locally

1. **Set Up Your API Key:**  
   Place your language model API key into the `apikey.txt` file. For example, if using OpenAI:
   ```text
   sk-YourSecretAPIKeyHere
   ```

2. **Prepare Your Prompt:**  
   Edit `prompt.txt` if you want to customize the instructions given to the language model. For example:
   ```text
   You are a flashcard generator. Given a student's notes, produce a JSON array of objects with 'front' and 'back' fields for each flashcard...
   ```

3. **Start the Flask Server:**
   ```bash
   python app.py
   ```
   
   By default, Flask runs the server at `http://127.0.0.1:5000`. Open this URL in your web browser.

4. **Upload a PDF and Generate Flashcards:**
   - On the main page, select a PDF file from your computer.
   - Click "Generate Flashcards".
   - The application will:
     - Extract and clean the text from the PDF.
     - Call the language model to produce flashcards.
     - Convert those flashcards into an Anki deck.
     - Prompt you to download the resulting `.apkg` file.

5. **Import into Anki:**
   Open Anki on your computer and import the `.apkg` file. You will see a new deck with the flashcards generated from your PDF notes.

## Customization & Advanced Use

- **Modifying the Prompt:**  
  Editing `prompt.txt` allows you to change how the language model interprets and formats the flashcards. For instance, you can ask for multiple-choice questions, definitions only, or advanced formatting.

- **Changing the Deck Name:**  
  In `app.py` or `helpers.py`, you can alter the `deck_name` used in `run_deck_creation()`. By default, it’s hard-coded to `"Deck_generated"`, but you can dynamically set this name based on user input or file names.

- **Styling the Interface:**  
  The `index.html` file uses a minimal amount of Bootstrap styling. For a better user experience, add a custom CSS file to `static/` and link it in `index.html`, or enhance the form’s layout, colors, and branding.

- **Authentication & Deployment:**
  For production use:
  - Keep `apikey.txt` out of your version control or add it to `.gitignore`.
  - Consider using environment variables (e.g., `export OPENAI_API_KEY="..."`
    in your system) and reading from `os.environ` instead of a plain text file.
  - Deploy the Flask app to a production server (such as Gunicorn with Nginx, or render.com, Heroku, etc.) for broader access.

## Troubleshooting

- **No Output or Empty Deck:**  
  If the model returns no flashcards, verify that:
  - The prompt in `prompt.txt` is correct and instructs the model to output JSON.
  - The `apikey.txt` contains a valid API key.
  - The text extraction worked properly (check the console or add print statements).

- **API Key or Rate Limiting Errors:**
  If you encounter authentication errors or rate limit issues, ensure you have a valid key and have not exceeded your rate limits. Double-check the correctness of your API key in `apikey.txt`.

- **JSON Parsing Errors:**
  If the returned JSON from the model cannot be parsed, check:
  - The prompt to ensure the model is instructed clearly to return valid JSON.
  - The raw output by printing the response in `helpers.py`.

## Conclusion

This project is a starting point for automating the creation of flashcards from PDFs. By coupling Flask, text extraction, an AI-driven summarization/flashcard generation model, and the Anki deck creation process, you have a powerful educational tool. You can customize the prompts, improve the front-end, add error handling, or integrate other language models. With this setup, turning your study materials into ready-to-go flashcards has never been easier.

---

This `README.md` is designed to guide you through understanding and running the project, as well as offering insights into customization and troubleshooting.
