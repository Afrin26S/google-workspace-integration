from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GoogleConnection
from app.services import get_sheet_data


router = APIRouter()


@router.get("/sheets/{spreadsheet_id}")
def read_sheet(
    spreadsheet_id: str,
    db: Session = Depends(get_db)
):

    connection = db.query(GoogleConnection).first()

    if not connection:
        return {
            "error": "Google account not connected"
        }


    data = get_sheet_data(
        connection,
        spreadsheet_id
    )


    return {
        "spreadsheet_id": spreadsheet_id,
        "data": data
    }