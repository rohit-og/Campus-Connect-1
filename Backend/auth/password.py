"""Password hashing utilities"""

from passlib.context import CryptContext
import bcrypt

# Use bcrypt directly to avoid passlib/bcrypt version compatibility issues
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        # Try using passlib first
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback to direct bcrypt if passlib fails
        try:
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
        except Exception:
            return False


def get_password_hash(password: str) -> str:
    """Hash a password"""
    # Bcrypt has a 72-byte limit, so ensure we don't exceed it
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    try:
        # Try using passlib first
        return pwd_context.hash(password)
    except Exception as e:
        # Fallback to direct bcrypt if passlib fails
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
