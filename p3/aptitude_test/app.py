from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Manikam@2005",   # 👉 your MySQL password
    database="aptitude_test"
)

cursor = db.cursor(dictionary=True)

@app.route("/")
def show_questions():
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    return render_template("questions.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
