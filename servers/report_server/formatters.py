"""Report formatting utilities."""

from datetime import datetime
from typing import Any, Dict, List


def format_date(date_str: str, format: str = "%Y-%m-%d") -> str:
    """
    Format date string.

    Args:
        date_str: Date string
        format: Output format

    Returns:
        Formatted date string
    """
    try:
        if not date_str:
            return "N/A"

        # Try parsing ISO format
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            dt = datetime.strptime(date_str, "%Y-%m-%d")

        return dt.strftime(format)
    except (ValueError, AttributeError):
        return date_str


def format_user(user_data: Dict[str, Any]) -> str:
    """
    Format user data.

    Args:
        user_data: User data dict

    Returns:
        Formatted user string
    """
    if not user_data:
        return "Unassigned"

    if isinstance(user_data, str):
        return user_data

    return user_data.get("displayName") or user_data.get("name") or "Unknown"


def format_list(items: List[str], separator: str = ", ") -> str:
    """
    Format list of items.

    Args:
        items: List of items
        separator: Separator string

    Returns:
        Formatted string
    """
    if not items:
        return "None"

    return separator.join(str(item) for item in items)


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length - 3] + "..."


def format_markdown_table(headers: List[str], rows: List[List[Any]]) -> str:
    """
    Format data as markdown table.

    Args:
        headers: Table headers
        rows: Table rows

    Returns:
        Markdown table string
    """
    if not headers or not rows:
        return ""

    # Build table
    lines = []

    # Header row
    lines.append("| " + " | ".join(str(h) for h in headers) + " |")

    # Separator row
    lines.append("| " + " | ".join("---" for _ in headers) + " |")

    # Data rows
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

    return "\n".join(lines)


def format_markdown_list(items: List[str], ordered: bool = False) -> str:
    """
    Format data as markdown list.

    Args:
        items: List items
        ordered: Whether to use ordered list

    Returns:
        Markdown list string
    """
    if not items:
        return ""

    lines = []
    for i, item in enumerate(items, 1):
        prefix = f"{i}." if ordered else "-"
        lines.append(f"{prefix} {item}")

    return "\n".join(lines)


def format_metric(value: Any, unit: str = "", precision: int = 2) -> str:
    """
    Format metric value.

    Args:
        value: Metric value
        unit: Unit string
        precision: Decimal precision

    Returns:
        Formatted metric string
    """
    if value is None:
        return "N/A"

    if isinstance(value, (int, float)):
        if precision > 0 and isinstance(value, float):
            formatted = f"{value:.{precision}f}"
        else:
            formatted = str(int(value))
    else:
        formatted = str(value)

    if unit:
        return f"{formatted} {unit}"

    return formatted
