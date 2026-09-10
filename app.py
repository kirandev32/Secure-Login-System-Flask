from flask import Flask, render_template, request, redirect, session
import re

from database import get_connection, create_database
from crypto import hash_password, verify_password


app = Flask(__name__)

app.secret_key = "secure_login_secret_key_2026"

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


create_database()


@app.route("/")
def home():

    if "user_id" in session:
        return redirect("/dashboard")

    return redirect("/login")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    error = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if len(username) < 3:

            error = "Username must have at least 3 characters."

        elif not re.match(r"^[A-Za-z0-9_]+$", username):

            error = "Username can contain letters, numbers and underscores only."

        elif "@" not in email:

            error = "Please enter a valid email."

        elif len(password) < 8:

            error = "Password must have at least 8 characters."

        else:

            try:

                hashed_password = hash_password(password)

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (
                        username,
                        email,
                        hashed_password
                    )
                )

                connection.commit()

                # Get the ID of the newly created user
                user_id = cursor.lastrowid

                connection.close()

                # Create login session immediately
                session["user_id"] = user_id
                session["username"] = username

                # Redirect directly to dashboard
                return redirect("/dashboard")

            except Exception as e:

                print("REGISTER ERROR:", e)

                try:
                    connection.close()
                except:
                    pass

                error = "Username or email already exists."

    return render_template(
        "register.html",
        error=error
    )


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:

            error = "Please enter username and password."

        else:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )

            user = cursor.fetchone()

            connection.close()

            if user:

                password_correct = verify_password(
                    password,
                    user["password"]
                )

                if password_correct:

                    # Create session
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]

                    # Redirect to dashboard
                    return redirect("/dashboard")

                else:

                    error = "Invalid username or password."

            else:

                error = "Invalid username or password."

    return render_template(
        "login.html",
        error=error
    )


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    # Check if user is logged in
    if "user_id" not in session:

        return redirect("/login")

    return render_template("dashboard.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":

    app.run(debug=True)