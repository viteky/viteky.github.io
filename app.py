from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, error

app = Flask(__name__)




# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///credits.db")


@app.route("/")
@login_required
def index():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Clear the user session
    session.clear()

    if request.method == "POST":

        username = request.form.get("username").strip()
        password = request.form.get("password")

        # Ensure username/email was submitted
        if username is None:
            return error("must provide username", 400)
        
        if password is None:
            return error("must provide password", 400)

        # Query db for user
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return error("invalid username and/or password", 400)
        
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirm-password")
        firstName = request.form.get("first-name").capitalize().strip()
        lastName = request.form.get("last-name").capitalize().strip()

        if username is None:
            return error("must provide username", 400)

        elif email is None:
            return error("must provide email", 400)
        
        elif firstName is None:
            return error("must provide first name", 400)

        elif lastName is None:
            return error("must provide last name", 400)

        elif password is None:
            return error("must provide password", 400)

        elif confirmation is None:
            return error("must confirm password", 400)
        
        elif password != confirmation:
            return error("passwords do not match", 400)
        
        # Query db for users
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(rows) != 0:
            return error("username already exists", 400)
        
        # Instert new user into the db
        db.execute("INSERT INTO users (username, hash, firstName, lastName, email) VALUES(:username, :hash, :firstName, :lastName, :email)",
                   username=username.strip(), hash=generate_password_hash(password),
                   firstName=firstName, lastName=lastName, email=email)
        
        # Set the user's session
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    
    else:
        return render_template("register.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()
    return redirect("/")

