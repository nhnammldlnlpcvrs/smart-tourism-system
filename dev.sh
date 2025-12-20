#!/bin/sh
set -e

echo "Starting FastAPI backend..."
cd backend
python -m uvicorn app.api.main:app --reload &
BACK_PID=$!

echo "Starting Svelte frontend..."
cd ../frontend/my-vietnam-map
npm run dev -- --host &
FRONT_PID=$!

trap "echo 'Stopping...'; kill $BACK_PID $FRONT_PID" INT TERM

wait