from .app import app, db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))

class ChatData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    usersname = db.Column(db.String(50), nullable=False)

class QAData(db.Model):
    question = db.Column(db.Text, primary_key=True)
    answer = db.Column(db.Text)
    ishelp = db.Column(db.String(1))

class GroupData(db.Model):
    gossip = db.Column(db.Text, primary_key=True)
    username = db.Column(db.String(50))

from flask import current_app

def initialize_database():
    with current_app.app_context():
        existing_tables = db.engine.table_names()
        if 'user' not in existing_tables and 'chat_data' not in existing_tables and 'group_data' not in existing_tables and 'qa_data' not in existing_tables:
            db.create_all()

        # Clean the database
        db.session.query(GroupData).delete()
        db.session.commit()
