# library/views.py - ПОЛНАЯ ВЕРСИЯ

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Book, Author, Reader
from .forms import BookForm, AuthorForm, ReaderForm, ReaderCreationForm


# Функции проверки прав доступа
def is_librarian(user):
    """Библиотекарь может просматривать"""
    return user.is_authenticated and (user.groups.filter(name='Библиотекарь').exists() or user.is_superuser)


def is_admin(user):
    """Администратор может делать все"""
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Администратор').exists())


def can_view(request):
    """Проверка на возможность просмотра"""
    return request.user.is_authenticated and (is_librarian(request.user) or is_admin(request.user))


def can_edit(request):
    """Проверка на возможность редактирования"""
    return request.user.is_authenticated and is_admin(request.user)


# Аутентификация
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('library:home')
    else:
        form = UserCreationForm()
    return render(request, 'library/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Сообщение о роли пользователя
                if user.is_superuser:
                    messages.success(request, f'Добро пожаловать, Администратор {username}!')
                elif user.groups.filter(name='Администратор').exists():
                    messages.success(request, f'Добро пожаловать, Администратор {username}!')
                elif user.groups.filter(name='Библиотекарь').exists():
                    messages.success(request, f'Добро пожаловать, Библиотекарь {username}!')
                else:
                    messages.success(request, f'Добро пожаловать, {username}!')

                return redirect('library:home')
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('library:home')


# ГЛАВНАЯ СТРАНИЦА (home_view)
def home_view(request):
    """Главная страница библиотеки"""
    books_count = Book.objects.count()
    authors_count = Author.objects.count()
    readers_count = Reader.objects.count()

    # Показываем роль пользователя
    user_role = "Гость"
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name='Администратор').exists():
            user_role = "Администратор"
        elif request.user.groups.filter(name='Библиотекарь').exists():
            user_role = "Библиотекарь"
        else:
            user_role = "Читатель"

    context = {
        'books_count': books_count,
        'authors_count': authors_count,
        'readers_count': readers_count,
        'user_role': user_role,
    }
    return render(request, 'library/home.html', context)


# CRUD для книг
def book_list_view(request):
    books = Book.objects.select_related('author').all()
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'library/book_list.html', {'page_obj': page_obj})


def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})


@login_required
@user_passes_test(is_admin)
def book_create_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно добавлена!')
            return redirect('library:book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Добавить книгу'})


@login_required
@user_passes_test(is_admin)
def book_edit_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно обновлена!')
            return redirect('library:book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Редактировать книгу'})


@login_required
@user_passes_test(is_admin)
def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Книга успешно удалена!')
        return redirect('library:book_list')
    return render(request, 'library/book_confirm_delete.html', {'object': book})


# CRUD для авторов
def author_list_view(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'library/author_list.html', {'page_obj': page_obj})


def author_detail_view(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'library/author_detail.html', {'author': author})


@login_required
@user_passes_test(is_admin)
def author_create_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автор успешно добавлен!')
            return redirect('library:author_list')
    else:
        form = AuthorForm()
    return render(request, 'library/author_form.html', {'form': form, 'title': 'Добавить автора'})


@login_required
@user_passes_test(is_admin)
def author_edit_view(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автор успешно обновлен!')
            return redirect('library:author_detail', pk=author.pk)
    else:
        form = AuthorForm(instance=author)
    return render(request, 'library/author_form.html', {'form': form, 'title': 'Редактировать автора'})


@login_required
@user_passes_test(is_admin)
def author_delete_view(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        messages.success(request, 'Автор успешно удален!')
        return redirect('library:author_list')
    return render(request, 'library/author_confirm_delete.html', {'object': author})


# CRUD для читателей
def reader_list_view(request):
    readers = Reader.objects.select_related('user').all()
    paginator = Paginator(readers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'library/reader_list.html', {'page_obj': page_obj})


def reader_detail_view(request, pk):
    reader = get_object_or_404(Reader, pk=pk)
    return render(request, 'library/reader_detail.html', {'reader': reader})


@login_required
@user_passes_test(is_admin)
def reader_create_view(request):
    """Создание нового читателя (пользователя) администратором"""
    if request.method == 'POST':
        form = ReaderCreationForm(request.POST)
        if form.is_valid():
            # Создаем нового пользователя
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Создаем профиль читателя
            reader = Reader.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )

            messages.success(request, f'Читатель {user.username} успешно добавлен!')
            return redirect('library:reader_detail', pk=reader.pk)
    else:
        form = ReaderCreationForm()

    return render(request, 'library/reader_create.html', {'form': form, 'title': 'Добавить нового читателя'})


@login_required
@user_passes_test(is_admin)
def reader_edit_view(request, pk):
    """Редактирование информации о читателе"""
    reader = get_object_or_404(Reader, pk=pk)

    if request.method == 'POST':
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о читателе успешно обновлена!')
            return redirect('library:reader_detail', pk=reader.pk)
    else:
        form = ReaderForm(instance=reader)

    return render(request, 'library/reader_form.html', {
        'form': form,
        'title': f'Редактировать читателя: {reader.user.get_full_name() or reader.user.username}',
        'reader': reader
    })


@login_required
@user_passes_test(is_admin)
def reader_delete_view(request, pk):
    """Удаление читателя"""
    reader = get_object_or_404(Reader, pk=pk)
    username = reader.user.username

    if request.method == 'POST':
        # Удаляем пользователя (читатель удалится каскадно)
        reader.user.delete()
        messages.success(request, f'Читатель {username} успешно удален!')
        return redirect('library:reader_list')

    return render(request, 'library/reader_confirm_delete.html', {'object': reader})


@login_required
@user_passes_test(is_admin)
def reset_password_view(request, pk):
    """Сброс пароля читателя администратором"""
    reader = get_object_or_404(Reader, pk=pk)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')

        if not new_password:
            # Генерируем случайный пароль
            import random
            import string
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        reader.user.set_password(new_password)
        reader.user.save()

        messages.success(request, f'Пароль для пользователя {reader.user.username} изменен на: {new_password}')
        return redirect('library:reader_detail', pk=reader.pk)

    return redirect('library:reader_detail', pk=reader.pk)