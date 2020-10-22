# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, exists, and_, join
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, class_mapper, join

# setting DB-file to work with
engine = create_engine('sqlite:///paybot_sqlalch.db',
                       connect_args={'check_same_thread': False})  # multiple threads error bypass

# DB tables description
Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chat'
    # Here we define columns for the table
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    chat_name = Column(String(250), nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    user_name = Column(String(250), nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.id'))


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer, nullable=False)
    body = Column(String(250), nullable=False)
    # First name column should be added !!!
    user_id = Column(Integer, ForeignKey('user.id'))


# Base.metadata.create_all(engine)  # Create all databases listed in classes above


# Adding data to Tables
DBSession = sessionmaker(bind=engine)
session = DBSession()


def new_chat(chat_id, chat_name):
    row_exists = session.query(exists().where(Chat.chat_id == chat_id)).scalar()
    if row_exists:
        return
    else:
        insert = Chat(chat_id=chat_id, chat_name=chat_name)
        session.add(insert)
        session.commit()


def new_user(user_id, user_name, chat_id):
    row_exists = session.query(exists().where(and_(User.chat_id == chat_id,
                                                   User.user_id == user_id))).scalar()
    if row_exists:
        return
    else:
        insert = User(user_id=user_id, user_name=user_name, chat_id=chat_id)
        session.add(insert)
        session.commit()


def new_post(timestamp, body, user_id):
    # First name column should be added !!!
    insert = Post(timestamp=timestamp, body=body, user_id=user_id)
    session.add(insert)
    session.commit()


def update_post(timestamp, body):
    session.query(Post.timestamp, Post.body). \
        filter(Post.timestamp == timestamp). \
        update({Post.body: body})
    session.commit()

# def show_stat(chat_id, user_id):


# -----------
#   Testing
# -----------

q = session.query(Post.user_id).join(User).all()
q = session.query(Post).join(User).join(User.user_name)
q = session.query(User).\
            join(Post, Post.user_id == User.user_id)
print(q)



#  User.user_id == 172613840))


# print(session.query(exists().where(User.user_id == '172613840').where(User.chat_id == '-253931503')).scalar())
# print(session.query(exists().where(User.user_id == '172613840').where(User.chat_id == '-243187088')).scalar())

# update_post(1522230738, 'update text new text 111')
# print(session.query(Post.timestamp, Post.body).filter(Post.timestamp == 1522230738).all())
# print(session.query(User.user_name, User.user_id).all())
# update_post(1522230738, 'test_update')

