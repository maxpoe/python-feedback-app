let feedbackData = []; // Store all feedback data here
let currentPage = 1; 
const itemsPerPage = 5; // Number of items per page

async function fetchFeedback() {
    const response = await fetch('http://localhost:8000/feedback');
    feedbackData = await response.json();
    renderPage(currentPage);
}

// Render a specific page of feedback
function renderPage(page) {
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageItems = feedbackData.slice(start, end);

    const responsesList = document.getElementById('responses-list');
    responsesList.innerHTML = ''; // Clear existing content

    pageItems.forEach(feedback => {
        // Create elements for feedback entry
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('response-item');

        const feedbackText = document.createElement('p');
        feedbackText.classList.add('feedback-text');
        feedbackText.textContent = feedback.feedback_text;

        const sentiment = document.createElement('p');
        sentiment.classList.add('sentiment');
        sentiment.textContent = `Sentiment: ${feedback.sentiment} | Date: ${new Date(feedback.timestamp).toLocaleString()}`;


        // Create buttons for editing and deleting
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.classList.add('edit-button');
        editButton.addEventListener('click', () => editFeedback(feedback.id));

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.classList.add('delete-button');
        deleteButton.addEventListener('click', () => deleteFeedback(feedback.id));


        // Append elements to item div
        itemDiv.appendChild(feedbackText);
        itemDiv.appendChild(sentiment);
        itemDiv.appendChild(editButton);
        itemDiv.appendChild(deleteButton);

        // Append item div to responses list
        responsesList.appendChild(itemDiv);
    });

    updatePaginationControls();
}

// Update pagination controls based on the current page and total data
function updatePaginationControls() {
    const paginationControls = document.getElementById('pagination-controls');
    paginationControls.innerHTML = ''; // Clear existing controls

    const totalPages = Math.ceil(feedbackData.length / itemsPerPage);

    // Create "Previous" button
    const prevButton = document.createElement('button');
    prevButton.textContent = 'Previous';
    prevButton.disabled = currentPage === 1; // Disable on the first page
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderPage(currentPage);
        }
    });
    paginationControls.appendChild(prevButton);

    // Create "Next" button
    const nextButton = document.createElement('button');
    nextButton.textContent = 'Next';
    nextButton.disabled = currentPage === totalPages; // Disable on the last page
    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderPage(currentPage);
        }
    });
    paginationControls.appendChild(nextButton);

    // Display page info
    const pageInfo = document.createElement('span');
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    paginationControls.appendChild(pageInfo);
}

// Edit feedback - open a prompt to change the feedback text
async function editFeedback(id) {
    const newFeedbackText = prompt("Edit feedback:");

    if (newFeedbackText) {
        const response = await fetch(`http://localhost:8000/feedback/${id}?feedback_text=${newFeedbackText}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            fetchFeedback(); // Reload feedback after update
        } else {
            alert('Failed to update feedback');
        }
    }
}

// Delete feedback
async function deleteFeedback(id) {
    const response = await fetch(`http://localhost:8000/feedback/${id}`, {
        method: 'DELETE',
    });

    if (response.ok) {
        fetchFeedback(); // Reload feedback after deletion
    } else {
        alert('Failed to delete feedback');
    }
}

// Fetch and display feedback on page load
window.addEventListener('DOMContentLoaded', fetchFeedback);

// Fetch and display feedback on page load
window.addEventListener('DOMContentLoaded', fetchFeedback);
