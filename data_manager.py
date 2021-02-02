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
        SELECT id, submission_time, vote_number, question_id, message, image
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
def add_new_comment(cursor: RealDictCursor,id:int,question_id:int,answer_id:int, message: str,submission_time:int, edited_number:int) -> list:
    query = """
        INSERT INTO comment(id, question_id, answer_id, message, submission_time, edited_number)
        VALUE %(id)s, %(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_number)s
        """
    cursor.execute(query, {"id": id,"question_id":question_id, "answer_id":answer_id, "message":message, "submission_time":submission_time, "edited_number":edited_number})
    return cursor.fetchall()


'''@database_common.connection_handler
def update_applicant_phone(cursor: RealDictCursor, number:str, code:int) -> list:
    query = """
        UPDATE applicant
        SET phone_number = %(number)s
        WHERE application_code = %(code)s"""
    cursor.execute(query,{"number":number, "code":code})'''







