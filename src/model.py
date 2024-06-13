from sqlmodel import SQLModel, Field 
from typing import Optional
 
class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    password: str
    email: str
    phone: str
    token: Optional[str] = None

 