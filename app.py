import time
import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PyPDF2 import PdfReader
import pickle
import google.generativeai as genai
from google.ai import generativelanguage as glm

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS

load_dotenv()
google_api_key = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=google_api_key)

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

text_data = None

def chat_with_groq(prompt, model):
    try:
        completion = model.generate_content(prompt)
        return completion.text
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return "Error in generating response from Server"

def get_summarization(user_doc, model, language_option):
#    print(f"Debug: language_option received: {language_option}")  # Debugging line
#    print(f"Debug: user_doc received: ")  # Debugging line
    
    prompt = ""
    if language_option in ['None', 'English', 'en']:
        prompt = f'''
        A user has uploaded an insurance document:

        {user_doc}

        Summarize the policy in the 5 most important points with maximum 75 words. Provide each point clearly, without any bullet markers, and separate each point with a newline.
        '''
    elif language_option in ['Hindi', 'hi']:
        prompt = f'''
        A user has uploaded an insurance document:

        {user_doc}

        Summarize the policy in Hindi language, focusing on the 5 most important points with maximum 75 words. Provide each point clearly, without any bullet markers, and separate each point with a newline.
        '''
#    else:
#        print(f"Debug: Unexpected language_option value: {language_option}")  # Debugging line
    
    if prompt:
        # print(f"Debug: Prompt generated: {prompt}")  # Debugging line
        return chat_with_groq(prompt, model)
    else:
        return "Error: Unable to generate summarization prompt"

def get_answers(user_doc, question, model, language_option=None):
    prompt = ""
    # print(f"yes we are here: {user_doc[:100]}, {question}")
    if user_doc and question:
        if language_option == 'None' or language_option == 'en':
            prompt = f'''
            A user has uploaded an insurance document and asked the following question:
            
            {question}
            
            Please provide an answer based on the attached document:
            
            {user_doc}
        '''
        elif language_option == 'Hindi' or language_option == 'hi':
            prompt = f'''
            A user has uploaded an insurance document and asked the following question:

            {question}

            Please provide an answer in Hindi language based on the attached document:

            {user_doc}
        '''
    if prompt:
        chat = model.start_chat(history=[{"role": "user", "parts": prompt}])
        return chat
    else:
        return "Error: Unable to generate answer prompt"

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload_file():
    global text_data
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
            text_data = text
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
        # print(f"Debug: Received document for summarization: {user_doc[:100]}")  # Print the first 100 characters for brevity
        # print(f"Debug: Language option: {language_option}")
        
        # Call the model to get the summarization as a full string
        summarization_full = get_summarization(user_doc, model, language_option)
        
        # Split the summarization into lines, assuming the model returns bullet points or new lines.
        summarization = [line.strip() for line in summarization_full.splitlines() if line.strip()]
        
        # print(f"Debug: Summarization result: {summarization[:200]}")
        return jsonify({"summary": summarization})
    except Exception as e:
        logger.error(f"Error in summarize endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/answer', methods=['POST'])
def answer():
    global text_data
    try:
        data = request.json
        user_doc = text_data
        question = data.get("question", "")
        language_option = data.get("language", "English")
        chat = get_answers(user_doc, question, model, language_option)
        answer = chat.send_message(question)
        # print(f"{answer}")
        return jsonify({"answer": answer.text})
    except Exception as e:
        logger.error(f"Error in answer endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
