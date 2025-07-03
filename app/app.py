from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from database import SessionLocal
from table_user import User
from table_post import Post
from table_feed import Feed
from schema import UserGet, PostGet, FeedGet

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db
    
@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user:
        return UserGet(id=user.id, gender=user.gender, age=user.age, country=user.country, city=user.city, exp_group=user.exp_group, os=user.os, source=user.source)
    else:
        raise HTTPException(status_code=404, detail="user not found")

@app.get("/post/{id}", response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if post:
        return PostGet(id=post.id, text=post.text, topic=post.topic)
    else:
        raise HTTPException(status_code=404, detail="user not found")
    

#task 9

@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_actions(id: int, limit: int=10, db: Session = Depends(get_db)):
    #feed = db.query(Feed).filter(Feed.user_id == id).first()
    return db.query(Feed).filter(Feed.user_id==id).order_by(Feed.time.desc()).limit(limit).all()




@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_actions(id: int, limit: int=10, db: Session = Depends(get_db)):
    #feed = db.query(Feed).filter(Feed.post_id == id).first()
    #print(f'feed={feed}')
    return db.query(Feed).filter(Feed.post_id==id).order_by(Feed.time.desc()).limit(limit).all()


@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_recommendations(id: int=0, limit: int=10, db: Session = Depends(get_db)):
    query = db.query(Post)\
    .select_from(Feed)\
    .filter(Feed.action == 'like')\
    .join(Post)\
    .group_by(Post.id)\
    .order_by(func.count(Post.id).desc())\
    .limit(limit).all()

    if query:
        return query
    else:
        return []




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8899)



#localhost:8899/sum_date?current_date=2008-01-15&offset=2
    