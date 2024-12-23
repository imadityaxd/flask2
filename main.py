# Import the create_app function from the website package
# This function initializes and configures the Flask application
from website import create_app

# Create an instance of the Flask application by calling the create_app function
app = create_app()

# Check if this script is being run directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application in debug mode
    # Debug mode enables live reloading and provides detailed error messages
    app.run(debug=True)
