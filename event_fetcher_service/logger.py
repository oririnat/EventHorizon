import logging

# Configure logging
logging.basicConfig(
    filename='event_fetcher.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)

# Use logging in your modules
logging.info("Fetching events from GitHub API.")
logging.error("An error occurred.", exc_info=True)
