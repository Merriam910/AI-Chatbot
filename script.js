async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    userInput.value = '';
    
    try {
        const response = await fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        addMessage(data.response, false);
    } catch (error) {
        console.error('Error:', error);
        addMessage("Sorry, there was an error connecting to the chatbot.", false);
    }
}