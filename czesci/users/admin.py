from django.contrib import admin

from .models import BuyerProfile
from .models import SellerProfile
from .models import PhoneNumber
from .models import Company


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", )

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", )

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("number", "profile_type", "is_active", "is_verified", "show_to_sellers", "created_at")
    list_filter = ("profile_type", "is_active", "is_verified", "show_to_sellers")
    search_fields = ("number",)
    raw_id_fields = ("buyer_profile", "seller_profile")

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("legal_name", "nip", "city", "country", "created_at")
    search_fields = ("legal_name", "nip", "regon", "krs") 