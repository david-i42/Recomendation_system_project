from database import Base,engine
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker

class Post(Base):
    __tablename__="post"
    id = Column(Integer, primary_key=True)	
    text = Column(String)
    topic = Column(String)

if __name__ == "__main__":
    Base.metadata.create_all(engine)


    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session=SessionLocal()

    session1 = session.query(Post)\
    .filter(Post.topic =="business")\
    .order_by(Post.id.desc())\
    .limit(10)

    print([post.id for post in session1])