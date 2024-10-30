FROM python:3.9-slim

# Set working directory
WORKDIR /app/events_rest_api_service

# Copy the main application code and Install dependencies
COPY events_rest_api_service /app/events_rest_api_service
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared services_utils directory
COPY services_utils /app/services_utils
# Expose port for FastAPI
EXPOSE 8000

RUN chmod +x /app/events_rest_api_service/start_with_delay.sh

# Set the script as the entrypoint
ENTRYPOINT ["/app/events_rest_api_service/start_with_delay.sh"]
