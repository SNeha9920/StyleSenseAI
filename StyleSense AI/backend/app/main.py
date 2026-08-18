from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine
from app.auth.router import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.skin_analysis import router as skin_analysis_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="StyleSense AI API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(skin_analysis_router)

@app.get("/")
def root():
    return {"message": "Welcome to StyleSense AI API✨💅🏻💄🪞"}


@app.get("/health/db")
def check_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "success",
            "database": "Connected"
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)