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


class BasicRegistrationForm(forms.Form):
    """Step 1 form for basic user data collection during registration.

    Collects only the minimal legally-required information as described in
    docs/004-Architecture/004.5-registration-onboarding-arch-en.md.
    """

    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("seller", "Seller"),
    ]

    first_name = forms.CharField(
        label=_("First name"),
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md",
                "placeholder": _("First name"),
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md mt-4",
                "placeholder": _("Last name"),
            }
        ),
    )
    from users.models import PHONE_REGEX  # local import to avoid circular

    phone = forms.CharField(
        label=_("Phone (E.164)"),
        validators=[PHONE_REGEX],
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md mt-4",
                "placeholder": _("+48123123123"),
                "pattern": "\\+?[0-9]{8,15}",
                "inputmode": "tel",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email (optional)"),
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md mt-4",
                "placeholder": _("you@example.com"),
            }
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md mt-4",
                "placeholder": _("Password"),
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md mt-4",
                "placeholder": _("Repeat password"),
            }
        ),
    )
    role = forms.ChoiceField(
        label=_("Account type"),
        choices=ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md mt-4",
            }
        ),
    )

    age_confirm = forms.BooleanField(
        label=_("I confirm I am at least 18 years old"),
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "mt-4 mr-2",
            }
        ),
    )
    consent_terms = forms.BooleanField(
        label=_("I accept the Terms of Service"),
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "mr-2",
            }
        ),
    )
    consent_privacy = forms.BooleanField(
        label=_("I have read the Privacy Policy"),
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "mr-2",
            }
        ),
    )

    consent_marketing = forms.BooleanField(
        label=_("I agree to receive marketing communications"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "mr-2",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get("password1")
        pwd2 = cleaned_data.get("password2")
        if pwd1 and pwd2 and pwd1 != pwd2:
            self.add_error("password2", _("Passwords do not match."))
        return cleaned_data 


class BuyerRegistrationForm(forms.Form):
    """Step 2 form for buyer-specific data."""

    delivery_address = forms.CharField(
        label=_("Delivery address"),
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-4 py-2 border rounded-md",
                "rows": 3,
                "placeholder": _("Street, number, city…"),
            }
        ),
    )


class SellerRegistrationForm(forms.Form):
    """Step 2 form for seller-specific data with legal entity support."""

    LEGAL_CHOICES = [
        ("sole_trader", "Sole Trader"),
        ("legal_entity", "Legal Entity"),
    ]

    legal_form = forms.ChoiceField(
        label=_("Legal form"),
        choices=LEGAL_CHOICES,
        widget=forms.Select(
            attrs={"class": "w-full px-4 py-2 border rounded-md"},
        ),
    )
    business_name = forms.CharField(
        label=_("Business name"),
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "w-full px-4 py-2 border rounded-md mt-4"},
        ),
    )
    business_address = forms.CharField(
        label=_("Business address"),
        widget=forms.Textarea(
            attrs={"class": "w-full px-4 py-2 border rounded-md mt-4", "rows": 3},
        ),
    )
    nip = forms.CharField(
        label="NIP",
        max_length=10,
        widget=forms.TextInput(
            attrs={"class": "w-full px-4 py-2 border rounded-md mt-4"},
        ),
    )
    regon = forms.CharField(
        label="REGON (optional)",
        max_length=9,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "w-full px-4 py-2 border rounded-md mt-4"},
        ),
    )
    krs = forms.CharField(
        label="KRS (optional)",
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "w-full px-4 py-2 border rounded-md mt-4"},
        ),
    )
    iban = forms.CharField(
        label="IBAN",
        max_length=34,
        widget=forms.TextInput(
            attrs={"class": "w-full px-4 py-2 border rounded-md mt-4"},
        ),
    )

    representative_name = forms.CharField(
        label=_("Representative name"),
        required=False,
        widget=forms.TextInput(
            attrs={"class": "w-full px-4 py-2 border rounded-md mt-4"},
        ),
    )
    representative_position = forms.CharField(
        label=_("Representative position"),
        required=False,
        widget=forms.TextInput(
            attrs={"class": "w-full px-4 py-2 border rounded-md mt-4"},
        ),
    )

    id_document = forms.FileField(
        label=_("ID document (PDF/JPEG)"),
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"class": "w-full px-4 py-2 mt-4 file:mr-4 file:py-2 file:px-4 file:border-0 file:rounded-md file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"},
        ),
    )
    representative_authorisation_doc = forms.FileField(
        label=_("Authorisation document (optional)"),
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"class": "w-full px-4 py-2 mt-4 file:mr-4 file:py-2 file:px-4 file:border-0 file:rounded-md file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"},
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        legal_form = cleaned_data.get("legal_form")
        krs = cleaned_data.get("krs")
        if legal_form == "legal_entity" and not krs:
            self.add_error("krs", _("KRS is required for legal entities."))
        return cleaned_data 