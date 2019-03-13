from flask import render_template

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from flask_login import login_required, current_user
from . import web


@web.route('/')
def index():
    """
        首页视图函数
    """
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    return render_template('personal.html', user=current_user.summary)
