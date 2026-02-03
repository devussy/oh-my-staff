"""JIRA MCP Server implementation."""

import sys
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Try to import MCP SDK, fall back to stub if not available
try:
    from mcp.types import Tool
except ImportError:
    from servers.common.mcp_stub import Tool

from servers.common import BaseMCPServer, validate_jql, validate_positive_int
from .api_client import JiraClient
from .tools.search import jira_search_issues, jira_get_issue, jira_get_sprint


class JiraMCPServer(BaseMCPServer):
    """JIRA MCP Server."""

    def __init__(self):
        """Initialize JIRA MCP Server."""
        super().__init__("jira", cache_dir="data/cache/jira")

        # Load configuration from environment
        jira_url = self.load_env_var("JIRA_URL")
        jira_email = self.load_env_var("JIRA_EMAIL")
        jira_token = self.load_env_var("JIRA_API_TOKEN")

        # Initialize JIRA client
        self.client = JiraClient(
            url=jira_url,
            username=jira_email,
            password=jira_token,
        )

        self.logger.info("JIRA MCP Server initialized")

    def get_tools(self) -> List[Tool]:
        """Get list of available JIRA tools."""
        return [
            Tool(
                name="jira_search_issues",
                description="Search JIRA issues using JQL (JIRA Query Language)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "jql": {
                            "type": "string",
                            "description": "JQL query string (e.g., 'project = PROJ AND status = Done')",
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 50)",
                            "default": 50,
                        },
                        "fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of fields to return (optional, returns all by default)",
                        },
                    },
                    "required": ["jql"],
                },
            ),
            Tool(
                name="jira_get_issue",
                description="Get detailed information about a specific JIRA issue",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_key": {
                            "type": "string",
                            "description": "Issue key (e.g., 'PROJ-123')",
                        },
                        "fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of fields to return (optional, returns all by default)",
                        },
                    },
                    "required": ["issue_key"],
                },
            ),
            Tool(
                name="jira_get_sprint",
                description="Get information about a JIRA sprint including its issues",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sprint_id": {
                            "type": "integer",
                            "description": "Sprint ID",
                        },
                    },
                    "required": ["sprint_id"],
                },
            ),
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a JIRA tool."""
        # Validate common arguments
        if "jql" in arguments:
            arguments["jql"] = validate_jql(arguments["jql"])

        if "max_results" in arguments:
            arguments["max_results"] = validate_positive_int(arguments["max_results"], max_value=1000)

        # Check cache first (for read operations)
        cache_key = self.get_cache_key(name, **arguments)
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            self.logger.info(f"Cache hit for {name}")
            return cached_result

        # Execute tool
        if name == "jira_search_issues":
            result = await jira_search_issues(self.client, arguments)
        elif name == "jira_get_issue":
            result = await jira_get_issue(self.client, arguments)
        elif name == "jira_get_sprint":
            result = await jira_get_sprint(self.client, arguments)
        else:
            return f"Unknown tool: {name}"

        # Cache result
        self.cache.set(cache_key, result)

        return result


def main():
    """Main entry point."""
    server = JiraMCPServer()
    server.run()


if __name__ == "__main__":
    main()
