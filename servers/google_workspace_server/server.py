"""Google Workspace MCP Server implementation."""

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

from servers.common import BaseMCPServer, validate_positive_int
from .api_client import GoogleWorkspaceClient
from .tools.docs import google_read_doc, google_list_docs
from .tools.sheets import google_read_sheet


class GoogleWorkspaceMCPServer(BaseMCPServer):
    """Google Workspace MCP Server."""

    def __init__(self):
        """Initialize Google Workspace MCP Server."""
        super().__init__("google-workspace", cache_dir="data/cache/google")

        # Load configuration from environment
        credentials_file = self.load_env_var("GOOGLE_CREDENTIALS_FILE")
        token_file = self.load_env_var("GOOGLE_TOKEN_FILE")

        # Initialize Google Workspace client
        self.client = GoogleWorkspaceClient(
            credentials_file=credentials_file,
            token_file=token_file,
        )

        self.logger.info("Google Workspace MCP Server initialized")

    def get_tools(self) -> List[Tool]:
        """Get list of available Google Workspace tools."""
        return [
            Tool(
                name="google_read_doc",
                description="Read content from a Google Doc",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_id": {
                            "type": "string",
                            "description": "Google Doc ID (from URL)",
                        },
                    },
                    "required": ["doc_id"],
                },
            ),
            Tool(
                name="google_read_sheet",
                description="Read data from a Google Sheet",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sheet_id": {
                            "type": "string",
                            "description": "Google Sheet ID (from URL)",
                        },
                        "range": {
                            "type": "string",
                            "description": "Range to read (e.g., 'Sheet1!A1:D10' or 'Sheet1')",
                            "default": "Sheet1",
                        },
                    },
                    "required": ["sheet_id"],
                },
            ),
            Tool(
                name="google_list_docs",
                description="List Google Docs in Drive",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query to filter documents by name",
                        },
                        "folder_id": {
                            "type": "string",
                            "description": "Folder ID to search in (optional)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 10)",
                            "default": 10,
                        },
                    },
                },
            ),
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a Google Workspace tool."""
        # Validate common arguments
        if "limit" in arguments:
            arguments["limit"] = validate_positive_int(arguments["limit"], max_value=100)

        # Check cache first (for read operations)
        cache_key = self.get_cache_key(name, **arguments)
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            self.logger.info(f"Cache hit for {name}")
            return cached_result

        # Execute tool
        if name == "google_read_doc":
            result = await google_read_doc(self.client, arguments)
        elif name == "google_read_sheet":
            result = await google_read_sheet(self.client, arguments)
        elif name == "google_list_docs":
            result = await google_list_docs(self.client, arguments)
        else:
            return f"Unknown tool: {name}"

        # Cache result
        self.cache.set(cache_key, result)

        return result


def main():
    """Main entry point."""
    server = GoogleWorkspaceMCPServer()
    server.run()


if __name__ == "__main__":
    main()
