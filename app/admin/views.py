from flask import Blueprint, request, render_template, redirect, session, url_for

# 蓝图
admin_bpt = Blueprint('admin_bpt', __name__, static_folder='static', template_folder='templates')


@admin_bpt.route("/", methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('logins.html')


@admin_bpt.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('web_bpt.register'))
