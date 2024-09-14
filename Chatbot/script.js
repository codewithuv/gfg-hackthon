document.addEventListener("DOMContentLoaded", function() {
    const chatlog = document.getElementById("chatlog");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.textContent = `${sender}: ${message}`;
        chatlog.appendChild(messageDiv);
        chatlog.scrollTop = chatlog.scrollHeight;  // Scroll to the bottom
    }

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        appendMessage("You", userMessage);
        userInput.value = "";

        fetch("/chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("Chatbot", data.response);
        })
        .catch(error => {
            console.error("Error:", error);
            appendMessage("Chatbot", "Sorry, something went wrong.");
        });
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
