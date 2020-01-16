import os


def get_mongo_uri():
    host = os.environ.get('MONGO_HOST', 'localhost')
    port = os.environ.get('MONGO_PORT', '27017')
    return f'mongodb://{host}:{port}/'

def get_redis_uri():
    host = os.environ.get('REDIS_HOST', 'localhost')
    port = os.environ.get('REDIS_PORT', '6379')
    return f'redis://{host}:{port}/'

