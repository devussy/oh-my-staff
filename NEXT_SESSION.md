# Next Session Quick Start

## 🎯 Priority 1: Configure API Credentials (30-60 min)

### Step 1: Create .env file
```bash
cd /Users/yun/Workspace/mss-staff
cp .env.example .env
```

### Step 2: Get API Tokens

#### JIRA & Confluence (10 min)
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy token
4. Edit `.env` and fill in:
   - `JIRA_URL` - Your company's Atlassian URL
   - `JIRA_EMAIL` - Your email
   - `JIRA_API_TOKEN` - Token you just created
   - (Same for CONFLUENCE_*)

#### Slack (15 min)
1. Go to: https://api.slack.com/apps
2. Create/select app
3. OAuth & Permissions → Add scopes:
   - `channels:history`
   - `channels:read`
   - `users:read`
4. Install to workspace
5. Copy "Bot User OAuth Token"
6. Edit `.env`:
   - `SLACK_BOT_TOKEN=xoxb-...`
   - `SLACK_USER_TOKEN=xoxp-...` (optional, for search)

#### Google Workspace (20 min)
1. Go to: https://console.cloud.google.com/
2. Enable APIs: Docs, Sheets, Drive
3. Create OAuth 2.0 credentials (Desktop app)
4. Download credentials.json
5. Save to project root
6. Edit `.env`:
   - `GOOGLE_CREDENTIALS_FILE=/Users/yun/Workspace/mss-staff/google_credentials.json`
   - `GOOGLE_TOKEN_FILE=/Users/yun/Workspace/mss-staff/google_token.json`

### Step 3: Test
```bash
source venv/bin/activate
python scripts/test_connections.py
```

**Expected:** All ✅ green checkmarks

---

## 📋 Current Status

### ✅ What's Done
- All 5 MCP servers implemented (15 tools)
- Python environment configured
- All dependencies installed
- Test scripts working
- Documentation complete

### ⏳ What's Next
- Configure API credentials (YOU ARE HERE)
- Test real API connections
- Generate first report
- Implement advanced tools

---

## 🚀 Quick Commands

```bash
# Activate environment
source venv/bin/activate

# Test connections
python scripts/test_connections.py

# Clear cache
rm -rf data/cache/*

# View README
cat README.md
```

---

## 📁 Key Files

- **HANDOFF.md** - Detailed session handoff
- **README.md** - Full documentation
- **QUICKSTART.md** - 10-minute guide
- **.env.example** - Template for credentials
- **scripts/test_connections.py** - Test script

---

## ❓ If Something Breaks

1. Check virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Check dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Check .env file exists:
   ```bash
   ls -la .env
   ```

4. Read HANDOFF.md troubleshooting section

---

**Time Estimate:** 30-60 minutes to configure and test
**Next Goal:** Get all 4 API connections working ✅
