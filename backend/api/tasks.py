from celery import shared_task
import requests
from services.redis import Redis
import uuid
from datetime import datetime


redis_client = Redis()

@shared_task
def get_quote_task(count):
    cache_key = redis_client.make_cache_key("breakingbad_quotes", count=count)
    cached = redis_client.cache_get(cache_key)
    if cached:
        return cached

    url = f"https://api.breakingbadquotes.xyz/v1/quotes/{count}"
    resp = requests.get(url).json()

    pipe = redis_client.redis.pipeline()

    for item in resp:
        key = f"breakingbad:{uuid.uuid4()}"
        pipe.hset(
            key,
            mapping={
                "source": "breakingbad",
                "quote": item["quote"],
                "author": item["author"],
                "timestamp": datetime.now().isoformat()
            }
        )

    pipe.execute()

    redis_client.cache_set(cache_key, resp)
    return resp

@shared_task
def get_cat_fact_task(count):
    cache_key = redis_client.make_cache_key("cat_facts", count=count)
    cached = redis_client.cache_get(cache_key)
    if cached:
        return cached

    url = f"https://meowfacts.herokuapp.com/?count={count}"
    resp = requests.get(url).json()

    pipe = redis_client.redis.pipeline()

    for fact in resp["data"]:
        key = f"catfact:{uuid.uuid4()}"
        pipe.hset(
            key,
            mapping={
                "source": "catfact",
                "fact": fact,
                "timestamp": datetime.now().isoformat()
            }
        )

    pipe.execute()
    redis_client.cache_set(cache_key, resp)

    return resp
