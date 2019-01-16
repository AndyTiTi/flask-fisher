from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True  # 这样sqlalchemy就不会去创建Base的表了
    status = Column(SmallInteger)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
