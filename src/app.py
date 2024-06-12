

from fastapi import FastAPI,  Depends    
from typing import Annotated 
from src.creating_tables import lifespan 
from fastapi.security import  OAuth2PasswordBearer
from src.login import signin,signout,signup
from src.oauth import oauth2_scheme
 
  
app = FastAPI(lifespan=lifespan, title='Login Portal')
 
 
@app.get("/mainpage", response_model=dict[str,str])
def main(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str,str]:
    return {"message": f"Welcome to the main page of our portal"}

app.include_router(signin.router)
app.include_router(signout.router)
app.include_router(signup.router)
 
 
 
 
 
 
 
  