from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Q, CheckConstraint, UniqueConstraint


class BuyerProfile(models.Model):
    """Profile information specific to a buyer account."""

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="buyer_profile",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    delivery_address = models.TextField(blank=False)

    def __str__(self) -> str:  # noqa: DunderStr
        return f"BuyerProfile for {self.user.username}"


class SellerProfile(models.Model):
    """Profile information specific to a seller account."""

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )
    business_name = models.CharField(max_length=255)
    business_address = models.TextField()
    nip = models.CharField(
        max_length=10,
        validators=[RegexValidator(r"^\d{10}$", "Enter 10–digit NIP without prefix.")],
    )
    regon = models.CharField(
        max_length=9,
        blank=True,
        validators=[RegexValidator(r"^\d{9}$", "Enter 9–digit REGON.")],
    )
    krs = models.CharField(
        max_length=10,
        blank=True,
        validators=[RegexValidator(r"^\d{10}$", "Enter 10–digit KRS.")],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # noqa: DunderStr
        return f"SellerProfile for {self.user.username} ({self.business_name})"


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
                    | (models.Q(buyer_profile__isnull=True) & models.Q(seller_profile__isnull=True))
                ),
                name="phone_profile_type_consistency",
            ),
        ]

    def __str__(self) -> str:  # noqa: DunderStr
        owner = self.buyer_profile or self.seller_profile
        return f"{self.number} ({owner})"


class Company(models.Model):
    """Normalized legal & invoicing data for a seller company (Poland default)."""
    # Identification
    legal_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=120, blank=True)
    LEGAL_FORMS = [
        ("JD", "Jednoosobowa działalność"),
        ("SPZOO", "Sp. z o.o."),
        ("SA", "Spółka Akcyjna"),
    ]
    legal_form = models.CharField(max_length=30, choices=LEGAL_FORMS, default="JD")

    # Address fields
    street = models.CharField(max_length=120)
    building_no = models.CharField(max_length=20)
    apartment_no = models.CharField(max_length=20, blank=True)
    postal_code = models.CharField(
        max_length=6,
        validators=[RegexValidator(r"^\d{2}-\d{3}$", "Enter postal code in NN-NNN format.")],
    )
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=2, default="PL")

    # Identifiers
    nip = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r"^\d{10}$", "Enter 10–digit NIP without prefix.")],
    )
    regon = models.CharField(
        max_length=9,
        blank=True,
        validators=[RegexValidator(r"^\d{9}$", "Enter 9–digit REGON.")],
    )
    krs = models.CharField(
        max_length=10,
        blank=True,
        validators=[RegexValidator(r"^\d{10}$", "Enter 10–digit KRS.")],
    )

    # VAT status
    vat_payer = models.BooleanField(default=True)
    vat_active_since = models.DateField(null=True, blank=True)

    # Contacts
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    contact_person = models.CharField(max_length=120, blank=True)

    # Payments
    bank_account_iban = models.CharField(max_length=34, blank=True)
    swift_bic = models.CharField(max_length=11, blank=True)

    # Invoice customisation
    invoice_display_name = models.CharField(max_length=255, blank=True)
    invoice_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"

        constraints = [
            # Ensure NIP unique across SellerProfile table
            UniqueConstraint(fields=["nip"], name="unique_seller_nip"),
            # If legal_entity then KRS must be non-blank
            CheckConstraint(
                check=Q(legal_form="sole_trader") | (Q(legal_form="legal_entity") & ~Q(krs="")),
                name="krs_required_for_legal_entity",
            ),
        ]

    def __str__(self) -> str:  # noqa: DunderStr
        return self.short_name or self.legal_name

    # Utility
    def invoice_nip(self) -> str:
        """Return NIP with optional PL prefix depending on VAT payer status."""
        return f"PL{self.nip}" if self.vat_payer else self.nip 


class Consent(models.Model):
    """Stores explicit user consents (ToS, Privacy, Marketing)."""

    class ConsentType(models.TextChoices):
        TERMS = "terms", "Terms of Service"
        PRIVACY = "privacy", "Privacy Policy"
        MARKETING = "marketing", "Marketing"
        AGE = "age", "Age Confirmation"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="consents")
    type = models.CharField(max_length=20, choices=ConsentType.choices)
    accepted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "type")

    def __str__(self) -> str:  # noqa: DunderStr
        return f"{self.user} consent {self.type}" 