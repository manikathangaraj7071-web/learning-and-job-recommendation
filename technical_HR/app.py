from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os, random

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "interview_secret")

# ---------------- DATABASE ----------------
def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        autocommit=True
    )

# ---------------- SESSION INIT ----------------
def init_session():
    session.setdefault("hr_index", 0)
    session.setdefault("tech_index", 0)
    session.setdefault("code_index", 0)

    session.setdefault("hr_answers", [])
    session.setdefault("hr_q", [])
    session.setdefault("tech_q", [])
    session.setdefault("code_q", [])

    session.setdefault("tech_score", 0)
    session.setdefault("code_score", 0)
    session.setdefault("code_answers", {})

# ---------------- START ----------------
@app.route("/")
def start():
    session.clear()
    init_session()
    return redirect("/hr")

# ---------------- HR ROUND ----------------
@app.route("/hr", methods=["GET", "POST"])
def hr_round():
    init_session()

    if not session["hr_q"]:
        try:
            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT * FROM tech_hr_questions")
            session["hr_q"] = cur.fetchall()
            random.shuffle(session["hr_q"])
            cur.close()
            db.close()
        except:
            return "Database connection error"

    index = session["hr_index"]

    if request.method == "POST":
        session["hr_answers"].append(request.form.get("answer", ""))
        session["hr_index"] += 1
        return redirect("/hr")

    if index >= len(session["hr_q"]):
        return redirect("/technical")

    return render_template(
        "hr_mic.html",
        question=session["hr_q"][index],
        current=index + 1,
        total=len(session["hr_q"])
    )

# ---------------- TECHNICAL MCQ ----------------
@app.route("/technical", methods=["GET", "POST"])
def technical_round():
    init_session()

    if not session["tech_q"]:
        try:
            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT * FROM tech_questions")
            session["tech_q"] = cur.fetchall()
            random.shuffle(session["tech_q"])
            cur.close()
            db.close()
        except:
            return "Database connection error"

    index = session["tech_index"]

    if index >= len(session["tech_q"]):
        return redirect("/code")

    if request.method == "POST":
        if request.form.get("answer") == session["tech_q"][index]["correct_option"]:
            session["tech_score"] += 1
        session["tech_index"] += 1
        return redirect("/technical")

    return render_template(
        "tech_one.html",
        question=session["tech_q"][index],
        current=index + 1,
        total=len(session["tech_q"])
    )

# ---------------- CODING ROUND ----------------
@app.route("/code", methods=["GET", "POST"])
def code_round():
    init_session()

    if not session["code_q"]:
        try:
            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT * FROM code_questions")
            session["code_q"] = cur.fetchall()
            random.shuffle(session["code_q"])
            cur.close()
            db.close()
        except:
            return "Database connection error"

    index = session["code_index"]

    if index >= len(session["code_q"]):
        return redirect("/result")

    if request.method == "POST":
        action = request.form.get("action", "next")
        session["code_answers"][str(index)] = request.form.get("code", "")

        if action == "prev":
            session["code_index"] = max(0, index - 1)
        elif action == "next":
            session["code_index"] += 1
        elif action == "finish":
            return redirect("/result")

        return redirect("/code")

    return render_template(
        "code_round.html",
        question=session["code_q"][index],
        current=index + 1,
        total=len(session["code_q"]),
        user_code=session["code_answers"].get(str(index), ""),
        result="Code execution disabled in online deploy"
    )

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    init_session()

    hr_total = len(session["hr_q"])
    tech_total = len(session["tech_q"])
    code_total = len(session["code_q"])

    hr_score = sum(1 for a in session["hr_answers"] if a.strip())
    tech_score = session["tech_score"]
    code_score = session["code_score"]

    hr_per = (hr_score / hr_total) * 100 if hr_total else 0
    tech_per = (tech_score / tech_total) * 100 if tech_total else 0
    code_per = (code_score / code_total) * 100 if code_total else 0

    status = "Selected" if (tech_per >= 70 and code_per >= 70) else "Not Selected"

    return render_template(
        "result.html",
        hr_score=hr_score,
        tech_score=tech_score,
        code_score=code_score,
        hr_percentage=round(hr_per, 2),
        tech_percentage=round(tech_per, 2),
        code_percentage=round(code_per, 2),
        status=status
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os, random

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "interview_secret")

# ---------------- DATABASE ----------------
def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        autocommit=True
    )

# ---------------- SESSION INIT ----------------
def init_session():
    session.setdefault("hr_index", 0)
    session.setdefault("tech_index", 0)
    session.setdefault("code_index", 0)

    session.setdefault("hr_answers", [])
    session.setdefault("hr_q", [])
    session.setdefault("tech_q", [])
    session.setdefault("code_q", [])

    session.setdefault("tech_score", 0)
    session.setdefault("code_score", 0)
    session.setdefault("code_answers", {})

# ---------------- START ----------------
@app.route("/")
def start():
    session.clear()
    init_session()
    return redirect("/hr")

# ---------------- HR ROUND ----------------
@app.route("/hr", methods=["GET", "POST"])
def hr_round():
    init_session()

    if not session["hr_q"]:
        try:
            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT * FROM tech_hr_questions")
            session["hr_q"] = cur.fetchall()
            random.shuffle(session["hr_q"])
            cur.close()
            db.close()
        except:
            return "Database connection error"

    index = session["hr_index"]

    if request.method == "POST":
        session["hr_answers"].append(request.form.get("answer", ""))
        session["hr_index"] += 1
        return redirect("/hr")

    if index >= len(session["hr_q"]):
        return redirect("/technical")

    return render_template(
        "hr_mic.html",
        question=session["hr_q"][index],
        current=index + 1,
        total=len(session["hr_q"])
    )

# ---------------- TECHNICAL MCQ ----------------
@app.route("/technical", methods=["GET", "POST"])
def technical_round():
    init_session()

    if not session["tech_q"]:
        try:
            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT * FROM tech_questions")
            session["tech_q"] = cur.fetchall()
            random.shuffle(session["tech_q"])
            cur.close()
            db.close()
        except:
            return "Database connection error"

    index = session["tech_index"]

    if index >= len(session["tech_q"]):
        return redirect("/code")

    if request.method == "POST":
        if request.form.get("answer") == session["tech_q"][index]["correct_option"]:
            session["tech_score"] += 1
        session["tech_index"] += 1
        return redirect("/technical")

    return render_template(
        "tech_one.html",
        question=session["tech_q"][index],
        current=index + 1,
        total=len(session["tech_q"])
    )

# ---------------- CODING ROUND ----------------
@app.route("/code", methods=["GET", "POST"])
def code_round():
    init_session()

    if not session["code_q"]:
        try:
            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT * FROM code_questions")
            session["code_q"] = cur.fetchall()
            random.shuffle(session["code_q"])
            cur.close()
            db.close()
        except:
            return "Database connection error"

    index = session["code_index"]

    if index >= len(session["code_q"]):
        return redirect("/result")

    if request.method == "POST":
        action = request.form.get("action", "next")
        session["code_answers"][str(index)] = request.form.get("code", "")

        if action == "prev":
            session["code_index"] = max(0, index - 1)
        elif action == "next":
            session["code_index"] += 1
        elif action == "finish":
            return redirect("/result")

        return redirect("/code")

    return render_template(
        "code_round.html",
        question=session["code_q"][index],
        current=index + 1,
        total=len(session["code_q"]),
        user_code=session["code_answers"].get(str(index), ""),
        result="Code execution disabled in online deploy"
    )

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    init_session()

    hr_total = len(session["hr_q"])
    tech_total = len(session["tech_q"])
    code_total = len(session["code_q"])

    hr_score = sum(1 for a in session["hr_answers"] if a.strip())
    tech_score = session["tech_score"]
    code_score = session["code_score"]

    hr_per = (hr_score / hr_total) * 100 if hr_total else 0
    tech_per = (tech_score / tech_total) * 100 if tech_total else 0
    code_per = (code_score / code_total) * 100 if code_total else 0

    status = "Selected" if (tech_per >= 70 and code_per >= 70) else "Not Selected"

    return render_template(
        "result.html",
        hr_score=hr_score,
        tech_score=tech_score,
        code_score=code_score,
        hr_percentage=round(hr_per, 2),
        tech_percentage=round(tech_per, 2),
        code_percentage=round(code_per, 2),
        status=status
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
