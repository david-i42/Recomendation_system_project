from database import Base,engine
from sqlalchemy import Column, Integer, String, Boolean, create_engine, func
from sqlalchemy.orm import sessionmaker

class User(Base):
    __tablename__="user"

    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)



if __name__ == "__main__":
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session=SessionLocal()

    result = session.query(User.country, User.os, func.count("*").label('user_count'))\
    .filter(User.exp_group ==3)\
    .group_by(User.country, User.os)\
    .having(func.count("*") > 100)\
    .order_by(func.count("*").desc())\
    .all()

    print(result)