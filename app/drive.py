from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GoogleConnection
from app.services import get_drive_files


router = APIRouter()


@router.get("/drive/files")
def list_drive_files(
    db: Session = Depends(get_db)
):

    # Get connected Google account
    connection = db.query(GoogleConnection).first()


    if not connection:
        return {
            "error": "Google account not connected"
        }


    files = get_drive_files(connection)


    return {
        "files": files
    }