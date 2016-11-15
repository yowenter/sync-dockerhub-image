
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

SOURCE_REGISTRY = os.getenv("SOURCE_REGISTRY", "index.docker.io")

TARGET_REGISTRY = os.getenv("TARGET_REGISTRY","localhost:5500")


