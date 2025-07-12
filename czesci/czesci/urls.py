from django.conf import settings
from django.contrib import admin
from django.urls import include
from core import views as core_views
from django.urls import path
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('login/', user_views.login_view, name='login'),
    path('register/', user_views.register_view, name='register'),
    path('verify-phone/', user_views.verify_phone_view, name='verify_phone'),
    path('register/buyer/', user_views.register_buyer_view, name='register_buyer'),
    path('register/seller/', user_views.register_seller_view, name='register_seller'),
    path('logout/', user_views.logout_view, name='logout'),
    path('switch-to-seller/', user_views.switch_to_seller, name='switch_to_seller'),
    path('switch-to-buyer/', user_views.switch_to_buyer, name='switch_to_buyer'),
    path('how-it-works/', core_views.how_it_works, name='how_it_works'),

    # Settings page
    path('settings/', user_views.settings_view, name='settings'),
    path('settings/buyer/', user_views.buyer_settings_partial, name='settings_buyer'),
    path('settings/seller/', user_views.seller_settings_partial, name='settings_seller'),
    path('settings/phone/add/', user_views.add_phone_view, name='phone_add'),
    path('settings/phone/verify/<int:pk>/<str:profile_type>/', user_views.verify_phone_settings_view, name='phone_verify'),
    path('settings/phone/deactivate/<int:pk>/', user_views.deactivate_phone_view, name='phone_deactivate'),
    path('settings/phone/visibility/<int:pk>/', user_views.toggle_phone_visibility_view, name='phone_toggle_visibility'),

]

if settings.DEBUG:
    urlpatterns.append(path('__reload__/', include('django_browser_reload.urls')))

