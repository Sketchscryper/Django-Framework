import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# База предсказаний
PREDICTIONS = [
    "🍀 Сегодня вас ждёт удача!",
    "⭐ Звёзды благоволят вам!",
    "💫 Счастливый случай изменит вашу жизнь",
    "🎯 Ваша цель ближе, чем вы думаете",
    "🌈 Доверьтесь своей интуиции",
    "🚀 Успех придёт неожиданно",
    "💝 Вас ждёт приятная встреча",
    "📈 Финансовый успех на горизонте",
    "🎨 Ваш талант раскроется сегодня",
    "😊 Улыбнитесь — это привлечёт удачу",
]


# ЗАДАНИЕ 1: Предсказание
@api_view(['GET'])
def prediction_view(request):
    """Возвращает случайное предсказание"""
    prediction = random.choice(PREDICTIONS)
    return Response({
        'prediction': prediction,
        'id': random.randint(1000, 9999)
    })


# ЗАДАНИЕ 2: Случайное число
@api_view(['GET'])
def random_number_view(request, min_val=None, max_val=None):
    """Возвращает случайное число"""
    # Если числа не переданы в URL, берем из параметров запроса
    if min_val is None:
        min_val = int(request.GET.get('min', 0))
    if max_val is None:
        max_val = int(request.GET.get('max', 100))

    # Проверка
    if min_val >= max_val:
        return Response(
            {'error': 'min должно быть меньше max'},
            status=status.HTTP_400_BAD_REQUEST
        )

    number = random.randint(min_val, max_val)
    return Response({
        'number': number,
        'min': min_val,
        'max': max_val
    })


# ЗАДАНИЕ 2 (доп): Список случайных чисел
@api_view(['GET'])
def random_list_view(request, count):
    """Возвращает список случайных чисел"""
    try:
        count = int(count)
        min_val = int(request.GET.get('min', 0))
        max_val = int(request.GET.get('max', 100))

        if count <= 0:
            raise ValueError
        if min_val >= max_val:
            return Response(
                {'error': 'min должно быть меньше max'},
                status=status.HTTP_400_BAD_REQUEST
            )

        numbers = [random.randint(min_val, max_val) for _ in range(count)]
        return Response({
            'numbers': numbers,
            'count': count,
            'min': min_val,
            'max': max_val
        })
    except ValueError:
        return Response(
            {'error': 'count должен быть положительным числом'},
            status=status.HTTP_400_BAD_REQUEST
        )
