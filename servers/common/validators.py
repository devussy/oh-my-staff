"""Input validation utilities."""

import re
from datetime import datetime
from typing import Optional


class ValidationError(Exception):
    """Validation error."""

    pass


def validate_date(date_str: str, format: str = "%Y-%m-%d") -> datetime:
    """
    Validate and parse date string.

    Args:
        date_str: Date string
        format: Expected date format

    Returns:
        Parsed datetime object

    Raises:
        ValidationError: If date is invalid
    """
    try:
        return datetime.strptime(date_str, format)
    except ValueError as e:
        raise ValidationError(f"Invalid date format: {date_str}. Expected format: {format}") from e


def validate_jql(jql: str) -> str:
    """
    Validate JQL (JIRA Query Language) query.

    Basic validation to prevent injection attacks.

    Args:
        jql: JQL query string

    Returns:
        Validated JQL string

    Raises:
        ValidationError: If JQL contains suspicious patterns
    """
    if not jql or not isinstance(jql, str):
        raise ValidationError("JQL query must be a non-empty string")

    # Check for suspicious patterns (basic security check)
    suspicious_patterns = [
        r";\s*drop\s+table",
        r";\s*delete\s+from",
        r";\s*update\s+",
        r"<script",
        r"javascript:",
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, jql, re.IGNORECASE):
            raise ValidationError(f"JQL query contains suspicious pattern: {pattern}")

    # JQL should have reasonable length
    if len(jql) > 5000:
        raise ValidationError("JQL query is too long (max 5000 characters)")

    return jql.strip()


def validate_cql(cql: str) -> str:
    """
    Validate CQL (Confluence Query Language) query.

    Basic validation to prevent injection attacks.

    Args:
        cql: CQL query string

    Returns:
        Validated CQL string

    Raises:
        ValidationError: If CQL contains suspicious patterns
    """
    if not cql or not isinstance(cql, str):
        raise ValidationError("CQL query must be a non-empty string")

    # Check for suspicious patterns (basic security check)
    suspicious_patterns = [
        r"<script",
        r"javascript:",
        r"onerror\s*=",
        r"onload\s*=",
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, cql, re.IGNORECASE):
            raise ValidationError(f"CQL query contains suspicious pattern: {pattern}")

    # CQL should have reasonable length
    if len(cql) > 5000:
        raise ValidationError("CQL query is too long (max 5000 characters)")

    return cql.strip()


def validate_email(email: str) -> str:
    """
    Validate email address.

    Args:
        email: Email address

    Returns:
        Validated email address

    Raises:
        ValidationError: If email is invalid
    """
    if not email or not isinstance(email, str):
        raise ValidationError("Email must be a non-empty string")

    # Simple email validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        raise ValidationError(f"Invalid email address: {email}")

    return email.strip()


def validate_url(url: str) -> str:
    """
    Validate URL.

    Args:
        url: URL string

    Returns:
        Validated URL string

    Raises:
        ValidationError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValidationError("URL must be a non-empty string")

    # Simple URL validation
    url_pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
    if not re.match(url_pattern, url):
        raise ValidationError(f"Invalid URL: {url}")

    return url.strip()


def validate_positive_int(value: int, max_value: Optional[int] = None) -> int:
    """
    Validate positive integer.

    Args:
        value: Integer value
        max_value: Optional maximum value

    Returns:
        Validated integer

    Raises:
        ValidationError: If value is invalid
    """
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(f"Value must be a positive integer, got: {value}")

    if max_value is not None and value > max_value:
        raise ValidationError(f"Value must be <= {max_value}, got: {value}")

    return value
