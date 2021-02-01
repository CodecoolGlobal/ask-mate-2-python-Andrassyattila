import csv
fieldnames_question = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]


def open_db_questions():
    results=[]
    csvfile = open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/question.csv","r")
    reader= csv.DictReader(csvfile)
    for row in reader:
        results.append(dict(row))
    return results

def open_db_answer():
    results = []
    csvfile = open("/home/gergely/projects/2.module/ask-mate-1-python-Andrassyattila/sample_data/answer.csv", "r")
    reader = csv.DictReader(csvfile)
    for row in reader:
        results.append(dict(row))
    return results

'''def update_csv(file, fieldnames, questions):
    upd_list=upd_list_a
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in questions:
            writer.writerow(row)'''

