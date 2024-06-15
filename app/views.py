import json
import math

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import EmptyPage, InvalidPage
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.views.decorators.http import require_http_methods, require_POST

from app.forms import LoginForm, SignupForm, ProfileForm, AskForm, AnswerForm, CorrectForm, VoteForm
from app.models import Question, Answer, Tag, Profile
from core.settings import QUESTIONS_PER_PAGE, ANSWERS_PER_PAGE


# Create your views here.
# QUESTIONS = [
#     {
#         "id": i,
#         "title": f"Question {i}",
#         "text": F"This is question number {i}"
#     } for i in range(200)
# ]

#
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import UserRegisterForm
# def register(request):
# 	if request.method == 'POST':
#     	form = UserRegisterForm(request.POST)
#     	if form.is_valid():
#         	form.save()
#         	username = form.cleaned_data.get('username')
#         	messages.success(request, f'Создан аккаунт {username}!')
#         	return redirect('blog-home')
# 	else:
#     	form = UserRegisterForm()
# 	return render(request, 'users/register.html', {'form': form})


def post_list_all(request):
    posts = Post.objects.filter(is_published=True)
    limit = request.GET.get('limit', 10)
    num_page = request.GET.get('page', 1)
    paginator = Paginator(posts, limit)
    page = paginator.page(num_page)  # Page
    return render(request, 'blog/post_by_tag.html', {
        'posts': page.object_list,
        'paginator': paginator, 'page': page,
    })


#
# def PageNotFound(request, exception):
#     return render(request, template_name='oops', status='404')
#
#
# def handler500(request, exception):
#     return render(request, template_name='oops', status=500)


def paginate(items, request, *, per_page=5):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(items, per_page)

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(1)

    return page_obj


# def index(request):
#     page_num = request.GET.get('page', 1)
#     paginator = Paginator(QUESTIONS, 5, allow_empty_first_page=False)
#     page_obj = paginator.page(page_num)
#     return render(request, "index.html", {"questions": page_obj})


def index(request):
    new_questions = list(Question.objects.new_questions())
    page_obj = paginate(new_questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }
    return render(request, 'index.html', context)


# def hot(request):
#     questions = QUESTIONS[::-1]
#     page_num = request.GET.get('page', 1)
#     paginator = Paginator(questions, 5, allow_empty_first_page=False)
#     page_obj = paginator.page(page_num)
#     return render(request, "hot.html", {"questions": page_obj})


def hot_questions(request):
    questions = list(Question.objects.hot_questions())
    page_obj = paginate(questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'hot_questions.html', context)


#
# @login_required(login_url="login")
# def login(request):
#     return render(request, "login.html")


# def log_in(request):
#     print(request.GET)
#     print(request.POST)
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(username=username, password=password)
#     if user:
#         return redirect(reverse('index'))
#     print('Failed to login')
#     return render(request, "login.html")


@require_http_methods(['GET', 'POST'])
# @csrf_protect
@requires_csrf_token
def login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                redirect_to = request.GET.get('continue', reverse('index'))
                return redirect(redirect_to)

    context = {
        'form': login_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'login.html', context)


# @require_http_methods(['GET', 'POST'])
# @csrf_protect
# def login(request):
#     login_form = LoginForm()
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user = auth.authenticate(request, **login_form.cleaned_data)
#             if user:
#                 auth.login(request, user)
#                 redirect_to = request.GET.get('continue', reverse('index'))
#                 return redirect(redirect_to)
#
#     context = {
#         'form': login_form,
#         'pop_tags': Tag.objects.get_pop_tags(),
#         'best_members': Profile.objects.get_best_profiles(),
#     }
#
#     return render(request, 'login.html', context)


# def ask(request):
#     return render(request, "ask.html")
@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def ask(request):
    ask_form = AskForm(request.user)
    if request.method == 'POST':
        ask_form = AskForm(request.user, request.POST)
        if ask_form.is_valid():
            question = ask_form.save()
            if question:
                return redirect('question', question_id=question.id)

    context = {
        'form': ask_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'ask.html', context)


def register(request):
    return render(request, "register.html")


@require_http_methods(['GET', 'POST'])
@csrf_protect
@requires_csrf_token
def settings1(request):
    context = {
        'form': ProfileForm,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }
    # return render(request, "settings.html", context)
    return render(request, 'settings.html', context)


@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def settings(request):
    profile_form = ProfileForm(request.user, initial={
        'username': request.user.username,
        'email': request.user.email,
    })
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.user,
            request.POST,
            files=request.FILES,
            instance=request.user
        )
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('settings'))

    context = {
        'form': profile_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'settings.html', context)


@login_required(login_url='login', redirect_field_name='continue')
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('index', reverse('index')))


# def question(request, question_id):
#     item = QUESTIONS[question_id]
#     return render(request, "question_detail.html", {"question": item})

def question(request, question_id):
    question = Question.objects.get_question(question_id)
    answers = list(Answer.objects.get_answers(question_id))
    page_obj = paginate(answers, request, per_page=ANSWERS_PER_PAGE)

    answer_form = AnswerForm(request.user, question)

    context = {
        'form': answer_form,
        'question': question,
        'answers': page_obj,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'question_details.html', context)


def tag(request, tag_name):
    name = TAGS[tag_name]
    return render(request, "tag_page.html", {"tag": tag_name})


def oops_404(request):
    return render(request, "layouts/404_oops.html")


# @login_required(login_url='login', redirect_field_name='continue')
# @require_POST
# @csrf_protect
# def answer(request, question_id):
#     question = Question.objects.get_question(question_id)
#     answer_form = AnswerForm(request.user, question, request.POST)
#     if answer_form.is_valid():
#         answer = answer_form.save()
#         answers_count = Answer.objects.get_answers(question_id).count()
#         return redirect(
#             reverse('question', kwargs={'question_id': question_id})
#             + f'?page={math.ceil(answers_count / ANSWERS_PER_PAGE)}'
#             + f'#{answer.id}'
#         )

# @login_required(login_url='login', redirect_field_name='continue')
# @require_POST
# @csrf_protect
# def answer(request, question_id):
#     ws_channel_name = f'question_{question_id}'
#
#     question = Question.objects.get_question(question_id)
#     answer_form = AnswerForm(request.user, question, request.POST)
#     if answer_form.is_valid():
#         answer = answer_form.save()
#         answers_count = Answer.objects.get_answers(question_id).count()
#
#         api_url = settings.CENTRIFUGO_API_URL
#         api_key = settings.CENTRIFUGO_API_KEY
#
#         body = model_to_dict(answer)
#         body |= {'avatar_url': request.user.profile.avatar.url}
#
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'apikey {api_key}'
#         }
#         data = {
#             'method': 'publish',
#             'params': {
#                 'channel': ws_channel_name,
#                 'data': body,
#             }
#         }
#         response = requests.post(api_url, headers=headers, data=json.dumps(data))
#
#         if response.status_code == 200:
#             return redirect(
#                 reverse('question', kwargs={'question_id': question_id})
#                 + f'?page={math.ceil(answers_count / ANSWERS_PER_PAGE)}'
#                 + f'#{answer.id}'
#             )

@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def answer(request, question_id):
    question = Question.objects.get_question(question_id)
    answer_form = AnswerForm(request.user, question, request.POST)
    if answer_form.is_valid():
        answer = answer_form.save()
        answers_count = Answer.objects.filter(question=question).count()

        # Убедитесь, что ответы обновляются без Centrifugo
        return redirect(
            reverse('question', kwargs={'question_id': question_id})
            + f'?page={math.ceil(answers_count / ANSWERS_PER_PAGE)}'
            + f'#{answer.id}'
        )
    else:
        # Если форма не валидна, вернуть ту же страницу с ошибками формы
        return render(request, 'question_detail.html', {
            'question': question,
            'form': answer_form,
        })


# @login_required(login_url='login', redirect_field_name='continue')
# @require_POST
# @csrf_protect
# def correct(request):
#     body = json.loads(request.body)
#
#     correct_form = CorrectForm(body)
#     if correct_form.is_valid():
#         answer = correct_form.save()
#         body['is_correct'] = answer.is_correct
#         return JsonResponse(body)
#
#     body['is_correct'] = False
#     return JsonResponse(body)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .forms import CorrectForm

@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def correct(request):
    body = json.loads(request.body)
    correct_form = CorrectForm(request.user, body)
    if correct_form.is_valid():
        answer = correct_form.save()
        body['is_correct'] = answer.is_correct
        return JsonResponse(body)

    body['is_correct'] = False
    return JsonResponse(body)






@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def vote(request):
    body = json.loads(request.body)

    vote_form = VoteForm(request.user, body)
    if vote_form.is_valid():
        rating = vote_form.save()
        body['rating'] = rating
        return JsonResponse(body)

    body['rating'] = 0
    return JsonResponse(body)


@csrf_protect
def signup(request):
    signup_form = SignupForm()
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))

    context = {
        'form': signup_form,
        # 'pop_tags': Tag.objects.get_pop_tags(),
        # 'best_members': Profile.objects.get_best_profiles(),
        **get_top_lists(),
    }

    return render(request, 'signup.html', context)


from django.shortcuts import render, redirect


@csrf_protect
def register(request):
    register_form = SignupForm()
    if request.method == 'POST':
        register_form = SignupForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))

    context = {
        'form': register_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'register.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             login(request, user)
#             return redirect('home')  # или другая страница после успешной регистрации
#     else:
#         form = RegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})
#


def questions_by_tag(request, tag_name):
    questions = list(Question.objects.questions_by_tag(tag_name))
    page_obj = paginate(questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
        'tag_name': tag_name,
    }

    return render(request, 'tag.html', context)
    # return render(request, 'tag_page.html', context)


# @login_required(login_url='login', redirect_field_name='continue')
# @require_http_methods(['GET', 'POST'])
# @csrf_protect
# def profile(request):
#     profile_form = ProfileForm(initial=model_to_dict(request.user))
#     if request.method == 'POST':
#         profile_form = ProfileForm(request.POST, files=request.FILES, instance=request.user)
#         if profile_form.is_valid():
#             profile_form.save()
#             return redirect(reverse('profile'))
#
#     context = {
#         'form': profile_form,
#         'pop_tags': Tag.objects.get_pop_tags(),
#         'best_members': Profile.objects.get_best_profiles(),
#     }
#
#     return render(request, 'profile.html', context)

@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def profile(request):
    profile_form = ProfileForm(request.user, initial={
        'username': request.user.username,
        'email': request.user.email,
    })
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.user,
            request.POST,
            files=request.FILES,
            instance=request.user
        )
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('settings'))

    context = {
        'form': profile_form,
        **get_top_lists(),
    }

    return render(request, 'settings.html', context)


#
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import UserSettingsForm
#
# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('settings')  # перенаправление на страницу профиля или другую страницу
#     else:
#         form = UserSettingsForm(instance=request.user)
#     return render(request, 'settings', {'form': form})


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .forms import UsernameChangeForm
#
# @login_required
# def change_username(request):
#     if request.method == 'POST':
#         form = UsernameChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your username has been updated!')
#             return redirect('profile')  # перенаправление на страницу профиля или другую страницу
#     else:
#         form = UsernameChangeForm(instance=request.user)
#     return render(request, 'change_username.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


@login_required
def profile_settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(user, request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_settings')
    else:
        form = ProfileForm(user, instance=user)

    return render(request, 'settings.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import AskForm
from .models import Question


def search(request):
    query = request.GET.get('q')
    return redirect('ask_question_with_query', query=query)


def ask_question(request, query=''):
    if request.method == 'POST':
        form = AskForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                'index')  # Замените 'some_page' на URL-адрес, на который нужно перенаправить после публикации вопроса
    else:
        form = AskForm(request.user, initial={'title': query})
    return render(request, 'ask.html', {'form': form})

    context = {

        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import Question, Answer, QuestionVote, AnswerVote


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import Question, Answer, QuestionVote, AnswerVote
from .forms import VoteForm

@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def like(request, component, component_id):
    form = VoteForm(request.user, request.POST)
    if form.is_valid():
        rating = form.save(commit=True)
        return JsonResponse({'rating': rating}, status=200)
    return JsonResponse({'error': 'Invalid form data'}, status=400)

