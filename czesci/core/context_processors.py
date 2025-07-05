from django.conf import settings


def main_settings(request):
    """Add settings to template context."""
    return {
        'settings': settings
    } 