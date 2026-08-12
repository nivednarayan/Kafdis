import os
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
DEFAULT_LIMIT = os.getenv("DEFAULT_LIMIT", int("100"))
DEFAULT_WINDOW_SIZE = os.getenv("DEFAULT_WINDOW_SIZE", int("60"))
