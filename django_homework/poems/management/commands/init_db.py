from django.core.management.base import BaseCommand
from poems.models import Author, Poem

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


class Command(BaseCommand):
    help = 'Инициализирует базу данных стихами'

    def handle(self, *args, **options):
        self.stdout.write('Заполняем базу данных...')

        for poem_data in INITIAL_POEMS:
            author, created = Author.objects.get_or_create(name=poem_data['author'])
            poem, created = Poem.objects.get_or_create(
                title=poem_data['title'],
                author=author,
                defaults={
                    'topic': poem_data['topic'],
                    'text': poem_data['text']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Добавлен стих: {poem.title}'))

        self.stdout.write(self.style.SUCCESS('✅ База данных заполнена!'))