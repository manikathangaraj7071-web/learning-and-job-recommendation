from flask import Flask, render_template, request

app = Flask(__name__)

# Correct answers
ANSWERS = {
    "q1": "A",
    "q2": "B",
    "q3": "C",
    "q4": "A",
    "q5": "D"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    total = len(ANSWERS)

    for q, ans in ANSWERS.items():
        if request.form.get(q) == ans:
            score += 1

    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)
