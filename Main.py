from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# In a real-world scenario, you'd use a more secure database
users = {'user1': {'username': 'user1', 'password': generate_password_hash('password1')},
         'user2': {'username': 'user2', 'password': generate_password_hash('password2')}}

# Basic routes
@app.route('/')
def index():
    return 'Welcome to the Home Page'

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        if username in users:
            return 'Username already taken. Please choose another.'

        # Store user information (in-memory storage, not suitable for production)
        users[username] = {'username': username, 'password': generate_password_hash(password)}
        return 'Registration successful! <a href="/login">Login</a>'

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username  # Store username in the session
            return redirect(url_for('profile'))

        return 'Invalid username or password. <a href="/login">Try again</a>'

    return render_template('login.html')

# User profile route
@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return f'Hello, {username}! <a href="/logout">Logout</a>'

    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'You have been logged out. <a href="/login">Login again</a>'

if __name__ == '__main__':
    app.run(debug=True)
