from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('hot/', views.hot, name='hot'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('login/', views.login, name='login'),
    # path('login/', views.logout, name='logout'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register'),

    path('questions/<int:question_id>', views.question, name='question'),
    path('question/<int:question_id>/answer', views.answer, name='answer'),
    path('answer/correct', views.correct, name='correct'),
    path('tags/<tag_name>', views.tag, name='tag'),
    path('404/', views.oops_404, name='oops'),

    path('ask/', views.ask_question, name='ask_question'),
    path('search/', views.search, name='search'),
    path('ask/<str:query>/', views.ask_question, name='ask_question_with_query'),
    path('like/<str:component>/<int:component_id>/', views.like, name='like'),
    path('correct/', views.correct, name='correct'),
]
