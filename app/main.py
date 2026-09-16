from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.auth import router
from app.drive import router as drive_router
from app.sheets import router as sheets_router
from app.docs import router as docs_router
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this"
)

app.include_router(router)
app.include_router(sheets_router)
app.include_router(drive_router)
app.include_router(docs_router)

@app.get("/")
def home():
    return {
        "message": "Google Workspace Integration API"
    }