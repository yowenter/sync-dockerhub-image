import os

REDIS_URL = os.getenv("REDIS_URL", "redis://10.1.4.167:6379/0")

DOCKER_REGISTRY_API = os.getenv("DOCKER_REGISTRY_API", "https://registry-1.docker.io/v2")
# default dockerhub registry url

TARGET_REGISTRY_API = os.getenv("TARGET_REGISTRY_API", "http://10.1.4.167:5000/v2")

# to do support authorize registry

TARGET_REGISTRY_ENDPOINT = os.getenv("TARGET_REGISTRY", "10.1.4.167:5000")

IMAGES_DIR = os.getenv("IMAGES", os.path.join(os.path.dirname(os.path.dirname(__file__)), "images"))

LIBRARY_IMAGE_LIST_PATH = os.path.join(IMAGES_DIR, 'image.list')
