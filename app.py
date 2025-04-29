from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from Chatbot import initialize_blenderbot, chat_with_blenderbot

app = Flask(__name__)
CORS(app)

# Initialize model
tokenizer, model = initialize_blenderbot()

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')
@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')
@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/ai-powered')
def ai_page():
    return render_template('ai-powered.html')
@app.route('/private')
def private_page():
    return render_template('private.html')
@app.route('/effortless')
def effortless_page():
    return render_template('effortless.html')
@app.route('/learnmore')
def lm_page():
    return render_template('learnmore.html')
@app.route('/report')
def report_page():
    return render_template('report.html')



@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    response = chat_with_blenderbot(user_input, tokenizer, model)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=False)
    
    