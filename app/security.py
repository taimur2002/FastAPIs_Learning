import os
from datetime import datetime, timedelta, timezone

import jwt  # PyJWT — encodes/decodes JSON Web Tokens
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()  # read SECRET_KEY etc. from the .env file

# =========================================================
#  PASSWORD HASHING
# =========================================================

# CryptContext is passlib's manager. We tell it to use the "bcrypt" algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Take a plain password -> return a bcrypt hash (safe to store in DB)."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Compare a plain password to a stored hash. Returns True if they match.
    (bcrypt is one-way, so we can't decrypt — we re-hash and compare.)"""
    return pwd_context.verify(plain, hashed)


# =========================================================
#  JWT TOKENS
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY")          # secret used to SIGN tokens (keep private!)
ALGORITHM = "HS256"                           # the signing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # token lifetime


def create_access_token(data: dict) -> str:
    """Build a signed JWT.
    `data` is the info we want inside the token, e.g. {"sub": "sara"}.
    We add an "exp" (expiry) claim, then sign it with our SECRET_KEY."""
    to_encode = data.copy()  # don't mutate the caller's dict
    # token becomes invalid after this moment:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # sign + encode into the "xxx.yyy.zzz" token string
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
