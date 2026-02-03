# Quick Start Guide

Get up and running with MSS Staff in 10 minutes.

## Prerequisites

- Python 3.9 or higher
- API access to JIRA, Confluence, Slack, Google Workspace
- Claude Code CLI installed

## Step 1: Initial Setup (2 minutes)

```bash
# Run setup script
./scripts/setup_env.sh

# Activate virtual environment
source venv/bin/activate
```

## Step 2: Configure API Tokens (5 minutes)

Edit `.env` file with your API tokens:

### JIRA & Confluence

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy token to `.env`:

```bash
JIRA_URL=https://your-company.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your_token_here

CONFLUENCE_URL=https://your-company.atlassian.net
CONFLUENCE_EMAIL=your-email@company.com
CONFLUENCE_API_TOKEN=your_token_here
```

### Slack

1. Go to https://api.slack.com/apps
2. Create or select your app
3. Go to "OAuth & Permissions"
4. Copy "Bot User OAuth Token"
5. Add to `.env`:

```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_USER_TOKEN=xoxp-your-user-token  # Optional, for search
```

Required scopes:
- `channels:history`
- `channels:read`
- `users:read`

### Google Workspace

1. Go to https://console.cloud.google.com/
2. Enable Google Docs API and Google Sheets API
3. Create OAuth 2.0 credentials
4. Download `credentials.json`
5. Add to `.env`:

```bash
GOOGLE_CREDENTIALS_FILE=/path/to/credentials.json
GOOGLE_TOKEN_FILE=/path/to/token.json
```

## Step 3: Test Connections (2 minutes)

```bash
python scripts/test_connections.py
```

Expected output:
```
✅ JIRA connection successful!
✅ Confluence connection successful!
✅ Slack connection successful!
✅ Google Workspace connection successful!
```

## Step 4: Start Using with Claude Code (1 minute)

The `.mcp.json` file is already configured. Claude Code will automatically detect it.

### Example Queries

**Search JIRA issues:**
```
"Find all high priority bugs in JIRA"
```

**Search Confluence:**
```
"Find API documentation in Confluence"
```

**Get Slack messages:**
```
"Show me messages from #dev-team channel this week"
```

**Generate weekly report:**
```
"Generate a weekly report for last week"
```

## Common Issues

### Issue: JIRA connection failed
- Check JIRA_URL format (should be `https://your-company.atlassian.net`)
- Verify API token is correct
- Ensure email matches Atlassian account

### Issue: Google OAuth not working
- Make sure you downloaded `credentials.json` from Google Cloud Console
- First run will open browser for authentication
- `token.json` will be created automatically after first auth

### Issue: Slack token invalid
- Verify you're using Bot token (starts with `xoxb-`)
- Check that required scopes are added
- Reinstall app to workspace if needed

## Next Steps

1. **Customize queries**: Edit `config/jira_queries.yaml`
2. **Customize reports**: Edit `config/report_config.yaml`
3. **Add more tools**: See Phase 2 in the main plan
4. **Create agents**: See Phase 3 for agent implementation

## Getting Help

- Check `README.md` for detailed documentation
- See `config/` directory for configuration examples
- Run `python scripts/test_connections.py` to diagnose issues

## Useful Commands

```bash
# Test all connections
python scripts/test_connections.py

# Check if MCP servers are working
# (Claude Code will do this automatically)

# Clear cache
rm -rf data/cache/*

# View generated reports
ls -l reports/weekly/
```

## Example Workflow

1. Monday morning: `"Generate last week's report"`
2. Check sprint: `"What's the status of current sprint?"`
3. Find blockers: `"Show me all blocked issues"`
4. Review docs: `"Find pages updated in Confluence this week"`
5. Team activity: `"Summarize dev-team Slack discussions"`

---

You're all set! Start using Claude Code with your MCP servers. 🚀
