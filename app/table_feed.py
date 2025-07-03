from database import Base,engine
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, create_engine, func, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from table_post import Post
from table_user import User

class Feed(Base):
    __tablename__="feed_action"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    action = Column(String)
    time = Column(TIMESTAMP)
    
    user = relationship(User)
    post = relationship(Post)

if __name__ == "__main__":
    Base.metadata.create_all(engine)