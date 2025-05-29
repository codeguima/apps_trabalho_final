import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

def get_redis():
    return redis_client

def cache():
    return redis_client