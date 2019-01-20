from flask import current_app

from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from collections import namedtuple
from app.spider.yushu_book import YuShuBook

EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)  # 是否送出去了

    @property
    def book(self):  # 通过isbn获取书籍的信息
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first  # 从api的搜索结果中获取第一本就行

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn，到Gift表中检索出相应的礼物， 并且计算出某个礼物的Wish心愿数量
        # query(func.count(Wish.id), Wish.isbn) 这样查询出来count_list列表的每个元素都是是 wish的数量,对应isbn 组成的元组
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()  # filter接收条件表达式
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]  # 改成字典
        return count_list

    @classmethod
    # 逻辑实现, 只筛选没有赠送出去的
    def recent(cls):
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
