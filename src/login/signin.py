from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from sqlmodel import Session
from src.database import get_session
from src.helper_fun import get_user, verify_password
from src.create_token import create_access_token

router = APIRouter()

@router.post("/signin")
def signin(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
           session: Annotated[Session, Depends(get_session)]):
    user = get_user(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=1)
    access_token = create_access_token(
        username=user.user_name, validation_time=access_token_expires
    )
    user.token = access_token
    session.add(user)
    session.commit()
    return {"message": "Login Successfully", "token": access_token}
