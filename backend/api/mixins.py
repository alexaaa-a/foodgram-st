from rest_framework.response import Response
from services.redis import redis_client


class CachedListMixin:
    cache_prefix = None
    cache_ttl = 3600

    def list(self, request, *args, **kwargs):
        assert self.cache_prefix, "cache_prefix is required"

        cache_key = redis_client.make_cache_key(
            self.cache_prefix,
            **request.query_params.dict()
        )

        cached = redis_client.cache_get(cache_key)
        if cached is not None:
            return Response(cached)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            redis_client.cache_set(
                cache_key,
                response.data,
                ttl=self.cache_ttl
            )
            return response

        serializer = self.get_serializer(queryset, many=True)
        redis_client.cache_set(
            cache_key,
            serializer.data,
            ttl=self.cache_ttl
        )
        return Response(serializer.data)
