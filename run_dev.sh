#!/usr/bin/env bash
set -e
export PYTHONPATH=$(pwd)
source .venv/bin/activate 2>/dev/null || true
(uvicorn backend.main:app --reload --port 8000 &)
python worker/worker.py
