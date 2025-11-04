#!/usr/bin/env bash
set -e
echo "Starting Aqarino v2 (simple)"
docker compose up -d --build
echo "Frontend: http://localhost:8081"
echo "Backend:  http://localhost:8000"
