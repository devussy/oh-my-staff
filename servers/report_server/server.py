"""Report MCP Server implementation."""

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

from servers.common import BaseMCPServer
from .tools.weekly import report_generate_weekly, report_export_markdown


class ReportMCPServer(BaseMCPServer):
    """Report MCP Server."""

    def __init__(self):
        """Initialize Report MCP Server."""
        super().__init__("report", cache_dir="data/cache/report")
        self.logger.info("Report MCP Server initialized")

    def get_tools(self) -> List[Tool]:
        """Get list of available Report tools."""
        return [
            Tool(
                name="report_generate_weekly",
                description="Generate a weekly report combining data from multiple sources",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "week_start_date": {
                            "type": "string",
                            "description": "Week start date in ISO format (e.g., '2024-01-01'). Defaults to last Monday.",
                        },
                        "include_sources": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["jira", "confluence", "slack", "google"],
                            },
                            "description": "Data sources to include in the report",
                            "default": ["jira", "confluence", "slack"],
                        },
                        "team_name": {
                            "type": "string",
                            "description": "Team name for the report",
                            "default": "Development Team",
                        },
                        "jira_data": {
                            "type": "object",
                            "description": "JIRA data (optional, can be JSON string or object)",
                        },
                        "confluence_data": {
                            "type": "object",
                            "description": "Confluence data (optional, can be JSON string or object)",
                        },
                        "slack_data": {
                            "type": "object",
                            "description": "Slack data (optional, can be JSON string or object)",
                        },
                        "metrics": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "value": {"type": "string"},
                                },
                            },
                            "description": "Additional metrics to include",
                        },
                    },
                },
            ),
            Tool(
                name="report_export_markdown",
                description="Export report data to a markdown file using a template",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "report_data": {
                            "type": "object",
                            "description": "Report data to render",
                        },
                        "template_name": {
                            "type": "string",
                            "description": "Template filename (e.g., 'weekly_report.md.j2')",
                            "default": "weekly_report.md.j2",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Output file path (optional, auto-generated if not provided)",
                        },
                    },
                    "required": ["report_data"],
                },
            ),
        ]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a Report tool."""
        # Report tools typically don't use cache since they generate new content
        # However, we could cache intermediate data processing

        # Execute tool
        if name == "report_generate_weekly":
            result = await report_generate_weekly(arguments)
        elif name == "report_export_markdown":
            result = await report_export_markdown(arguments)
        else:
            return f"Unknown tool: {name}"

        return result


def main():
    """Main entry point."""
    server = ReportMCPServer()
    server.run()


if __name__ == "__main__":
    main()
