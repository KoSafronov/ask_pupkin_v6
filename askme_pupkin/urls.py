"""
URL configuration for askme_pupkin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('', include('app.urls'), name='index'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    # path('hot/', views.hot, name='hot_questions'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('question/<int:question_id>', views.question, name='question'),
    path('question/<int:question_id>/answer', views.answer, name='answer'),
    path('answer/correct', views.correct, name='correct'),
    path('vote/', views.vote, name='vote'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('login/', views.logout, name='logout'),
    # path('new/', views.index, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('tag/<tag_name>/', views.questions_by_tag, name='tag'),
    path('profile/edit', views.profile, name='profile'),
    # path('uploads/', views.static, name="static"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += [
#     path('login/', 'django.contrib.auth.views.login'),
#     path('logout/', 'django.contrib.auth.views.logout'),
# ]
