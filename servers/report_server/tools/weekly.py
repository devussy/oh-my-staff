"""Weekly report generation tool."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader


async def report_generate_weekly(arguments: Dict[str, Any]) -> str:
    """
    Generate weekly report.

    This is a meta-tool that would typically call other MCP servers
    (JIRA, Confluence, Slack) to gather data. For MVP, it generates
    a template-based report with provided data.

    Args:
        arguments: Tool arguments

    Returns:
        JSON string with report path and content
    """
    week_start_date = arguments.get("week_start_date")
    include_sources = arguments.get("include_sources", ["jira", "confluence", "slack"])
    team_name = arguments.get("team_name", "Development Team")

    # Parse dates
    if week_start_date:
        try:
            week_start = datetime.fromisoformat(week_start_date)
        except ValueError:
            return json.dumps({"error": f"Invalid date format: {week_start_date}"})
    else:
        # Default to last Monday
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday() + 7)

    week_end = week_start + timedelta(days=6)

    # Prepare template data
    template_data = {
        "week_start": week_start.strftime("%Y-%m-%d"),
        "week_end": week_end.strftime("%Y-%m-%d"),
        "team_name": team_name,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": "Weekly report summarizing team activities and accomplishments.",
        "completed_issues": [],
        "total_story_points": 0,
        "confluence_updates": [],
        "slack_summary": None,
        "metrics": [],
        "next_week_plan": "Plan to be determined in sprint planning.",
    }

    # Add data from arguments if provided
    if "jira_data" in arguments:
        jira_data = arguments["jira_data"]
        if isinstance(jira_data, str):
            try:
                jira_data = json.loads(jira_data)
            except json.JSONDecodeError:
                pass

        if isinstance(jira_data, dict):
            template_data["completed_issues"] = jira_data.get("issues", [])
            template_data["total_story_points"] = jira_data.get("total_story_points", 0)

    if "confluence_data" in arguments:
        confluence_data = arguments["confluence_data"]
        if isinstance(confluence_data, str):
            try:
                confluence_data = json.loads(confluence_data)
            except json.JSONDecodeError:
                pass

        if isinstance(confluence_data, dict):
            template_data["confluence_updates"] = confluence_data.get("updates", [])

    if "slack_data" in arguments:
        slack_data = arguments["slack_data"]
        if isinstance(slack_data, str):
            try:
                slack_data = json.loads(slack_data)
            except json.JSONDecodeError:
                pass

        if isinstance(slack_data, dict):
            template_data["slack_summary"] = slack_data

    if "metrics" in arguments:
        template_data["metrics"] = arguments["metrics"]

    # Load and render template
    try:
        # Get template directory
        template_dir = Path(__file__).parent.parent / "templates"

        # Create Jinja environment
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template("weekly_report.md.j2")

        # Render report
        report_content = template.render(**template_data)

        # Save report
        report_dir = Path("reports/weekly")
        report_dir.mkdir(parents=True, exist_ok=True)

        filename = f"weekly-report-{week_start.strftime('%Y-W%W')}.md"
        report_path = report_dir / filename

        with open(report_path, "w") as f:
            f.write(report_content)

        return json.dumps({
            "success": True,
            "file_path": str(report_path),
            "week_start": template_data["week_start"],
            "week_end": template_data["week_end"],
            "content": report_content,
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def report_export_markdown(arguments: Dict[str, Any]) -> str:
    """
    Export report to markdown file.

    Args:
        arguments: Tool arguments

    Returns:
        JSON string with export result
    """
    report_data = arguments.get("report_data", {})
    template_name = arguments.get("template_name", "weekly_report.md.j2")
    output_path = arguments.get("output_path")

    if not report_data:
        return json.dumps({"error": "Report data is required"})

    try:
        # Get template directory
        template_dir = Path(__file__).parent.parent / "templates"

        # Create Jinja environment
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template(template_name)

        # Render report
        report_content = template.render(**report_data)

        # Determine output path
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_path = f"reports/ad_hoc/report-{timestamp}.md"

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save report
        with open(output_file, "w") as f:
            f.write(report_content)

        return json.dumps({
            "success": True,
            "file_path": str(output_file),
            "content_length": len(report_content),
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
