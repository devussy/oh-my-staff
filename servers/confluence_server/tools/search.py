"""Confluence search tools."""

import json
from typing import Any, Dict

from ..api_client import ConfluenceClient


async def confluence_search_pages(client: ConfluenceClient, arguments: Dict[str, Any]) -> str:
    """
    Search Confluence pages using CQL.

    Args:
        client: Confluence API client
        arguments: Tool arguments

    Returns:
        JSON string with search results
    """
    cql = arguments.get("cql", "")
    space = arguments.get("space")
    limit = arguments.get("limit", 25)

    if not cql:
        return json.dumps({"error": "CQL query is required"})

    # Add space filter if provided
    if space:
        if "space" not in cql.lower():
            cql = f"space = {space} AND ({cql})"

    try:
        result = client.search_pages(
            cql=cql,
            limit=limit,
            expand="body.storage,version",
        )

        # Format response
        results = result.get("results", [])
        formatted_results = []

        for page in results:
            # Extract body content (truncate if too long)
            body_content = ""
            if "body" in page and "storage" in page["body"]:
                body_content = page["body"]["storage"].get("value", "")
                if len(body_content) > 500:
                    body_content = body_content[:500] + "..."

            formatted_results.append({
                "id": page.get("id"),
                "title": page.get("title"),
                "type": page.get("type"),
                "space": {
                    "key": page.get("space", {}).get("key"),
                    "name": page.get("space", {}).get("name"),
                } if "space" in page else None,
                "url": page.get("_links", {}).get("webui"),
                "version": page.get("version", {}).get("number"),
                "last_updated": page.get("version", {}).get("when"),
                "body_preview": body_content,
            })

        return json.dumps({
            "total": result.get("totalSize", 0),
            "limit": result.get("limit", 0),
            "start": result.get("start", 0),
            "results": formatted_results,
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def confluence_get_page(client: ConfluenceClient, arguments: Dict[str, Any]) -> str:
    """
    Get Confluence page by ID.

    Args:
        client: Confluence API client
        arguments: Tool arguments

    Returns:
        JSON string with page data
    """
    page_id = arguments.get("page_id", "")

    if not page_id:
        return json.dumps({"error": "Page ID is required"})

    try:
        page = client.get_page(
            page_id=page_id,
            expand="body.storage,version,space,history",
        )

        # Get labels
        labels = client.get_page_labels(page_id=page_id)

        # Format response
        body_content = ""
        if "body" in page and "storage" in page["body"]:
            body_content = page["body"]["storage"].get("value", "")

        formatted_page = {
            "id": page.get("id"),
            "title": page.get("title"),
            "type": page.get("type"),
            "space": {
                "key": page.get("space", {}).get("key"),
                "name": page.get("space", {}).get("name"),
            } if "space" in page else None,
            "url": page.get("_links", {}).get("webui"),
            "version": {
                "number": page.get("version", {}).get("number"),
                "when": page.get("version", {}).get("when"),
                "by": page.get("version", {}).get("by", {}).get("displayName"),
            } if "version" in page else None,
            "created": page.get("history", {}).get("createdDate"),
            "created_by": page.get("history", {}).get("createdBy", {}).get("displayName"),
            "labels": labels,
            "body": body_content,
        }

        return json.dumps(formatted_page, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def confluence_get_space(client: ConfluenceClient, arguments: Dict[str, Any]) -> str:
    """
    Get Confluence space information.

    Args:
        client: Confluence API client
        arguments: Tool arguments

    Returns:
        JSON string with space data
    """
    space_key = arguments.get("space_key", "")

    if not space_key:
        return json.dumps({"error": "Space key is required"})

    try:
        space = client.get_space(space_key=space_key)

        # Get space content summary
        content = client.get_space_content(space_key=space_key, limit=10)

        formatted_space = {
            "key": space.get("key"),
            "name": space.get("name"),
            "type": space.get("type"),
            "description": space.get("description", {}).get("plain", {}).get("value"),
            "url": space.get("_links", {}).get("webui"),
            "homepage": {
                "id": space.get("homepage", {}).get("id"),
                "title": space.get("homepage", {}).get("title"),
            } if "homepage" in space else None,
            "content_count": content.get("size", 0),
            "recent_pages": [
                {
                    "id": page.get("id"),
                    "title": page.get("title"),
                }
                for page in content.get("results", [])[:5]
            ],
        }

        return json.dumps(formatted_space, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
