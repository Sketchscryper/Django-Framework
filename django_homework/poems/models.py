from django.db import models


class Author(models.Model):
    """Модель автора"""
    name = models.CharField(max_length=200, verbose_name='Имя автора')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Poem(models.Model):
    """Модель стихотворения"""
    title = models.CharField(max_length=300, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='poems', verbose_name='Автор')
    topic = models.CharField(max_length=100, blank=True, verbose_name='Тематика')
    text = models.TextField(verbose_name='Текст стиха')

    def __str__(self):
        return f'"{self.title}" - {self.author.name}'

    class Meta:
        verbose_name = 'Стихотворение'
        verbose_name_plural = 'Стихотворения'
