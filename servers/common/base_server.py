"""Base MCP server class with common functionality."""

import os
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

# Try to import MCP SDK, fall back to stub if not available
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    # Use stub implementation for testing
    from .mcp_stub import Server, stdio_server, Tool, TextContent

from .cache import Cache
from .logging_config import setup_logging


class BaseMCPServer(ABC):
    """Base class for MCP servers with common functionality."""

    def __init__(self, name: str, cache_dir: Optional[str] = None):
        """
        Initialize base MCP server.

        Args:
            name: Server name
            cache_dir: Optional cache directory (defaults to data/cache/{name})
        """
        self.name = name
        self.logger = setup_logging(f"mcp.{name}")
        self.server = Server(name)

        # Set up cache
        if cache_dir is None:
            cache_dir = f"data/cache/{name}"
        self.cache = Cache(cache_dir, ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "3600")))

        # Register handlers
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register MCP handlers."""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools."""
            tools = self.get_tools()
            self.logger.info(f"Listed {len(tools)} tools")
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Call a tool."""
            self.logger.info(f"Calling tool: {name} with arguments: {arguments}")

            try:
                result = await self.execute_tool(name, arguments)
                self.logger.info(f"Tool {name} executed successfully")

                # Convert result to TextContent
                if isinstance(result, str):
                    return [TextContent(type="text", text=result)]
                elif isinstance(result, dict):
                    import json
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]
                else:
                    return [TextContent(type="text", text=str(result))]

            except Exception as e:
                self.logger.error(f"Error executing tool {name}: {e}", exc_info=True)
                error_message = f"Error: {str(e)}"
                return [TextContent(type="text", text=error_message)]

    @abstractmethod
    def get_tools(self) -> List[Tool]:
        """
        Get list of available tools.

        Returns:
            List of Tool definitions

        This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool execution result

        This method must be implemented by subclasses.
        """
        pass

    def run(self) -> None:
        """Run the MCP server."""
        self.logger.info(f"Starting {self.name} MCP server")

        try:
            import asyncio
            asyncio.run(stdio_server(self.server))
        except KeyboardInterrupt:
            self.logger.info(f"{self.name} MCP server stopped by user")
        except Exception as e:
            self.logger.error(f"Error running {self.name} MCP server: {e}", exc_info=True)
            sys.exit(1)

    def get_cache_key(self, prefix: str, **kwargs) -> str:
        """
        Generate cache key from prefix and arguments.

        Args:
            prefix: Cache key prefix
            **kwargs: Key-value pairs to include in cache key

        Returns:
            Cache key string
        """
        # Sort kwargs for consistent keys
        sorted_kwargs = sorted(kwargs.items())
        key_parts = [prefix] + [f"{k}={v}" for k, v in sorted_kwargs]
        return ":".join(str(p) for p in key_parts)

    def load_env_var(self, var_name: str, required: bool = True) -> Optional[str]:
        """
        Load environment variable with validation.

        Args:
            var_name: Environment variable name
            required: Whether the variable is required

        Returns:
            Environment variable value or None

        Raises:
            ValueError: If required variable is not set
        """
        value = os.getenv(var_name)

        if required and not value:
            raise ValueError(f"Required environment variable {var_name} is not set")

        return value
