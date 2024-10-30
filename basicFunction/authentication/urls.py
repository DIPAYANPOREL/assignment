# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, home, change_password
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
]
