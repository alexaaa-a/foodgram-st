from celery import shared_task
import requests
from services.redis_client import get_redis_client
import uuid
from datetime import datetime


@shared_task
def get_quote_task(count):
    url = f"https://api.breakingbadquotes.xyz/v1/quotes/{count}"
    resp = requests.get(url).json()

    redis = get_redis_client()
    pipe = redis.pipeline()

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
    return resp

@shared_task
def get_cat_fact_task(count):
    url = f"https://meowfacts.herokuapp.com/?count={count}"
    resp = requests.get(url).json()

    redis = get_redis_client()
    pipe = redis.pipeline()

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
    return resp