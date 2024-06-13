from fastapi import FastAPI, Depends, Header
from typing import Annotated
from src.creating_tables import lifespan
from fastapi.security import OAuth2PasswordBearer
from src.login import signin, signout, signup
from src.oauth import oauth2_scheme
from src.helper_fun import get_current_user
from src.database import get_session
from sqlmodel import Session, select
from src.model import Users
from jose import jwt

from src.setting import ALGORITHM,SECRET_KEY
app = FastAPI()


@app.get("/newmainpage", response_model=dict[str, str])
def main(token:Annotated[OAuth2PasswordBearer,Depends(oauth2_scheme)] , session: Annotated[Session, Depends(get_session)]) -> dict[str, str]:
    print(f"signout token is {token}")
    current_user = session.exec(select(Users).where(Users.token == token)).first()
    if current_user:
        return {"message": "Welcome to the main page of our portal","token":token}
    else:
        return {"message": "Please login"}


app.include_router(signin.router)
app.include_router(signout.router)
app.include_router(signup.router)
