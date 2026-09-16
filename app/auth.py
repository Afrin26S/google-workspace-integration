from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

import requests

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from app.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI
)

from app.database import get_db
from app.models import GoogleConnection


router = APIRouter()


SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents"
    ]



def get_client_config():
    return {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                GOOGLE_REDIRECT_URI
            ]
        }
    }


# Step 1: Redirect user to Google Login
@router.get("/auth/google/connect")
def connect_google(request: Request):

    flow = Flow.from_client_config(
        get_client_config(),
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true",
        code_challenge_method="S256"
    )

    request.session["oauth_state"] = state
    request.session["code_verifier"] = flow.code_verifier

    return RedirectResponse(authorization_url)




# Step 2: Google redirects back here
@router.get("/auth/google/callback")
def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):

    code = request.query_params.get("code")

    if not code:
        return {
            "message": "Authorization code missing"
        }

    flow = Flow.from_client_config(
        get_client_config(),
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    flow.oauth2session.scope = None

    # Restore PKCE code verifier
    flow.code_verifier = request.session.get("code_verifier")

    # Exchange authorization code for tokens
    flow.fetch_token(
        code=code,
        include_client_id=True
    )
    
    credentials = flow.credentials

    print("ACCESS TOKEN:", credentials.token)
    print("REFRESH TOKEN:", credentials.refresh_token)
    print("SCOPES:", credentials.scopes)

    # Get Google user email
    oauth_service = build(
        "oauth2",
        "v2",
        credentials=credentials
    )

    user_info = oauth_service.userinfo().get().execute()
    print("USER INFO:", user_info)

    email = user_info["email"]

    # Store tokens in database
    connection = GoogleConnection(

    email=email,

    access_token=credentials.token,

    refresh_token=credentials.refresh_token,

    token_uri=credentials.token_uri,

    scopes=" ".join(credentials.scopes or SCOPES)

)

    

    db.add(connection)
    db.commit()
    db.refresh(connection)

    return {

        "message": "Google account connected successfully",

        "stored": True,

        "email": email,

        "has_refresh_token": credentials.refresh_token is not None

    }

@router.delete("/auth/google/disconnect")
def disconnect_google(
    db: Session = Depends(get_db)
):

    connection = db.query(GoogleConnection).first()


    if not connection:
        return {
            "message": "No Google account connected"
        }


    # Revoke Google access token
    requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={
            "token": connection.access_token
        },
        headers={
            "content-type": "application/x-www-form-urlencoded"
        }
    )


    # Delete stored credentials
    db.delete(connection)
    db.commit()


    return {
        "message": "Google account disconnected successfully"
    }