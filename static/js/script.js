document.getElementById('sendButton').addEventListener('click', async () => {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === '') return;

    // Display user input in conversation
    const conversation = document.getElementById('conversation');
    const userMessage = document.createElement('div');
    userMessage.textContent = `User: ${userInput}`;
    conversation.appendChild(userMessage);

    // Send user input to backend
    const response = await fetch('/get_recommendation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: userInput })
    });

    const data = await response.json();

    // Display assistant response in conversation
    const assistantMessage = document.createElement('div');
    assistantMessage.textContent = `Assistant: ${data.recommendation}`;
    conversation.appendChild(assistantMessage);

    // Clear input field
    document.getElementById('userInput').value = '';
});