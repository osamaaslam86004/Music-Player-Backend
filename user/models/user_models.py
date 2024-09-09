from sqlalchemy import Column, String
from passlib.context import CryptContext
from database import Base  # Import the Base from your database setup

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, unique=True, index=True)
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    def hash_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)
