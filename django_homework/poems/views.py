import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Poem

# БАЗА ДАННЫХ СТИХОВ (для инициализации)
INITIAL_POEMS = [
    {'title': 'Я вас любил', 'author': 'Александр Пушкин', 'topic': 'любовь',
     'text': 'Я вас любил: любовь еще, быть может,\nВ душе моей угасла не совсем;\nНо пусть она вас больше не тревожит;\nЯ не хочу печалить вас ничем.'},
    {'title': 'Узник', 'author': 'Александр Пушкин', 'topic': 'свобода',
     'text': 'Сижу за решеткой в темнице сырой.\nВскормленный в неволе орел молодой,\nМой грустный товарищ, махая крылом,\nКровавую пищу клюет под окном.'},
    {'title': 'Парус', 'author': 'Михаил Лермонтов', 'topic': 'свобода',
     'text': 'Белеет парус одинокой\nВ тумане моря голубом!\nЧто ищет он в стране далекой?\nЧто кинул он в краю родном?..'},
    {'title': 'Смерть поэта', 'author': 'Михаил Лермонтов', 'topic': 'творчество',
     'text': 'Погиб поэт! — невольник чести —\nПал, оклеветанный молвой,\nС свинцом в груди и жаждой мести,\nПоникнув гордой головой!..'},
    {'title': 'Выхожу один я на дорогу', 'author': 'Михаил Лермонтов', 'topic': 'жизнь',
     'text': 'Выхожу один я на дорогу;\nСквозь туман кремнистый путь блестит;\nНочь тиха. Пустыня внемлет богу,\nИ звезда с звездою говорит.'},
    {'title': 'К морю', 'author': 'Александр Пушкин', 'topic': 'природа',
     'text': 'Прощай, свободная стихия!\nВ последний раз передо мной\nТы катишь волны голубые\nИ блещешь гордою красой.'},
]

# ЗАДАНИЕ 3: Случайный стих
@api_view(['GET'])
def random_poem(request):
    """Возвращает случайный стих"""
    poems = Poem.objects.all()
    if not poems:
        return Response({'error': 'Нет стихов в базе'}, status=status.HTTP_404_NOT_FOUND)
    poem = random.choice(list(poems))
    return Response({
        'id': poem.id,
        'title': poem.title,
        'author': poem.author.name,
        'topic': poem.topic,
        'text': poem.text
    })

# ЗАДАНИЕ 3: Случайный стих автора
@api_view(['GET'])
def random_poem_by_author(request, author_name):
    """Возвращает случайный стих указанного автора"""
    try:
        author = Author.objects.get(name__icontains=author_name)
        poems = Poem.objects.filter(author=author)
        if not poems:
            return Response({'error': f'У автора {author_name} нет стихов'}, status=status.HTTP_404_NOT_FOUND)
        poem = random.choice(list(poems))
        return Response({
            'id': poem.id,
            'title': poem.title,
            'author': poem.author.name,
            'topic': poem.topic,
            'text': poem.text
        })
    except Author.DoesNotExist:
        return Response({'error': f'Автор {author_name} не найден'}, status=status.HTTP_404_NOT_FOUND)

# ЗАДАНИЕ 3: Случайный стих по теме
@api_view(['GET'])
def random_poem_by_topic(request, topic):
    """Возвращает случайный стих по тематике"""
    poems = Poem.objects.filter(topic__icontains=topic)
    if not poems:
        return Response({'error': f'Стихов на тему {topic} не найдено'}, status=status.HTTP_404_NOT_FOUND)
    poem = random.choice(list(poems))
    return Response({
        'id': poem.id,
        'title': poem.title,
        'author': poem.author.name,
        'topic': poem.topic,
        'text': poem.text
    })

# ЗАДАНИЕ 4: Список всех авторов
@api_view(['GET'])
def authors_list(request):
    """Возвращает список всех авторов"""
    authors = Author.objects.all()
    return Response({
        'authors': [{'id': a.id, 'name': a.name, 'poems_count': a.poems.count()} for a in authors]
    })

# ЗАДАНИЕ 4: Список всех тематик
@api_view(['GET'])
def topics_list(request):
    """Возвращает список всех тематик"""
    topics = Poem.objects.values_list('topic', flat=True).distinct()
    topics = [t for t in topics if t]  # убираем пустые
    return Response({'topics': topics})

# ЗАДАНИЕ 4: Названия стихов автора
@api_view(['GET'])
def author_titles(request, author_name):
    """Возвращает список названий стихов автора"""
    try:
        author = Author.objects.get(name__icontains=author_name)
        titles = Poem.objects.filter(author=author).values_list('title', flat=True)
        return Response({
            'author': author.name,
            'titles': list(titles),
            'count': len(titles)
        })
    except Author.DoesNotExist:
        return Response({'error': f'Автор {author_name} не найден'}, status=status.HTTP_404_NOT_FOUND)

# ЗАДАНИЕ 4: Названия стихов по теме
@api_view(['GET'])
def topic_titles(request, topic):
    """Возвращает список названий стихов по теме"""
    poems = Poem.objects.filter(topic__icontains=topic)
    titles = poems.values_list('title', flat=True)
    return Response({
        'topic': topic,
        'titles': list(titles),
        'count': len(titles)
    })
