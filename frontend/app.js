document.getElementById("feedback-form").addEventListener("submit", async function(event) {
    event.preventDefault();  // Prevent the default form submission

    // Get feedback text from textarea
    const feedbackText = document.getElementById("feedback-text").value;

    // Make API request to FastAPI
    const responseMessage = document.getElementById("response-message");

    try {
        // Call the FastAPI backend
        const response = await fetch(`http://localhost:8000/submit-feedback/?feedback_text=${feedbackText}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Failed to submit feedback');
        }

        // Parse the JSON response
        const data = await response.json();

        // Display the sentiment
        responseMessage.textContent = `Sentiment: ${data.sentiment}`;
        responseMessage.style.color = data.sentiment === "Positive" ? "green" :
                                      data.sentiment === "Negative" ? "red" : "gray";
    } catch (error) {
        // Handle any errors (e.g., failed request)
        responseMessage.textContent = `Error: ${error.message}`;
        responseMessage.style.color = "red";
    }
});
