from flask import Flask, render_template
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
def listen_repeat():
    cursor.execute("SELECT * FROM listen_repeat ORDER BY id")
    questions = cursor.fetchall()
    return render_template("listen_repeat.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
