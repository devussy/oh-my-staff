"""Confluence MCP Server implementation."""

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

from servers.common import BaseMCPServer, validate_cql, validate_positive_int
from .api_client import ConfluenceClient
from .tools.search import confluence_search_pages, confluence_get_page, confluence_get_space


class ConfluenceMCPServer(BaseMCPServer):
    """Confluence MCP Server."""

    def __init__(self):
        """Initialize Confluence MCP Server."""
        super().__init__("confluence", cache_dir="data/cache/confluence")

        # Load configuration from environment
        confluence_url = self.load_env_var("CONFLUENCE_URL")
        confluence_email = self.load_env_var("CONFLUENCE_EMAIL")
        confluence_token = self.load_env_var("CONFLUENCE_API_TOKEN")

        # Initialize Confluence client
        self.client = ConfluenceClient(
            url=confluence_url,
            username=confluence_email,
            password=confluence_token,
        )

        self.logger.info("Confluence MCP Server initialized")

    def get_tools(self) -> List[Tool]:
        """Get list of available Confluence tools."""
        return [
            Tool(
                name="confluence_search_pages",
                description="Search Confluence pages using CQL (Confluence Query Language)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cql": {
                            "type": "string",
                            "description": "CQL query string (e.g., 'type=page AND title~\"API\"')",
                        },
                        "space": {
                            "type": "string",
                            "description": "Space key to search in (optional, filters results to this space)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 25)",
                            "default": 25,
                        },
                    },
                    "required": ["cql"],
                },
            ),
            Tool(
                name="confluence_get_page",
                description="Get detailed information about a specific Confluence page",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "Page ID",
                        },
                    },
                    "required": ["page_id"],
                },
            ),
            Tool(
                name="confluence_get_space",
                description="Get information about a Confluence space",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "space_key": {
                            "type": "string",
                            "description": "Space key (e.g., 'TEAM', 'DEV')",
                        },
                    },
                    "required": ["space_key"],
                },
            ),
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a Confluence tool."""
        # Validate common arguments
        if "cql" in arguments:
            arguments["cql"] = validate_cql(arguments["cql"])

        if "limit" in arguments:
            arguments["limit"] = validate_positive_int(arguments["limit"], max_value=1000)

        # Check cache first (for read operations)
        cache_key = self.get_cache_key(name, **arguments)
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            self.logger.info(f"Cache hit for {name}")
            return cached_result

        # Execute tool
        if name == "confluence_search_pages":
            result = await confluence_search_pages(self.client, arguments)
        elif name == "confluence_get_page":
            result = await confluence_get_page(self.client, arguments)
        elif name == "confluence_get_space":
            result = await confluence_get_space(self.client, arguments)
        else:
            return f"Unknown tool: {name}"

        # Cache result
        self.cache.set(cache_key, result)

        return result


def main():
    """Main entry point."""
    server = ConfluenceMCPServer()
    server.run()


if __name__ == "__main__":
    main()
