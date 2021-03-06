from app.libs.enums import PendingStatus
from .base import Base
from sqlalchemy import Column, Integer, String, SmallInteger


class Drift(Base):
    """
    一次具体的交易信息
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    request_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)  # 状态

    @property
    def pending(self):
        """
        读取_pending,转化为枚举类型
        :return:
        """
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        """
        把枚举转化为_pending
        :param status:
        :return:
        """
        self._pending = status.value
