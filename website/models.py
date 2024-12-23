# Import the database object (db) from the current package
from . import db

# Import UserMixin for user authentication support in Flask-Login
from flask_login import UserMixin

# Import func from SQLAlchemy for database functions (e.g., current timestamp)
from sqlalchemy.sql import func

# Define the Note model to represent notes in the database
class Note(db.Model):
    # Define the primary key column for the Note model (unique identifier for each note)
    id = db.Column(db.Integer, primary_key=True)

    # Define a column to store the content of the note, allowing up to 10,000 characters
    data = db.Column(db.String(10000))

    # Define a column to store the date and time when the note was created
    # The default value is the current timestamp, set using func.now()
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # Define a foreign key to associate the note with a specific user
    # This links the note to a user by the user's ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Define the User model to represent users in the database
class User(db.Model, UserMixin):
    # Define the primary key column for the User model (unique identifier for each user)
    id = db.Column(db.Integer, primary_key=True)

    # Define a column for the user's email, ensuring it is unique for each user
    email = db.Column(db.String(150), unique=True)

    # Define a column to store the user's password (hashed for security)
    password = db.Column(db.String(150))

    # Define a column for the user's first name
    first_name = db.Column(db.String(150))

    # Define a relationship to link the User model with the Note model
    # This allows easy access to all notes associated with a user
    notes = db.relationship('Note')
