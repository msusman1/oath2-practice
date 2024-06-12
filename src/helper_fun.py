

from fastapi import   Depends 
from sqlmodel import Session, select
from jose import jwt
from src.model import Users
from typing import Annotated
from src.database import get_session
from src.oauth import oauth2_scheme
from src.setting import ALGORITHM,SECRET_KEY
 

def get_user(session: Session, username: str):
    return session.exec(select(Users).where(Users.user_name == username)).first()

def verify_password(user_password, db_password):
    return user_password == db_password   
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session:Annotated[Session , Depends(get_session)]):
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = decode_token.get("sub")
    user = get_user(session, username)
    return user





 