from flask import Flask, render_template, request, redirect
import data_handler
import data_manager
from operator import itemgetter
import csv
from datetime import datetime

app = Flask(__name__)
def get_data(file, id):
    for row in file:
        if row['id'] == id:
            return row

def get_data_answer(file, id):
    for row in file:
        if row['question_id'] == id:
            return row


def get_id(questions):
    sorted_questions = sorted(questions, key=itemgetter("id"))
    if len(sorted_questions)>0:
        return int(sorted_questions[-1]['id'])+1
    else:
        return 1    

def get_id_ans(answers):
    sorted_answers = sorted(answers, key=itemgetter("id"))
    if len(sorted_answers)>0:
        return int(sorted_answers[-1]['id'])+1
    else:
        return 1    


@app.route("/")
@app.route("/list")
def list():
    TABLE_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    questions = data_manager.get_questions()
    return render_template("list.html", TABLE_HEADERS=TABLE_HEADERS, questions=questions)


@app.route("/question/<string:question_id>/", methods=["POST", "GET"])
def display_question(question_id):
    questions = data_manager.get_questions()
    answers = data_manager.get_answers()
    return render_template("question.html", question_id=question_id, answers=answers, questions=questions)


@app.route("/question/<string:question_id>/edit/", methods=["POST", "GET"])
def edit(question_id):
    questions = data_manager.get_questions()
    question_to_update = get_data(questions, question_id)
    update_form = dict(request.form)
    if request.method == "POST":
        for row in questions:
            if row["id"] == question_to_update["id"]:
                question_to_update["title"] = update_form["title"]
                question_to_update["message"] = update_form["message"]
                questions.pop(questions.index(row))
                questions.append(question_to_update)
                with open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/question.csv", 'w', newline='') as csvfile:
                    fieldnames = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in questions:
                        writer.writerow(row)
        return redirect("/question/"+question_id)
    else:
        
        return render_template("edit.html", question_id=question_id, questions = questions, question_to_update = question_to_update,update_form=update_form )

    

@app.route("/add_question", methods=["POST", "GET"])
def question():
    if request.method == "POST":
        data = dict(request.form)
        with open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/question.csv", "a") as f:
            f.writelines(str(get_id(data_handler.open_db_questions()))+",")
            for i in range(2):
                f.writelines(" " + ",")
            f.writelines("0"+",")
            for i in data:
                if i == "question_name":
                    f.writelines(data[i] + ",")
                elif i == "description":
                    f.writelines(data[i])
            f.writelines("," + " " + "\n")
        return redirect("/list")
    return render_template("add-question.html")


@app.route("/question/<string:question_id>/newanswer/", methods=["POST", "GET"])
def answer(question_id):
    if request.method == "POST":
        data = dict(request.form)
        with open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/answer.csv", "a") as f:
            f.writelines(str(get_id_ans(data_handler.open_db_answer()))+",")
            for i in range(3):
                if i == 2:
                    f.writelines(question_id + ",")
                elif i == 1:
                    f.writelines("0"+",")
                else:
                    f.writelines(" " + ",")
            
            f.writelines(data["comment"])
            f.writelines("," + " " + "\n")
        return redirect("/list")
    return render_template("newanswer.html")



@app.route("/<string:question_id>/vote_up", methods=["POST","GET"])
def vote_up(question_id):
    question_id=question_id
    questions = data_manager.get_questions()
    question_to_update = get_data(questions, question_id)
    vote = int(question_to_update["vote_number"])
    if request.method == "GET":
        vote += 1
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
