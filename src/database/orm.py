"""
Database ORM
"""
import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relation, relationship
from sqlalchemy.ext.declarative import declarative_base

from config.system import CONN_URL


engine = create_engine(CONN_URL, echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)


def create_all():
    Base.metadata.create_all(engine)


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id = Column(Integer, primary_key=True, unique=True)
    is_bot = Column(Boolean)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    added = Column(DateTime, default=datetime.datetime.now())


class BackendData(Base):
    __tablename__ = "backend_data"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey(TelegramUser.id), unique=True)
    telegram_user = relation('TelegramUser', remote_side=TelegramUser.id)
    data = Column(String)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey(TelegramUser.id), unique=True)
    telegram_user = relation('TelegramUser', remote_side=TelegramUser.id)
    is_root = Column(Boolean, default=False)

    # TODO add permissions system for admins


if __name__ == '__main__':
    create_all()
