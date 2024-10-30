FROM python:3.9-slim

# Set working directory
WORKDIR /app/events_processor_service

# Copy the requirements file and install dependencies
COPY events_processor_service /app/events_processor_service
RUN pip install --no-cache-dir -r requirements.txt

# Copy the shared services_utils directory
COPY services_utils /app/services_utils

RUN chmod +x /app/events_processor_service/start_with_delay.sh

# Set the script as the entrypoint
ENTRYPOINT ["/app/events_processor_service/start_with_delay.sh"]