from django.contrib import admin

from .models import BuyerProfile
from .models import SellerProfile
from .models import PhoneNumber


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", )

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "created_at")
    search_fields = ("user__username", "company_name", )

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("number", "profile_type", "is_active", "is_verified", "created_at")
    list_filter = ("profile_type", "is_active", "is_verified")
    search_fields = ("number",)
    raw_id_fields = ("buyer_profile", "seller_profile") 