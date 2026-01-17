from flask import Flask, render_template, request, redirect, session
import mysql.connector
from difflib import SequenceMatcher

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manikam@2005",
    database="communication_db"
)
cursor = db.cursor(dictionary=True)


@app.route("/")
def home():
    session.clear()
    return redirect("/speak/1")


@app.route("/speak/<int:qno>")
def speak(qno):
    cursor.execute("SELECT * FROM speech_questions")
    questions = cursor.fetchall()

    if qno > len(questions):
        return redirect("/result")

    session["questions"] = questions

    return render_template(
        "speak.html",
        question=questions[qno-1],
        qno=qno,
        total=len(questions)
    )


@app.route("/submit_speak/<int:qno>", methods=["POST"])
def submit_speak(qno):
    user_answer = request.form.get("answer", "").lower()
    correct_text = session["questions"][qno-1]["question_text"].lower()

    score = calculate_score(correct_text, user_answer)

    if "score" not in session:
        session["score"] = 0

    session["score"] += score

    return redirect(f"/speak/{qno+1}")


def calculate_score(correct, user):
    similarity = SequenceMatcher(None, correct, user).ratio()
    percentage = similarity * 100

    if percentage >= 90:
        return 1
    elif percentage >= 75:
        return 0.75
    elif percentage >= 50:
        return 0.5
    else:
        return 0


@app.route("/result")
def result():
    total = len(session.get("questions", []))
    score = session.get("score", 0)

    return render_template("result.html", score=score, total=total)


if __name__ == "__main__":
    app.run(debug=True)
