from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Article(models.Model):
    """Статья/новость"""
    TYPE_CHOICES = [
        ('news', 'Новость'),
        ('article', 'Статья'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    article_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='news', verbose_name='Тип')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    saves_count = models.IntegerField(default=0, verbose_name='Сохранения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views_count += 1
        self.save()

    def increment_saves(self):
        self.saves_count += 1
        self.save()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']


class Comment(models.Model):
    """Комментарий"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f'Комментарий от {self.author.username}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']


class SavedArticle(models.Model):
    """Сохраненные статьи"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_articles', verbose_name='Пользователь')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='saved_by', verbose_name='Статья')
    saved_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата сохранения')

    class Meta:
        unique_together = ['user', 'article']
        verbose_name = 'Сохраненная статья'
        verbose_name_plural = 'Сохраненные статьи'


class BannedUser(models.Model):
    """Забаненный пользователь"""
    DURATION_CHOICES = [
        ('day', 'День'),
        ('week', 'Неделя'),
        ('month', 'Месяц'),
        ('forever', 'Навсегда'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bans', verbose_name='Пользователь')
    banned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_bans', verbose_name='Забанил')
    reason = models.TextField(blank=True, verbose_name='Причина')
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, verbose_name='Длительность')
    banned_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата бана')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Истекает')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def save(self, *args, **kwargs):
        if self.duration == 'day':
            self.expires_at = timezone.now() + timedelta(days=1)
        elif self.duration == 'week':
            self.expires_at = timezone.now() + timedelta(weeks=1)
        elif self.duration == 'month':
            self.expires_at = timezone.now() + timedelta(days=30)
        elif self.duration == 'forever':
            self.expires_at = None
        super().save(*args, **kwargs)

    def is_expired(self):
        if self.duration == 'forever':
            return False
        return timezone.now() > self.expires_at

    def __str__(self):
        return f'{self.user.username} забанен'

    class Meta:
        verbose_name = 'Забаненный пользователь'
        verbose_name_plural = 'Забаненные пользователи'


class SiteSettings(models.Model):
    """Настройки сайта"""
    background_color = models.CharField(max_length=20, default='#ffffff', verbose_name='Цвет фона')
    text_color = models.CharField(max_length=20, default='#000000', verbose_name='Цвет текста')
    font_size = models.CharField(max_length=10, default='16px', verbose_name='Размер шрифта')

    def __str__(self):
        return 'Настройки сайта'

    class Meta:
        verbose_name = 'Настройка сайта'
        verbose_name_plural = 'Настройки сайта'