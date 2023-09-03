from django.core.cache import cache

def cache_get_product_count(queryset, user_id):
    cache_key = f'product_count_{user_id}'
    count = cache.get(cache_key, None)
    if not count:
        count = queryset.count()
        cache.set(cache_key, count, 60 * 60)
    return count