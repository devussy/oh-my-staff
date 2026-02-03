#!/usr/bin/env python3
"""Test API connections for all services."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_jira():
    """Test JIRA connection."""
    print("\n🔍 Testing JIRA connection...")

    try:
        from servers.jira_server.api_client import JiraClient

        jira_url = os.getenv("JIRA_URL")
        jira_email = os.getenv("JIRA_EMAIL")
        jira_token = os.getenv("JIRA_API_TOKEN")

        if not all([jira_url, jira_email, jira_token]):
            print("❌ JIRA credentials not configured in .env")
            return False

        client = JiraClient(
            url=jira_url,
            username=jira_email,
            password=jira_token,
        )

        # Test basic query
        result = client.search_issues(jql="order by created DESC", max_results=1)
        print(f"✅ JIRA connection successful! Found {result.get('total', 0)} total issues")
        return True

    except Exception as e:
        print(f"❌ JIRA connection failed: {str(e)}")
        return False


def test_confluence():
    """Test Confluence connection."""
    print("\n🔍 Testing Confluence connection...")

    try:
        from servers.confluence_server.api_client import ConfluenceClient

        confluence_url = os.getenv("CONFLUENCE_URL")
        confluence_email = os.getenv("CONFLUENCE_EMAIL")
        confluence_token = os.getenv("CONFLUENCE_API_TOKEN")

        if not all([confluence_url, confluence_email, confluence_token]):
            print("❌ Confluence credentials not configured in .env")
            return False

        client = ConfluenceClient(
            url=confluence_url,
            username=confluence_email,
            password=confluence_token,
        )

        # Test basic query
        spaces = client.get_all_spaces(limit=1)
        print(f"✅ Confluence connection successful! Found {len(spaces)} spaces")
        return True

    except Exception as e:
        print(f"❌ Confluence connection failed: {str(e)}")
        return False


def test_slack():
    """Test Slack connection."""
    print("\n🔍 Testing Slack connection...")

    try:
        from servers.slack_server.api_client import SlackClient

        bot_token = os.getenv("SLACK_BOT_TOKEN")
        user_token = os.getenv("SLACK_USER_TOKEN")

        if not bot_token:
            print("❌ Slack bot token not configured in .env")
            return False

        client = SlackClient(
            bot_token=bot_token,
            user_token=user_token,
        )

        # Test basic query
        channels = client.list_channels(limit=1)
        print(f"✅ Slack connection successful! Found {len(channels)} channels")

        if user_token:
            print("✅ User token configured (search enabled)")
        else:
            print("⚠️  User token not configured (search disabled)")

        return True

    except Exception as e:
        print(f"❌ Slack connection failed: {str(e)}")
        return False


def test_google_workspace():
    """Test Google Workspace connection."""
    print("\n🔍 Testing Google Workspace connection...")

    try:
        from servers.google_workspace_server.api_client import GoogleWorkspaceClient

        credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
        token_file = os.getenv("GOOGLE_TOKEN_FILE")

        if not all([credentials_file, token_file]):
            print("❌ Google Workspace credentials not configured in .env")
            return False

        if not os.path.exists(credentials_file):
            print(f"❌ Credentials file not found: {credentials_file}")
            return False

        client = GoogleWorkspaceClient(
            credentials_file=credentials_file,
            token_file=token_file,
        )

        # Test basic query
        files = client.list_files(page_size=1)
        print(f"✅ Google Workspace connection successful! Found {len(files)} files")
        return True

    except Exception as e:
        print(f"❌ Google Workspace connection failed: {str(e)}")
        return False


def main():
    """Run all connection tests."""
    print("=" * 60)
    print("MSS Staff - API Connection Tests")
    print("=" * 60)

    results = {
        "JIRA": test_jira(),
        "Confluence": test_confluence(),
        "Slack": test_slack(),
        "Google Workspace": test_google_workspace(),
    }

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    for service, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{service:20} {status}")

    passed = sum(results.values())
    total = len(results)

    print(f"\nTotal: {passed}/{total} services connected successfully")

    if passed == total:
        print("\n🎉 All services connected successfully!")
        return 0
    else:
        print("\n⚠️  Some services failed. Check your .env configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
