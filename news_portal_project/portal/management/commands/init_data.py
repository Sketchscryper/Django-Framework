from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portal.models import Article, Comment, SiteSettings

class Command(BaseCommand):
    help = 'Создает тестовые данные'

    def handle(self, *args, **options):
        # Создаем админа
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        admin.set_password('admin123')
        admin.save()
        self.stdout.write('Админ создан: admin / admin123')

        # Создаем тестового пользователя
        user, _ = User.objects.get_or_create(
            username='user',
            defaults={'email': 'user@example.com'}
        )
        user.set_password('user123')
        user.save()
        self.stdout.write('Пользователь создан: user / user123')

        # Создаем статьи
        articles_data = [
            ('Открытие нового парка', 'news', 'Сегодня состоялось торжественное открытие нового городского парка. На мероприятии присутствовал мэр города.'),
            ('Изменение расписания автобусов', 'news', 'С 1 января меняется расписание городских автобусов. Будьте внимательны!'),
            ('Как выбрать профессию', 'article', 'Советы по выбору будущей профессии для школьников и студентов.'),
            ('Секреты здорового сна', 'article', 'Почему важно высыпаться и как улучшить качество сна.'),
            ('Новый год в городе', 'news', 'Праздничная программа на Новый год будет проходить на главной площади.'),
        ]

        for title, art_type, content in articles_data:
            article, created = Article.objects.get_or_create(
                title=title,
                defaults={
                    'content': content,
                    'article_type': art_type,
                    'author': admin,
                    'is_published': True
                }
            )
            if created:
                self.stdout.write(f'Создана статья: {title}')

        # Создаем настройки
        SiteSettings.objects.get_or_create(id=1)
        self.stdout.write(self.style.SUCCESS('✅ Данные созданы!'))