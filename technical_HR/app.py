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
    session.setdefault("hr_q", [])
    session.setdefault("tech_q", [])
    session.setdefault("code_q", [])
    session.setdefault("hr_answers", {})
    session.setdefault("tech_score", 0)
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

    if request.method == "POST":
        # Store all HR answers from form
        hr_answers = {}
        for q in session["hr_q"]:
            hr_answers[str(q["id"])] = request.form.get(f"hr{q['id']}", "")
        session["hr_answers"] = hr_answers
        return redirect("/technical")

    return render_template("hr_round.html", hr_questions=session["hr_q"])

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

    if request.method == "POST":
        tech_score = 0
        for q in session["tech_q"]:
            user_ans = request.form.get(f"tech{q['id']}", "")
            if user_ans == q["correct_option"]:
                tech_score += 1
        session["tech_score"] = tech_score
        return redirect("/code")

    return render_template("tech_round.html", tech_questions=session["tech_q"])

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

    if request.method == "POST":
        for idx, q in enumerate(session["code_q"]):
            session["code_answers"][str(idx)] = request.form.get(f"code{q['id']}", "")
        return redirect("/result")

    return render_template("code_round.html", code_questions=session["code_q"], code_answers=session["code_answers"])

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    init_session()

    hr_total = len(session["hr_q"])
    tech_total = len(session["tech_q"])
    code_total = len(session["code_q"])

    hr_score = sum(1 for ans in session["hr_answers"].values() if ans.strip())
    tech_score = session.get("tech_score", 0)
    code_score = 0  # Optional: You can add code scoring logic later

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
