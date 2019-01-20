from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import desc, func
from app.spider.yushu_book import YuShuBook
from flask import current_app


class Wish(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)  # 是否送出去了
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)

    @classmethod
    def get_user_wishes(cls, uid):
        gifts = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return gifts

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from .gift import Gift
        # 根据传入的一组isbn，到Wish表中检索出相应的心愿， 并且计算出某个心愿的Gift心愿数量
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(Gift.launched == False,
                                                                             Gift.isbn.in_(isbn_list),
                                                                             Gift.status == 1).group_by(
            Gift.isbn).all()  # filter接收条件表达式
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @classmethod
    def recent(cls):
        recent_gift = Wish.query.filter_by(launched=False).group_by(Wish.isbn).order_by(desc(Wish.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()

        return recent_gift

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

