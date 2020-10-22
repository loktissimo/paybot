from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from paybotsqlalch import users, posts, Base, engine


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


session = DBSession()

# Insert a user in the person table
new_user = users(username='User 1')
session.add(new_user)
session.commit()

# Insert a post in the
new_post = posts(body='text text text', users=new_user)
session.add(new_post)
session.commit()