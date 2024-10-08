from app.auth.schemas import UserCreate, UserLogin
from app.auth.utils import create_access_token, hash_password, verify_password
from app.db.crud import add_user, get_user_by_email
from app.db.database import get_db
from app.db.models import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = await hash_password(request.password)
    db_user = await get_user_by_email(email=request.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password_hash=hashed_password,
    )
    await add_user(user=user, db=db)
    return {"msg": "User registered successfully"}


@router.post("/login")
async def login(request: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(request.email, db)
    if not db_user or not await verify_password(db_user.password_hash, request.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"user_id": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
