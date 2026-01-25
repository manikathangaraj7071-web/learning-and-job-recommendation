from flask import Flask, render_template, request, redirect, session
import mysql.connector, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "render_secret")

# ---------- DB ----------
def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "localhost"),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD", "Manikam@2005"),
        database=os.getenv("MYSQLDATABASE", "login"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )

# ---------- LOGIN (FIRST PAGE) ----------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = user["username"]
            return redirect("/dashboard")
        else:
            error = "Username or Password mismatch ❌"

    return render_template("login.html", error=error)

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        db = get_db()
        cur = db.cursor(dictionary=True)

        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            msg = "User already exists ❗"
        else:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            db.commit()
            cur.close()
            db.close()

            # 🔁 IMPORTANT: redirect to login
            return redirect("/login")

        cur.close()
        db.close()

    return render_template("register.html", msg=msg)
@app.route("/front5")
def front5():
    return "This is front5"




# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return f"<h2>Welcome {session['user']} 🎉</h2><a href='/logout'>Logout</a>"

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
