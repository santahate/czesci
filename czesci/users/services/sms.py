"""SMS gateway abstraction.
Currently logs OTP to console — replace with real provider (e.g., Twilio) in production.
"""

import logging

logger = logging.getLogger(__name__)


class SmsGateway:  # pylint: disable=too-few-public-methods
    """Simple SMS gateway stub."""

    @staticmethod
    def send_otp(number: str, code: str) -> None:  # noqa: D401
        """Send OTP via SMS (stub)."""
        logger.info("[SMS] Sending OTP %s to %s", code, number) 