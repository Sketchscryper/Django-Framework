from django.urls import path
from . import views

urlpatterns = [
    path('prediction/', views.prediction_view, name='prediction'),
    path('random/', views.random_number_view, name='random'),
    path('random/<int:min_val>/<int:max_val>/', views.random_number_view, name='random_range'),
    path('random-list/<int:count>/', views.random_list_view, name='random_list'),
]