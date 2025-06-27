from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    identifier = forms.CharField(
        label=_("Phone or Email"),
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md",
                "placeholder": _("Phone or Email"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md",
                "placeholder": _("Password"),
            }
        ),
    ) 