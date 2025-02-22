from flask import Flask, render_template, request
import config  # Importing the config file to access the API_KEY
import requests
from transformers import pipeline 

app = Flask(__name__)

# Get the API key from config.py
API_KEY = config.API_KEY
API_URL = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Translation function
def translate(text, src_lang="eng_Latn", tgt_lang="som_Latn"):
    payload = {
        "inputs": text,
        "parameters": {"src_lang": src_lang, "tgt_lang": tgt_lang}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]["translation_text"]
    elif response.status_code == 503:
            print(f"Model is loading. Retrying in _ seconds...")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Homepage Route
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Translation Route
@app.route("/translate", methods=["GET", "POST"])
def translate_page():
    translated_text = None
    if request.method == "POST":
        user_text = request.form["text"]
        translated_text = translate(user_text)
    return render_template("index.html", translated_text=translated_text)

if __name__ == "__main__":
    app.run(debug=True)
