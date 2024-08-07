import time
import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PyPDF2 import PdfReader
from groq import Groq
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS

load_dotenv()
groq_api_key = os.environ['GROQ_API_KEY']
client = Groq(api_key=groq_api_key)
model = "llama3-8b-8192"

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def chat_with_groq(client, prompt, model):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in chat_with_groq: {e}")
        return "Error in generating response from Groq"

def get_summarization(client, user_doc, model, language_option=None):
    print(f"Debug: language_option received: {language_option}")  # Debugging line
    print(f"Debug: user_doc received: ")  # Debugging line
    
    prompt = ""
    if language_option in ['None', 'English', 'en']:
        prompt = f'''
        A user has uploaded an insurance document:

        {user_doc}

        In a few sentences, summarize the data in 10 most important points.
        '''
    elif language_option in ['Hindi', 'hi']:
        prompt = f'''
        A user has uploaded an insurance document:

        {user_doc}

        In a few sentences, summarize the data in Hindi language in 10 most important points.
        '''
    else:
        print(f"Debug: Unexpected language_option value: {language_option}")  # Debugging line
    
    if prompt:
        print(f"Debug: Prompt generated: ")  # Debugging line
        return chat_with_groq(client, prompt, model)
    else:
        return "Error: Unable to generate summarization prompt"

def get_answers(client, user_doc, question, model, language_option=None):
    prompt = ""
    if user_doc and question:
        if language_option == 'None' or language_option == 'English':
            prompt = f'''
            A user has uploaded an insurance document and asked the following question:
            
            {question}
            
            Please provide an answer based on the attached document:
            
            {user_doc}
        '''
        elif language_option == 'Hindi':
            prompt = f'''
            A user has uploaded an insurance document and asked the following question:

            {question}

            Please provide an answer in Hindi language based on the attached document:

            {user_doc}
        '''
    if prompt:
        return chat_with_groq(client, prompt, model)
    else:
        return "Error: Unable to generate answer prompt"

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            text = ""
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
            store_name = file.filename[:-4]
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(text, f)
            return jsonify({"message": "File uploaded successfully", "text": text})
    except Exception as e:
        logger.error(f"Error in upload_file: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        user_doc = data.get("text", "")
        language_option = data.get("language", "English")
        print(f"Debug: Received document for summarization: {user_doc[:100]}")  # Print the first 100 characters for brevity
        print(f"Debug: Language option: {language_option}")
        summarization = get_summarization(client, user_doc, model, language_option)
        print(f"Debug: Summarization result: {summarization[:50]}")
        return jsonify({"summary": summarization})
    except Exception as e:
        logger.error(f"Error in summarize endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/answer', methods=['POST'])
def answer():
    try:
        data = request.json
        user_doc = data.get("text", "")
        question = data.get("question", "")
        language_option = data.get("language", "English")
        answer = get_answers(client, user_doc, question, model, language_option)
        return jsonify({"answer": answer})
    except Exception as e:
        logger.error(f"Error in answer endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
