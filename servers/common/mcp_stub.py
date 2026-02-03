"""
Minimal MCP stub for testing until official SDK is available.
This allows API connection testing without the full MCP SDK.
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
import sys
import json


@dataclass
class Tool:
    """Tool definition."""
    name: str
    description: str
    inputSchema: Dict[str, Any]


@dataclass
class TextContent:
    """Text content response."""
    type: str
    text: str


class Server:
    """Minimal MCP server stub."""

    def __init__(self, name: str):
        self.name = name
        self._list_tools_handler: Optional[Callable] = None
        self._call_tool_handler: Optional[Callable] = None

    def list_tools(self):
        """Decorator for list_tools handler."""
        def decorator(func):
            self._list_tools_handler = func
            return func
        return decorator

    def call_tool(self):
        """Decorator for call_tool handler."""
        def decorator(func):
            self._call_tool_handler = func
            return func
        return decorator


async def stdio_server(server: Server):
    """Minimal stdio server stub."""
    print(f"[STUB] {server.name} MCP Server (using stub implementation)")
    print(f"[STUB] Real MCP SDK not installed")
    print(f"[STUB] To use with Claude Code, install the official MCP SDK")
    print(f"[STUB] For now, use test_connections.py to verify API credentials")


# Create module structure to match real mcp package
class types:
    Tool = Tool
    TextContent = TextContent


class server:
    Server = Server

    class stdio:
        stdio_server = stdio_server


# Add to sys.modules to allow imports
sys.modules['mcp'] = type(sys)('mcp')
sys.modules['mcp'].types = types
sys.modules['mcp'].server = server
sys.modules['mcp.types'] = types
sys.modules['mcp.server'] = server
sys.modules['mcp.server.stdio'] = server.stdio
