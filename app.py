from flask import Flask, render_template, request, jsonify
import openai
import json

app = Flask(__name__)

# ✅ Set up OpenAI API key
openai.api_key = "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"

# ✅ STEM subject prompts
STEM_PROMPTS = {
    "math": "You are a mathematics tutor. Focus on explaining mathematical concepts clearly, showing step-by-step solutions, and providing practice problems when appropriate. Cover topics from algebra, calculus, statistics, and other mathematical fields.",
    "science": "You are a science tutor. Explain scientific concepts with real-world examples, break down complex processes, and relate topics to current scientific developments. Cover physics, chemistry, and biology concepts.",
    "tech": "You are a technology and computer science tutor. Provide clear explanations of programming concepts, include code examples when relevant, and explain technical concepts in an accessible way. Focus on practical applications.",
    "engineering": "You are an engineering tutor. Focus on applied mathematics, physics, and design principles. Explain engineering concepts with real-world examples and problem-solving approaches."
}

QUIZ_PROMPTS = {
    "math": "Generate a math quiz question appropriate for the current topic. Format: {'question': 'detailed question', 'correct_answer': 'answer', 'explanation': 'detailed explanation'}",
    "science": "Generate a science quiz question about fundamental concepts. Format: {'question': 'detailed question', 'correct_answer': 'answer', 'explanation': 'detailed explanation'}",
    "tech": "Generate a technology/programming quiz question. Format: {'question': 'detailed question', 'correct_answer': 'answer', 'explanation': 'detailed explanation'}",
    "engineering": "Generate an engineering quiz question. Format: {'question': 'detailed question', 'correct_answer': 'answer', 'explanation': 'detailed explanation'}"
}

# ✅ Quiz tracking variables
current_quiz_question = None  
quiz_total_questions = 0  
quiz_correct_answers = 0  
quiz_target_questions = 0  

@app.route("/")
def home():
    return render_template("index.html")

# ✅ Handle General Questions
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    mode = data.get("mode", "math")

    messages = [
        {"role": "system", "content": STEM_PROMPTS.get(mode, "You are a knowledgeable AI tutor.")},
        {"role": "user", "content": question}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": STEM_PROMPTS.get(mode, "You are a knowledgeable AI tutor.")}, {"role": "user", "content": question}]
        )

        ai_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Start Quiz (User Specifies Number of Questions)
@app.route("/start_quiz", methods=["POST"])
def start_quiz():
    global quiz_total_questions, quiz_correct_answers, quiz_target_questions
    data = request.json
    quiz_target_questions = int(data.get("num_questions", 1))  
    quiz_total_questions = 0  
    quiz_correct_answers = 0
    return generate_quiz_question(data.get("mode", "math"))

# ✅ Generate a Quiz Question
def generate_quiz_question(mode="math"):
    global current_quiz_question
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": QUIZ_PROMPTS[mode]},
                {"role": "user", "content": "Generate a question in valid JSON format with fields: question, correct_answer, and explanation"}
            ],
            temperature=0.7
        )

        content = response["choices"][0]["message"]["content"].strip()
        
        if not content.startswith('{'):
            content = content[content.find('{'):]
        if not content.endswith('}'):
            content = content[:content.rfind('}')+1]

        current_quiz_question = json.loads(content)

        return jsonify(current_quiz_question)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Check User's Answer and Continue Quiz
@app.route("/check_answer", methods=["POST"])
def check_answer():
    global current_quiz_question, quiz_total_questions, quiz_correct_answers

    data = request.json
    user_answer = data.get("answer", "").strip().lower()
    mode = data.get("mode", "math")

    if not current_quiz_question:
        return jsonify({"response": "No active quiz question. Please start a quiz first."})

    correct_answer = current_quiz_question["correct_answer"].strip().lower()
    is_correct = user_answer == correct_answer

    quiz_total_questions += 1
    if is_correct:
        quiz_correct_answers += 1

    response_text = "✅ Correct!" if is_correct else f"❌ Incorrect. The correct answer is: {current_quiz_question['correct_answer']}"

    if quiz_total_questions >= quiz_target_questions:
        percentage = (quiz_correct_answers / quiz_total_questions) * 100
        final_grade = f"📊 Quiz Over! You answered {quiz_correct_answers} out of {quiz_total_questions} correctly. Your score: {percentage:.1f}%."
        return jsonify({"response": response_text, "explanation": current_quiz_question["explanation"], "final": final_grade})

    # Get the next question as a Python dict
    next_question_response = generate_quiz_question(mode)
    if next_question_response.status_code == 200:
        next_question_data = json.loads(next_question_response.get_data())
        return jsonify({
            "response": response_text,
            "explanation": current_quiz_question["explanation"],
            "next_question": next_question_data["question"]
        })
    else:
        return jsonify({"response": response_text, "error": "Failed to generate next question."})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
