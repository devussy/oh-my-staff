"""Google Sheets tools."""

import json
from typing import Any, Dict

from ..api_client import GoogleWorkspaceClient


async def google_read_sheet(client: GoogleWorkspaceClient, arguments: Dict[str, Any]) -> str:
    """
    Read Google Sheet.

    Args:
        client: Google Workspace API client
        arguments: Tool arguments

    Returns:
        JSON string with sheet data
    """
    sheet_id = arguments.get("sheet_id", "")
    range_name = arguments.get("range", "Sheet1")

    if not sheet_id:
        return json.dumps({"error": "Sheet ID is required"})

    try:
        result = client.read_sheet(sheet_id=sheet_id, range_name=range_name)

        # Get metadata
        metadata = client.get_file_metadata(file_id=sheet_id)

        formatted_sheet = {
            "id": sheet_id,
            "title": metadata.get("name"),
            "metadata": {
                "created": metadata.get("createdTime"),
                "modified": metadata.get("modifiedTime"),
                "owners": [
                    owner.get("displayName")
                    for owner in metadata.get("owners", [])
                ],
                "url": metadata.get("webViewLink"),
            },
            "range": result.get("range"),
            "values": result.get("values", []),
            "row_count": len(result.get("values", [])),
        }

        return json.dumps(formatted_sheet, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
