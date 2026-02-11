from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def build_request_id(user_id: int, request_time: datetime) -> str:
    """Generate a stable request id using user id and first message timestamp."""
    return f"REQ-{request_time.strftime('%Y%m%d%H%M%S')}-{user_id}"


class GoogleTablesClient:
    def __init__(self, spreadsheet_id: str, credentials_path: str, sheet_name: str = "Sheet1"):
        self.spreadsheet_id = spreadsheet_id
        self.credentials_path = credentials_path
        self.sheet_name = sheet_name

    def _service(self):
        credentials = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=SCOPES,
        )
        return build("sheets", "v4", credentials=credentials)

    def append_complaint(
        self,
        request_id: str,
        request_time: datetime,
        user_name: str,
        sector: int,
        device: int,
        complaint_text: str,
    ) -> None:
        service = self._service()
        row = [
            request_id,
            request_time.strftime("%Y-%m-%d %H:%M:%S"),
            user_name,
            sector,
            device,
            complaint_text,
        ]

        service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=f"{self.sheet_name}!A:F",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": [row]},
        ).execute()


def append_complaint_to_google_tables(
    spreadsheet_id: Optional[str],
    credentials_path: Optional[str],
    sheet_name: str,
    request_id: str,
    request_time: datetime,
    user_name: str,
    sector: int,
    device: int,
    complaint_text: str,
) -> None:
    """Append complaint to Google Sheets (Google Tables API style storage)."""
    if not spreadsheet_id or not credentials_path:
        return

    credentials_file = Path(credentials_path)
    if not credentials_file.exists():
        return

    client = GoogleTablesClient(
        spreadsheet_id=spreadsheet_id,
        credentials_path=str(credentials_file),
        sheet_name=sheet_name,
    )
    client.append_complaint(
        request_id=request_id,
        request_time=request_time,
        user_name=user_name,
        sector=sector,
        device=device,
        complaint_text=complaint_text,
    )
