import redis

redis_pool = redis.ConnectionPool(host="localhost", port=6380, db=0)
redis_client = redis.Redis(connection_pool=redis_pool)


def get_redis_client():
    return redis_client
