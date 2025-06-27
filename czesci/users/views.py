from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from users.models import PhoneNumber


User = get_user_model()


def login_view(request):
    """Render and process the login form accepting phone/email and password."""

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"].strip()
            password = form.cleaned_data["password"]

            # Basic authentication logic: try email, then username.
            # 1. Try by email
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            # 2. Try by verified phone number
            if user is None:
                phone_entry = (
                    PhoneNumber.objects.select_related("buyer_profile__user", "seller_profile__user")
                    .filter(number=identifier, is_verified=True, is_active=True)
                    .first()
                )
                if phone_entry:
                    related_user = None
                    if phone_entry.buyer_profile:
                        related_user = phone_entry.buyer_profile.user
                    elif phone_entry.seller_profile:
                        related_user = phone_entry.seller_profile.user

                    if related_user is not None:
                        user = authenticate(request, username=related_user.username, password=password)

            # 3. Fall back to username login (for superusers etc.)
            if user is None:
                user = authenticate(request, username=identifier, password=password)

            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next") or reverse("home"))
            messages.error(request, _("Invalid credentials. Please try again."))
    else:
        form = LoginForm()

    # If request via HTMX, return partial template only.
    template = "users/login_form_partial.html" if request.headers.get("HX-Request") else "users/login.html"
    return render(request, template, {"form": form})


# ---------------- View Mode Switchers -----------------


@login_required
def switch_to_seller(request):
    """Set session flag to seller and redirect back."""
    request.session["view_mode"] = "seller"
    return redirect(request.META.get("HTTP_REFERER", reverse("home")))


@login_required
def switch_to_buyer(request):
    """Set session flag to buyer and redirect back."""
    request.session["view_mode"] = "buyer"
    return redirect(request.META.get("HTTP_REFERER", reverse("home"))) 