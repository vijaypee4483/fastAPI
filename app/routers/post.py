from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from app import oauth2
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# @app.get("/")
# def root():
#     return {"message": "Welcome to my api"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()

    # return{"status": posts}

# @router.get('/', response_model=List[schemas.Post])
@router.get('/',response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user),
            Limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.owner_id == 
    #     current_user.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True
                ).group_by(models.Post.id).filter(models.Post.title.contains(search)
                ).limit(Limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts

# @app.post('/createposts')
# def create_posts(new_post: schemas.PostCreate):
#     print (new_post)
#     return {"data": "new post"}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title = post.title, content = post.content, 
                            # published = post.published)
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True
                ).filter(models.Post.id == id).group_by(models.Post.id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found")
        # responce.status_code = status.HTTP_404_NOT_FOUND
        # return {"post_detail": f"Post with id: {id} was not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id),)
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
                        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorised to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    return {"message": "Post was successfully deleted"}

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # print(post)
    # return {"message": "Post is updated"}
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorised to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # print(post_dict)
    # my_posts[index] = post_dict
    return post_query.first()



