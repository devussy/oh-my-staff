"""Google Workspace API client."""

from __future__ import annotations
import os
from typing import Any, Dict, List, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleWorkspaceClient:
    """Google Workspace API client wrapper."""

    SCOPES = [
        "https://www.googleapis.com/auth/documents.readonly",
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    def __init__(self, credentials_file: str, token_file: str):
        """
        Initialize Google Workspace client.

        Args:
            credentials_file: Path to credentials.json
            token_file: Path to token.json
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = self._get_credentials()

        # Initialize services
        self.docs_service = build("docs", "v1", credentials=self.creds)
        self.sheets_service = build("sheets", "v4", credentials=self.creds)
        self.drive_service = build("drive", "v3", credentials=self.creds)

    def _get_credentials(self) -> Credentials:
        """Get or create credentials."""
        creds = None

        # Load token if exists
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}. "
                        "Please download from Google Cloud Console."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return creds

    def read_doc(self, doc_id: str) -> Dict[str, Any]:
        """
        Read Google Doc.

        Args:
            doc_id: Document ID

        Returns:
            Document data
        """
        try:
            doc = self.docs_service.documents().get(documentId=doc_id).execute()
            return doc
        except Exception as e:
            raise Exception(f"Error reading document: {str(e)}")

    def read_sheet(
        self,
        sheet_id: str,
        range_name: str = "Sheet1",
    ) -> Dict[str, Any]:
        """
        Read Google Sheet.

        Args:
            sheet_id: Spreadsheet ID
            range_name: Range to read (e.g., 'Sheet1!A1:D10')

        Returns:
            Sheet data
        """
        try:
            result = (
                self.sheets_service.spreadsheets()
                .values()
                .get(spreadsheetId=sheet_id, range=range_name)
                .execute()
            )
            return result
        except Exception as e:
            raise Exception(f"Error reading spreadsheet: {str(e)}")

    def list_files(
        self,
        query: Optional[str] = None,
        page_size: int = 10,
        order_by: str = "modifiedTime desc",
    ) -> List[Dict[str, Any]]:
        """
        List files in Drive.

        Args:
            query: Search query (e.g., "name contains 'report'")
            page_size: Number of results
            order_by: Sort order

        Returns:
            List of files
        """
        try:
            kwargs = {
                "pageSize": page_size,
                "orderBy": order_by,
                "fields": "files(id, name, mimeType, modifiedTime, webViewLink)",
            }
            if query:
                kwargs["q"] = query

            results = self.drive_service.files().list(**kwargs).execute()
            return results.get("files", [])
        except Exception as e:
            raise Exception(f"Error listing files: {str(e)}")

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Get file metadata.

        Args:
            file_id: File ID

        Returns:
            File metadata
        """
        try:
            file = (
                self.drive_service.files()
                .get(
                    fileId=file_id,
                    fields="id, name, mimeType, createdTime, modifiedTime, owners, webViewLink",
                )
                .execute()
            )
            return file
        except Exception as e:
            raise Exception(f"Error getting file metadata: {str(e)}")

    def extract_doc_text(self, doc: Dict[str, Any]) -> str:
        """
        Extract plain text from Google Doc.

        Args:
            doc: Document data from read_doc()

        Returns:
            Plain text content
        """
        text_parts = []

        content = doc.get("body", {}).get("content", [])
        for element in content:
            if "paragraph" in element:
                para = element["paragraph"]
                for elem in para.get("elements", []):
                    if "textRun" in elem:
                        text_parts.append(elem["textRun"].get("content", ""))

        return "".join(text_parts)
