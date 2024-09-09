from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from main import app
from database import get_db
from user.utils import create_access_token
from user.schemas.user_schemas import UserCreate, UserLogin
from user.models.user_models import User


@app.post("/signup/")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(
            select(User).filter(User.username == user.username)
        )
        db_user = result.scalar_one_or_none()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        new_user = User(username=user.username)
        new_user.hash_password(user.password)
        session.add(new_user)
        await session.commit()
        # When we use async with db as session:, we are essentially creating a new context
        # for the session object. When the execution exits this context [[ither by successfully
        # completing the operations or due to an exception]], the __aexit__ method
        # of the db object is called, which closes the session.

    return {"msg": "User created successfully"}


@app.post("/login/")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(
            select(User).filter(User.username == user.username)
        )
        db_user = result.scalar_one_or_none()
        if not db_user or not db_user.verify_password(user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Create JWT token
        access_token = create_access_token(data={"sub": db_user.username})
        return {"access_token": access_token, "token_type": "bearer"}
