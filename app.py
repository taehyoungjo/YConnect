import os
import json

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

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
        classes = db.execute("SELECT * FROM classes")
        return render_template("index.html", majors=majors, classes=classes)


# Check to see if username is available
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


# Check if user is already registered for class
@app.route("/class_check", methods=["GET"])
def class_check():
    """Return true if not registered for class available, else false, in JSON format"""

    # Check if registration already exists
    if not db.execute("SELECT class_id FROM class_registration WHERE class_id=:class_id AND user_id=:id", class_id=request.args.get('class_id'), id=session["user_id"]):
        return jsonify(True)
    else:
        return jsonify(False)

# Query database for classes that a user is registered for
@app.route("/registered_classes")
def registered_classes():
    """"""
    registrations = db.execute("SELECT * FROM class_registration WHERE user_id=:id", id=session["user_id"])
    return jsonify(registrations)


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

    # Render register template
    if request.method == "GET":
        return render_template("register.html")

    # Register User
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

        # Server validation to see if username is available
        if not result:
            return apology("Username already exists", 400)

        # Set user_id to session id to use across website
        session["user_id"] = result

        return redirect("/updateprofile")


# Search for users based on profile info
@app.route("/search")
def search():
    """"""
    name = request.args.get("name")

    # Edit name so "LIKE" database query can be use ex. 'oh' would return 'John'
    name_edit = '%' + name + '%'

    major = request.args.get("major")
    year = request.args.get("year")
    rc = request.args.get("res")

    print(rc)

    if major == "NULL":
        major_true = ""
    else:
        major_true = " AND major = :major"

    if year == "NULL":
        year_true = ""
    else:
        year_true = " AND year = :year"

    if rc == "NULL":
        rc_true = ""
    else:
        rc_true = " AND residential_college = :rc" 

    execute_statement = "SELECT * FROM profile WHERE name LIKE :name" + major_true + year_true + rc_true         
    print(execute_statement)

    if major == "NULL":
        if year == "NULL":
            if rc == "NULL":
                profiles = db.execute(execute_statement, name=name_edit)
            else:
                profiles = db.execute(execute_statement, name=name_edit, rc=rc)            
        else:
            if rc == "NULL":
                profiles = db.execute(execute_statement, name=name_edit, year=year)
            else:
                profiles = db.execute(execute_statement, name=name_edit, year=year, rc=rc)
    else:
        if year == "NULL":
            if rc == "NULL":
                profiles = db.execute(execute_statement, name=name_edit, major=major)
            else:
                profiles = db.execute(execute_statement, name=name_edit, major=major, rc=rc)            
        else:
            if rc == "NULL":
                profiles = db.execute(execute_statement, name=name_edit, major=major, year=year)
            else:
                profiles = db.execute(execute_statement, name=name_edit, major=major, year=year, rc=rc)


    # if major == "NULL" and year == "NULL":
    #     profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name", name=name_edit)
    # elif major == "NULL":
    #     profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name AND year = :year", name=name_edit, year=year)
    # elif year == "NULL":
    #     profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name AND major = :major", name=name_edit, major=major)
    # elif major and year:
    #     profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name AND major = :major AND year = :year", name=name_edit, major=major, year=year)
    return jsonify(profiles)


# Search for classes given a string
@app.route("/class_search")
def class_search():
    """"""
    class_id = request.args.get("class_id")
    class_id = str(class_id)
    class_id_edit = class_id + '%'
    classes = db.execute("SELECT * FROM classes WHERE class_id LIKE :class_id", class_id=class_id_edit)
    return jsonify(classes)


# Remove class that a user registered for
@app.route("/remove_class")
def remove_class():
    """"""
    db.execute("DELETE FROM class_registration WHERE user_id=:id AND class_id=:class_id",
               id=session["user_id"], class_id=request.args.get("class_id"))
    return redirect("/profile?id=self")


# Register classes for a user
@app.route("/class_change")
def class_change():
    """"""
    class_id = request.args.get("class_id")
    classes = db.execute("INSERT INTO class_registration (user_id, class_id) VALUES(:id, :class_id)",
                         id=session["user_id"], class_id=class_id)
    registrations = db.execute("SELECT * FROM class_registration WHERE user_id=:id", id=session["user_id"])
    return jsonify(registrations)


# User profile
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """"""
    if request.method == "GET":
        id = request.args.get("id")

        # Generate profile different if own
        if id == "self":
            profile = db.execute("SELECT * FROM profile WHERE id = :id", id=session["user_id"])
            return render_template("profile.html", profile=profile, isSelf=True)

        # Display profile of other user
        else:
            profile = db.execute("SELECT * FROM profile WHERE id = :id", id=id)
            connection = db.execute("SELECT * FROM connections WHERE (follower = :follower AND followed = :followed)",
                                    follower=session["user_id"], followed=id)

            # Determine if user has connection with profile
            if (not connection):
                return render_template("profile.html", profile=profile, isSelf=False, isConnected=False, id=json.dumps(id))
            else:
                return render_template("profile.html", profile=profile, isSelf=False, isConnected=True)

    # ???
    elif request.method == "POST":
        id = (int)(request.form.get("id"))
        profile = db.execute("SELECT * FROM profile WHERE id = :id", id=id)
        db.execute("INSERT INTO connections (follower, followed) VALUES (:follower, :followed)",
                   follower=session["user_id"], followed=id)
        return jsonify(True)


# Create and update profile
@app.route("/updateprofile", methods=["GET", "POST"])
@login_required
def updateprofile():
    """"""
    # Get information for form
    if request.method == "GET":
        majors = db.execute("SELECT id FROM majors")
        classes = db.execute("SELECT * FROM classes")
        return render_template("updateprofile.html", majors=majors, classes=classes)
    # Create / update user
    elif request.method == "POST":

        # Query to see if user already exists
        exist = db.execute("SELECT * FROM profile WHERE id = :id", id=session["user_id"])

        # If no profile picture submitted, add default
        if 'file' not in request.files:
            file_path = "./static/profile_pictures/yale.png"

        # If profile picture is added, add to static files
        else:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join('./static/profile_pictures', filename))
            file_path = "./static/profile_pictures/" + filename

        # If user exists, update their profile
        if exist:
            old_pic = db.execute("SELECT file_path FROM profile WHERE id=:id", id=session["user_id"])
<<<<<<< HEAD
            os.remove(old_pic[0]['file_path'])
=======
>>>>>>> 0a82d418adcee5b2df83f50c068d9eb706e5472f
            result = db.execute("UPDATE profile SET name=:name, major=:major, year=:year, residential_college=:residential_college, bio=:bio, file_path=:file_path WHERE id=:id", id=session["user_id"],
                                name=request.form.get("name"), major=request.form.get("major"), year=request.form.get("year"), residential_college=request.form.get("residential_college"), bio=request.form.get("bio"),
                                file_path=file_path)
        # Otherwise, create new user
        else:
            result = db.execute("INSERT INTO profile (id, name, major, year, residential_college, bio, file_path) VALUES(:id, :name, :major, :year, :residential_college, :bio, :file_path)", id=session["user_id"],
                                name=request.form.get("name"), major=request.form.get("major"), year=request.form.get("year"), residential_college=request.form.get("residential_college"), bio=request.form.get("bio"),
                                file_path=file_path)

        # Redirect to personal profile page
        return redirect("/profile?id=self")


# Allow users to connect with others
@app.route("/connections", methods=["GET", "POST"])
@login_required
def connections():

    # Display previously made connections
    if request.method == "GET":
        connections = []
        connections = db.execute("SELECT * FROM connections WHERE follower=:id", id=session["user_id"])
        followeds = []

        # Get information of connections
        for connection in connections:
            followeds.append(db.execute("SELECT * FROM profile WHERE id=:id", id=connection['followed'])[0])

        return render_template("connections.html", followeds=followeds)

    # ???
    if request.method == "POST":
        followedid = (int)(request.form.get("id"))
        db.execute("DELETE FROM connections WHERE (follower = :id AND followed = :followedid)",
                   id=session["user_id"], followedid=followedid)
        return jsonify(True)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run()