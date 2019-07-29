#!python

import uuid
import json
from typing import Any, Tuple
from flask import Flask, request, render_template, session, url_for, redirect

app = Flask(__name__)

app.config["SECRET_KEY"] = "fjq8fhwfgvhva90v7ha7hfv9gagv"

BAD_REQUEST = (
    json.dumps({"success": False}),
    400,
    {"Content-Type": "application/json"}
)


def get_db_csrf_tokens(username: str) -> Tuple[str, str]:
    session_token = None
    form_token = None

    with open("database.json", "r") as pf:
        db = json.load(pf)
        username_data = db.get(username)
        session_token = username_data.get('session_token')
        form_token = username_data.get('form_token')

    return session_token, form_token


def create_db_csrf_tokens(username: str) -> Tuple[str, str]:
    session_token = str(uuid.uuid4())
    form_token = str(uuid.uuid4())

    db = None

    # load db
    try:
        with open("database.json", "r") as pf:
            db = json.load(pf)
    except FileNotFoundError:
        db = {}

    # write to db
    with open("database.json", "w") as pf:
        db[username] = {
            "session_token": session_token,
            "form_token": form_token
        }
        json.dump(db, pf)

    return session_token, form_token


@app.route("/")
def index() -> Any:
    username = session.get("username")

    # make sure to handle anti-forgery tokens creation and retrieval
    csrf_session_token = session.get("csrf-token")
    db_form_token = ""
    db_session_token = None

    if csrf_session_token is not None:
        print("INDEX[CSRF]: Detected existing tokens")
        db_session_token, db_form_token = get_db_csrf_tokens(username)
        if db_form_token is None:
            print("INDEX[CSRF] Form token missing, remake all!")
            db_session_token, db_form_token = create_db_csrf_tokens(username)
    else:
        print("INDEX: No CSRF tokens detected. Create new ones!")
        db_session_token, db_form_token = create_db_csrf_tokens(username)
        session["csrf-token"] = db_session_token

    print(f"INDEX[CSRF]: SESSION {db_session_token} FORM {db_form_token}")

    print(f"INDEX: Determined logged as \"{username}\"")

    context = {
        "logged": username is not None,
        "csrf_token": db_form_token
    }
    return render_template("index.html", **context)


@app.route("/login", methods=["POST"])
def login() -> Any:
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(f"LOGIN: {username} {password}")
        if not (username == "myuser" and password == "1234"):
            return (
                json.dumps({"success": False}),
                400,
                {"Content-Type": "application/json"}
            )

        session['username'] = username
        return redirect(url_for("index"))


@app.route("/logout")
def logout() -> Any:
    username = session.pop("username")
    print(f"LOGOUT: {username}")
    return redirect(url_for("index"))


@app.route("/postmessage", methods=["POST"])
def post_message() -> Any:
    if request.method == "POST":
        username = session.get("username")
        message = request.form.get("message")

        # get CSRF tokens
        csrf_session_token = session.get("csrf-token")
        csrf_form_token = request.form.get("csrf_token")
        db_session_token, db_form_token = get_db_csrf_tokens(username)

        is_csrf_session_null = csrf_session_token is None
        is_csrf_form_null = csrf_form_token is None
        is_invalid_csrf_session = csrf_session_token != db_session_token
        is_invalid_csrf_form = csrf_form_token != db_form_token

        post_message = "POSTMESSAGE[CSRF STATE]: \n"
        post_message += f"CSRF SESSION NULL: {is_csrf_session_null}\n"
        post_message += f"CSRF FORM NULL: {is_csrf_form_null}\n"
        post_message += f"CSRF SESSION INVALID: {is_invalid_csrf_session}\n"
        post_message += f"CSRF FORM INVALID: {is_invalid_csrf_form}\n"
        print(post_message)

        if (any([
            is_csrf_session_null,
            is_csrf_form_null,
            is_invalid_csrf_session,
            is_invalid_csrf_form
        ])):
            return BAD_REQUEST

        if username is not None:
            print(f"POSTMESSAGE: User {username} posts {message}")

            return redirect(url_for("post_success", **{'message': message}))

        return BAD_REQUEST


@app.route("/postsuccess")
def post_success() -> Any:
    message = request.args.get('message')
    return render_template('success.html', **{'message': message})


if __name__ == "__main__":
    app.run(debug=True)
