
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

SOURCE_REGISTRY_API = os.getenv("SOURCE_REGISTRY", "https://registry-1.docker.io/v2")
# default dockerhub registry url

TARGET_REGISTRY_API = os.getenv("TARGET_REGISTRY_API","http://localhost:5000/v2")

TARGET_REGISTRY = os.getenv("TARGET_REGISTRY","localhost:5000")


