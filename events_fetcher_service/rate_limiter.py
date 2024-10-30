class RateLimiter:
    def __init__(self):
        self.remaining = 5000  # Starting assumption for authenticated requests
        self.reset_time = None

    def update(self, headers):
        self.remaining = int(headers.get("X-RateLimit-Remaining", self.remaining))
        self.reset_time = int(headers.get("X-RateLimit-Reset", self.reset_time))

    def should_wait(self):
        return self.remaining <= 0