from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GoogleConnection
from app.services import get_document_content


router = APIRouter()


@router.get("/docs/{document_id}")
def read_document(
    document_id: str,
    db: Session = Depends(get_db)
):

    connection = db.query(GoogleConnection).first()


    if not connection:
        return {
            "error": "Google account not connected"
        }


    document = get_document_content(
        connection,
        document_id
    )


    return document