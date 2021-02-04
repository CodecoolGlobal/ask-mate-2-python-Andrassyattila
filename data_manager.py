from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, img
        FROM question
        ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags(cursor: RealDictCursor) -> list:
    query = """
        SELECT name
        FROM tag
        ORDER BY name"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_comments(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM comment
        ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_data_question(cursor: RealDictCursor, id: int) -> list:
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, img
        FROM question
        WHERE id=%(id)s
        ORDER BY submission_time"""
    cursor.execute(query, {"id": id})
    return cursor.fetchall()

@database_common.connection_handler
def get_data_answer(cursor: RealDictCursor, id: int) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE id=%(id)s
        ORDER BY submission_time"""
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


@database_common.connection_handler
def get_data_answer_question(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE question_id=%(question_id)s
        ORDER BY submission_time"""
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()



@database_common.connection_handler
def get_data_comment(cursor: RealDictCursor, id: int) -> list:
    query = """
        SELECT question_id, message, submission_time, edited_number
        FROM comment
        WHERE id=%(id)s
        ORDER BY submission_time"""
    cursor.execute(query, {"id": id})
    return cursor.fetchall()



@database_common.connection_handler
def add_new_comment(cursor: RealDictCursor, question_id: int, message: str, submission_time: int, edited_number: int) -> list:
    query = """
        INSERT INTO comment(question_id, message, submission_time, edited_number)
        VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_number)s)
        """
    cursor.execute(query, {"question_id": question_id, "message": message, "submission_time": submission_time, "edited_number": edited_number})



@database_common.connection_handler
def add_new_answer(cursor: RealDictCursor,submission_time: int, vote_number: int, question_id: int, message: str,  image:str) -> list:
    query = """
        INSERT INTO answer(submission_time,vote_number, question_id, message, image)
        VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s,  %(image)s)
        """
    cursor.execute(query, {"question_id": question_id, "message": message, "submission_time": submission_time,"vote_number":vote_number, "image": image})



@database_common.connection_handler
def add_new_question(cursor: RealDictCursor, submission_time: int, view_number: int, vote_number: int, title: str, message: str, img: str) -> list:
    query = """
        INSERT INTO question( submission_time, view_number, vote_number, title, message, img)
        VALUES  (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(img)s)
        """
    cursor.execute(query, {"submission_time":submission_time, "view_number":view_number, "vote_number":vote_number, "title":title, "message":message, "img":img})


@database_common.connection_handler
def update_question(cursor: RealDictCursor, title:str, message: str, id:int) -> list:
    query = """
        UPDATE question
        SET title = %(title)s, message = %(message)s
        WHERE id = %(id)s"""
    cursor.execute(query,{"title":title, "message":message, "id":id})


@database_common.connection_handler
def update_question_vote(cursor: RealDictCursor, vote_number:int, id:int) -> list:
    query = """
        UPDATE question
        SET vote_number = %(vote)s
        WHERE id = %(id)s"""
    cursor.execute(query,{"vote":vote_number, "id":id})


@database_common.connection_handler
def update_answer_vote(cursor: RealDictCursor, vote_number:int, id:int) -> list:
    query = """i
        WHERE id = %(id)s
        UPDATE answer
        SET vote_number = %(vote)s
        WHERE id = %(id)s"""
    cursor.execute(query,{"vote":vote_number, "id":id})


@database_common.connection_handler
def get_data_question_vote(cursor: RealDictCursor, id: int) -> int:
    query = """
        SELECT vote_number
        WHERE id = %(id)s
        FROM question
        WHERE id=%(id)s
        """
    cursor.execute(query, {"id": id})
    return cursor.fetchall()

@database_common.connection_handler
def search_question(cursor: RealDictCursor, found_data: str) -> int:
    phrase = f'%{found_data}%'
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, img
        FROM question
        WHERE title LIKE %(found_data)s or message LIKE %(found_data)s
        """
    cursor.execute(query, {"found_data": phrase})
    return cursor.fetchall()


@database_common.connection_handler
def question_top_five(cursor: RealDictCursor) -> int:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC
        LIMIT 2
        """
    cursor.execute(query)
    return cursor.fetchall()


def select_comments(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT * FROM comment
        WHERE question_id = '{}'""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_new_comment_to_answer(cursor: RealDictCursor, answer_id: int, message: str, submission_time: int, edited_number: int) -> list:
    query = """
        INSERT INTO comment(answer_id, message, submission_time, edited_number)
        VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(edited_number)s)
        """
    cursor.execute(query, {"answer_id": answer_id, "message": message, "submission_time": submission_time, "edited_number": edited_number})


@database_common.connection_handler
def select_comments_to_answer(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT * FROM comment
        WHERE answer_id = '{}'""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int) -> list:
    query = """
    DELETE FROM question WHERE id=%(question_id)s"""
    cursor.execute(query, {"question_id": question_id})
    

@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
    DELETE FROM answer WHERE id=%(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id})


@database_common.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id: int) -> list:
    query = """
    DELETE FROM comment WHERE id=%(comment_id)s"""
    cursor.execute(query, {"comment_id": comment_id})


@database_common.connection_handler
def add_new_tag(cursor: RealDictCursor, tag:str) -> list:
    query = """
        INSERT INTO tag(name)
        VALUES (%(tag)s)
        """
    cursor.execute(query, {"tag":tag})


@database_common.connection_handler
def tag_to_question(cursor: RealDictCursor, question_id: int, tag_id:int) -> list:
    query = """
        INSERT INTO question_tag(question_id, tag_id)
        VALUES (%(question_id)s, %(tag_id)s)
        """
    cursor.execute(query, {"question_id":question_id,"tag_id":tag_id})