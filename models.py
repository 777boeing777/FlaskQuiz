from typing import Iterable, Any, Dict
from config import db
import datetime
from marshmallow import Schema


class QuizQuestion(db.Model):
    __tablename__ = 'quiz'

    prev_data = []
    temp_data = []

    def __init__(self, id: int, question: str, answer: str, created_at: datetime) -> None:
        self.id = id
        self.question = question
        self.answer = answer
        self.created_at = created_at

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Date)

    @classmethod
    def get_ids_set(cls) -> set:
        return set(db.session.query(QuizQuestion.id).all())

    @classmethod
    def add_new_question(cls, data: dict):
        q = QuizQuestion(**data)
        db.session.add(q)
        db.session.commit()

    @classmethod
    def insert_data(cls, data: Iterable):
        cleared_data = []
        for question in data:
            instance = db.session.query(QuizQuestion).filter(QuizQuestion.id == question['id']).one_or_none()
            if instance is None:
                cleared_data.append(question)
        if cleared_data:
            db.session.bulk_insert_mappings(QuizQuestion, cleared_data)
            cls.mark_data_as_prev(data=cleared_data)
            db.session.commit()
        else:
            return False

    @classmethod
    def delete_all(cls):
        db.session.query(QuizQuestion).delete()
        db.session.commit()

    @classmethod
    def mark_data_as_prev(cls, data: Iterable):
        cls.prev_data = cls.temp_data
        cls.temp_data = data

    @classmethod
    def get_prev_data(cls):
        return cls.prev_data

    @classmethod
    def get_all_questions(cls):
        return db.session.query(QuizQuestion).all()

    def __repr__(self) -> str:
        return '<Quiz(id={id}, question={qtext})>'.format(id=self.id, qtext=self.question)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
