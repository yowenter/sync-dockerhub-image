from log_config import logging_config, dictConfig

dictConfig(logging_config)
from redis.connection import ConnectionPool
from huey import RedisHuey
from settings import REDIS_URL

redis_pool = ConnectionPool.from_url(REDIS_URL)

docker_huey = RedisHuey('docker_huey', connection_pool=redis_pool)
