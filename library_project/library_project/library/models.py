# library/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    """Модель автора книги"""
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    bio = models.TextField('Биография', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Book(models.Model):
    """Модель книги"""
    title = models.CharField('Название', max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор', related_name='books')
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    publication_year = models.IntegerField('Год публикации')
    description = models.TextField('Описание', blank=True)
    total_copies = models.IntegerField('Всего экземпляров', default=1)
    available_copies = models.IntegerField('Доступно экземпляров', default=1)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Reader(models.Model):
    """Модель читателя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=20)
    address = models.CharField('Адрес', max_length=200)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'


class BorrowRecord(models.Model):
    """Модель записи о выдаче книги"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='Читатель')
    borrow_date = models.DateTimeField('Дата выдачи', auto_now_add=True)
    due_date = models.DateTimeField('Срок возврата')
    return_date = models.DateTimeField('Дата возврата', null=True, blank=True)
    is_returned = models.BooleanField('Возвращена', default=False)

    def __str__(self):
        return f"{self.book.title} - {self.reader}"

    class Meta:
        verbose_name = 'Выдача книги'
        verbose_name_plural = 'Выдачи книг'
