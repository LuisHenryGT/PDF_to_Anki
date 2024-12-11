from flask import Flask, render_template, request, send_file, jsonify
from helpers import extract_text_from_pdf, clean_extracted_text, run_flashcard_generation, run_deck_creation

# Initialize Flask app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file and file.filename.endswith('.pdf'):

            # Process PDF and generate flashcards
            pdf_text = extract_text_from_pdf(file)
            cleaned_text = clean_extracted_text(pdf_text)
            try:
                deck_name = "Deck_generated"
                flashcards = run_flashcard_generation(cleaned_text)
                anki_deck = run_deck_creation(flashcards, deck_name)
                return send_file(anki_deck, as_attachment=True)
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return "Invalid file format. Please upload a PDF file."

    return render_template('index.html')
