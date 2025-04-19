from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the pre-trained model (GPT-2) once when the app starts
chatbot_pipeline = pipeline("text-generation", model="gpt2")

# Define a route for the root URL
@app.route("/")
def home():
    return "Welcome to the AI Chatbot API! Use the /chat endpoint to interact with the chatbot."

# Define the /chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Please provide a prompt"}), 400

    # Generate a response using the pre-trained model
    result = chatbot_pipeline(prompt, max_length=50, do_sample=True)
    response_text = result[0]['generated_text']
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)