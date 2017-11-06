import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///tiddly.db", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)

dbsession = Session()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    def repr(self):
        return "<User (name=%s, email=%s, )>" % (name, email)

class Dual(Base):
    __tablename__ = "dual"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    def repr(self):
        return "<Dual (id=%s, text=%s)>" % (id, text)
