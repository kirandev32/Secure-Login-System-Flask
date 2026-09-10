# Secure Login System

A secure user authentication web application built using Python Flask and SQLite.

## Features

- User registration
- Secure password hashing using bcrypt
- User login authentication
- SQLite database
- Protection against SQL injection using parameterized queries
- Input validation
- Session management
- Protected dashboard
- Logout functionality

## Technologies Used

- Python
- Flask
- SQLite
- bcrypt
- HTML
- CSS

## Project Structure

secure-login-system/

app.py - Main Flask application

database.py - Database operations

crypto.py - Password hashing and verification

templates/ - HTML pages

static/ - CSS files

## Installation

Clone the repository:

git clone YOUR_REPOSITORY_URL

Navigate to the project folder:

cd secure-login-system

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Open the application in your browser:

http://127.0.0.1:5000

## Security Features

Passwords are hashed using bcrypt before being stored in the database.

Parameterized SQL queries are used to help prevent SQL injection attacks.

Session management protects the dashboard and allows users to securely log out.
