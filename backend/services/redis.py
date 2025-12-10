import sys
import redis
import json

sys.path.insert(0, '/app')

from services.vault_helper import vault_helper
from redis.commands.search.field import TextField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType


class Redis:
    _client = None
    _vault_data = None

    def __init__(self):
        if Redis._client is None:
            Redis._client = self._create_client()

        self.redis = Redis._client

    def _get_vault_data(self):
        if Redis._vault_data is None:
            Redis._vault_data = vault_helper.get_redis_credentials()
        return Redis._vault_data

    def _create_client(self):
        creds = self._get_vault_data()
        return redis.Redis(
            host=creds["host"],
            port=creds["port"],
            decode_responses=True
        )

    def create_index(self):
        try:
            self.redis.ft("idx_docs").create_index(
                fields=[
                    TextField("quote"),
                    TextField("author"),
                    TextField("fact"),
                    TagField("source"),
                ],
                definition=IndexDefinition(
                    prefix=["breakingbad:", "catfact:"],
                    index_type=IndexType.HASH
                )
            )
            print("Redis index created")
        except Exception as e:
            print("Index create skipped:", e)

    def make_cache_key(self, prefix, **params):
        parts = [prefix] + [f"{k}:{v}" for k, v in sorted(params.items())]
        return "|".join(parts)

    def cache_get(self, key):
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    def cache_set(self, key, value, ttl=86400):
        self.redis.set(key, json.dumps(value), ex=ttl)
