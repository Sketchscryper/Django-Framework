from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.index, name='index'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/save/', views.save_article, name='save_article'),

    # Вход и выход для пользователей
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Используем кастомный выход

    # АДМИНИСТРАТИВНЫЕ СТРАНИЦЫ
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/article/create/', views.article_create, name='article_create'),
    path('dashboard/article/<int:article_id>/edit/', views.article_edit, name='article_edit'),
    path('dashboard/article/<int:article_id>/delete/', views.article_delete, name='article_delete'),
    path('dashboard/users/', views.user_list, name='user_list'),
    path('dashboard/users/add/', views.user_add, name='user_add'),
    path('dashboard/users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('dashboard/users/<int:user_id>/ban/', views.user_ban, name='user_ban'),
    path('dashboard/users/<int:user_id>/unban/', views.user_unban, name='user_unban'),
    path('dashboard/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('dashboard/settings/', views.site_settings_view, name='site_settings'),
    path('dashboard/statistics/', views.statistics_view, name='statistics'),
]