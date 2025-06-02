import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

#? REMEMBER TO IMPORT THE FUNCTIONS INTO HERE IF YOU ADD MORE
from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd
app.debug = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///casino.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
@login_required
def index():
    """ Show the menu """
    
    flash('Message')
    
    return apology('TODO')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Allow user to register for an account """
    
    # Checks if the user is already logged in
    if 'user_id' in session:
        return apology('Already logged in')

    # If the user presses the register button
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        
        # Checks if the user stuff in the textfields
        if not username or not password or not confirmation:
            return apology('Missing textfields', 406)
        
        # Checks if the length of the username, password, and confirmation password is in the min and max range
        if len(username) < 3 or len(username) > 20 or len(password) < 8 or len(password) > 200 or len(confirmation) < 8 or len(confirmation) > 200:
            return apology("Please stop hacking I'm scared", 406)
        
        # Insert the user's username and hashed password into the database
        db.execute('INSERT INTO users (username, hash) VALUES (?, ?)', username, generate_password_hash(password))
        
        # Log the user in
        session['user_id'] = db.execute('SELECT id FROM users WHERE username = ?', username)[0]['id']
        
        return redirect('/')

    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")