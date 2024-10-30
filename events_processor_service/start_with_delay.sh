#!/bin/sh
echo "Waiting for RabbitMQ to be ready..."
sleep 10
echo "Starting events_processor_service..."
python app.py
