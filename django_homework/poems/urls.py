from django.urls import path
from . import views

urlpatterns = [
    # Задание 3: случайные стихи
    path('poem/random/', views.random_poem, name='random_poem'),
    path('poem/author/<str:author_name>/', views.random_poem_by_author, name='poem_by_author'),
    path('poem/topic/<str:topic>/', views.random_poem_by_topic, name='poem_by_topic'),

    # Задание 4: списки
    path('poem/authors/', views.authors_list, name='authors_list'),
    path('poem/topics/', views.topics_list, name='topics_list'),
    path('poem/author/<str:author_name>/titles/', views.author_titles, name='author_titles'),
    path('poem/topic/<str:topic>/titles/', views.topic_titles, name='topic_titles'),
]