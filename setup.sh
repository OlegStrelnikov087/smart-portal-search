#!/bin/bash
# setup.sh - Automated setup script for Smart Portal Search

echo "🚀 Starting Smart Portal Search setup..."
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download NLP dependencies
echo "🤖 Downloading NLP dependencies..."
python download_dependencies.py

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p storage data/provided/ks data/provided/contracts models

# Initialize database
echo "💾 Initializing database..."
python -c "
from app.database.crud import init_db
init_db()
print('✅ Database initialized successfully!')
"

# Create indexes for search
echo "🔍 Creating search indexes..."
python -c "
from app.search.whoosh_index import search_engine
import pandas as pd

# Create basic index
try:
    search_engine.create_index()
    print('✅ Search index created successfully!')
except Exception as e:
    print(f'⚠️  Error creating index: {e}')
"

echo " "
echo "=========================================="
echo "✅ Setup completed successfully!"
echo " "
echo "🎯 Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo " "
echo "2. Start the server:"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo " "
echo "3. Open in browser:"
echo "   🌐 Web UI: http://localhost:8000/ui"
echo "   📄 API Docs: http://localhost:8000/docs"
echo " "
echo "4. Test the API:"
echo "   curl -X POST http://localhost:8000/api/search \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"q\": \"как создать котировочную сессию\"}'"
echo "=========================================="