"""Common utilities for MCP servers."""

from .base_server import BaseMCPServer
from .cache import Cache
from .logging_config import setup_logging, mask_sensitive_data
from .validators import validate_date, validate_jql, validate_cql

# Try to import MCP types, use stub if not available
try:
    from mcp.types import Tool, TextContent
except ImportError:
    from .mcp_stub import Tool, TextContent

__all__ = [
    "BaseMCPServer",
    "Cache",
    "setup_logging",
    "mask_sensitive_data",
    "validate_date",
    "validate_jql",
    "validate_cql",
    "Tool",
    "TextContent",
]
