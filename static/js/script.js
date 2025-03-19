document.getElementById('sendButton').addEventListener('click', sendMessage);

document.getElementById('userInput').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();  // Prevents newline in input field
        sendMessage();
    }
});

async function sendMessage() {
    const userInputField = document.getElementById('userInput');
    const userInput = userInputField.value.trim();  // Get trimmed value

    if (userInput === '') return;  // Prevent sending empty messages

    const conversation = document.getElementById('conversation');

    // Create User Message
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.innerHTML = `<strong>You:</strong> ${userInput}`;
    conversation.appendChild(userMessage);

    // Clear input field immediately after sending message
    userInputField.value = '';

    // Send user input to backend
    const response = await fetch('/get_recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userInput })
    });

    const data = await response.json();

    let formattedResponse = data.recommendation
        .replace(/```([\s\S]*?)```/g, '<pre class="code-box"><code>$1</code></pre>')  // Code block
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold text
        .replace(/### (.*?)\n/g, '<h3>$1</h3>')  // Triple hash headers
        .replace(/^[\*\-\+] (.+)$/gm, '<li>$1</li>')  // Bullet points
        .replace(/<li>(.+)<\/li>\n(?=<li>)/g, '<li>$1</li>')  // Group consecutive list items
        .replace(/(<li>.+<\/li>)+/g, '<ul>$&</ul>')  // Wrap list items in ul tags
        .replace(/\n/g, '<br>');  // Line breaks

    // Create Assistant Message
    const assistantMessage = document.createElement('div');
    assistantMessage.classList.add('message', 'assistant-message');
    assistantMessage.innerHTML = '<strong>Assistant:</strong><br><span class="typing-text"></span>';
    conversation.appendChild(assistantMessage);

    // Get typing area
    const typingArea = assistantMessage.querySelector('.typing-text');
    
    // Type the message with animation
    typeText(typingArea, formattedResponse, function() {
        // Callback after typing completes
        conversation.scrollTop = conversation.scrollHeight;
    });

// Add this function to implement the typing effect
function typeText(element, html, callback, speed = 30) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    const text = tempDiv.textContent;
    let i = 0;
    
    function typeNextChar() {
        if (i < text.length) {
            // Show one character at a time while typing
            const progress = i / text.length;
            element.textContent = text.slice(0, i + 1);
            i++;
            
            // Scroll while typing
            const conversation = document.getElementById('conversation');
            conversation.scrollTop = conversation.scrollHeight;
            
            setTimeout(typeNextChar, speed);
        } else {
            // Typing complete - replace with fully formatted HTML
            element.innerHTML = html;
            if (callback) callback();
        }
    }
    
    typeNextChar();
}
    // Scroll to the bottom of the chat
    // conversation.scrollTop = conversation.scrollHeight;

    
}
