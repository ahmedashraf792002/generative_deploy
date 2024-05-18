import os
from flask import Flask, request, jsonify, render_template
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load model and tokenizer
def load_model(model_path):
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model

def load_tokenizer(tokenizer_path):
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    return tokenizer

model = load_model('ahmed792002/custom_model')
tokenizer = load_tokenizer('ahmed792002/custom_model')

# Create Flask app
app = Flask(__name__)

# Maximum length of the generated text
max_length = 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.form['Data']
    sequence = data
    if not sequence:
        return jsonify({"error": "No input sequence provided"}), 400

    # Encode input sequence
    ids = tokenizer.encode(sequence, return_tensors='pt')
    
    # Generate text
    final_outputs = model.generate(
        ids,
        do_sample=True,
        max_length=max_length,
        pad_token_id=model.config.eos_token_id,
        top_k=50,
        top_p=0.95,
    )
    
    # Decode generated text
    text = tokenizer.decode(final_outputs[0], skip_special_tokens=True)
    if len(text.split('"')[1]) > 1:
        text = text.split('"')[1]
    return jsonify({"generated_text": text})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
