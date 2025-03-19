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
    },10);

// Add this function to implement the typing effect
// ...existing code...

// Replace your current typeText function with this one
function typeText(element, html, callback, speed = 30) {
    // Split HTML into chunks, preserving HTML tags
    const chunks = splitHTMLIntoChunks(html);
    let currentIndex = 0;
    
    function typeNextChunk() {
        if (currentIndex < chunks.length) {
            // Add the next chunk (which could be a tag or text)
            element.innerHTML += chunks[currentIndex];
            currentIndex++;
            
            // Scroll while typing
            const conversation = document.getElementById('conversation');
            conversation.scrollTop = conversation.scrollHeight;
            
            // Only delay for visible text chunks, not for HTML tags
            const delay = chunks[currentIndex - 1].startsWith('<') && chunks[currentIndex - 1].endsWith('>') ? 0 : speed;
            setTimeout(typeNextChunk, delay);
        } else {
            if (callback) callback();
        }
    }
    
    element.innerHTML = ''; // Clear the element before starting
    typeNextChunk();
}

// Helper function to split HTML into chunks
function splitHTMLIntoChunks(html) {
    // First identify and protect code blocks
    const codeBlocks = [];
    let processedHtml = html.replace(/<pre class="code-box"><code>([\s\S]*?)<\/code><\/pre>/g, (match, codeContent, index) => {
        const placeholder = `__CODE_BLOCK_${codeBlocks.length}__`;
        codeBlocks.push(match);
        return placeholder;
    });
    
    const result = [];
    let inTag = false;
    let currentChunk = '';
    
    // Process HTML character by character
    for (let i = 0; i < processedHtml.length; i++) {
        const char = processedHtml[i];
        
        // Check for code block placeholder
        if (char === '_' && processedHtml.substring(i, i+13) === '__CODE_BLOCK_') {
            // If we have accumulated visible text, add it as a chunk
            if (currentChunk) {
                result.push(currentChunk);
                currentChunk = '';
            }
            
            // Extract placeholder index
            const endIndex = processedHtml.indexOf('__', i+13);
            const blockNum = parseInt(processedHtml.substring(i+13, endIndex));
            
            // Add the entire code block as a single chunk
            result.push(codeBlocks[blockNum]);
            
            // Skip to end of placeholder
            i = endIndex + 1;
            continue;
        }
        
        // Start of an HTML tag
        if (char === '<') {
            // If we have accumulated visible text, add it as a chunk
            if (currentChunk && !inTag) {
                result.push(currentChunk);
                currentChunk = '';
            }
            inTag = true;
            currentChunk += char;
        } 
        // End of an HTML tag
        else if (char === '>' && inTag) {
            currentChunk += char;
            result.push(currentChunk); // Add complete tag as a chunk
            currentChunk = '';
            inTag = false;
        }
        // Any other character
        else {
            currentChunk += char;
            // If not in tag and reached a good breakpoint (space or punctuation), add as chunk
            if (!inTag && (char === ' ' || char === '.' || char === ',' || char === ';' || char === ':' || char === '!' || char === '?')) {
                result.push(currentChunk);
                currentChunk = '';
            }
        }
    }
    
    // Add any remaining content
    if (currentChunk) {
        result.push(currentChunk);
    }
    
    return result;
}
    // Scroll to the bottom of the chat
    // conversation.scrollTop = conversation.scrollHeight;

    
}
