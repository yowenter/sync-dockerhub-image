import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

DOCKER_REGISTRY_API = os.getenv("DOCKER_REGISTRY_API", "https://registry-1.docker.io/v2")
# default dockerhub registry url

TARGET_REGISTRY_API = os.getenv("TARGET_REGISTRY_API", "http://localhost:5000/v2")

# to do support authorize registry

TARGET_REGISTRY_ENDPOINT = os.getenv("TARGET_REGISTRY", "localhost:5000")

IMAGES_DIR = os.getenv("IMAGES_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "images"))

LIBRARY_IMAGE_LIST_PATH = os.path.join(IMAGES_DIR, 'image.list')
THIRD_PARTY_LIST_PATH = os.path.join(IMAGES_DIR, 'third_party.list')
IMAGE_NAME_CONVERT_LIST_PATH = os.path.join(IMAGES_DIR, 'image_name_convert.list')

PROD = str(os.getenv("PROD")) in ('yes', '1', 'true', 'True')

TARGET_THIRD_PARTY_NAMESPACE = os.getenv("TARGET_THIRD_PARTY_NAMESPACE", "daocloud")
