"""Slack API client."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    """Slack API client wrapper."""

    def __init__(self, bot_token: str, user_token: Optional[str] = None):
        """
        Initialize Slack client.

        Args:
            bot_token: Slack bot token
            user_token: Optional user token for search
        """
        self.bot_client = WebClient(token=bot_token)
        self.user_client = WebClient(token=user_token) if user_token else None

    def search_messages(
        self,
        query: str,
        count: int = 20,
        sort: str = "timestamp",
    ) -> Dict[str, Any]:
        """
        Search messages (requires user token).

        Args:
            query: Search query
            count: Number of results
            sort: Sort order (timestamp, score)

        Returns:
            Search results
        """
        if not self.user_client:
            raise ValueError("User token required for search")

        try:
            response = self.user_client.search_messages(
                query=query,
                count=count,
                sort=sort,
            )
            return response.data
        except SlackApiError as e:
            raise Exception(f"Slack API error: {e.response['error']}")

    def get_channel_history(
        self,
        channel_id: str,
        oldest: Optional[str] = None,
        latest: Optional[str] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Get channel message history.

        Args:
            channel_id: Channel ID
            oldest: Oldest timestamp (Unix timestamp)
            latest: Latest timestamp (Unix timestamp)
            limit: Number of messages

        Returns:
            Channel history
        """
        try:
            kwargs = {
                "channel": channel_id,
                "limit": limit,
            }
            if oldest:
                kwargs["oldest"] = oldest
            if latest:
                kwargs["latest"] = latest

            response = self.bot_client.conversations_history(**kwargs)
            return response.data
        except SlackApiError as e:
            raise Exception(f"Slack API error: {e.response['error']}")

    def get_thread_replies(
        self,
        channel_id: str,
        thread_ts: str,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Get thread replies.

        Args:
            channel_id: Channel ID
            thread_ts: Thread timestamp
            limit: Number of messages

        Returns:
            Thread messages
        """
        try:
            response = self.bot_client.conversations_replies(
                channel=channel_id,
                ts=thread_ts,
                limit=limit,
            )
            return response.data
        except SlackApiError as e:
            raise Exception(f"Slack API error: {e.response['error']}")

    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        Get user information.

        Args:
            user_id: User ID

        Returns:
            User data
        """
        try:
            response = self.bot_client.users_info(user=user_id)
            return response.data.get("user", {})
        except SlackApiError as e:
            raise Exception(f"Slack API error: {e.response['error']}")

    def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """
        Get channel information.

        Args:
            channel_id: Channel ID

        Returns:
            Channel data
        """
        try:
            response = self.bot_client.conversations_info(channel=channel_id)
            return response.data.get("channel", {})
        except SlackApiError as e:
            raise Exception(f"Slack API error: {e.response['error']}")

    def list_channels(
        self,
        types: str = "public_channel,private_channel",
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List channels.

        Args:
            types: Channel types (comma-separated)
            limit: Number of channels

        Returns:
            List of channels
        """
        try:
            response = self.bot_client.conversations_list(
                types=types,
                limit=limit,
            )
            return response.data.get("channels", [])
        except SlackApiError as e:
            raise Exception(f"Slack API error: {e.response['error']}")

    def get_permalink(self, channel_id: str, message_ts: str) -> str:
        """
        Get message permalink.

        Args:
            channel_id: Channel ID
            message_ts: Message timestamp

        Returns:
            Permalink URL
        """
        try:
            response = self.bot_client.chat_getPermalink(
                channel=channel_id,
                message_ts=message_ts,
            )
            return response.data.get("permalink", "")
        except SlackApiError as e:
            raise Exception(f"Slack API error: {e.response['error']}")
