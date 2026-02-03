"""Slack message tools."""

import json
from typing import Any, Dict
from datetime import datetime, timedelta

from ..api_client import SlackClient


async def slack_search_messages(client: SlackClient, arguments: Dict[str, Any]) -> str:
    """
    Search Slack messages.

    Args:
        client: Slack API client
        arguments: Tool arguments

    Returns:
        JSON string with search results
    """
    query = arguments.get("query", "")
    count = arguments.get("count", 20)

    if not query:
        return json.dumps({"error": "Query is required"})

    try:
        result = client.search_messages(query=query, count=count)

        # Format response
        messages = result.get("messages", {}).get("matches", [])
        formatted_messages = []

        for msg in messages:
            formatted_messages.append({
                "text": msg.get("text"),
                "user": msg.get("username"),
                "channel": msg.get("channel", {}).get("name"),
                "timestamp": msg.get("ts"),
                "permalink": msg.get("permalink"),
            })

        return json.dumps({
            "total": result.get("messages", {}).get("total", 0),
            "messages": formatted_messages,
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def slack_get_channel_history(client: SlackClient, arguments: Dict[str, Any]) -> str:
    """
    Get Slack channel history.

    Args:
        client: Slack API client
        arguments: Tool arguments

    Returns:
        JSON string with channel history
    """
    channel_id = arguments.get("channel_id", "")
    start_date = arguments.get("start_date")
    end_date = arguments.get("end_date")
    limit = arguments.get("limit", 100)

    if not channel_id:
        return json.dumps({"error": "Channel ID is required"})

    try:
        # Convert dates to Unix timestamps
        oldest = None
        latest = None

        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date)
                oldest = str(int(start_dt.timestamp()))
            except ValueError:
                return json.dumps({"error": f"Invalid start_date format: {start_date}"})

        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date)
                latest = str(int(end_dt.timestamp()))
            except ValueError:
                return json.dumps({"error": f"Invalid end_date format: {end_date}"})

        result = client.get_channel_history(
            channel_id=channel_id,
            oldest=oldest,
            latest=latest,
            limit=limit,
        )

        # Get channel info
        channel_info = client.get_channel_info(channel_id)

        # Format response
        messages = result.get("messages", [])
        formatted_messages = []

        for msg in messages:
            user_id = msg.get("user")
            user_name = None
            if user_id:
                try:
                    user_info = client.get_user_info(user_id)
                    user_name = user_info.get("real_name") or user_info.get("name")
                except Exception:
                    user_name = user_id

            formatted_messages.append({
                "text": msg.get("text"),
                "user": user_name,
                "timestamp": msg.get("ts"),
                "thread_ts": msg.get("thread_ts"),
                "reply_count": msg.get("reply_count", 0),
                "reactions": [
                    {"name": r.get("name"), "count": r.get("count")}
                    for r in msg.get("reactions", [])
                ],
            })

        return json.dumps({
            "channel": {
                "id": channel_info.get("id"),
                "name": channel_info.get("name"),
                "is_private": channel_info.get("is_private", False),
            },
            "message_count": len(formatted_messages),
            "has_more": result.get("has_more", False),
            "messages": formatted_messages,
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def slack_get_thread(client: SlackClient, arguments: Dict[str, Any]) -> str:
    """
    Get Slack thread conversation.

    Args:
        client: Slack API client
        arguments: Tool arguments

    Returns:
        JSON string with thread messages
    """
    channel_id = arguments.get("channel_id", "")
    thread_ts = arguments.get("thread_ts", "")

    if not channel_id or not thread_ts:
        return json.dumps({"error": "Channel ID and thread timestamp are required"})

    try:
        result = client.get_thread_replies(
            channel_id=channel_id,
            thread_ts=thread_ts,
        )

        # Format response
        messages = result.get("messages", [])
        formatted_messages = []

        for msg in messages:
            user_id = msg.get("user")
            user_name = None
            if user_id:
                try:
                    user_info = client.get_user_info(user_id)
                    user_name = user_info.get("real_name") or user_info.get("name")
                except Exception:
                    user_name = user_id

            formatted_messages.append({
                "text": msg.get("text"),
                "user": user_name,
                "timestamp": msg.get("ts"),
                "reactions": [
                    {"name": r.get("name"), "count": r.get("count")}
                    for r in msg.get("reactions", [])
                ],
            })

        return json.dumps({
            "thread_ts": thread_ts,
            "message_count": len(formatted_messages),
            "messages": formatted_messages,
        }, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


async def slack_get_user_info(client: SlackClient, arguments: Dict[str, Any]) -> str:
    """
    Get Slack user information.

    Args:
        client: Slack API client
        arguments: Tool arguments

    Returns:
        JSON string with user data
    """
    user_id = arguments.get("user_id", "")

    if not user_id:
        return json.dumps({"error": "User ID is required"})

    try:
        user = client.get_user_info(user_id=user_id)

        formatted_user = {
            "id": user.get("id"),
            "name": user.get("name"),
            "real_name": user.get("real_name"),
            "display_name": user.get("profile", {}).get("display_name"),
            "email": user.get("profile", {}).get("email"),
            "title": user.get("profile", {}).get("title"),
            "is_bot": user.get("is_bot", False),
            "is_admin": user.get("is_admin", False),
            "timezone": user.get("tz"),
        }

        return json.dumps(formatted_user, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
