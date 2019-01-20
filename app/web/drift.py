from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web

from sqlalchemy import desc, or_


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.request_id == current_user.id,
                                    Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()
    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


# 用filter代替filter_by， 并使用or_


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)

    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的，不能向自己索要书籍')
        return redirect('web.book_detail', isbn=current_gift.isbn)

    can = current_user.can_send_drift()  # 当前用户是否可以发起鱼漂
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html', wisher=current_user,
                  gift=current_gift)  # 发邮件通知
        return redirect(url_for('web.pending'))
    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


# 一系列其他视图函数之后

def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)  # form数据传递给模型

        drift.gift_id = current_gift.id
        drift.request_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.grifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)
