from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Встроенная админка Django
    path('', include('portal.urls')), # Наши URL (будут доступны по /dashboard/...)
]