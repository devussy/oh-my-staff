"""Google Docs tools."""

import json
from typing import Any, Dict

from ..api_client import GoogleWorkspaceClient


async def google_read_doc(client: GoogleWorkspaceClient, arguments: Dict[str, Any]) -> str:
    """
    Read Google Doc.

    Args:
        client: Google Workspace API client
        arguments: Tool arguments

    Returns:
        JSON string with document data
    """
    doc_id = arguments.get("doc_id", "")

    if not doc_id:
        return json.dumps({"error": "Document ID is required"})

    try:
        doc = client.read_doc(doc_id=doc_id)

        # Extract metadata
        metadata = client.get_file_metadata(file_id=doc_id)

        # Extract text content
        text_content = client.extract_doc_text(doc)

        formatted_doc = {
            "id": doc.get("documentId"),
            "title": doc.get("title"),
            "metadata": {
                "created": metadata.get("createdTime"),
                "modified": metadata.get("modifiedTime"),
                "owners": [
                    owner.get("displayName")
                    for owner in metadata.get("owners", [])
                ],
                "url": metadata.get("webViewLink"),
            },
            "content": text_content,
        }

        return json.dumps(formatted_doc, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def google_list_docs(client: GoogleWorkspaceClient, arguments: Dict[str, Any]) -> str:
    """
    List Google Docs.

    Args:
        client: Google Workspace API client
        arguments: Tool arguments

    Returns:
        JSON string with document list
    """
    query = arguments.get("query", "")
    folder_id = arguments.get("folder_id")
    limit = arguments.get("limit", 10)

    try:
        # Build query
        query_parts = ["mimeType='application/vnd.google-apps.document'"]

        if query:
            query_parts.append(f"name contains '{query}'")

        if folder_id:
            query_parts.append(f"'{folder_id}' in parents")

        full_query = " and ".join(query_parts)

        files = client.list_files(
            query=full_query,
            page_size=limit,
        )

        formatted_files = [
            {
                "id": f.get("id"),
                "name": f.get("name"),
                "modified": f.get("modifiedTime"),
                "url": f.get("webViewLink"),
            }
            for f in files
        ]

        return json.dumps({
            "count": len(formatted_files),
            "documents": formatted_files,
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
