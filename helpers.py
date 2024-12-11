import json
import random
import genanki
from openai import OpenAI
import pdfplumber
import re

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n"
    return extracted_text.strip()

# Remove multiple spaces and replace with a single space
def clean_extracted_text(text):
    # Remove multiple spaces and replace with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove common PDF artifacts like headers, footers, and page numbers
    text = re.sub(r'Page \d+|©.*|\d{4}-\d{4}', '', text)
    return text.strip()

# Read content from a file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

# Function to generate flashcards using OpenAI
def run_flashcard_generation(cleaned_text):
    """Function that uses the OpenAI API to generate flashcards in JSON format."""
    # Initialize OpenAI client
    client = OpenAI(api_key=read_file("apikey.txt"))

    # Load system and user prompts
    system_prompt = read_file("prompt.txt")
    pdf_notes = cleaned_text

    # Create the chat completion request
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pdf_notes}
        ],
        response_format={"type": "text"},
        temperature=0.7,
        max_tokens=8192,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Get the response content
    response_content = completion.choices[0].message.content
    output_file = "output_flashcards.json"

    # Validate and save JSON
    try:
        parsed_json = json.loads(response_content)
        with open(output_file, "w") as file:
            json.dump(parsed_json, file, indent=4)
        return output_file
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        print(completion.choices[0].message.content)
        return 0

# Function to create Anki deck
def run_deck_creation(json_file, deck_name):
    """Function to create an Anki deck from the generated JSON flashcards."""
    # Generate a unique Deck ID
    unique_deck_id = random.randrange(1 << 30, 1 << 31)


    # Load JSON file with card data
    with open(json_file, 'r') as json_file:
        cards = json.load(json_file)

    # Define the model (template for cards)
    anki_model = genanki.Model(
        1607392321,  # Random model ID
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''
                    <div class="card-content">
                      {{Question}}
                    </div>
                ''',
                'afmt': '''
                    <div class="card-content">
                      {{FrontSide}}
                      <hr>
                      {{Answer}}
                    </div>
                ''',
            },
        ],
        css='''
            .card-content {
                font-family: "Calibri", sans-serif;
                font-size: 20px;
                font-weight: bold;
                color: silver;
                text-align: center;
                margin: 20px auto;
            }

            hr {
                border: 0;
                height: 1px;
                background: silver;
                margin: 20px 0;
            }
        '''
    )

    # Create a deck
    anki_deck = genanki.Deck(
        unique_deck_id,  # Random deck ID
        deck_name
    )

    # Add notes to the deck
    for card in cards:
        note = genanki.Note(
            model=anki_model,
            fields=[card['front'], card['back']]
        )
        anki_deck.add_note(note)

    # Save the deck to a file
    output_file = f"{deck_name}.apkg"
    genanki.Package(anki_deck).write_to_file(output_file)
    return output_file
