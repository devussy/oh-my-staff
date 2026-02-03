"""JIRA API client."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from atlassian import Jira


class JiraClient:
    """JIRA API client wrapper."""

    def __init__(self, url: str, username: str, password: str):
        """
        Initialize JIRA client.

        Args:
            url: JIRA instance URL
            username: JIRA username (email)
            password: JIRA API token
        """
        self.client = Jira(
            url=url,
            username=username,
            password=password,
            cloud=True,
        )

    def search_issues(
        self,
        jql: str,
        max_results: int = 50,
        fields: Optional[List[str]] = None,
        start_at: int = 0,
    ) -> Dict[str, Any]:
        """
        Search issues using JQL.

        Args:
            jql: JQL query string
            max_results: Maximum number of results
            fields: List of fields to return (None for all)
            start_at: Starting index

        Returns:
            Search results
        """
        return self.client.jql(
            jql=jql,
            limit=max_results,
            fields=fields or "*all",
            start=start_at,
        )

    def get_issue(self, issue_key: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get issue by key.

        Args:
            issue_key: Issue key (e.g., PROJ-123)
            fields: List of fields to return (None for all)

        Returns:
            Issue data
        """
        return self.client.issue(issue_key, fields=fields or "*all")

    def get_sprint(self, sprint_id: int) -> Dict[str, Any]:
        """
        Get sprint information.

        Args:
            sprint_id: Sprint ID

        Returns:
            Sprint data
        """
        return self.client.get(f"rest/agile/1.0/sprint/{sprint_id}")

    def get_sprint_issues(
        self,
        sprint_id: int,
        max_results: int = 100,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get issues in a sprint.

        Args:
            sprint_id: Sprint ID
            max_results: Maximum number of results
            fields: List of fields to return

        Returns:
            Sprint issues
        """
        params = {
            "maxResults": max_results,
        }
        if fields:
            params["fields"] = ",".join(fields)

        return self.client.get(f"rest/agile/1.0/sprint/{sprint_id}/issue", params=params)

    def get_board_sprints(
        self,
        board_id: int,
        state: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get sprints for a board.

        Args:
            board_id: Board ID
            state: Sprint state (active, closed, future)

        Returns:
            List of sprints
        """
        params = {}
        if state:
            params["state"] = state

        response = self.client.get(f"rest/agile/1.0/board/{board_id}/sprint", params=params)
        return response.get("values", [])

    def get_project_boards(self, project_key: str) -> List[Dict[str, Any]]:
        """
        Get boards for a project.

        Args:
            project_key: Project key

        Returns:
            List of boards
        """
        response = self.client.get(
            "rest/agile/1.0/board",
            params={"projectKeyOrId": project_key},
        )
        return response.get("values", [])

    def get_issue_changelog(self, issue_key: str) -> List[Dict[str, Any]]:
        """
        Get issue changelog.

        Args:
            issue_key: Issue key

        Returns:
            Changelog entries
        """
        issue = self.client.issue(issue_key, expand="changelog")
        return issue.get("changelog", {}).get("histories", [])

    def get_project(self, project_key: str) -> Dict[str, Any]:
        """
        Get project information.

        Args:
            project_key: Project key

        Returns:
            Project data
        """
        return self.client.project(project_key)
