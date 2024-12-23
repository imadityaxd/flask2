// Define a function to delete a note by its ID
function deleteNote(noteId) {
    // Send a POST request to the '/delete-note' route using the Fetch API
    fetch('/delete-note', {
        method: 'POST', // Specify the HTTP method as POST
        body: JSON.stringify({ noteId: noteId }) // Convert the noteId into a JSON object and include it in the request body
    })
    .then((_res) => {
        // Once the response is received, redirect the user to the home page ('/')
        window.location.href = "/";
    });
}
