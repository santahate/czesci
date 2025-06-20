from django.contrib import admin
from django.urls import include
from core import views as core_views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('__reload__/', include('django_browser_reload.urls')),
]

