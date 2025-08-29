from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "super-secret"

# ------------------- Calculator -------------------
@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]

        if operation == "add":
            result = num1 + num2
        elif operation == "sub":
            result = num1 - num2
        elif operation == "mul":
            result = num1 * num2
        elif operation == "div":
            result = num1 / num2 if num2 != 0 else "Error: Division by 0"

        if "history" not in session:
            session["history"] = []
        session["history"].insert(0, f"{num1} {operation} {num2} = {result}")
        session["history"] = session["history"][:5]

    return render_template("calculator.html", result=result)

@app.route("/history")
def history():
    return render_template("history.html", history=session.get("history", []))

# ------------------- Feedback -------------------
feedbacks = []

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        feedbacks.append({"name": name, "email": email, "message": message})
        return render_template("feedback.html", success=True)
    return render_template("feedback.html")

@app.route("/all_feedback")
def all_feedback():
    return render_template("all_feedback.html", feedbacks=feedbacks)

# ------------------- Quiz -------------------
questions = [
    {"q": "Which keyword is used to define a function in Python?",
     "options": ["func", "def", "function", "lambda"],
     "answer": "def"},
    {"q": "Which data type is immutable in Python?",
     "options": ["List", "Dictionary", "Tuple", "Set"],
     "answer": "Tuple"},
    {"q": "What does len([1,2,3]) return?",
     "options": ["2", "3", "4", "Error"],
     "answer": "3"}
]

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        score = 0
        for i, q in enumerate(questions):
            if request.form.get(f"q{i}") == q["answer"]:
                score += 1
        return render_template("quiz_result.html", score=score, total=len(questions))
    return render_template("quiz.html", questions=questions)


if __name__ == "__main__":
    app.run(debug=True)
