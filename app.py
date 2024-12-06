from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Initializing custom questions list and category management
custom_questions = []
categories = set()  # Set to store unique categories

def get_random_questions(num_questions, questions_per_test):
    selected_questions = []
    category_counts = {}

    while len(selected_questions) < num_questions:
        random_question = random.choice(custom_questions)
        category = random_question['category']

        if category not in category_counts:
            category_counts[category] = 0
        
        if category_counts[category] < questions_per_test:
            selected_questions.append(random_question)
            category_counts[category] += 1

    return selected_questions

@app.route('/', methods=['GET', 'POST'])
def index():
    global custom_questions, categories

    if request.method == 'POST':
        if 'add_question' in request.form:
            custom_question_text = request.form['custom_question']
            category = request.form['category']
            custom_questions.append({"question": custom_question_text, "category": category})
            categories.add(category)  # Add category to the set to track it

        elif 'generate_tests' in request.form:
            num_tests = int(request.form['num_tests'])
            num_questions = int(request.form['num_questions'])
            questions_per_test = int(request.form['questions_per_test'])

            test_questions = get_random_questions(num_questions, questions_per_test)
            tests = [test_questions[i::num_tests] for i in range(num_tests)]

            return render_template('index.html', tests=tests, custom_questions=custom_questions, categories=categories, enumerate=enumerate)

    return render_template('index.html', tests=None, custom_questions=custom_questions, categories=categories, enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)
