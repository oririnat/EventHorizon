FROM python:3.9-slim

WORKDIR /app

COPY ./events_fetcher_service/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./events_fetcher_service /app

RUN chmod +x /app/start_with_delay.sh

# Set the script as the entrypoint
ENTRYPOINT ["/app/start_with_delay.sh"]