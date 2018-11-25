import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///yconnect.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """"""
    if request.method == "GET":
        majors = db.execute("SELECT id FROM majors")
        return render_template("index.html", majors=majors)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    if request.method == "GET":
        q = str(request.args.get("username"))
        usernames = db.execute("SELECT username FROM users")
        l = []
        for username in usernames:
            l.append(username["username"])
        if (len(q) >= 1) and not(q in l):
            return jsonify(True)
        else:
            return jsonify(False)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        # Check if each field has input
        if not request.form.get("username"):
            return apology("Must enter username", 400)
        elif not request.form.get("password"):
            return apology("Must enter password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match", 400)
        # Insert new user
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password")))
        if not result:
            return apology("Username already exists", 400)
        session["user_id"] = result
        return redirect("/updateprofile")

@app.route("/search")
def search():
    """"""
    name = request.args.get("name")
    name_edit = name + '%'
    major = request.args.get("major")
    profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name AND major = :major", name=name_edit, major=major)
    return jsonify(profiles)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """"""
    if request.method == "GET":
        profile = db.execute("SELECT * FROM profile WHERE id = :id", id=session["user_id"])
        return render_template("profile.html", profile=profile)

@app.route("/updateprofile", methods=["GET", "POST"])
@login_required
def updateprofile():
    """"""
    if request.method == "GET":
        majors = db.execute("SELECT id FROM majors")
        return render_template("updateprofile.html", majors=majors) 
    elif request.method == "POST":
        exist = db.execute("SELECT * FROM profile WHERE id = :id", id=session["user_id"])
        if exist:
            result = db.execute("UPDATE profile SET name=:name, major=:major, year=:year WHERE id=:id", id=session["user_id"],
                name=request.form.get("name"), major=request.form.get("major"), year=request.form.get("year"))
        else:
            result = db.execute("INSERT INTO profile (id, name, major, year) VALUES(:id, :name, :major, :year)", id=session["user_id"], 
                name=request.form.get("name"), major=request.form.get("major"), year=request.form.get("year"))
        return redirect("/profile")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
