

from fastapi import  Form, Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from src.model import Users
from typing import Annotated
from src.database import get_session
from src.validation.phone_no_validation import validate_phone_number
from src.validation.email_validation import validate_email_format,is_allowed_domain,is_temporary_email,TEMP_EMAIL_DOMAINS

 
router =APIRouter() 

@router.post('/signup')
def signup(session: Annotated[Session, Depends(get_session)],
           user_name: Annotated[str, Form()],
           email: Annotated[str, Form()],
           phone: Annotated[str, Form()],
           password: Annotated[str, Form()],
           
          ):
    
    allowed_domains = ["gmail.com", "yahoo.com", "outlook.com"]  

    if not validate_phone_number(phone):
        raise HTTPException(status_code=400, detail="Invalid phone number format.")

    if not validate_email_format(email):
        raise HTTPException(status_code=400, detail="Invalid email format.")
    
    if not is_allowed_domain(email, allowed_domains):
        raise HTTPException(status_code=400, detail="Email domain is not allowed.")
    
    if is_temporary_email(email, TEMP_EMAIL_DOMAINS):
        raise HTTPException(status_code=400, detail="Temporary email addresses are not allowed.")

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

