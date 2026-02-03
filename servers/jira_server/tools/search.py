"""JIRA search tools."""

import json
from typing import Any, Dict

from ..api_client import JiraClient


async def jira_search_issues(client: JiraClient, arguments: Dict[str, Any]) -> str:
    """
    Search JIRA issues using JQL.

    Args:
        client: JIRA API client
        arguments: Tool arguments

    Returns:
        JSON string with search results
    """
    jql = arguments.get("jql", "")
    max_results = arguments.get("max_results", 50)
    fields = arguments.get("fields")

    if not jql:
        return json.dumps({"error": "JQL query is required"})

    try:
        result = client.search_issues(
            jql=jql,
            max_results=max_results,
            fields=fields,
        )

        # Format response
        issues = result.get("issues", [])
        formatted_issues = []

        for issue in issues:
            fields_data = issue.get("fields", {})
            formatted_issues.append({
                "key": issue.get("key"),
                "summary": fields_data.get("summary"),
                "status": fields_data.get("status", {}).get("name"),
                "assignee": fields_data.get("assignee", {}).get("displayName") if fields_data.get("assignee") else None,
                "priority": fields_data.get("priority", {}).get("name") if fields_data.get("priority") else None,
                "created": fields_data.get("created"),
                "updated": fields_data.get("updated"),
                "fields": fields_data,
            })

        return json.dumps({
            "total": result.get("total", 0),
            "max_results": result.get("maxResults", 0),
            "start_at": result.get("startAt", 0),
            "issues": formatted_issues,
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def jira_get_issue(client: JiraClient, arguments: Dict[str, Any]) -> str:
    """
    Get JIRA issue by key.

    Args:
        client: JIRA API client
        arguments: Tool arguments

    Returns:
        JSON string with issue data
    """
    issue_key = arguments.get("issue_key", "")
    fields = arguments.get("fields")

    if not issue_key:
        return json.dumps({"error": "Issue key is required"})

    try:
        issue = client.get_issue(issue_key=issue_key, fields=fields)

        # Format response
        fields_data = issue.get("fields", {})

        formatted_issue = {
            "key": issue.get("key"),
            "id": issue.get("id"),
            "self": issue.get("self"),
            "summary": fields_data.get("summary"),
            "description": fields_data.get("description"),
            "status": fields_data.get("status", {}).get("name"),
            "assignee": {
                "name": fields_data.get("assignee", {}).get("displayName"),
                "email": fields_data.get("assignee", {}).get("emailAddress"),
            } if fields_data.get("assignee") else None,
            "reporter": {
                "name": fields_data.get("reporter", {}).get("displayName"),
                "email": fields_data.get("reporter", {}).get("emailAddress"),
            } if fields_data.get("reporter") else None,
            "priority": fields_data.get("priority", {}).get("name") if fields_data.get("priority") else None,
            "labels": fields_data.get("labels", []),
            "components": [c.get("name") for c in fields_data.get("components", [])],
            "created": fields_data.get("created"),
            "updated": fields_data.get("updated"),
            "resolution_date": fields_data.get("resolutiondate"),
            "all_fields": fields_data,
        }

        return json.dumps(formatted_issue, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def jira_get_sprint(client: JiraClient, arguments: Dict[str, Any]) -> str:
    """
    Get JIRA sprint information.

    Args:
        client: JIRA API client
        arguments: Tool arguments

    Returns:
        JSON string with sprint data
    """
    sprint_id = arguments.get("sprint_id")

    if not sprint_id:
        return json.dumps({"error": "Sprint ID is required"})

    try:
        sprint_id = int(sprint_id)
        sprint = client.get_sprint(sprint_id=sprint_id)

        # Get sprint issues
        issues_result = client.get_sprint_issues(sprint_id=sprint_id)

        formatted_sprint = {
            "id": sprint.get("id"),
            "name": sprint.get("name"),
            "state": sprint.get("state"),
            "startDate": sprint.get("startDate"),
            "endDate": sprint.get("endDate"),
            "completeDate": sprint.get("completeDate"),
            "goal": sprint.get("goal"),
            "issues": {
                "total": issues_result.get("total", 0),
                "issues": [
                    {
                        "key": issue.get("key"),
                        "summary": issue.get("fields", {}).get("summary"),
                        "status": issue.get("fields", {}).get("status", {}).get("name"),
                    }
                    for issue in issues_result.get("issues", [])
                ],
            },
        }

        return json.dumps(formatted_sprint, indent=2)

    except ValueError:
        return json.dumps({"error": "Sprint ID must be an integer"})
    except Exception as e:
        return json.dumps({"error": str(e)})
