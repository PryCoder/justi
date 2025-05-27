from flask import Flask, request, jsonify, render_template
import json
import re
from rapidfuzz import fuzz
import os


app = Flask(__name__)

# Load vulgar words from JSON
with open("vulgar_words.json", "r", encoding='utf-8') as f:
    vulgar_data = json.load(f)

vulgar_words = set()
for item in vulgar_data['gaalis']:
    for key in ['hindi', 'hinglish', 'slang', 'english']:
        if item.get(key):
            word = item[key].lower().replace('*', '')
            # Skip empty entries
            if word.strip():
                vulgar_words.add(word)

# Add hardcoded English vulgar words that may be missing from JSON
extra_english_vulgar = {
    "motherfucker",
    "motherfucking",
    "fuck",
    "fucker",
    "fucking",
    "bitch",
    "asshole",
    "bastard",
    "dick",
    "pussy",
    "cock",
    # add more as needed
}

def clean_text(text):
    text = text.lower()
    # Remove special chars except spaces and alphabets/numbers
    text = re.sub(r'[^\w\s]', '', text)
    return text

def normalize_repeated_chars(word):
    # Reduce repeated characters to a single character, e.g. "fuuuuck" -> "fuck"
    return re.sub(r'(.)\1{2,}', r'\1', word)

def contains_vulgar(text):
    cleaned_text = clean_text(text)
    normalized_text = normalize_repeated_chars(cleaned_text)

    # Check whole phrases first (for multi-word vulgar phrases)
    for vw in vulgar_words:
        vw_norm = normalize_repeated_chars(vw)
        if vw_norm in normalized_text:
            return True
        # Also fuzzy partial ratio to catch typos or variations
        if fuzz.partial_ratio(normalized_text, vw_norm) > 85:
            return True

    # Then check word by word
    words = normalized_text.split()
    for w in words:
        if w in extra_english_vulgar:
            return True
        for vw in vulgar_words:
            vw_norm = normalize_repeated_chars(vw)
            if w == vw_norm or fuzz.ratio(w, vw_norm) > 85:
                return True

    return False

@app.route('/moderate', methods=['POST'])
def moderate():
    data = request.get_json(force=True)
    comment = data.get('comment', '')
    flagged = contains_vulgar(comment)
    return jsonify({
        "allowed": not flagged,
        "flagged": flagged
    })

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
