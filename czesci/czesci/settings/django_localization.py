from django.utils.translation import gettext_lazy

USE_I18N = True
USE_TZ = True
TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ("en", gettext_lazy("English")),
    ("pl", gettext_lazy("Polish")),
    ("uk", gettext_lazy("Ukrainian")),
]
