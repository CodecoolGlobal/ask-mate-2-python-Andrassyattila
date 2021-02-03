from flask import Flask, render_template, request, redirect
import data_handler
import data_manager
from operator import itemgetter
import csv
from datetime import datetime

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def list():
    TABLE_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    questions = data_manager.get_questions()
    return render_template("list.html", TABLE_HEADERS=TABLE_HEADERS, questions=questions)


@app.route("/question/<string:question_id>/", methods=["POST", "GET"])
def display_question(question_id):
    questions = data_manager.get_data_question(question_id)
    answers = data_manager.get_answers()
    return render_template("question.html", question_id=question_id, answers=answers, questions=questions)


@app.route("/question/<string:question_id>/edit/", methods=["POST", "GET"])
def edit(question_id):
    question_to_update = data_manager.get_data_question(question_id)
    if request.method == "POST":
        new_title = request.form["update-title"]
        new_message = request.form["update-message"]
        data_manager.update_question(new_title, new_message, question_id)
        return redirect("/question/"+question_id)
    else:
        
        return render_template("edit.html", question_id=question_id, question_to_update = question_to_update)


@app.route("/add_question", methods=["POST", "GET"])
def question():
    if request.method == "POST":
        data_manager.add_new_question(0, 0, 0, request.form["question_name"], request.form["description"], "")
        return redirect("/list")
    return render_template("add-question.html")


@app.route("/question/<string:question_id>/newanswer/", methods=["POST", "GET"])
def answer(question_id):
    if request.method == "POST":
        data_manager.add_new_answer(0, 0, question_id, request.form["comment"],"")
        return redirect("/question/"+question_id)
    return render_template("newanswer.html")



@app.route("/<string:question_id>/vote_up", methods=["POST","GET"])
def vote_up(question_id):
    question_id=question_id
    question_to_update = data_manager.get_data_question(question_id)
    vote = int(question_to_update["vote_number"])
    if request.method == "GET":
        vote += 1
        data_manager.update_question_vote(vote, question_id)
        return redirect("/list")
   

@app.route("/<string:question_id>/vote_down", methods=["POST","GET"])
def vote_down(question_id):
    question_id = question_id
    questions = data_manager.get_questions()
    question_to_update = get_data(questions, question_id)
    vote = int(question_to_update["vote_number"])
    if request.method == "GET":
        vote -= 1
        question_to_update["vote_number"]=str(vote)
        questions.pop(questions.index(question_to_update))
        questions.append(question_to_update)
        with open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/question.csv", 'w', newline='') as csvfile:
            fieldnames = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in questions:
                writer.writerow(row)
        return redirect("/list")

@app.route("/question/<string:question_id>/delete_question/",methods=["POST", "GET"])
def delete_question(question_id):
    questions = data_manager.get_questions()
    question_to_update = get_data(questions, question_id)
    if request.method == "GET":
        questions.pop(questions.index(question_to_update))
        with open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/question.csv", 'w', newline='') as csvfile:
                fieldnames = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in questions:
                    writer.writerow(row)
        return redirect("/list")


@app.route("/question/<string:question_id>/delete_answer/<string:answer_id>/", methods=["POST", "GET"])
def delete_answer(answer_id,question_id):
    question_id=question_id
    answers = data_manager.get_answers()
    answer_to_update = get_data(answers, answer_id)
    if request.method == "GET":
        answers.pop(answers.index(answer_to_update))
        with open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/answer.csv", 'w', newline='') as csvfile:
            fieldnames = ["id","submission_time","vote_number","question_id","message","image"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in answers:
                writer.writerow(row)
        return redirect("/list")


@app.route("/question/<string:question_id>/vote_up_answer", methods=["POST", "GET"])
def vote_up_answer(question_id):
    question_id=question_id
    answers = data_manager.get_answers()
    answer_to_update = get_data_answer(answers, question_id)
    vote = int(answer_to_update["vote_number"])
    if request.method == "GET":
        vote += 1
        answer_to_update["vote_number"]=str(vote)
        answers.pop(answers.index(answer_to_update))
        answers.append(answer_to_update)
        with open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/answer.csv", 'w', newline='') as csvfile:
            fieldnames = ["id","submission_time","vote_number","question_id","message,image"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in answers:
                writer.writerow(row)
        return redirect("/list")

@app.route("/question/<string:question_id>/vote_down_aswer", methods=["POST", "GET"])
def vote_down_answer(question_id):
    question_id = question_id
    questions = data_manager.get_questions()
    question_to_update = get_data_answer(questions, question_id)
    vote = int(question_to_update["vote_number"])
    if request.method == "GET":
        vote -= 1
        question_to_update["vote_number"]=str(vote)
        questions.pop(questions.index(question_to_update))
        questions.append(question_to_update)
        with open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/question.csv", 'w', newline='') as csvfile:
            fieldnames = ["id","submission_time","vote_number","question_id","message,image"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in questions:
                writer.writerow(row)
        return redirect("/list")
if __name__ == "__main__":
    app.run(
        debug=True
    )
