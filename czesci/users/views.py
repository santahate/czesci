from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth import logout  # Added for logout functionality
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
import random
from .forms import (
    LoginForm,
    BasicRegistrationForm,
    BuyerRegistrationForm,
    SellerRegistrationForm,
)
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

                # Handle HTMX redirect properly to avoid duplicating page fragments
                if request.headers.get("HX-Request"):
                    response = HttpResponse(status=204)
                    response["HX-Redirect"] = request.GET.get("next") or reverse("home")
                    return response

                return redirect(request.GET.get("next") or reverse("home"))
            messages.error(request, _("Invalid credentials. Please try again."))
    else:
        form = LoginForm()

    # If request via HTMX, return partial template only.
    template = "users/login_form_partial.html" if request.headers.get("HX-Request") else "users/login.html"
    return render(request, template, {"form": form})


def logout_view(request):
    """Log out the current user via GET and redirect to home"""
    logout(request)
    return redirect(request.GET.get("next") or reverse("home"))


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


# ---------------- Registration Flow -----------------

def register_view(request):
    """Render and process the basic registration form (Step 1).

    After a successful POST the user object is created and an OTP is generated.
    The OTP is **temporarily** stored in the session for demo purposes only.
    The user is then redirected to the phone-verification screen.
    """

    # Determine desired role from query-param; default to buyer
    role = request.GET.get("type", "buyer")
    if role not in {"buyer", "seller"}:
        role = "buyer"

    if request.method == "POST":
        form = BasicRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Create a unique username (phone preferred, fallback to timestamp)
            username_base = cd["phone"].lstrip("+") or str(int(timezone.now().timestamp()))
            username = username_base
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{username_base}_{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                first_name=cd["first_name"],
                last_name=cd["last_name"],
                email=cd.get("email", ""),
                password=cd["password1"],
            )

            # Persist helper fields in session for the next step
            otp_code = f"{random.randint(100000, 999999)}"
            request.session["pending_user_id"] = user.id
            request.session["pending_phone"] = cd["phone"]
            request.session["pending_role"] = role
            request.session["pending_otp"] = otp_code

            messages.info(
                request,
                _(f"For demo purposes, your OTP is {otp_code}. It would normally be sent via SMS."),
            )

            # For HTMX request use HX-Redirect header to trigger client-side redirect
            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse("verify_phone")
                return response

            return redirect(reverse("verify_phone"))
    else:
        form = BasicRegistrationForm(initial={"role": role})

    template = "users/register_form_partial.html" if request.headers.get("HX-Request") else "users/register.html"
    return render(request, template, {"form": form, "role": role})


def verify_phone_view(request):
    """Simple OTP verification screen (Step 1b)."""

    if not request.session.get("pending_user_id"):
        # No pending registration, redirect to registration start
        return redirect(reverse("register"))

    if request.method == "POST":
        otp_entered = request.POST.get("otp", "").strip()
        if otp_entered == request.session.get("pending_otp"):
            user_id = request.session.pop("pending_user_id")
            # Clean-up helper session variables
            request.session.pop("pending_phone", None)
            role = request.session.pop("pending_role", "buyer")
            request.session.pop("pending_otp", None)

            user = User.objects.get(id=user_id)
            login(request, user)

            # Decide next step based on chosen role
            next_url = reverse("register_buyer") if role == "buyer" else reverse("register_seller")

            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = next_url
                return response

            return redirect(next_url)

        messages.error(request, _("Invalid OTP. Please try again."))

    template = "users/verify_phone.html"
    return render(request, template)


# ---------------- Step 2 Views -----------------


@login_required
def register_buyer_view(request):
    """Step 2: Collect buyer profile information."""

    # If profile already exists, redirect home
    if getattr(request.user, "buyer_profile", None):
        return redirect(reverse("home"))

    if request.method == "POST":
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            from users.models import BuyerProfile

            buyer_profile, created = BuyerProfile.objects.get_or_create(
                user=request.user,
                defaults={"delivery_address": cd["delivery_address"]},
            )

            messages.success(request, _("Buyer profile created. Your account is ready!"))

            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse("home")
                return response

            return redirect(reverse("home"))
    else:
        form = BuyerRegistrationForm()

    template = "users/buyer_register_form_partial.html" if request.headers.get("HX-Request") else "users/buyer_register.html"
    return render(request, template, {"form": form})


@login_required
def register_seller_view(request):
    """Step 2: Collect seller profile information."""

    if getattr(request.user, "seller_profile", None):
        return redirect(reverse("home"))

    if request.method == "POST":
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            from users.models import SellerProfile

            seller_profile, created = SellerProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    "legal_form": cd["legal_form"],
                    "business_name": cd["business_name"],
                    "business_address": cd["business_address"],
                    "nip": cd["nip"],
                    "regon": cd.get("regon", ""),
                    "krs": cd.get("krs", ""),
                    "iban": cd["iban"],
                    "representative_name": cd.get("representative_name", ""),
                    "representative_position": cd.get("representative_position", ""),
                    "id_document": cd.get("id_document"),
                    "representative_authorisation_doc": cd.get("representative_authorisation_doc"),
                },
            )

            messages.success(request, _("Seller profile created. Your account is ready!"))

            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = reverse("home")
                return response

            return redirect(reverse("home"))
    else:
        form = SellerRegistrationForm()

    template = "users/seller_register_form_partial.html" if request.headers.get("HX-Request") else "users/seller_register.html"
    return render(request, template, {"form": form})
