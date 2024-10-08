from datetime import datetime

from app.auth.routes import router as auth_router
from app.chat.routes import router as chats_router
from app.db.database import (
    get_db,  # Assuming you have a get_db function to get the DB session
)
from app.docs.routes import router as docs_router
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

app = FastAPI()

# Track the startup time
startup_time = datetime.utcnow()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chats_router, prefix="/chats", tags=["chats"])
app.include_router(docs_router, prefix="/docs", tags=["docs"])

# Health check endpoint


@app.get("/")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Check DB connection by executing a simple query
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    # Calculate app uptime
    uptime_seconds = (datetime.utcnow() - startup_time).total_seconds()

    return {
        "database_status": db_status,
        "uptime_seconds": uptime_seconds
    }
