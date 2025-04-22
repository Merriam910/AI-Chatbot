from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch

def initialize_blenderbot():
    """Initialize the model and tokenizer with error handling"""
    try:
        model_name = "facebook/blenderbot-400M-distill"
        print("Loading model and tokenizer...")
        
        # Load tokenizer
        tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
        
        # Load model with device auto-detection
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        model = BlenderbotForConditionalGeneration.from_pretrained(model_name).to(device)
        
        print("Model loaded successfully!")
        return tokenizer, model
    
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        return None, None

def chat_with_blenderbot(user_input, tokenizer, model):
    """Generate a response from BlenderBot with error handling"""
    try:
        if not user_input or not isinstance(user_input, str):
            return "Please provide a valid text input."
            
        if tokenizer is None or model is None:
            return "Chat model is not properly initialized."
            
        # Tokenize the input and move to same device as model
        inputs = tokenizer([user_input], return_tensors="pt").to(model.device)
        
        # Generate response
        reply_ids = model.generate(**inputs)
        response = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
        
        return response
        
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Main execution
if __name__ == "__main__":
    # Initialize the model once
    tokenizer, model = initialize_blenderbot()
    
    if tokenizer and model:
        print("BlenderBot is ready to chat! Type 'quit' to exit.")
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                response = chat_with_blenderbot(user_input, tokenizer, model)
                print("Bot:", response)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error in chat loop: {str(e)}")
                continue