from django.contrib.auth.models import User

from app import models
from app.models import Profile
from core.settings import NEW_QUESTION_AWARD, NEW_ANSWER_AWARD

from django import forms

import re


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=30)


class SignupForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField(min_length=6, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and models.User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')

        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')

        return password_confirm

    def save(self, commit=True):
        user = models.User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password'])
        profile = models.Profile(user=user)

        if commit:
            user.save()
            profile.save()

        return user


from django import forms
from django.contrib.auth.models import User
from .models import Profile

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=30, required=False)
    email = forms.EmailField(min_length=6, max_length=30, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = models.User
        fields = ['username', 'email', 'avatar']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and models.User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError('A user with that email already exists.')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        email = self.cleaned_data.get('email')
        if email:
            user.email = email

        avatar = self.cleaned_data.get('avatar')
        if avatar:
            user.profile.avatar = avatar

        if commit:
            user.save()
            user.profile.save()

        return user






from django import forms
from .models import Question, Tag

class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'content']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if not re.match(r'^[a-zA-Z\-_ ]+$', tags):
            raise forms.ValidationError('A tag name can only consist of letters and dashes.')
        tags = tags.split()
        if len(tags) > 3:
            raise forms.ValidationError('You can add up to 3 tags only.')
        return tags

    def save(self, commit=True):
        question = super().save(commit=False)
        question.user = self.user
        if commit:
            question.save()
            tags = self.cleaned_data.get('tags')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
            question.save()
        return question





class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['content']

    def __init__(self, user, question, *args, **kwargs):
        self.user = user
        self.question = question
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = models.Answer(content=self.cleaned_data.get('content'))
        answer.user = self.user
        answer.question = self.question
        answer.is_correct = False
        self.user.profile.rating += NEW_ANSWER_AWARD

        if commit:
            answer.save()
            self.question.answers_count += 1
            self.question.save()
            self.user.profile.save()

        return answer








class CorrectForm(forms.Form):
    answer_id = forms.IntegerField()
    is_correct = forms.BooleanField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        answer_id = self.cleaned_data['answer_id']
        if models.Answer.objects.get(id=answer_id).question.user != self.user:
            raise forms.ValidationError('You can not perform this request.')

    def save(self, commit=True):
        answer_id = self.cleaned_data['answer_id']
        answer = models.Answer.objects.get(id=answer_id)

        answer.is_correct = self.cleaned_data['is_correct']

        if commit:
            answer.save()

        return answer


class VoteForm(forms.Form):
    ACTIONS = (
        ('upvote', 'upvote'),
        ('downvote', 'downvote'),
    )

    COMPONENTS = (
        ('question', 'question'),
        ('answer', 'answer'),
    )

    action = forms.ChoiceField(choices=ACTIONS)
    component = forms.ChoiceField(choices=COMPONENTS)
    component_id = forms.IntegerField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        action = self.cleaned_data['action']
        component = self.cleaned_data['component']
        component_id = self.cleaned_data['component_id']

        if component == 'question':
            question = models.Question.objects.get(id=component_id)
            vote = models.QuestionVote.objects.filter(user=self.user, question_id=component_id).first()
            if vote:
                if vote.vote_type == action[0]:
                    vote.delete()
                else:
                    vote.vote_type = action[0]

                    if commit:
                        vote.save()
            else:
                vote = models.QuestionVote(
                    user=self.user,
                    question_id=component_id,
                    vote_type=action[0]
                )

                if commit:
                    vote.save()

            upvotes = models.QuestionVote.objects.filter(question_id=component_id, vote_type='u').count()
            downvotes = models.QuestionVote.objects.filter(question_id=component_id, vote_type='d').count()
            rating = upvotes - downvotes

            question.score = rating
            if commit:
                question.save()

        else:
            answer = models.Answer.objects.get(id=component_id)
            vote = models.AnswerVote.objects.filter(user=self.user, answer_id=component_id).first()
            if vote:
                if vote.vote_type == action[0]:
                    vote.delete()
                else:
                    vote.vote_type = action[0]

                    if commit:
                        vote.save()
            else:
                vote = models.AnswerVote(
                    user=self.user,
                    answer_id=component_id,
                    vote_type=action[0]
                )

                if commit:
                    vote.save()

            upvotes = models.AnswerVote.objects.filter(answer_id=component_id, vote_type='u').count()
            downvotes = models.AnswerVote.objects.filter(answer_id=component_id, vote_type='d').count()
            rating = upvotes - downvotes

            answer.score = rating
            if commit:
                answer.save()

        return rating


from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Sorry, this email address already registred!")
        return email


from django import forms
from django.contrib.auth.models import User
from .models import Profile


from django import forms
from django.contrib.auth.models import User
