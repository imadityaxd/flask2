# Import necessary modules for authentication routes
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User  # Import the User model for database operations
from werkzeug.security import generate_password_hash, check_password_hash  # Functions for hashing and verifying passwords
from . import db  # Import the database instance
from flask_login import login_user, login_required, logout_user, current_user  # Flask-Login utilities for user session management

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__)

# Define the login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login form submission
    if request.method == 'POST':
        email = request.form.get('email')  # Get the email from the form
        password = request.form.get('password')  # Get the password from the form

        # Query the database for a user with the given email
        user = User.query.filter_by(email=email).first()
        if user:
            # Check if the password matches the hashed password in the database
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)  # Log in the user and remember the session
                return redirect(url_for('views.home'))  # Redirect to the home page
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    # Render the login page
    return render_template("login.html", user=current_user)

# Define the logout route
@auth.route('/logout')
@login_required  # Ensure the user is logged in to access this route
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('auth.login'))  # Redirect to the login page

# Define the sign-up route
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Handle sign-up form submission
    if request.method == 'POST':
        email = request.form.get('email')  # Get the email from the form
        first_name = request.form.get('firstName')  # Get the first name from the form
        password1 = request.form.get('password1')  # Get the password from the form
        password2 = request.form.get('password2')  # Get the confirm password from the form

        # Check if the email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 3:
            flash('First Name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Password and confirm password should be the same.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            # Add a new user to the database
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')  # Hash the password
            )
            db.session.add(new_user)  # Add the new user to the database session
            db.session.commit()  # Commit the session to save the user
            login_user(new_user, remember=True)  # Log in the new user
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.home'))  # Redirect to the home page

    # Render the sign-up page
    return render_template("sign_up.html", user=current_user)
