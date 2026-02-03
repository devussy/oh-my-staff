"""Confluence API client."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from atlassian import Confluence


class ConfluenceClient:
    """Confluence API client wrapper."""

    def __init__(self, url: str, username: str, password: str):
        """
        Initialize Confluence client.

        Args:
            url: Confluence instance URL
            username: Confluence username (email)
            password: Confluence API token
        """
        self.client = Confluence(
            url=url,
            username=username,
            password=password,
            cloud=True,
        )

    def search_pages(
        self,
        cql: str,
        limit: int = 25,
        start: int = 0,
        expand: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search pages using CQL.

        Args:
            cql: CQL query string
            limit: Maximum number of results
            start: Starting index
            expand: Fields to expand (e.g., 'body.storage,version')

        Returns:
            Search results
        """
        return self.client.cql(
            cql=cql,
            limit=limit,
            start=start,
            expand=expand,
        )

    def get_page(
        self,
        page_id: str,
        expand: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get page by ID.

        Args:
            page_id: Page ID
            expand: Fields to expand (e.g., 'body.storage,version')

        Returns:
            Page data
        """
        expand = expand or "body.storage,version,space,history"
        return self.client.get_page_by_id(
            page_id=page_id,
            expand=expand,
        )

    def get_page_by_title(
        self,
        space_key: str,
        title: str,
        expand: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get page by title in a space.

        Args:
            space_key: Space key
            title: Page title
            expand: Fields to expand

        Returns:
            Page data or None if not found
        """
        expand = expand or "body.storage,version,space,history"
        return self.client.get_page_by_title(
            space=space_key,
            title=title,
            expand=expand,
        )

    def get_space(self, space_key: str) -> Dict[str, Any]:
        """
        Get space information.

        Args:
            space_key: Space key

        Returns:
            Space data
        """
        return self.client.get_space(
            space_key=space_key,
            expand="description.plain,homepage",
        )

    def get_all_spaces(
        self,
        limit: int = 25,
        start: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get all spaces.

        Args:
            limit: Maximum number of results
            start: Starting index

        Returns:
            List of spaces
        """
        result = self.client.get_all_spaces(
            limit=limit,
            start=start,
        )
        return result.get("results", [])

    def get_page_labels(self, page_id: str) -> List[str]:
        """
        Get labels for a page.

        Args:
            page_id: Page ID

        Returns:
            List of label names
        """
        result = self.client.get_page_labels(page_id=page_id)
        return [label.get("name") for label in result.get("results", [])]

    def get_page_children(
        self,
        page_id: str,
        expand: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get child pages.

        Args:
            page_id: Parent page ID
            expand: Fields to expand

        Returns:
            List of child pages
        """
        result = self.client.get_page_child_by_type(
            page_id=page_id,
            type="page",
            expand=expand,
        )
        return result.get("results", [])

    def get_space_content(
        self,
        space_key: str,
        content_type: str = "page",
        limit: int = 25,
        start: int = 0,
    ) -> Dict[str, Any]:
        """
        Get content in a space.

        Args:
            space_key: Space key
            content_type: Content type (page, blogpost)
            limit: Maximum number of results
            start: Starting index

        Returns:
            Content data
        """
        return self.client.get_space_content(
            space_key=space_key,
            content_type=content_type,
            limit=limit,
            start=start,
        )

    def get_page_history(self, page_id: str) -> Dict[str, Any]:
        """
        Get page history.

        Args:
            page_id: Page ID

        Returns:
            Page history
        """
        page = self.get_page(page_id, expand="history,version")
        return page.get("history", {})
