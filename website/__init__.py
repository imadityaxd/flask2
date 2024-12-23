# Import necessary modules
from flask import Flask  # Flask is the framework for creating web applications
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy is used for database management
from os import path  # Used to check the existence of files
from flask_login import LoginManager  # Flask-Login manages user sessions

# Initialize the SQLAlchemy object (used for database operations)
db = SQLAlchemy()

# Define the database name
DB_NAME = "database.db"

# Function to create and configure the Flask app
def create_app():
    # Create a Flask app instance
    app = Flask(__name__)

    # Set a secret key for securely signing session cookies
    app.config['SECRET_KEY'] = 'asecretkey'

    # Set the database URI to use SQLite with the specified database name
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints for modularizing routes
    from .views import views  # Import routes for general views
    from .auth import auth  # Import routes for authentication

    # Register blueprints with URL prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import database models (User and Note)
    from .models import User, Note

    # Create the database if it doesn't exist
    create_database(app)

    # Initialize the LoginManager to handle user sessions
    login_manager = LoginManager()

    # Define the view to redirect unauthenticated users
    login_manager.login_view = 'auth.login'

    # Link the login manager with the app
    login_manager.init_app(app)

    # Define the function to load a user by ID (used by Flask-Login)
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))  # Retrieve user by primary key (ID)

    # Return the configured app instance
    return app

# Function to create the database if it doesn't exist
def create_database(app):
    # Check if the database file already exists
    if not path.exists('website/' + DB_NAME):
        # Create the database tables within the app context
        with app.app_context():
            db.create_all()
            print('Created Database!')  # Print a confirmation message
