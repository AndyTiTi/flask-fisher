from app.libs.helper import is_isbn_or_key
from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)  # 数据库表的字段名默认为为_password， 这里手动设置为password
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))  # 将来开发小程序使用的
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):  # 检查传入密码是否正确
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
            # 不允许一个用户同时赠送多本相同的书
            # launched表示 如果有书但没送出去，你也不能上传书
            gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
            wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
            if not gifting and not wishing:
                return True
            else:
                return False


@login_manager.user_loader
def get_user(uid):  # 给flask_login 的login_required用得
    return User.query.get(int(uid))  # 通过id返回用户模型
