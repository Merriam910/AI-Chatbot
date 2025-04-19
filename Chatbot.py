from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

app = Flask(__name__)

# Improved model selection (using larger DialoGPT)
MODEL_NAME = "microsoft/DialoGPT-large"  # More capable than medium version
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
chatbot = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1  # Use GPU if available
)

# Enhanced conversation handling
conversation_history = []
SYSTEM_PROMPT = """You are a helpful, empathetic AI assistant. Provide thoughtful responses that:
- Acknowledge the user's message
- Show understanding of their context
- Offer helpful information or suggestions
- Maintain natural conversation flow

Current conversation:
{history}
User: {input}
AI:"""

def format_prompt(history, user_input):
    return SYSTEM_PROMPT.format(
        history="\n".join(history[-4:]),  # Last 4 exchanges
        input=user_input
    )

def enhance_response(response, user_input):
    """Improve response quality with post-processing"""
    # Extract AI's response
    ai_response = response.split("AI:")[-1].strip()
    
    # Common emotional triggers with better responses
    emotional_responses = {
        "sad": "I'm sorry to hear you're feeling this way. Would you like to talk about what's bothering you?",
        "okay": "I'm functioning well, thank you for asking! How can I assist you today?",
        "happy": "That's wonderful to hear! What's making you happy today?",
        "angry": "I understand this must be frustrating. Sometimes taking deep breaths can help."
    }
    
    # Check for emotional keywords
    lower_input = user_input.lower()
    for emotion, reply in emotional_responses.items():
        if emotion in lower_input:
            return reply
            
    # Ensure complete sentences
    if not any(ai_response.endswith(punct) for punct in ['.', '!', '?']):
        ai_response += " Could you tell me more about that?"
        
    return ai_response

@app.route("/")
def home():
    return "Advanced AI Chatbot - Use POST /chat with {'prompt':'your message'}"

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    
    try:
        data = request.get_json()
        user_input = data.get("prompt", "").strip()
        
        if not user_input:
            return jsonify({"error": "Please provide a prompt"}), 400

        # Format with system prompt and history
        full_prompt = format_prompt(conversation_history, user_input)
        
        # Generate with optimized parameters
        response = chatbot(
            full_prompt,
            max_length=200,
            temperature=0.7,
            top_p=0.92,
            top_k=50,
            repetition_penalty=1.15,
            num_beams=3,
            do_sample=True,
            early_stopping=True
        )[0]['generated_text']
        
        # Process and enhance the response
        ai_response = enhance_response(response, user_input)
        
        # Update history (keep last 5 exchanges)
        conversation_history.extend([f"User: {user_input}", f"AI: {ai_response}"])
        conversation_history = conversation_history[-10:]
        
        return jsonify({
            "response": ai_response,
            "history": conversation_history
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)