
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('authentication.urls')),  # Assuming authentication is your app name
    path('', lambda request: redirect('accounts/signup')),
]
