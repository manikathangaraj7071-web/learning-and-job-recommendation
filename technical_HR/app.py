from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
import random

app = Flask(
    __name__,
    template_folder="technical_HR/templates",
    static_folder="technical_HR/static"
)
app.secret_key = "interview_secret"

# ---------------- DATABASE ----------------
def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )

# ---------------- START ----------------
@app.route("/")
def start():
    # Clear session and initialize all variables safely
    session.clear()
    session["hr_index"] = 0
    session["tech_index"] = 0
    session["code_index"] = 0

    session["hr_answers"] = []
    session["tech_score"] = 0
    session["code_score"] = 0

    session["hr_q"] = []
    session["tech_q"] = []
    session["code_q"] = []

    session["code_answers"] = {}

    return redirect("/hr")

# ---------------- HR ROUND ----------------
@app.route("/hr", methods=["GET", "POST"])
def hr_round():
    if "hr_q" not in session:
        session["hr_q"] = []
    if "hr_answers" not in session:
        session["hr_answers"] = []
    if "hr_index" not in session:
        session["hr_index"] = 0

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM tech_hr_questions")
    questions = cur.fetchall()
    cur.close()
    db.close()

    if not questions:
        return "No HR questions in database"

    if not session["hr_q"]:
        random.shuffle(questions)
        session["hr_q"] = questions
    else:
        questions = session["hr_q"]

    index = session["hr_index"]

    if request.method == "POST":
        session["hr_answers"].append(request.form.get("answer"))
        session["hr_index"] += 1
        return redirect("/hr")

    if index >= len(questions):
        return redirect("/technical")

    return render_template(
        "hr_mic.html",
        question=questions[index],
        current=index + 1,
        total=len(questions)
    )

# ---------------- TECHNICAL MCQ ----------------
@app.route("/technical", methods=["GET", "POST"])
def technical_round():
    if "tech_q" not in session:
        session["tech_q"] = []
    if "tech_index" not in session:
        session["tech_index"] = 0
    if "tech_score" not in session:
        session["tech_score"] = 0

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM tech_questions")
    questions = cur.fetchall()
    cur.close()
    db.close()

    if not questions:
        return "No Technical questions in database"

    if not session["tech_q"]:
        random.shuffle(questions)
        session["tech_q"] = questions
    else:
        questions = session["tech_q"]

    index = session["tech_index"]

    if index >= len(questions):
        return redirect("/code")

    if request.method == "POST":
        if request.form.get("answer") == questions[index]["correct_option"]:
            session["tech_score"] += 1
        session["tech_index"] += 1
        return redirect("/technical")

    return render_template(
        "tech_one.html",
        question=questions[index],
        current=index + 1,
        total=len(questions)
    )

# ---------------- C CODING ROUND ----------------
@app.route("/code", methods=["GET", "POST"])
def code_round():
    if "code_q" not in session:
        session["code_q"] = []
    if "code_index" not in session:
        session["code_index"] = 0
    if "code_score" not in session:
        session["code_score"] = 0
    if "code_answers" not in session:
        session["code_answers"] = {}

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM code_questions")
    questions = cur.fetchall()
    cur.close()
    db.close()

    if not questions:
        return "No Coding questions in database"

    if not session["code_q"]:
        random.shuffle(questions)
        session["code_q"] = questions
    else:
        questions = session["code_q"]

    index = session["code_index"]

    if index >= len(questions):
        return redirect("/result")

    question = questions[index]
    result = session.pop("code_result", "")
    user_code = session["code_answers"].get(str(index), "")

    if request.method == "POST":
        action = request.form.get("action", "next")
        user_code = request.form.get("code", "")
        session["code_answers"][str(index)] = user_code

        if action == "prev":
            session["code_index"] -= 1
            return redirect("/code")

        # ------------------------
        # C CODE EXECUTION DISABLED FOR ONLINE DEPLOY
        result = "Code execution disabled in online deploy."

        if action == "next":
            session["code_index"] += 1
        if action == "finish":
            session["code_index"] = len(questions)

        session["code_result"] = result
        return redirect("/code")

    return render_template(
        "code_round.html",
        question=question,
        current=index + 1,
        total=len(questions),
        result=result,
        user_code=user_code
    )

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    hr_total = len(session.get("hr_q", []))
    tech_total = len(session.get("tech_q", []))
    code_total = len(session.get("code_q", []))

    hr_score = len([a for a in session.get("hr_answers", []) if a and a.strip()])
    tech_score = session.get("tech_score", 0)
    code_score = session.get("code_score", 0)

    hr_per = (hr_score / hr_total) * 100 if hr_total else 0
    tech_per = (tech_score / tech_total) * 100 if tech_total else 0
    code_per = (code_score / code_total) * 100 if code_total else 0

    total_score = hr_score + tech_score + code_score
    status = "Selected" if (hr_per >= 70 and tech_per >= 70 and code_per >= 70) else "Not Selected"

    return render_template(
        "result.html",
        hr_score=hr_score,
        tech_score=tech_score,
        code_score=code_score,
        total=total_score,
        hr_percentage=round(hr_per, 2),
        tech_percentage=round(tech_per, 2),
        code_percentage=round(code_per, 2),
        status=status
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
