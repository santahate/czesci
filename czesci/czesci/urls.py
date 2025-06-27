from django.contrib import admin
from django.urls import include
from core import views as core_views
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('login', user_views.login_view, name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('switch-to-seller', user_views.switch_to_seller, name='switch_to_seller'),
    path('switch-to-buyer', user_views.switch_to_buyer, name='switch_to_buyer'),
    path('__reload__/', include('django_browser_reload.urls')),
]

