from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from Chatbot import initialize_blenderbot, chat_with_blenderbot

app = Flask(__name__)
CORS(app)

# Initialize model
tokenizer, model = initialize_blenderbot()

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    response = chat_with_blenderbot(user_input, tokenizer, model)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)