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
        WHERE question_id=%(id)s
        ORDER BY submission_time"""
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


@database_common.connection_handler
def add_new_comment(cursor: RealDictCursor, question_id: int, answer_id: int, message: str, submission_time: int, edited_number: int) -> list:
    query = """
        INSERT INTO comment(id, question_id, answer_id, message, submission_time, edited_number)
        VALUES (%(id)s, %(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_number)s)
        """
    cursor.execute(query, {"id": id, "question_id": question_id, "answer_id": answer_id, "message": message, "submission_time": submission_time, "edited_number": edited_number})



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
    query = """
        UPDATE answer
        SET vote_number = %(vote)s
        WHERE id = %(id)s"""
    cursor.execute(query,{"vote":vote_number, "id":id})

