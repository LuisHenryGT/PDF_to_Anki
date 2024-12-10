# Project Overview

This project is a simple Flask-based web application that demonstrates how to integrate a language model’s capabilities within a web interface. It uses a carefully structured folder setup, modular code organization, and minimalistic templates to present a clean, functional user experience. The application reads in a prompt from a text file, uses an external API key for authentication, and then displays results returned by a language generation model. The user-facing interface is built in HTML and styled with simple static assets. The key goal of this project is to show a clear pipeline: reading input data (prompt and keys), generating text output using helper functions, and rendering that output for display in a web browser.

## Key Features

- **Flask-based Web Server:** The core of the application runs on Flask, a lightweight Python framework. It handles routing, request processing, and response generation.
- **Separation of Concerns:**
  - `app.py` is the main entry point, handling the web server logic, importing helper functions, and defining routes.
  - `helpers.py` contains all the core logic used by the application—reading from files, calling language models, and processing responses.
- **Structured Data Files:**
  - `prompt.txt` contains the prompt template that you feed into your language model. This helps separate content from logic.
  - `apikey.txt` stores a single secret key that authenticates requests to an external language model API. Storing it separately from code helps keep the codebase clean and allows for easy key rotation.
- **Static and Template Directories:**
  - `static/` holds images and logos that appear in the frontend.
  - `templates/` contains the `index.html` file that defines the structure and presentation of the web page.

## Project Structure

The directory layout of the project is as follows:

```
project_folder/
├─ static/
│  ├─ logo1.png
│  ├─ logo2.png
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

### Explanation of Each Component

1. **`app.py`**
   This is the main Python application file. It imports and configures Flask, loads helper functions, and defines the route(s) for the web application. Specifically:
   - It sets up a Flask `app` instance.
   - It defines the root endpoint (`/`) which serves the main page.
   - On requests to the index route, it might use functions from `helpers.py` to read the `prompt.txt` file, communicate with the language model API using the `apikey.txt` for authentication, and then render results on the `index.html` template.

2. **`helpers.py`**
   The `helpers.py` file is dedicated to the application’s logic and reusable code blocks. Within this file, you might find functions to:
   - **Read the API Key:** A function that opens `apikey.txt` and extracts the key needed for API authentication.
   - **Load Prompt Data:** A function that reads `prompt.txt` and returns the prompt content.
   - **Call the External API (Language Model):** Another function could use the prompt and API key to send a request to a language model’s endpoint (e.g., OpenAI’s GPT model). The function returns the generated text or keys back to `app.py`.
   - **Validation or Utilities:** Additional helper methods might include formatting returned text, handling exceptions if the API call fails, or caching results.

3. **`templates/index.html`**
   This file defines the front-end structure of the web application. It typically includes:
   - A basic HTML structure, with a `<head>` and `<body>`.
   - References to static assets such as logos from the `static` folder.
   - A form or display area where the generated text from the language model is shown.
   - Optional placeholders for dynamic content that are replaced by Flask’s `render_template` function in `app.py`.

4. **`static/` folder**
   This directory contains static files such as images, logos, or style sheets. In this project, you have two logos that might be displayed on the front page or as part of the site branding. These files do not change dynamically and can be referenced directly in the HTML template or through Flask’s `url_for('static', filename='...')` function.

5. **`prompt.txt`**
   This text file stores the input prompt that the language model uses to generate output. Storing the prompt externally allows you to experiment with various prompts without altering the Python code. By simply editing this file, you can influence how the model responds.

6. **`apikey.txt`**
   This file contains the secret API key required to communicate with the external language model’s API. By keeping this key in a separate file, you maintain a cleaner codebase and reduce the risk of accidentally committing sensitive credentials to a public repository. It is advisable to add `apikey.txt` to `.gitignore` if using version control.

## Running the Project

To run the project locally, follow these steps:

1. **Install Dependencies:**
   Ensure you have Python 3 installed. Create and activate a virtual environment if desired, then install required packages:
   ```bash
   pip install flask requests
   ```
   (The `requests` package is mentioned as an example if your `helpers.py` uses it to call the external API. Adjust this step based on your actual dependencies.)

2. **Prepare the API Key and Prompt:**
   - Place your secret API key in `apikey.txt`.
   - Edit `prompt.txt` to include the prompt you want to send to the language model.

3. **Run the Application:**
   From the project’s root directory, start the Flask server:
   ```bash
   python app.py
   ```
   By default, Flask runs on `http://127.0.0.1:5000`. Navigate to this URL in your web browser to view the application.

## How It Works

When a user visits the site, `app.py`:
- Loads the prompt from `prompt.txt`.
- Reads the API key from `apikey.txt`.
- Uses a helper function to send a request to the language model API.
- Receives the response text (or keys) generated by the model.
- Passes that response to `index.html` via `render_template`, replacing placeholder variables in the template.
- The user sees a webpage that includes the logos from the `static` folder and the generated content from the model.

## Customization and Extensions

- **Changing the Prompt:**
  Modify `prompt.txt` to influence the output. For example, if you are generating a list of keys or summarizing text, the prompt can shape the final generated output.

- **Styling the Front-End:**
  Add CSS files or customize `index.html` for a more polished interface. Place your CSS in `static/` and reference it in the template.

- **Adding Routes or Pages:**
  Extend `app.py` to include additional Flask routes. For example, you can create a `/about` page with more information or a form that allows users to submit custom prompts.

- **Enhanced Security:**
  Ensure `apikey.txt` is not exposed. Update `.gitignore` to exclude it from version control if needed. For production deployment, consider environment variables or a secure key management system.

## Troubleshooting

- **API Key Errors:**
  If you receive authentication errors, verify that `apikey.txt` contains a valid key. Ensure no extra spaces or newline characters are causing issues.

- **Empty Responses:**
  If the language model returns no content, double-check the prompt or verify the model’s API status. Print out response data in `helpers.py` to debug.

- **Server Not Running:**
  If Flask does not run, ensure you have installed all required dependencies and that `app.py` includes a proper `if __name__ == '__main__': app.run()` block (if required).
