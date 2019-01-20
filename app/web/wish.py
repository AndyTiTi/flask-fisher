from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models.base import db
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from . import web


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/<isbn>')
@login_required
def satisfy_wish(isbn):
    pass


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id

            db.session.add(wish)
    else:
        flash("这本书以添加进您的赠送清单或已经存在于您的心愿清单，请不要重复添加")
    return redirect(url_for('web.book_detail', isbn=isbn))
