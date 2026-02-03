"""Slack MCP Server implementation."""

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
from .api_client import SlackClient
from .tools.messages import (
    slack_search_messages,
    slack_get_channel_history,
    slack_get_thread,
    slack_get_user_info,
)


class SlackMCPServer(BaseMCPServer):
    """Slack MCP Server."""

    def __init__(self):
        """Initialize Slack MCP Server."""
        super().__init__("slack", cache_dir="data/cache/slack")

        # Load configuration from environment
        bot_token = self.load_env_var("SLACK_BOT_TOKEN")
        user_token = self.load_env_var("SLACK_USER_TOKEN", required=False)

        # Initialize Slack client
        self.client = SlackClient(
            bot_token=bot_token,
            user_token=user_token,
        )

        self.logger.info("Slack MCP Server initialized")

    def get_tools(self) -> List[Tool]:
        """Get list of available Slack tools."""
        return [
            Tool(
                name="slack_search_messages",
                description="Search Slack messages (requires user token)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (e.g., 'error in:dev-team after:2024-01-01')",
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of results to return (default: 20)",
                            "default": 20,
                        },
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="slack_get_channel_history",
                description="Get message history from a Slack channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel_id": {
                            "type": "string",
                            "description": "Channel ID (e.g., 'C01234567')",
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date in ISO format (e.g., '2024-01-01T00:00:00')",
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date in ISO format (e.g., '2024-01-31T23:59:59')",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of messages to return (default: 100)",
                            "default": 100,
                        },
                    },
                    "required": ["channel_id"],
                },
            ),
            Tool(
                name="slack_get_thread",
                description="Get all messages in a Slack thread",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "channel_id": {
                            "type": "string",
                            "description": "Channel ID",
                        },
                        "thread_ts": {
                            "type": "string",
                            "description": "Thread timestamp (parent message timestamp)",
                        },
                    },
                    "required": ["channel_id", "thread_ts"],
                },
            ),
            Tool(
                name="slack_get_user_info",
                description="Get information about a Slack user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "User ID (e.g., 'U01234567')",
                        },
                    },
                    "required": ["user_id"],
                },
            ),
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a Slack tool."""
        # Validate common arguments
        if "count" in arguments:
            arguments["count"] = validate_positive_int(arguments["count"], max_value=100)

        if "limit" in arguments:
            arguments["limit"] = validate_positive_int(arguments["limit"], max_value=1000)

        # Check cache first (for read operations)
        # Use shorter TTL for Slack (15 minutes)
        cache_key = self.get_cache_key(name, **arguments)
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            self.logger.info(f"Cache hit for {name}")
            return cached_result

        # Execute tool
        if name == "slack_search_messages":
            result = await slack_search_messages(self.client, arguments)
        elif name == "slack_get_channel_history":
            result = await slack_get_channel_history(self.client, arguments)
        elif name == "slack_get_thread":
            result = await slack_get_thread(self.client, arguments)
        elif name == "slack_get_user_info":
            result = await slack_get_user_info(self.client, arguments)
        else:
            return f"Unknown tool: {name}"

        # Cache result
        self.cache.set(cache_key, result)

        return result


def main():
    """Main entry point."""
    server = SlackMCPServer()
    server.run()


if __name__ == "__main__":
    main()
