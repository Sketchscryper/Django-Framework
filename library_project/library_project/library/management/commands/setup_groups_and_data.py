# library/management/commands/setup_groups_and_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import datetime, timedelta
from library.models import Book, Author, Reader, BorrowRecord


class Command(BaseCommand):
    help = 'Создает группы пользователей и тестовые данные'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю настройку групп и тестовых данных...')

        # 1. СОЗДАНИЕ ГРУПП И ПРАВ
        self.create_groups()

        # 2. СОЗДАНИЕ ТЕСТОВЫХ ПОЛЬЗОВАТЕЛЕЙ
        self.create_test_users()

        # 3. СОЗДАНИЕ ТЕСТОВЫХ АВТОРОВ
        self.create_authors()

        # 4. СОЗДАНИЕ ТЕСТОВЫХ КНИГ
        self.create_books()

        # 5. СОЗДАНИЕ ТЕСТОВЫХ ЧИТАТЕЛЕЙ
        self.create_readers()

        # 6. СОЗДАНИЕ ТЕСТОВЫХ ЗАПИСЕЙ О ВЫДАЧЕ
        self.create_borrow_records()

        self.stdout.write(self.style.SUCCESS('✅ Все данные успешно созданы!'))

    def create_groups(self):
        # Получаем все модели в приложении
        models = [Book, Author, Reader]

        # ГРУППА БИБЛИОТЕКАРЬ (только просмотр)
        librarian_group, created = Group.objects.get_or_create(name='Библиотекарь')
        if created:
            self.stdout.write('  📚 Создана группа "Библиотекарь"')

        # Назначаем права только на просмотр
        view_permissions = []
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__startswith='view_'
            )
            view_permissions.extend(permissions)

        librarian_group.permissions.set(view_permissions)
        self.stdout.write(f'  ✓ Группе "Библиотекарь" выданы права на просмотр ({len(view_permissions)} прав)')

        # ГРУППА АДМИНИСТРАТОР (полные права)
        admin_group, created = Group.objects.get_or_create(name='Администратор')
        if created:
            self.stdout.write('  🔧 Создана группа "Администратор"')

        # Назначаем все права
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)
        self.stdout.write(f'  ✓ Группе "Администратор" выданы все права ({all_permissions.count()} прав)')

    def create_test_users(self):
        # Создаем суперпользователя (автоматически администратор)
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@library.com',
                password='admin123',
                first_name='Администратор',
                last_name='Системы'
            )
            self.stdout.write('  👑 Создан суперпользователь: admin (пароль: admin123)')

        # Создаем пользователя-библиотекаря
        if not User.objects.filter(username='librarian').exists():
            librarian_user = User.objects.create_user(
                username='librarian',
                email='librarian@library.com',
                password='librarian123',
                first_name='Мария',
                last_name='Иванова'
            )
            # Добавляем в группу Библиотекарь
            librarian_group = Group.objects.get(name='Библиотекарь')
            librarian_user.groups.add(librarian_group)
            self.stdout.write('  📖 Создан библиотекарь: librarian (пароль: librarian123)')

        # Создаем пользователя-администратора (не суперпользователь, но с правами)
        if not User.objects.filter(username='library_admin').exists():
            admin_user = User.objects.create_user(
                username='library_admin',
                email='library_admin@library.com',
                password='admin456',
                first_name='Петр',
                last_name='Сидоров'
            )
            # Добавляем в группу Администратор
            admin_group = Group.objects.get(name='Администратор')
            admin_user.groups.add(admin_group)
            self.stdout.write('  🔐 Создан администратор: library_admin (пароль: admin456)')

        # Создаем обычного пользователя (читатель)
        if not User.objects.filter(username='reader_user').exists():
            reader_user = User.objects.create_user(
                username='reader_user',
                email='reader@example.com',
                password='reader123',
                first_name='Анна',
                last_name='Петрова'
            )
            self.stdout.write('  👤 Создан обычный пользователь: reader_user (пароль: reader123)')

    def create_authors(self):
        authors_data = [
            {
                'first_name': 'Федор',
                'last_name': 'Достоевский',
                'birth_date': datetime(1821, 11, 11).date(),
                'bio': 'Великий русский писатель, мыслитель, философ и публицист. Классик мировой литературы.'
            },
            {
                'first_name': 'Лев',
                'last_name': 'Толстой',
                'birth_date': datetime(1828, 9, 9).date(),
                'bio': 'Один из наиболее известных русских писателей и мыслителей, один из величайших писателей-романистов мира.'
            },
            {
                'first_name': 'Антон',
                'last_name': 'Чехов',
                'birth_date': datetime(1860, 1, 29).date(),
                'bio': 'Русский писатель, прозаик, драматург, публицист, врач. Классик мировой литературы.'
            },
            {
                'first_name': 'Михаил',
                'last_name': 'Булгаков',
                'birth_date': datetime(1891, 5, 15).date(),
                'bio': 'Русский писатель советского периода, врач, драматург, театральный режиссёр и актёр.'
            },
            {
                'first_name': 'Александр',
                'last_name': 'Пушкин',
                'birth_date': datetime(1799, 6, 6).date(),
                'bio': 'Русский поэт, драматург и прозаик, заложивший основы русского реалистического направления.'
            },
            {
                'first_name': 'Джордж',
                'last_name': 'Оруэлл',
                'birth_date': datetime(1903, 6, 25).date(),
                'bio': 'Британский писатель и публицист, автор культовых романов "1984" и "Скотный двор".'
            },
            {
                'first_name': 'Джейн',
                'last_name': 'Остин',
                'birth_date': datetime(1775, 12, 16).date(),
                'bio': 'Английская писательница, автор классических романов о любви и нравах.'
            }
        ]

        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                first_name=author_data['first_name'],
                last_name=author_data['last_name'],
                defaults=author_data
            )
            if created:
                self.stdout.write(f'  ✍️ Создан автор: {author.first_name} {author.last_name}')

    def create_books(self):
        books_data = [
            {
                'title': 'Преступление и наказание',
                'author_first': 'Федор',
                'author_last': 'Достоевский',
                'isbn': '9785170917642',
                'publication_year': 1866,
                'description': 'Роман об убийстве и моральных страданиях главного героя.',
                'total_copies': 5,
                'available_copies': 3
            },
            {
                'title': 'Война и мир',
                'author_first': 'Лев',
                'author_last': 'Толстой',
                'isbn': '9785170917659',
                'publication_year': 1869,
                'description': 'Масштабный роман-эпопея о жизни русского общества в эпоху наполеоновских войн.',
                'total_copies': 8,
                'available_copies': 5
            },
            {
                'title': 'Анна Каренина',
                'author_first': 'Лев',
                'author_last': 'Толстой',
                'isbn': '9785170917666',
                'publication_year': 1877,
                'description': 'Трагическая история любви замужней женщины.',
                'total_copies': 4,
                'available_copies': 2
            },
            {
                'title': 'Чайка',
                'author_first': 'Антон',
                'author_last': 'Чехов',
                'isbn': '9785170917673',
                'publication_year': 1895,
                'description': 'Комедия в четырёх действиях о творчестве и любви.',
                'total_copies': 3,
                'available_copies': 3
            },
            {
                'title': 'Мастер и Маргарита',
                'author_first': 'Михаил',
                'author_last': 'Булгаков',
                'isbn': '9785170917680',
                'publication_year': 1967,
                'description': 'Мистический роман о дьяволе, любви и творчестве.',
                'total_copies': 6,
                'available_copies': 4
            },
            {
                'title': 'Евгений Онегин',
                'author_first': 'Александр',
                'author_last': 'Пушкин',
                'isbn': '9785170917697',
                'publication_year': 1833,
                'description': 'Роман в стихах о судьбе "лишнего человека".',
                'total_copies': 7,
                'available_copies': 6
            },
            {
                'title': '1984',
                'author_first': 'Джордж',
                'author_last': 'Оруэлл',
                'isbn': '9785170917703',
                'publication_year': 1949,
                'description': 'Антиутопия о тотальном контроле и подавлении личности.',
                'total_copies': 5,
                'available_copies': 2
            },
            {
                'title': 'Гордость и предубеждение',
                'author_first': 'Джейн',
                'author_last': 'Остин',
                'isbn': '9785170917710',
                'publication_year': 1813,
                'description': 'Классический роман о любви и социальных нормах.',
                'total_copies': 4,
                'available_copies': 4
            }
        ]

        for book_data in books_data:
            author = Author.objects.get(
                first_name=book_data['author_first'],
                last_name=book_data['author_last']
            )
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    'title': book_data['title'],
                    'author': author,
                    'publication_year': book_data['publication_year'],
                    'description': book_data['description'],
                    'total_copies': book_data['total_copies'],
                    'available_copies': book_data['available_copies']
                }
            )
            if created:
                self.stdout.write(f'  📖 Создана книга: {book.title}')

    def create_readers(self):
        readers_data = [
            {'username': 'reader_user', 'phone': '+7 (999) 123-45-67', 'address': 'ул. Пушкина, д. 10, кв. 5'},
            {'username': 'reader_user2', 'phone': '+7 (999) 234-56-78', 'address': 'ул. Лермонтова, д. 15, кв. 12'},
        ]

        # Создаем второго пользователя если его нет
        if not User.objects.filter(username='reader_user2').exists():
            User.objects.create_user(
                username='reader_user2',
                email='reader2@example.com',
                password='reader456',
                first_name='Сергей',
                last_name='Волков'
            )
            self.stdout.write('  👤 Создан пользователь: reader_user2 (пароль: reader456)')

        for reader_data in readers_data:
            user = User.objects.get(username=reader_data['username'])
            reader, created = Reader.objects.get_or_create(
                user=user,
                defaults={
                    'phone': reader_data['phone'],
                    'address': reader_data['address']
                }
            )
            if created:
                self.stdout.write(f'  👥 Создан читатель: {user.get_full_name() or user.username}')

    def create_borrow_records(self):
        # Создаем несколько записей о выдаче книг
        books = Book.objects.all()
        readers = Reader.objects.all()

        if readers.exists() and books.exists():
            # Берем первую книгу и первого читателя
            book = books.first()
            reader = readers.first()

            borrow_record, created = BorrowRecord.objects.get_or_create(
                book=book,
                reader=reader,
                is_returned=False,
                defaults={
                    'due_date': timezone.now() + timedelta(days=14),
                    'borrow_date': timezone.now() - timedelta(days=5)
                }
            )
            if created:
                self.stdout.write(f'  📅 Создана запись о выдаче: {book.title} -> {reader.user.username}')

            # Добавляем еще одну запись для второй книги
            if books.count() > 1:
                book2 = books[1]
                borrow_record2, created = BorrowRecord.objects.get_or_create(
                    book=book2,
                    reader=reader,
                    is_returned=True,
                    defaults={
                        'due_date': timezone.now() - timedelta(days=7),
                        'borrow_date': timezone.now() - timedelta(days=21),
                        'return_date': timezone.now() - timedelta(days=5)
                    }
                )
                if created:
                    self.stdout.write(f'  📅 Создана запись о возврате: {book2.title} -> {reader.user.username}')