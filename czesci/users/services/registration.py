"""Registration service layer implementing business logic.

Each public method is wrapped in a DB transaction to ensure consistency.
The service isolates model manipulation from Django views / API views.
"""

from __future__ import annotations

from typing import Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import BuyerProfile, SellerProfile, PhoneNumber
from users.services.sms import SmsGateway
from users.services.phone import PhoneService

User = get_user_model()


class RegistrationService:  # pylint: disable=too-few-public-methods
    """Encapsulates the registration and onboarding flow."""

    @staticmethod
    @transaction.atomic
    def register_basic(data: dict, ip_address: str | None = None) -> Tuple[User, str]:
        """Create *User* and inactive *PhoneNumber*.

        Returns tuple (user, otp_code).
        """
        required = {"first_name", "last_name", "phone", "password1"}
        if not required.issubset(data):
            raise ValidationError("Missing required fields for basic registration.")

        phone = data["phone"].strip()
        first_name = data["first_name"].strip()
        last_name = data["last_name"].strip()
        email = data.get("email", "").strip()
        raw_pwd = data["password1"]

        # Generate unique username from phone or timestamp
        username_base = phone.lstrip("+") or str(int(timezone.now().timestamp()))
        username = username_base
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{username_base}_{counter}"
            counter += 1

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(raw_pwd),
            is_active=True,
        )

        # Store phone (inactive & unverified until OTP succeeds)
        PhoneNumber.objects.create(
            buyer_profile=None,
            seller_profile=None,
            profile_type=PhoneNumber.ProfileType.BUYER if data.get("role") == "buyer" else PhoneNumber.ProfileType.SELLER,
            number=phone,
            is_active=True,
            is_verified=False,
        )

        # Generate OTP (6-digits)
        otp_code = PhoneService.generate_otp()

        # Send via SMS gateway (stub)
        SmsGateway.send_otp(phone, otp_code)

        # Store consents
        from users.models import Consent  # local import to avoid circular

        consents = [
            Consent(user=user, type=Consent.ConsentType.TERMS, ip_address=ip_address),
            Consent(user=user, type=Consent.ConsentType.PRIVACY, ip_address=ip_address),
            Consent(user=user, type=Consent.ConsentType.AGE, ip_address=ip_address),
        ]
        if data.get("consent_marketing"):
            consents.append(Consent(user=user, type=Consent.ConsentType.MARKETING, ip_address=ip_address))

        Consent.objects.bulk_create(consents)

        # In production we would persist hashed OTP with TTL or send via provider.
        return user, otp_code

    @staticmethod
    @transaction.atomic
    def verify_phone(phone_number: str, otp_entered: str, expected_otp: str) -> bool:  # noqa: D401
        """Validate OTP and mark phone as verified by delegating to PhoneService."""
        if otp_entered != expected_otp:
            return False

        phone_entry = PhoneNumber.objects.filter(number=phone_number, is_verified=False).first()
        if phone_entry:
            PhoneService.mark_verified(phone_entry)

        # Return True if OTP matches, consistent with original behaviour
        return True

    @staticmethod
    @transaction.atomic
    def register_buyer(user: User, data: dict, phone_number: str) -> BuyerProfile:
        """Persist BuyerProfile and associate the verified phone number."""
        if BuyerProfile.objects.filter(user=user).exists():
            return user.buyer_profile

        profile = BuyerProfile.objects.create(
            user=user,
            delivery_address=data["delivery_address"],
        )

        # Associate phone number
        phone_entry = PhoneNumber.objects.filter(
            number=phone_number, profile_type=PhoneNumber.ProfileType.BUYER, buyer_profile__isnull=True
        ).first()
        if phone_entry:
            phone_entry.buyer_profile = profile
            phone_entry.save()

        return profile

    @staticmethod
    @transaction.atomic
    def register_seller(user: User, data: dict, phone_number: str) -> SellerProfile:
        """Persist SellerProfile and associate the verified phone number."""
        if SellerProfile.objects.filter(user=user).exists():
            return user.seller_profile

        profile = SellerProfile.objects.create(
            user=user,
            business_name=data["business_name"],
            business_address=data["business_address"],
            nip=data["nip"],
            regon=data.get("regon", ""),
            krs=data.get("krs", ""),
        )

        # Associate phone number
        phone_entry = PhoneNumber.objects.filter(
            number=phone_number, profile_type=PhoneNumber.ProfileType.SELLER, seller_profile__isnull=True
        ).first()
        if phone_entry:
            phone_entry.seller_profile = profile
            phone_entry.save()

        return profile
