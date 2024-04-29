from dependencies.database import get_db
from .tokenBaseModel import Token
from .auth_utils import create_access_token, get_current_user, get_user_by_username, verify_password
from core.config import settings
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

authRouter = APIRouter()

# Endpoint used to get the current user's details.
# It uses the get_current_user dependency to get the current user's details.
# The endpoint is a GET request to "/users/me/".
@authRouter.get("/users/me/")
async def read_users_me(current_user: str=Depends(get_current_user)):
    return {"username": current_user}

# Endpoint used to authenticate a user and provide them with an access token.
# It uses the OAuth2PasswordRequestForm dependency to get the user's login details.
# The endpoint is a POST request to "/auth".
# If the user is authenticated successfully, it returns a Token.
# If the user is not authenticated, it raises an HTTPException.
@authRouter.post("/auth/", response_model=Token)
async def login_for_access_token(db=Depends(get_db), form_data: OAuth2PasswordRequestForm=Depends()):
    user = get_user_by_username(db, form_data.username)
    def raise_login_exeption():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user:
        raise_login_exeption()
    if not verify_password(form_data.password, user.password):
        raise_login_exeption()
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}