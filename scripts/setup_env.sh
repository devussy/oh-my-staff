#!/bin/bash
# Setup script for MSS Staff project

set -e

echo "=========================================="
echo "MSS Staff - Environment Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python 3 is installed"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API tokens!"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/cache/{jira,confluence,slack,google}
mkdir -p data/history/{weekly_reports,analyses}
mkdir -p reports/{weekly,monthly,ad_hoc}
echo "✅ Directories created"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API tokens"
echo "2. Run: python scripts/test_connections.py"
echo "3. Start using the MCP servers with Claude Code"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
