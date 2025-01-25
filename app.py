from flask import Flask, request, render_template_string
import sqlite3
from hashlib import sha256  # For password hashing

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Create a users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hash a password
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Route: Home Page
@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome</h1>
        <p><a href="/register">Register</a> | <a href="/login">Login</a></p>
    ''')

# Route: Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)  # Hash the password

        # Save the new user to the database
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()
            return 'Registration successful! <a href="/login">Login here</a>'
        except sqlite3.IntegrityError:
            return 'Username already exists. <a href="/register">Try again</a>'
        except Exception as e:
            return f'An error occurred: {str(e)}'

    return render_template_string('''
        <h1>Register</h1>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
    ''')

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)  # Hash the password

        # Use parameterized queries to prevent SQL injection
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()
            conn.close()

            if user:
                return f'Hello, {username}!'
            else:
                return 'Invalid username or password. <a href="/login">Try again</a>'
        except Exception as e:
            return f'An error occurred: {str(e)}'

    return render_template_string('''
        <h1>Login</h1>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

# Bind to all interfaces 
if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0')  # Set debug=False for production
