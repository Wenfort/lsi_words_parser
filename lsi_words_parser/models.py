from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    password = Column(String)

    __table_args__ = {'schema': 'lsi_words'}


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    shortlink = Column(String)
    is_complete = Column(Boolean)

    __table_args__ = {'schema': 'lsi_words'}


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    order_id = Column(Integer, ForeignKey('lsi_words.order.id'))

    __table_args__ = {'schema': 'lsi_words'}


class LSI(Base):
    __tablename__ = 'lsi'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    percent = Column(Integer)
    request_id = Column(Integer, ForeignKey('lsi_words.request.id'))

    __table_args__ = {'schema': 'lsi_words'}


class IpHistory(Base):
    __tablename__ = 'ip_history'

    ip = Column(String, primary_key=True)
    counter = Column(Integer)

    __table_args__ = {'schema': 'lsi_words'}


if __name__ == '__main__':
    from lsi_words_parser.db import engine

    User.__table__.create(engine)
    Order.__table__.create(engine)
    Request.__table__.create(engine)
    LSI.__table__.create(engine)
    IpHistory.__table__.create(engine)
