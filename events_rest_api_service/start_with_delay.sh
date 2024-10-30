#!/bin/sh
echo "Waiting for DB to be ready..."
sleep 10
echo "Starting events_rest_api_service..."
uvicorn main:app --host 0.0.0.0 --port 8000
