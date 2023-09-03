from django.core.cache import cache

CACHE_PRODUCT_COUNT = 'product_count'

def get_cache_product_count_key(user_id):
    return f'{CACHE_PRODUCT_COUNT}_{user_id}'


def cache_get_product_count(queryset, user_id):
    cache_key = get_cache_product_count_key(user_id)
    count = cache.get(cache_key, None)
    if not count:
        count = queryset.count()
        cache.set(cache_key, count, 60 * 1)
    return count