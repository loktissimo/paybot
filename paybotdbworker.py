# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, exists, and_, join
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, class_mapper, join

# setting DB-file to work with
engine = create_engine('sqlite:///paybot_db.db',
                       connect_args={'check_same_thread': False})  # multiple threads error bypass

# DB tables description
Base = declarative_base()

# Creating session instance
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Here we define columns for the table
class Chat(Base):
    __tablename__ = 'chat'
    num = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)

    def new_chat(id, name):
        row_exists = session.query(exists().where(Chat.id == id)).scalar()
        if row_exists:
            return
        else:
            insert = Chat(id=id, name=name)
            session.add(insert)
            session.commit()


class User(Base):
    __tablename__ = 'user'
    num = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)

    def new_user(id, name, firstname):
        row_exists = session.query(exists().where(User.id == id)).scalar()
        if row_exists:
            return
        else:
            insert = User(id=id, name=name, firstname=firstname)
            session.add(insert)
            session.commit()


class Post(Base):
    __tablename__ = 'post'
    num = Column(Integer, primary_key=True)
    timestamp = Column(Integer, nullable=False)
    body = Column(String(250), nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def new_post(timestamp, body, chat_id, user_id):
        insert = Post(timestamp=timestamp, body=body, chat_id=chat_id, user_id=user_id)
        session.add(insert)
        session.commit()

    def update_post(timestamp, body):
        session.query(Post.timestamp, Post.body). \
            filter(Post.timestamp == timestamp). \
            update({Post.body: body})
        session.commit()

    # def show_stat(chat_id, user_id):


# Base.metadata.create_all(engine)  # Create all databases listed in classes above

def main():
    pass


if __name__ == "__main__":
    main()


# Testing

print(session.query(Post.body, User.name, Chat.name).
      join(User).
      join(Chat).
      filter(User.name == 'Alexander').
      filter(Chat.name == 'bot_test_1').
      all())


# new_chat(111, 'Test')
# new_user(111, '@lkt', 'Alex')
# new_post(123123, '/text text', 111, 111)

#  User.user_id == 172613840))

# print(session.query(exists().where(User.user_id == '172613840').where(User.chat_id == '-253931503')).scalar())
# print(session.query(exists().where(User.user_id == '172613840').where(User.chat_id == '-243187088')).scalar())

# update_post(1522230738, 'update text new text 111')
# print(session.query(Post.timestamp, Post.body).filter(Post.timestamp == 1522230738).all())
# print(session.query(User.user_name, User.user_id).all())
# update_post(1522230738, 'test_update')

