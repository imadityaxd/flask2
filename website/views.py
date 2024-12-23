# Import necessary modules for the views
from flask import Blueprint, render_template, request, flash, jsonify  # Flask utilities for routing, templates, and JSON responses
from flask_login import login_required, current_user  # Flask-Login utilities to manage user sessions
from .models import Note  # Import the Note model for database operations
from . import db  # Import the database instance
import json  # Module to parse JSON data

# Create a Blueprint for general views
views = Blueprint('views', __name__)

# Define the home route (main page)
@views.route('/', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def home():
    # Handle form submission for adding a new note
    if request.method == 'POST':
        note = request.form.get('note')  # Get the note content from the form

        # Validate the note content
        if len(note) < 1:
            flash('Note is too short!', category='error')  # Show an error message if the note is empty
        else:
            # Create a new Note object linked to the current user
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)  # Add the new note to the database session
            db.session.commit()  # Commit the session to save the note
            flash('Note added!', category='success')  # Show a success message

    # Render the home page template, passing the current user to the template
    return render_template("home.html", user=current_user)

# Define the route to delete a note
@views.route('/delete-note', methods=['POST'])
def delete_note():
    # Parse the JSON data from the request
    note = json.loads(request.data)
    noteId = note['note']  # Extract the note ID from the parsed data
    note = Note.query.get(noteId)  # Query the database for the note by its ID

    # Check if the note exists and belongs to the current user
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)  # Delete the note from the database
            db.session.commit()  # Commit the session to finalize the deletion

    # Return an empty JSON response to indicate success
    return jsonify({})
