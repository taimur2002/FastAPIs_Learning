from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm  # standard login form (username+password)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import Token
from app.security import verify_password, create_access_token

# All routes here start with /auth and are grouped under "Auth" in the docs
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    # OAuth2PasswordRequestForm reads FORM fields "username" and "password"
    # (this is the OAuth2 standard — that's why login uses form data, not JSON)
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),  # get a DB session (auto-closed)
):
    """Log in with username + password -> receive a JWT access token."""

    # 1. Look up the user by the username they typed
    user = db.query(User).filter(User.username == form.username).first()

    # 2. Reject if user not found OR password doesn't match the stored hash.
    #    We give the SAME error for both cases so attackers can't tell which
    #    part was wrong (a small security best-practice).
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # 3. Build a signed token carrying the username in the "sub" (subject) claim.
    token = create_access_token({"sub": user.username})

    # 4. Return it in the standard shape: {access_token, token_type}
    return {"access_token": token, "token_type": "bearer"}
