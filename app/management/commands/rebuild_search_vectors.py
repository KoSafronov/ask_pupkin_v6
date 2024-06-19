from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from app.models import Question

class Command(BaseCommand):
    help = 'Rebuild search vectors for questions'

    def handle(self, *args, **kwargs):
        questions = Question.objects.all()
        for question in questions:
            question.search_vector = SearchVector('title', 'content')
            question.save()
        self.stdout.write(self.style.SUCCESS('Successfully rebuilt search vectors'))
