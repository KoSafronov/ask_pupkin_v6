
from django.core.management.base import BaseCommand
from django.core.cache import cache
from app.models import Tag, Profile, Question

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        pop_tags = Tag.objects.get_pop_tags()
        best_users = Profile.objects.get_best_profiles()

        cache.set('pop_tags', pop_tags, 3600)
        cache.set('best_users', best_users, 3600)
