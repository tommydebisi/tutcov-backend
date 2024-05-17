from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework.views import exception_handler

class CustomUserRateThrottle(UserRateThrottle):
    history_key = 'custom_user_throttle_history'

    def wait(self):
        self.rate = '1000/minute'
        """
        Override the wait method to return a custom throttling message.
        """
        self.num_requests, self.duration = self.parse_rate(self.rate)
        self.history = self.cache.get(self.history_key, [])
        self.now = self.timer()
        self.history.append(self.now)
        self.history = self.history[-self.num_requests:]
        if len(self.history) >= self.num_requests:
            if self.now - self.history[0] < self.duration:
                wait_time = self.duration - (self.now - self.history[0])
                return Response(
                    {"message": "You are being throttled. Please try again later."},
                    status=429,
                    headers={"Retry-After": wait_time},
                )
        return None

