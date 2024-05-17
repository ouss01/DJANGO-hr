from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('EmployeeApp.urls')),  # Assuming EmployeeApp has its own URLs
]
