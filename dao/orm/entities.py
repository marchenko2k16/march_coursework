from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, ForeignKey, ForeignKeyConstraint, ARRAY, JSON
Base = declarative_base()


class Company(Base):
    __tablename__ = 'company'
    Company = Column(String, primary_key = True, nullable=False)

class Department(Base):
    __tablename__ = 'department'
    Department = Column(String, primary_key = True, nullable=False)

class User(Base):
    __tablename__ = 'user'
    Username = Column(String, primary_key = True, nullable=False)
    Password = Column(String, nullable=False)
    Company = Column(String, nullable= False)
    Department = Column(String, nullable=False)

class Message(Base):
    __tablename__ = 'message'
    MessageContent = Column(String)
    MessageReciever = Column(String)
    MessageSender = Column(String)
    MessageID = Column(Integer, primary_key=True, nullable=False)
    MessageDate = Column(Date)
