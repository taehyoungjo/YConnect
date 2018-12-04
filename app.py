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
    name_edit = '%' + name + '%'
    major = request.args.get("major")
    year = request.args.get("year")
    if major == "NULL" and year == "NULL":
        profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name", name=name_edit)
    elif major == "NULL":
        profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name AND year = :year", name=name_edit, year=year)
    elif year == "NULL":
        profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name AND major = :major", name=name_edit, major=major)
    elif major and year:
        profiles = db.execute("SELECT * FROM profile WHERE name LIKE :name AND major = :major AND year = :year", name=name_edit, major=major, year=year)
    return jsonify(profiles)

@app.route("/class_search")
def class_search():
    """"""
    class_id = request.args.get("class_id")
    class_id = str(class_id)
    class_id_edit = class_id + '%'
    classes = db.execute("SELECT * FROM classes WHERE class_id LIKE :class_id", class_id=class_id_edit)
    return jsonify(classes)

@app.route("/class_change")
def class_change():
    """"""
    class_id = request.args.get("class_id")
    classes = db.execute("INSERT INTO course_registration (user_id, course_id) VALUES(:id, :class_id)", id=session["user_id"], class_id=class_id)
    registrations = db.execute("SELECT * FROM course_registration WHERE user_id=:id", id=session["user_id"])
    return jsonify(registrations)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """"""
    if request.method == "GET":
        id = request.args.get("id")
        if id == "self":
            profile = db.execute("SELECT * FROM profile WHERE id = :id", id=session["user_id"])
            return render_template("profile.html", profile=profile, isSelf=True)
        else:
            profile = db.execute("SELECT * FROM profile WHERE id = :id", id=id)
            connection = db.execute("SELECT * FROM connections WHERE (follower = :follower AND followed = :followed)", follower=session["user_id"], followed=id)
            if (not connection):
                return render_template("profile.html", profile=profile, isSelf=False, isConnected=False, id=json.dumps(id))
            else:
                return render_template("profile.html", profile=profile, isSelf=False, isConnected=True)

    elif request.method == "POST":
        id = (int)(request.form.get("id"))
        profile = db.execute("SELECT * FROM profile WHERE id = :id", id=id)
        db.execute("INSERT INTO connections (follower, followed) VALUES (:follower, :followed)", follower=session["user_id"], followed=id)
        return jsonify(True);

@app.route("/updateprofile", methods=["GET", "POST"])
@login_required
def updateprofile():
    """"""
    if request.method == "GET":
        majors = db.execute("SELECT id FROM majors")
        classes = db.execute("SELECT * FROM classes")
        return render_template("updateprofile.html", majors=majors, classes=classes)
    elif request.method == "POST":
        exist = db.execute("SELECT * FROM profile WHERE id = :id", id=session["user_id"])
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('./static/profile_pictures', filename))
        file_path = "./static/profile_pictures/" + filename
        if exist:
            old_pic = db.execute("SELECT file_path FROM profile WHERE id=:id", id=session["user_id"])
            #os.remove(old_pic[0]['file_path'])
            result = db.execute("UPDATE profile SET name=:name, major=:major, year=:year, residential_college=:residential_college, bio=:bio, file_path=:file_path WHERE id=:id", id=session["user_id"],
                name=request.form.get("name"), major=request.form.get("major"), year=request.form.get("year"), residential_college=request.form.get("residential_college"), bio=request.form.get("bio"),
                file_path=file_path)
        else:
            result = db.execute("INSERT INTO profile (id, name, major, year, residential_college, bio, file_path) VALUES(:id, :name, :major, :year, :residential_college, :bio, :file_path)", id=session["user_id"],
                name=request.form.get("name"), major=request.form.get("major"), year=request.form.get("year"), residential_college=request.form.get("residential_college"), bio=request.form.get("bio"),
                file_path=file_path)
        return redirect("/profile?id=self")

@app.route("/connections", methods=["GET", "POST"])
@login_required
def connections():

    connections = []
    if request.method == "GET":
        connections = db.execute("SELECT * FROM connections WHERE follower=:id", id=session["user_id"])
        print(connections)

    followeds = []
    for connection in connections:
        followeds.append(db.execute("SELECT * FROM profile WHERE id=:id", id=connection['followed'])[0])

    print(followeds)

    return render_template("connections.html", followeds=followeds)

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