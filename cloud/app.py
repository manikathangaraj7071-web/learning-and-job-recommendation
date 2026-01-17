from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "interview_secret"

# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Manikam@2005",
        database="interview_db"
    )

# ---------------- START HR ROUND ----------------
@app.route("/")
def start_hr():
    session.clear()
    session["index"] = 0
    session["hr_answers"] = []
    return redirect("/hr")

# ---------------- HR ROUND (ONE QUESTION, MIC) ----------------
@app.route("/hr", methods=["GET", "POST"])
def hr():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM cloud_hr_questions")
    questions = cur.fetchall()
    cur.close()
    db.close()

    index = session.get("index", 0)

    if request.method == "POST":
        answer = request.form.get("answer")
        session["hr_answers"].append(answer)
        index += 1
        session["index"] = index

    # HR finished → Result
    if index >= len(questions):
        return redirect("/result")

    return render_template(
        "hr_mic.html",
        question=questions[index],
        current=index + 1,
        total=len(questions)
    )

# ---------------- RESULT PAGE (HR ONLY) ----------------
@app.route("/result")
def result():
    hr_answers = session.get("hr_answers", [])
    hr_score = len([ans for ans in hr_answers if ans and ans.strip() != ""])

    tech_score = 0  # Technical disabled
    total = hr_score

    status = "Selected" if hr_score >= 3 else "Not Selected"

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO interview_results (hr_score, tech_score, total_score, status) VALUES (%s,%s,%s,%s)",
        (hr_score, tech_score, total, status)
    )
    db.commit()
    cur.close()
    db.close()

    return render_template(
        "result.html",
        hr_score=hr_score,
        tech_score=tech_score,
        total=total,
        status=status
    )

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(port=5004,debug=True)
