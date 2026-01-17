from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manikam@2005",   # your MySQL password
    database="aptitude_test1"
)

cursor = db.cursor(dictionary=True)

# ---------------- HOME PAGE ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- TEST PAGE ----------------
@app.route('/test')
def test():
    cursor.execute("SELECT * FROM project")
    questions = cursor.fetchall()
    return render_template('test.html', questions=questions)

# ---------------- SUBMIT & RESULT ----------------
@app.route("/submit", methods=["POST"])
def submit():
    cursor.execute("SELECT * FROM project")
    questions = cursor.fetchall()

    print(request.form)   # DEBUG

    score = 0
    total = len(questions)

    for q in questions:
        user_answer = request.form.get(f"q{q['id']}")

        if user_answer is not None and int(user_answer) == int(q['correct_option']):
            score += 1

    return render_template("result.html", score=score, total=total)





# ---------------- RUN SERVER ----------------
if __name__ == '__main__':
    app.run(port=5000,debug=True)
