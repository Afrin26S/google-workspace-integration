# Google Workspace Integration Service

## Overview

This project is a backend service built using FastAPI that integrates with Google Workspace APIs.

The application allows users to authenticate using Google OAuth 2.0 and provides access to Google Drive, Google Sheets, and Google Docs APIs.

After the user connects their Google account once, the backend securely stores OAuth credentials and can access authorized Google Workspace resources until the user disconnects.

---

# Features

## Authentication

- Google OAuth 2.0 login
- Secure authorization flow
- Access token and refresh token handling
- Store Google credentials in database

## Google Workspace Integrations

### Google Drive

- Fetch user's Drive files
- Retrieve file names, IDs, and MIME types


### Google Sheets

- Read spreadsheet data
- Access spreadsheet values using Spreadsheet ID


### Google Docs

- Fetch Google Document details
- Extract document text content


## Account Management

- Connect Google account
- Disconnect Google account
- Revoke Google access token
- Remove stored credentials

---

# Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Uvicorn

## Google APIs

- Google OAuth 2.0
- Google Drive API
- Google Sheets API
- Google Docs API

## Database

- SQLite

---

# Project Structure
