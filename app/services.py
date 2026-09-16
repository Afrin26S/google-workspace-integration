from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def get_credentials(connection):

    creds = Credentials(
        token=connection.access_token,
        refresh_token=connection.refresh_token,
        token_uri=connection.token_uri,
        scopes=connection.scopes.split(" ")
    )

    return creds



def get_drive_service(connection):

    credentials = get_credentials(connection)

    service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    return service



def get_drive_files(connection):

    service = get_drive_service(connection)

    results = service.files().list(
        pageSize=10,
        fields="files(id, name, mimeType)"
    ).execute()

    return results.get("files", [])

def get_sheets_service(connection):

    credentials = get_credentials(connection)

    service = build(
        "sheets",
        "v4",
        credentials=credentials
    )

    return service



def get_sheet_data(connection, spreadsheet_id):

    service = get_sheets_service(connection)

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="All Orders"
    ).execute()

    return result.get("values", [])

def get_docs_service(connection):

    credentials = get_credentials(connection)

    service = build(
        "docs",
        "v1",
        credentials=credentials
    )

    return service



def get_document_content(connection, document_id):

    service = get_docs_service(connection)

    document = service.documents().get(
        documentId=document_id
    ).execute()


    content = []

    for element in document.get("body", {}).get("content", []):

        if "paragraph" in element:

            for text_run in element["paragraph"].get("elements", []):

                if "textRun" in text_run:

                    content.append(
                        text_run["textRun"]["content"]
                    )


    return {
        "title": document.get("title"),
        "content": content
    }