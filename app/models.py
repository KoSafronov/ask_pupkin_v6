from core.settings import POP_TAGS_COUNT, BEST_USERS_COUNT, HOT_QUESTIONS_COUNT

from django.db import models
from django.contrib.auth.models import User


class TagManager(models.Manager):
    def get_pop_tags(self):
        return self.order_by("-usages_count")[:POP_TAGS_COUNT]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    usages_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_question(self, question_id):
        return self.get(pk=question_id)

    def new_questions(self):
        return self.order_by("-created_at")

    def hot_questions(self):
        return self.order_by('-score')[:HOT_QUESTIONS_COUNT]

    def questions_by_tag(self, tag):
        return self.filter(tags__name=tag)

from django.contrib.postgres.indexes import GinIndex

from django.contrib.postgres.search import SearchVector

from django.contrib.postgres.indexes import GinIndex

#/tmp/crontab.NkMSvm/crontab
#/tmp/crontab.Cizcn6/crontab
from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    score = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()
    search_vector = SearchVectorField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]





# Add index
from django.contrib.postgres.indexes import GinIndex

class Meta:
    indexes = [GinIndex(fields=['search_vector'])]

class AnswerManager(models.Manager):
    def get_answer(self, answer_id):
        return self.get(pk=answer_id)

    def get_answers(self, question_id):
        return self.filter(question_id=question_id).order_by('-is_correct', '-score')


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return self.content


class ProfileManager(models.Manager):
    def get_best_profiles(self):
        return self.order_by('-rating')[:BEST_USERS_COUNT]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="uploads/avatars/", default='/uploads/avatars/empty/inkognito.jpg')
    rating = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class QuestionVote(models.Model):
    TYPES = [
        ("u", "upvote"),
        ("d", "downvote"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=1, choices=TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'question')


class AnswerVote(models.Model):
    TYPES = [
        ("u", "upvote"),
        ("d", "downvote"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=1, choices=TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'answer')