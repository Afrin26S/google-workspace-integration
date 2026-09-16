from sqlalchemy import Column, Integer, String

from app.database import Base

class GoogleConnection(Base):
    __tablename__ = "google_connections"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True)

    access_token = Column(String)

    refresh_token = Column(String)

    token_uri = Column(String)

    scopes = Column(String)