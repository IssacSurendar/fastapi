from fastapi import APIRouter, HTTPException, Response, status, Depends
import schemas, models, utils, oauth2
from database import *
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=['posts'])

@router.get('/', response_model=List[schemas.PostOut])
async def get_all_post(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search:Optional[str]=""):

    # post_data = db.query(models.Post).filter(models.Post.user_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.user_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create(request: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **request.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.PostOut)
async def get_post_byid(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    # post_data = db.query(models.Post).filter(models.Post.id == id).first()
    post_data = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post_data)
    if post_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id:{id} not found")

    if post_data.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action")   

    return post_data


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id : {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message': "deleted successfully."}


@router.put('/{id}')
async def update_post(id:int, request: schemas.PostBase, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    query.update(request.dict(), synchronize_session=False)
    db.commit()
    return query.first()