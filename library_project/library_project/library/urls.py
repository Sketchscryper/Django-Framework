# library/urls.py

from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Главная
    path('', views.home_view, name='home'),  # Имя 'home'

    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Книги
    path('books/', views.book_list_view, name='book_list'),
    path('books/<int:pk>/', views.book_detail_view, name='book_detail'),
    path('books/create/', views.book_create_view, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit_view, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete_view, name='book_delete'),

    # Авторы
    path('authors/', views.author_list_view, name='author_list'),
    path('authors/<int:pk>/', views.author_detail_view, name='author_detail'),
    path('authors/create/', views.author_create_view, name='author_create'),
    path('authors/<int:pk>/edit/', views.author_edit_view, name='author_edit'),
    path('authors/<int:pk>/delete/', views.author_delete_view, name='author_delete'),

    # Читатели
    path('readers/', views.reader_list_view, name='reader_list'),
    path('readers/<int:pk>/', views.reader_detail_view, name='reader_detail'),
    path('readers/create/', views.reader_create_view, name='reader_create'),
    path('readers/<int:pk>/edit/', views.reader_edit_view, name='reader_edit'),
    path('readers/<int:pk>/delete/', views.reader_delete_view, name='reader_delete'),
    path('readers/<int:pk>/reset-password/', views.reset_password_view, name='reset_password'),
]

