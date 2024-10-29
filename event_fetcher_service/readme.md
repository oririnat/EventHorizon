# Event Fetcher Service

## Description
This is a simple event fetcher service that fetches events from a remote server and submitting them to RabbitMQ for further processing. 

It dose this by fetching events from a remote server every 'POLL_INTERVAL_SECONDS' seconds will doing his best to avoiding duplicates events submitting.

## Installation
First you need to rename the .env_template file to .env and fill in the required fields.

Then, to install and run the service, you need to have python3 installed on your machine. 
And then run the following commands:


```bash
pip3 install -r requirements.txt
python3 app.py
```

