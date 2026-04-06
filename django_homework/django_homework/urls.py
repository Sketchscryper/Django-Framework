from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Функция для главной страницы (справочник по API)
def home(request):
    return JsonResponse({
        'message': 'Добро пожаловать в API домашнего задания по Django!',
        'available_endpoints': {
            'Задание 1 - Предсказания': {
                'random_prediction': '/api/prediction/'
            },
            'Задание 2 - Случайные числа': {
                'random_number_default': '/api/random/',
                'random_number_in_range': '/api/random/10/50/',
                'random_number_with_params': '/api/random/?min=1&max=20',
                'random_list': '/api/random-list/5/',
                'random_list_with_range': '/api/random-list/5/?min=10&max=50'
            },
            'Задание 3 - Случайные стихи': {
                'random_poem': '/api/poem/random/',
                'random_poem_by_author': '/api/poem/author/Пушкин/',
                'random_poem_by_topic': '/api/poem/topic/любовь/'
            },
            'Задание 4 - Списки': {
                'all_authors': '/api/poem/authors/',
                'all_topics': '/api/poem/topics/',
                'author_titles': '/api/poem/author/Лермонтов/titles/',
                'topic_titles': '/api/poem/topic/свобода/titles/'
            }
        },
        'example_requests': {
            'curl_prediction': 'curl http://127.0.0.1:8000/api/prediction/',
            'curl_random': 'curl http://127.0.0.1:8000/api/random/1/100/',
            'curl_poem': 'curl http://127.0.0.1:8000/api/poem/random/'
        }
    }, json_dumps_params={'ensure_ascii': False, 'indent': 2})

urlpatterns = [
    path('', home, name='home'),  # Главная страница - теперь будет работать
    path('admin/', admin.site.urls),
    path('api/', include('predictions.urls')),
    path('api/', include('poems.urls')),
]

