from . import web
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from app.forms.auth import RegisterForm, LoginForm
from app.models.user import User
from app.models.base import db


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('web.login'))  # 注册完成后重定向, 原理是修改location的信息，即url_for得到的url
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():  # 通过验证，则存入数据库
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)  # 设置remember=True则默认保存365天， 没有remember则是一次性cookie
            # 实质依然是把 user数据保存在cookie中
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')

    return render_template('auth/login.html', form=form)


@web.route('/forget-password', methods=['GET', 'POST'])
def forget_password_request():
    pass
