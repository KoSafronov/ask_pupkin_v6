
from django.core.cache import cache

def pop_tags_and_best_users(request):
    pop_tags = cache.get('pop_tags')
    best_users = cache.get('best_users')
    return {'pop_tags': pop_tags, 'best_users': best_users}
