import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import SECRET_KEY, ALGORITHM

# Tells FastAPI tokens arrive as  "Authorization: Bearer <token>".
# tokenUrl="auth/login" powers the "Authorize" button in Swagger docs.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),   # pull the token out of the request header
    db: Session = Depends(get_db),
) -> User:
    """Decode the JWT, find the matching user, or raise 401."""
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # verify the signature + expiry, then read the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")          # we stored the username in "sub"
        if username is None:
            raise credentials_exc
    except jwt.PyJWTError:                      # bad/expired/tampered token
        raise credentials_exc

    # confirm the user still exists in the DB
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exc
    return user
