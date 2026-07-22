from passlib.context import CryptContext

# bcrypt = a strong, slow, one-way hashing algorithm for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Turn a plain password into a bcrypt hash (for storing)."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Check a plain password against a stored hash (for login)."""
    return pwd_context.verify(plain, hashed)
