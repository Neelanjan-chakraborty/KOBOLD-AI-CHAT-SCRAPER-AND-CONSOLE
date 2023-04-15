const form = document.querySelector('.message-form');
const input = document.querySelector('input[type="text"]');
const messages = document.querySelector('.messages');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Get user input and clear the input field
    const userInput = input.value.trim();
    input.value = '';

    // Display user message on the screen
    displayMessage(userInput, 'user');

    // Send user input to the backend to get the bot's response
    const response = await fetch('/bot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    });

    // Get the bot's response and display it on the screen
    const data = await response.json();
    const botResponse = data.message;
    displayMessage(botResponse, 'bot');
});

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    messages.appendChild(messageElement);
}