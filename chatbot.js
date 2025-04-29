const API_URL = 'http://127.0.0.1:5000/';  // Replace with your actual Flask backend URL

document.getElementById('send-btn').addEventListener('click', async function () {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if (message) {
        const userMsg = document.createElement('div');
        userMsg.className = 'user-message';
        userMsg.textContent = message;
        document.getElementById('chat-messages').appendChild(userMsg);
        userInput.value = '';

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            const botMsg = document.createElement('div');
            botMsg.className = 'bot-message';
            botMsg.textContent = data.response;
            document.getElementById('chat-messages').appendChild(botMsg);

            const chatBox = document.getElementById('chat-messages');
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            console.error('Error:', error);
        }
    }
});
