#!/usr/bin/env bash
# Start the Council web app
# Usage: ./start.sh  (ANTHROPIC_API_KEY must be set in env or .env)

set -e
cd "$(dirname "$0")"

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "Error: ANTHROPIC_API_KEY is not set."
  echo "Create council_web/.env with: ANTHROPIC_API_KEY=sk-ant-..."
  exit 1
fi

# Create venv if needed
if [ ! -d .venv ]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi

echo "Starting Council on http://localhost:5050"
.venv/bin/python app.py
