from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from src.model import Users
from typing import Annotated
from src.database import get_session
from src.helper_fun import get_current_user
from src.oauth import oauth2_scheme

router = APIRouter()


@router.post("/signout")
def signout(
    token: Annotated[OAuth2PasswordBearer, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)],
):
    print(f"signout token is {token}")
    user = get_current_user(token, session)
    if user:
        user.token = None
        session.add(user)
        session.commit()
    return {"message": f"Successfully signed out and token is {token} user:{user}"}
