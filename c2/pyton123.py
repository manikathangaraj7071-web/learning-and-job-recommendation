from flask import Flask, render_template, jsonify, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manikam@2005",
    database="communication_db"
)
cursor = db.cursor(dictionary=True)


@app.route("/")
def index():
    return render_template("test.html")


@app.route("/get_questions")
def get_questions():
    questions = []

    # PART A – Reading & Listening (8)
    cursor.execute("SELECT id, passage FROM reading_listening LIMIT 8")
    for q in cursor.fetchall():
        questions.append({
            "section": "Reading & Listening",
            "type": "read_mic",
            "id": q["id"],
            "question_text": q["passage"]
        })

    # PART B – Listen & Repeat (8)
    cursor.execute("""
        SELECT id, question_text, correct_text, audio_file 
        FROM listen_repeat 
        LIMIT 8
    """)
    for q in cursor.fetchall():
        questions.append({
            "section": "Listen & Repeat",
            "type": "audio_mic",
            "id": q["id"],
            "question_text": q["question_text"],
            "audio_file": q["audio_file"],
            "answer": q["correct_text"]
        })

    # PART C – Speak on Topic (1)
    cursor.execute("SELECT id, topic FROM speak_topic LIMIT 1")
    q = cursor.fetchone()
    if q:
        questions.append({
            "section": "Speak on Topic",
            "type": "prep_speak",
            "id": q["id"],
            "question_text": q["topic"]
        })

    # PART D – MCQ (10)
    cursor.execute("""
        SELECT id, question, option_a, option_b, option_c, option_d, correct_option
        FROM mcq_questions
        LIMIT 10
    """)
    for q in cursor.fetchall():
        questions.append({
            "section": "MCQ",
            "type": "mcq",
            "id": q["id"],
            "question_text": q["question"],
            "options": [
                q["option_a"],
                q["option_b"],
                q["option_c"],
                q["option_d"]
            ],
            "correct_answer": q["correct_option"]
        })

    # ✅ RETURN MUST BE INSIDE FUNCTION
    return jsonify(questions)

@app.route("/result")
def result():
    score = request.args.get("score", 0)
    return render_template("result.html", score=int(score))



@app.route("/save_result", methods=["POST"])
def save_result():
    data = request.json
    cursor.execute(
        "INSERT INTO user_results (section, question_id, user_answer, score) VALUES (%s,%s,%s,%s)",
        (data["section"], data["question_id"], data["user_answer"], data["score"])
    )
    db.commit()
    return jsonify({"status": "saved"})


if __name__ == "__main__":
    app.run(port=5001,debug=True)
