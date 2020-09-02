from flask import Blueprint, request, render_template, redirect, session, url_for
# 函数库
from utils.get_md5 import get_md5
from utils.ch_login import is_login
# 数据库模型
from app.models import db, User
import datetime

web_bpt = Blueprint('web_bpt', __name__, static_folder='static', template_folder='templates')

# 测试页面
@web_bpt.route('/test', methods=['get', 'post'])
def test():
    if request.method == 'GET':
        return render_template('test.html')

# 登录页面
@web_bpt.route('/', methods=['GET', 'POST'])
@web_bpt.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    # if request.method == 'POST':
    #     return render_template('component_bottom.html')


@web_bpt.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        # 密码MD5加密
        password = get_md5(request.form['password'])

        if not all([username, password]):
            msg = '*请填写完整的信息'
            return render_template('login.html', msg=msg)
        # 验证账号密码
        if User.query.filter_by(username=username, password=password).first():
            session['username'] = username
            session['password'] = password
            return redirect(url_for('index'))
        else:
            msg = '* 用户名或者密码不一致'
            return render_template('login.html', msg=msg)

# 注册页面
@web_bpt.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', msg='用户名重复')
        if len(username) < 3 or len(username) > 15:
            return render_template('register.html', msg='用户名长度3-15')
        password1 = get_md5(request.form['pwd1'])
        password2 = get_md5(request.form['pwd2'])
        if password1 != password2:
            return render_template('register.html', msg='两次密码不一致')

        time = datetime.datetime.now()
        db.session.add(User(username=username, password=password2, u_create_time=time))
        db.session.commit()
        return redirect(url_for('login'))

# 注销
@web_bpt.route('/logout', methods=['GET', 'POST'])
@is_login
def logout():
    if request.method == 'GET':
        # 清楚session
        session.clear()
        return redirect(url_for('login'))