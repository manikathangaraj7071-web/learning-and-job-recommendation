from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manikam@2005",   # your MySQL password
    database="aptitude_test1"
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    cursor.execute("SELECT * FROM sample")
    questions = cursor.fetchall()
    return render_template('test.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    cursor.execute("SELECT * FROM sample")
    questions = cursor.fetchall()

    score = 0

    for q in questions:
        user_answer = request.form.get(f"q{q['id']}")
        if user_answer == q['correct_option']:
            score += 1

    return render_template(
        'result.html',
        score=score,
        total=len(questions)
    )

if __name__ == '__main__':
    app.run(debug=True)
