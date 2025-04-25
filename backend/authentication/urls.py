from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_info, name='user_info'),
    path('csrf/', views.csrf_token, name='csrf_token'),
] 