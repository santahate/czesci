"""Phone related helper functions: OTP generation, send, add/deactivate numbers."""

from __future__ import annotations

import random
from typing import Tuple

from django.db import transaction

from users.models import PhoneNumber, BuyerProfile, SellerProfile
from users.services.sms import SmsGateway


class PhoneService:  # pylint: disable=too-few-public-methods
    """Utility service for phone number operations used outside of initial registration."""

    @staticmethod
    def generate_otp() -> str:
        """Return 6-digit zero-padded OTP string."""
        return f"{random.randint(0, 999999):06d}"

    # ---------------------------------------------------
    # Public helpers
    # ---------------------------------------------------

    @staticmethod
    @transaction.atomic
    def add_number_and_send_otp(profile, number: str) -> Tuple[PhoneNumber, str]:
        """Persist new inactive PhoneNumber linked to *profile* and send OTP.

        Returns (phone_obj, otp_code).
        """
        if isinstance(profile, BuyerProfile):
            phone_obj = PhoneNumber.objects.create(
                buyer_profile=profile,
                seller_profile=None,
                profile_type=PhoneNumber.ProfileType.BUYER,
                number=number,
                is_active=True,
                is_verified=False,
            )
        elif isinstance(profile, SellerProfile):
            phone_obj = PhoneNumber.objects.create(
                buyer_profile=None,
                seller_profile=profile,
                profile_type=PhoneNumber.ProfileType.SELLER,
                number=number,
                is_active=True,
                is_verified=False,
            )
        else:
            raise ValueError("Profile must be BuyerProfile or SellerProfile")

        otp_code = PhoneService.generate_otp()
        SmsGateway.send_otp(number, otp_code)
        return phone_obj, otp_code

    @staticmethod
    @transaction.atomic
    def mark_verified(phone_obj: PhoneNumber) -> None:  # noqa: D401
        """Mark phone number as verified."""
        phone_obj.is_verified = True
        phone_obj.save(update_fields=["is_verified"]) 