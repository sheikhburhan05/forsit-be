#!/bin/bash
#
# App entrypoint, for Dockerfile
#

### Things to do before app starts
echo "[*] Running  migrations"

### Start the app
echo "[*] Starting app"
cd "$(dirname "$0")/.."

uvicorn src.main:app --host 0.0.0.0 --port 8000 
