from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.community import CommunityPost, CommunityComment, PostLike, CommentLike
from models.user import User
from utils.dependencies import get_current_user
from schemas.community import PostCreate, CommentCreate, PostResponse

router = APIRouter(tags=["Community"])

@router.post("", response_model=PostResponse, summary="게시글 작성")
def create_post(post_data: PostCreate, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    post = CommunityPost(
        title=post_data.title,
        content=post_data.content,
        desired_job=post_data.desired_job,
        author_id=user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.put("/{post_id}", summary="게시글 수정")
def update_post(post_id: int, post_data: PostCreate, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    user = db.query(User).filter(User.email == current_user_email).first()
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")
    post.title = post_data.title
    post.content = post_data.content
    post.desired_job = post_data.desired_job
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", summary="게시글 삭제")
def delete_post(post_id: int, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    user = db.query(User).filter(User.email == current_user_email).first()
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
    db.delete(post)
    db.commit()
    return {"message": "게시글이 삭제되었습니다."}

@router.post("/{post_id}/comments", summary="댓글 작성")
def create_comment(post_id: int, comment_data: CommentCreate, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    comment = CommunityComment(
        content=comment_data.content,
        post_id=post_id,
        author_id=user.id
    )
    db.add(comment)
    db.commit()
    return {"message": "댓글이 작성되었습니다."}

@router.put("/{post_id}/comments/{comment_id}", summary="댓글 수정")
def update_comment(post_id: int, comment_id: int, comment_data: CommentCreate, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    comment = db.query(CommunityComment).filter(CommunityComment.id == comment_id, CommunityComment.post_id == post_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    user = db.query(User).filter(User.email == current_user_email).first()
    if comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")
    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return {"message": "댓글이 수정되었습니다."}

@router.delete("/{post_id}/comments/{comment_id}", summary="댓글 삭제")
def delete_comment(post_id: int, comment_id: int, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    comment = db.query(CommunityComment).filter(CommunityComment.id == comment_id, CommunityComment.post_id == post_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    user = db.query(User).filter(User.email == current_user_email).first()
    if comment.author_id != user.id:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
    db.delete(comment)
    db.commit()
    return {"message": "댓글이 삭제되었습니다."}

@router.post("/{post_id}/like", summary="게시글 좋아요")
def like_post(post_id: int, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    existing = db.query(PostLike).filter(PostLike.post_id == post_id, PostLike.user_id == user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 좋아요를 눌렀습니다.")

    like = PostLike(post_id=post_id, user_id=user.id)
    db.add(like)
    db.commit()
    return {"message": f"게시글 {post_id}에 좋아요가 추가되었습니다."}

@router.delete("/{post_id}/like", summary="게시글 좋아요 취소")
def unlike_post(post_id: int, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    like = db.query(PostLike).filter(PostLike.post_id == post_id, PostLike.user_id == user.id).first()
    if not like:
        raise HTTPException(status_code=404, detail="좋아요 기록이 없습니다.")

    db.delete(like)
    db.commit()
    return {"message": "게시글 좋아요가 취소되었습니다."}

@router.post("/{post_id}/comments/{comment_id}/like", summary="댓글 좋아요")
def like_comment(post_id: int, comment_id: int, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    existing = db.query(CommentLike).filter(CommentLike.comment_id == comment_id, CommentLike.user_id == user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 좋아요를 눌렀습니다.")

    like = CommentLike(comment_id=comment_id, user_id=user.id)
    db.add(like)
    db.commit()
    return {"message": f"댓글 {comment_id}에 좋아요가 추가되었습니다."}

@router.delete("/{post_id}/comments/{comment_id}/like", summary="댓글 좋아요 취소")
def unlike_comment(post_id: int, comment_id: int, current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    like = db.query(CommentLike).filter(CommentLike.comment_id == comment_id, CommentLike.user_id == user.id).first()
    if not like:
        raise HTTPException(status_code=404, detail="좋아요 기록이 없습니다.")

    db.delete(like)
    db.commit()
    return {"message": "댓글 좋아요가 취소되었습니다."}