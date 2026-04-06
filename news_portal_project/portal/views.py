from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from .models import Article, Comment, SavedArticle, BannedUser, SiteSettings
from .forms import ArticleForm, CommentForm, SiteSettingsForm, BanUserForm, AddUserForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


# ============ ОСНОВНЫЕ СТРАНИЦЫ ============

def index(request):
    """Главная страница"""
    articles = Article.objects.filter(is_published=True).order_by('-created_at')

    # Фильтрация по типу
    type_filter = request.GET.get('type', 'all')
    if type_filter == 'news':
        articles = articles.filter(article_type='news')
    elif type_filter == 'article':
        articles = articles.filter(article_type='article')

    return render(request, 'portal/index.html', {
        'articles': articles,
        'current_type': type_filter,
    })


def article_detail(request, article_id):
    """Детальная страница статьи"""
    article = get_object_or_404(Article, id=article_id, is_published=True)
    article.increment_views()

    comments = Comment.objects.filter(article=article, is_active=True)

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()

    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedArticle.objects.filter(user=request.user, article=article).exists()

    return render(request, 'portal/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'is_saved': is_saved,
    })


@login_required
def save_article(request, article_id):
    """Сохранить статью"""
    article = get_object_or_404(Article, id=article_id)
    saved, created = SavedArticle.objects.get_or_create(user=request.user, article=article)
    if created:
        article.increment_saves()
        messages.success(request, 'Статья сохранена!')
    else:
        messages.info(request, 'Вы уже сохранили эту статью')
    return redirect('article_detail', article_id=article.id)


# ============ АДМИНИСТРАТИВНЫЕ СТРАНИЦЫ ============

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Панель администратора"""
    context = {
        'total_articles': Article.objects.count(),
        'total_users': User.objects.count(),
        'total_comments': Comment.objects.count(),
        'banned_users': BannedUser.objects.filter(is_active=True).count(),
        'recent_articles': Article.objects.order_by('-created_at')[:5],
        'recent_users': User.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'portal/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def article_create(request):
    """Создание статьи"""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Статья создана!')
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm()
    return render(request, 'portal/article_form.html', {'form': form, 'title': 'Создать статью'})


@login_required
@user_passes_test(is_admin)
def article_edit(request, article_id):
    """Редактирование статьи"""
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья обновлена!')
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'portal/article_form.html', {'form': form, 'title': 'Редактировать статью'})


@login_required
@user_passes_test(is_admin)
def article_delete(request, article_id):
    """Удаление статьи"""
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена!')
        return redirect('index')
    return render(request, 'portal/article_confirm_delete.html', {'article': article})


@login_required
@user_passes_test(is_admin)
def user_list(request):
    """Список пользователей"""
    users = User.objects.all().order_by('-date_joined')
    search = request.GET.get('search', '')
    if search:
        users = users.filter(Q(username__icontains=search) | Q(email__icontains=search))

    # Проверяем баны
    for user in users:
        user.active_ban = BannedUser.objects.filter(user=user, is_active=True).first()
        if user.active_ban and user.active_ban.is_expired():
            user.active_ban.is_active = False
            user.active_ban.save()
            user.active_ban = None

    return render(request, 'portal/user_list.html', {'users': users, 'search': search})


@login_required
@user_passes_test(is_admin)
def user_add(request):
    """Добавление пользователя"""
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Пользователь {user.username} создан!')
            return redirect('user_list')
    else:
        form = AddUserForm()
    return render(request, 'portal/user_form.html', {'form': form, 'title': 'Добавить пользователя'})


@login_required
@user_passes_test(is_admin)
def user_delete(request, user_id):
    """Удаление пользователя"""
    user_to_delete = get_object_or_404(User, id=user_id)
    if user_to_delete == request.user:
        messages.error(request, 'Нельзя удалить самого себя!')
        return redirect('user_list')

    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'Пользователь {username} удален!')
        return redirect('user_list')

    return render(request, 'portal/user_confirm_delete.html', {'user_to_delete': user_to_delete})


@login_required
@user_passes_test(is_admin)
def user_ban(request, user_id):
    """Бан пользователя"""
    user_to_ban = get_object_or_404(User, id=user_id)

    if user_to_ban == request.user:
        messages.error(request, 'Нельзя забанить себя!')
        return redirect('user_list')

    if user_to_ban.is_staff:
        messages.error(request, 'Нельзя банить администратора!')
        return redirect('user_list')

    if request.method == 'POST':
        form = BanUserForm(request.POST)
        if form.is_valid():
            BannedUser.objects.filter(user=user_to_ban, is_active=True).update(is_active=False)
            ban = BannedUser(
                user=user_to_ban,
                banned_by=request.user,
                duration=form.cleaned_data['duration'],
                reason=form.cleaned_data['reason']
            )
            ban.save()
            messages.success(request, f'Пользователь {user_to_ban.username} забанен!')
            return redirect('user_list')
    else:
        form = BanUserForm()

    return render(request, 'portal/user_ban.html', {'user': user_to_ban, 'form': form})


@login_required
@user_passes_test(is_admin)
def user_unban(request, user_id):
    """Разбан пользователя"""
    user_to_unban = get_object_or_404(User, id=user_id)
    BannedUser.objects.filter(user=user_to_unban, is_active=True).update(is_active=False)
    messages.success(request, f'Пользователь {user_to_unban.username} разбанен!')
    return redirect('user_list')


@login_required
@user_passes_test(is_admin)
def comment_delete(request, comment_id):
    """Удаление комментария"""
    comment = get_object_or_404(Comment, id=comment_id)
    article_id = comment.article.id
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удален!')
        return redirect('article_detail', article_id=article_id)
    return render(request, 'portal/comment_confirm_delete.html', {'comment': comment})


@login_required
@user_passes_test(is_admin)
def site_settings_view(request):
    """Настройки сайта"""
    settings, created = SiteSettings.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Настройки сохранены!')
            return redirect('site_settings')
    else:
        form = SiteSettingsForm(instance=settings)
    return render(request, 'portal/site_settings.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def statistics_view(request):
    """Статистика"""
    top_by_views = Article.objects.filter(is_published=True).order_by('-views_count')[:10]
    top_by_comments = Article.objects.filter(is_published=True).annotate(
        comment_count=Count('comments')
    ).order_by('-comment_count')[:10]
    top_by_saves = Article.objects.filter(is_published=True).order_by('-saves_count')[:10]

    context = {
        'top_by_views': top_by_views,
        'top_by_comments': top_by_comments,
        'top_by_saves': top_by_saves,
        'total_articles': Article.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_users': User.objects.count(),
        'total_views': sum(a.views_count for a in Article.objects.all()),
    }
    return render(request, 'portal/statistics.html', context)

def custom_logout(request):
    """Выход из системы"""
    logout(request)
    return redirect('/')