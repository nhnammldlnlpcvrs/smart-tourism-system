#!/bin/sh
set -e

echo "Starting FastAPI backend..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACK_PID=$!

echo "Starting Svelte frontend..."
cd ../frontend/my-vietnam-map
npm run dev -- --host &
FRONT_PID=$!

trap "echo 'Stopping...'; kill $BACK_PID $FRONT_PID" INT TERM

wait