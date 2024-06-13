

from fastapi import FastAPI,  Depends    
from typing import Annotated 
from src.creating_tables import lifespan 
from fastapi.security import  OAuth2PasswordBearer
from src import signin,signup,signout,helper_fun

 
 
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
app = FastAPI(lifespan=lifespan, title='Login Portal')
 
@app.get("/mainpage",response_model=dict[str,str])
def main(token: Annotated[OAuth2PasswordBearer, Depends(oauth2_scheme)])->dict[str,str]:
    return {"message": f"Welcome to the main page of our portal"}
 

app.include_router(signin.router)
app.include_router(signout.router)
app.include_router(signup.router)
 
 
oauth2_scheme.include_router(helper_fun.oauth_scheme)
oauth2_scheme.include_router(signout.oauth_scheme)
 
 
 
 
 
from jose import jwt
from datetime import datetime, timedelta
ALGORITHM = "HS256"
SECRET_KEY = "A Secure Secret Key"

def create_access_token(username: str, validation_time: timedelta) -> str:
    expiry_minutes = datetime.utcnow() + validation_time
    json_data = {"sub": username, "exp": expiry_minutes}
    encoded_jwt = jwt.encode(json_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
 
 

from fastapi import FastAPI
from src.database import engine
from contextlib import asynccontextmanager
from src.model import Users


def create_tables():
    Users.metadata.create_all(engine)
     
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("This statement will executes before the Creating tables....")
    create_tables()
    yield  
     
from sqlmodel import create_engine, Session 
from src.setting import DATA_BASE_URL
 
connection_string = str(DATA_BASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine( connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

def get_session():
    with Session(engine) as session:
        yield session
   


from fastapi import   Depends, HTTPException,APIRouter
from sqlmodel import Session, select
from jose import JWTError,jwt
from src.model import Users
from typing import Annotated
from src.database import get_session
from src.app import oauth2_scheme
from src.create_token import ALGORITHM,SECRET_KEY

oauth_scheme = APIRouter() 


def get_user(session: Session, username: str):
    return session.exec(select(Users).where(Users.user_name == username)).first()

def verify_password(user_password, db_password):
    return user_password == db_password   
def get_current_user(token: Annotated[str, Depends(oauth_scheme)], session:Annotated[Session , Depends(get_session)]):
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = decode_token.get("sub")
    user = get_user(session, username)
    return user

from sqlmodel import SQLModel, Field 
from typing import Optional
 


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    password: str
    email: str
    phone: str
    token: Optional[str] = None

 

from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    print('Error: The .env file does not exist')
except Exception as e:
    print("Error:", e)

DATA_BASE_URL = config("DATA_BASE_URL", cast=Secret)
 
   
from fastapi import   Depends, HTTPException,APIRouter
from sqlmodel import Session 
from typing import Annotated
from src.database import get_session 
from datetime import timedelta
from src.create_token import create_access_token
from src.helper_fun import verify_password,get_user 
from fastapi.security import  OAuth2PasswordRequestForm


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
    access_token_expires = timedelta(minutes=10)
    access_token = create_access_token(
        username=user.user_name, validation_time=access_token_expires
    )
    return {"message": "Login Successfully", "token": access_token}



from fastapi import Depends, APIRouter
from sqlmodel import Session 
from src.model import Users
from typing import Annotated
from src.database import get_session
from src.helper_fun import get_current_user
 

router =APIRouter()
oauth_scheme =APIRouter()
 
 
@router.post("/signout")
def signout(token: Annotated[str, Depends(oauth_scheme)], session:Annotated[Session , Depends(get_session)]):
    user = get_current_user(token, session)
    user.token = None
    session.add(user)
    session.commit()
    return {"message": "Successfully signed out"}   




from fastapi import  Form, Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from src.model import Users
from typing import Annotated
from src.database import get_session
 
router =APIRouter() 

@router.post('/signup')
def signup(session: Annotated[Session, Depends(get_session)],
           email: Annotated[str, Form()],
           password: Annotated[str, Form()],
           phone: Annotated[str, Form()],
           user_name: Annotated[str, Form()]):
   
    existing_email = session.exec(select(Users).where(Users.email == email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail=f"Email {email} is already in use.")

    existing_user_name = session.exec(select(Users).where(Users.user_name == user_name)).first()
    if existing_user_name:
        raise HTTPException(status_code=400, detail=f"Username {user_name} is already in use.")
 
    user = Users(email=email, password=password, phone=phone, user_name=user_name)

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except :
        raise HTTPException(status_code=400, detail="An error occurred while creating the user.")
    return {"message": f"User with email {email} created successfully"}

