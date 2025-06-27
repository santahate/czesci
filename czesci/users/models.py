from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import RegexValidator


class BuyerProfile(models.Model):
    """Profile information specific to a buyer account."""

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="buyer_profile",
    )
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # noqa: DunderStr
        return f"BuyerProfile for {self.user.username}"


class SellerProfile(models.Model):
    """Profile information specific to a seller account."""

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )
    company_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # noqa: DunderStr
        return f"SellerProfile for {self.user.username} ({self.company_name})"


PHONE_REGEX = RegexValidator(
    regex=r"^\+?[1-9]\d{7,14}$",
    message="Enter a valid phone number in E.164 format.",
)


class PhoneNumber(models.Model):
    """Stores multiple phone numbers per BuyerProfile or SellerProfile.

    Exactly one of ``buyer_profile`` or ``seller_profile`` must be set. ``profile_type``
    mirrors the FK that is populated and is used for efficient filtering.
    """

    class ProfileType(models.TextChoices):
        BUYER = "buyer", "Buyer"
        SELLER = "seller", "Seller"

    buyer_profile = models.ForeignKey(
        "BuyerProfile",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="phone_numbers",
    )
    seller_profile = models.ForeignKey(
        "SellerProfile",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="phone_numbers",
    )
    profile_type = models.CharField(
        max_length=10,
        choices=ProfileType.choices,
    )
    number = models.CharField(max_length=32, validators=[PHONE_REGEX])
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    (models.Q(buyer_profile__isnull=False) & models.Q(seller_profile__isnull=True) & models.Q(profile_type='buyer'))
                    | (models.Q(seller_profile__isnull=False) & models.Q(buyer_profile__isnull=True) & models.Q(profile_type='seller'))
                ),
                name="phone_profile_type_consistency",
            ),
        ]

    def __str__(self) -> str:  # noqa: DunderStr
        owner = self.buyer_profile or self.seller_profile
        return f"{self.number} ({owner})" 