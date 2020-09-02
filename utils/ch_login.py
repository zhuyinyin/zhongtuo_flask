from flask import url_for,redirect,session
from functools import wraps
from app.models import User

"""
登录验证装饰器
"""


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user = session.get('username')
        psw = session.get('password')
        if User.query.filter_by(username=user, password=psw).first():
            return func(*args, **kwargs)
        else:
            return redirect(url_for('web_bpt.login'))
    return check_login
