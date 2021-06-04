import json
import redis
import logging
import requests

logger = logging.getLogger(__name__)

db = redis.Redis()


def fetch_and_cache(url, key):
    try:
        response = requests.get(url)
        logger.debug(f"request:get url:{url}")

        if response.status_code == 200:
            db.set(key, json.dumps(response.json()))
            logger.debug(f"request:set key:{key}")
    except Exception as err:
        logger.debug("Cannot fetch and url -> {} : {}", url, err)


def cache(key, data):
    db.set(key, json.dumps(data))


def get_one(key):
    cached = db.get(key)
    logger.debug(f"redis:get key:{key}")
    return json.loads(cached)


def get_all(keys):
    cached = []
    p = db.pipeline()

    for key in keys:
        logger.debug(f"redis:get key:{key}")
        p.get(key)
    for value in p.execute():
        if value:
            cached.append(json.loads(value))
    return cached
