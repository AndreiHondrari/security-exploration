#!python

import json
from typing import Any
from flask import Flask, request, render_template, session, url_for, redirect

app = Flask(__name__)

app.config["SECRET_KEY"] = "fjq8fhwfgvhva90v7ha7hfv9gagv"


@app.route("/")
def index() -> Any:
    username = session.get("username")
    print(f"INDEX: Determined logged as \"{username}\"")

    context = {
        "logged": username is not None
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
        if username is not None:
            print(f"POSTMESSAGE: User {username} posts {message}")
            return redirect(url_for("post_success", **{'message': message}))

        return (
            json.dumps({"success": False}),
            400,
            {"Content-Type": "application/json"}
        )


@app.route("/postsuccess")
def post_success() -> Any:
    message = request.args.get('message')
    return render_template('success.html', **{'message': message})


if __name__ == "__main__":
    app.run(debug=True)
