from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolean = True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName)< 3:
            flash('First Name must be greater than 2 characters.', category='error')
        elif password1 !=password2:
            flash('Password and confirm password should be same.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            #add user to database
            flash('Account created successfully.', category='success')
    return render_template("sign_up.html")