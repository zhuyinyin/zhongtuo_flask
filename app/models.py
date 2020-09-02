from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 用户模型
class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(32))
    u_create_time = db.Column(db.DateTime, default=datetime.now)

