import bcrypt
from typing import Optional
from db.database import get_session
from db.models import Admin


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def login(email: str, password: str) -> Optional[Admin]:
    session = get_session()
    try:
        admin = session.query(Admin).filter_by(email=email).first()
        if admin and verify_password(password, admin.password_hash):
            return admin
        return None
    finally:
        session.close()
