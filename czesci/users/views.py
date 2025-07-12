from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import (
    LoginForm,
    BasicRegistrationForm,
    BuyerRegistrationForm,
    SellerRegistrationForm,
    BuyerProfileForm,
    SellerProfileForm,
)

from .models import PhoneNumber
from users.services.registration import RegistrationService


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

    # Determine initial dropdown selection from query-param (GET only)
    initial_role = request.GET.get("type", "buyer")
    if initial_role not in {"buyer", "seller"}:
        initial_role = "buyer"

    if request.method == "POST":
        form = BasicRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Delegate to service layer
            user, otp_code = RegistrationService.register_basic(cd, request.META.get("REMOTE_ADDR"))

            # Persist helper fields in session for the next step
            request.session["pending_user_id"] = user.id
            request.session["pending_phone"] = cd["phone"]
            request.session["pending_role"] = cd["role"]
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
        form = BasicRegistrationForm(initial={"role": initial_role})

    template = "users/register_form_partial.html" if request.headers.get("HX-Request") else "users/register.html"
    return render(request, template, {"form": form, "role": initial_role})


def verify_phone_view(request):
    """Simple OTP verification screen (Step 1b)."""

    if not request.session.get("pending_user_id"):
        # No pending registration, redirect to registration start
        return redirect(reverse("register"))

    if request.method == "POST":
        otp_entered = request.POST.get("otp", "").strip()
        expected_otp = request.session.get("pending_otp")

        # Rate-limiting: allow max 5 attempts per session
        attempt_key = "otp_attempts"
        attempts = request.session.get(attempt_key, 0) + 1
        request.session[attempt_key] = attempts
        if attempts > settings.MAX_SMS_ATTEMPTS:
            messages.error(request, _("Too many failed attempts. Please restart registration."))
            return redirect(reverse("register"))

        if otp_entered == expected_otp:
            user_id = request.session["pending_user_id"]
            phone_number = request.session["pending_phone"]
            role = request.session["pending_role"]

            # Mark phone verified via service
            RegistrationService.verify_phone(phone_number, otp_entered, expected_otp)

            # Log the user in and clean up session
            user = User.objects.get(id=user_id)
            login(request, user)
            for key in ["pending_user_id", "pending_otp", "otp_attempts"]:
                request.session.pop(key, None)

            # Decide next step based on chosen role
            next_url = reverse("register_buyer") if role == "buyer" else reverse("register_seller")

            if request.headers.get("HX-Request"):
                response = HttpResponse(status=204)
                response["HX-Redirect"] = next_url
                return response

            return redirect(next_url)

        messages.error(request, _(f"Invalid OTP. Attempts left: {settings.MAX_SMS_ATTEMPTS - attempts}"))

    template = "users/verify_phone.html"
    return render(request, template)


# ---------------- Step 2 Views -----------------


def register_buyer_view(request):
    """Step 2: Collect buyer profile information."""

    if not request.user.is_authenticated:
        return redirect(reverse_lazy("register") + "?type=buyer")
    # If profile already exists, redirect home
    if getattr(request.user, "buyer_profile", None):
        return redirect(reverse("home"))

    if request.method == "POST":
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = request.session.get("pending_phone")
            RegistrationService.register_buyer(request.user, cd, phone_number)

            # Clean up session
            for key in ["pending_phone", "pending_role"]:
                request.session.pop(key, None)

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


def register_seller_view(request):
    """Step 2: Collect seller profile information."""

    if not request.user.is_authenticated:
        return redirect(reverse_lazy("register") + "?type=seller")

    if getattr(request.user, "seller_profile", None):
        return redirect(reverse("home"))

    if request.method == "POST":
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = request.session.get("pending_phone")
            RegistrationService.register_seller(request.user, cd, phone_number)

            # Clean up session
            for key in ["pending_phone", "pending_role"]:
                request.session.pop(key, None)

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


# ---------------- Settings Page Views -----------------

@login_required
def settings_view(request):
    """Wrapper page that loads the settings template with empty container.
    HTMX will fetch the buyer/seller partials.
    """
    return render(request, "users/settings.html")


@login_required
def buyer_settings_partial(request):
    """HTMX fragment for Buyer settings.

    Renders editable form if profile exists, else CTA button.
    Supports POST updates with HX-Refresh.
    """

    profile = getattr(request.user, "buyer_profile", None)

    if not profile:
        # No profile yet – show CTA
        return render(request, "users/buyer_settings_partial.html", {"profile_exists": False})

    if request.method == "POST":
        form = BuyerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            if request.headers.get("HX-Request"):
                resp = HttpResponse(status=204)
                resp["HX-Refresh"] = "true"
                return resp
    else:
        form = BuyerProfileForm(instance=profile)

    numbers = profile.phone_numbers.filter(is_active=True)
    return render(
        request,
        "users/buyer_settings_partial.html",
        {
            "profile_exists": True,
            "form": form,
            "phone_numbers": numbers,
        },
    )


@login_required
def seller_settings_partial(request):
    """HTMX fragment for Seller settings.

    Similar logic to buyer.
    """

    profile = getattr(request.user, "seller_profile", None)

    if not profile:
        return render(request, "users/seller_settings_partial.html", {"profile_exists": False})

    if request.method == "POST":
        form = SellerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            if request.headers.get("HX-Request"):
                resp = HttpResponse(status=204)
                resp["HX-Refresh"] = "true"
                return resp
    else:
        form = SellerProfileForm(instance=profile)

    numbers = profile.phone_numbers.filter(is_active=True)
    return render(
        request,
        "users/seller_settings_partial.html",
        {
            "profile_exists": True,
            "form": form,
            "phone_numbers": numbers,
        },
    )


@login_required
def add_phone_view(request):
    """Handle phone addition form (POST) – create PhoneNumber and send OTP.

    Expects POST body with field ``number`` (E.164). After creating the number sends OTP
    via ``PhoneService`` and redirects user to verification view.
    """

    if request.method != "POST":
        return HttpResponse(status=405)

    number_raw = request.POST.get("number", "").strip()
    profile_type = request.POST.get("profile_type")

    if not number_raw:
        return HttpResponse("Missing phone number", status=400)

    if profile_type == "buyer":
        profile = getattr(request.user, "buyer_profile", None)
    elif profile_type == "seller":
        profile = getattr(request.user, "seller_profile", None)
    else:
        return HttpResponse("Invalid profile type", status=400)

    if not profile:
        return HttpResponse("Profile not found", status=400)

    try:
        from users.services.phone import PhoneService  # local import to avoid cycles

        phone_obj, otp_code = PhoneService.add_number_and_send_otp(profile, number_raw)

    except Exception as exc:  # pylint: disable=broad-except
        return HttpResponse(f"Error: {exc}", status=400)

    # Store expected OTP in session keyed by phone id (demo only)
    otp_session_key = f"settings_phone_otp_{phone_obj.id}"
    request.session[otp_session_key] = otp_code

    verify_url = reverse("phone_verify", args=[phone_obj.id, profile_type])

    if request.headers.get("HX-Request"):
        resp = HttpResponse(status=204)
        resp["HX-Redirect"] = verify_url
        return resp

    return redirect(verify_url)


@login_required
def verify_phone_settings_view(request, pk, profile_type):
    """Verify phone number (Settings flow). Displays same template & handles OTP POST.

    OTP code is stored in the session under key ``settings_phone_otp_<pk>`` during addition.
    After successful verification marks the number as verified and redirects back to settings.
    """

    from users.models import PhoneNumber  # local import avoid top circular
    try:
        phone_obj = PhoneNumber.objects.get(id=pk, is_active=True)
    except PhoneNumber.DoesNotExist:
        return HttpResponse("Phone not found", status=404)

    session_key = f"settings_phone_otp_{pk}"
    expected_otp = request.session.get(session_key)

    if settings.DEBUG and expected_otp:
        messages.info(
            request,
            _(f"For demo purposes, your OTP is {expected_otp}. It would normally be sent via SMS."),
        )

    if request.method == "POST":
        otp_entered = request.POST.get("otp", "").strip()

        if not expected_otp:
            messages.error(request, _("OTP expired. Please resend or add number again."))
        elif otp_entered == expected_otp:
            from users.services.phone import PhoneService  # avoid cycles

            PhoneService.mark_verified(phone_obj)
            # Clean session key
            request.session.pop(session_key, None)

            messages.success(request, _("Phone number verified."))

            # For HTMX flow we can trigger refresh of partial
            if request.headers.get("HX-Request"):
                resp = HttpResponse(status=204)
                resp["HX-Refresh"] = "true"
                return resp

            redirect_url = reverse("settings")
            if profile_type == "seller":
                redirect_url += "#seller"

            return redirect(redirect_url)
        else:
            messages.error(request, _("Invalid OTP. Please try again."))

    # GET or failed POST renders template
    return render(request, "users/verify_phone.html")


@login_required
def deactivate_phone_view(request, pk):
    """Soft-deactivate (is_active=False) selected phone number.

    Only the owner of the related profile may deactivate. Supports HTMX.
    """

    if request.method != "POST":
        return HttpResponse(status=405)

    from users.models import PhoneNumber

    try:
        phone_obj = PhoneNumber.objects.get(id=pk, is_active=True)
    except PhoneNumber.DoesNotExist:
        return HttpResponse("Phone not found", status=404)

    # Ownership check
    owner_ok = False
    if phone_obj.buyer_profile and getattr(request.user, "buyer_profile", None) == phone_obj.buyer_profile:
        owner_ok = True
    if phone_obj.seller_profile and getattr(request.user, "seller_profile", None) == phone_obj.seller_profile:
        owner_ok = True

    if not owner_ok:
        return HttpResponse("Forbidden", status=403)

    phone_obj.is_active = False
    phone_obj.save(update_fields=["is_active"])

    if request.headers.get("HX-Request"):
        resp = HttpResponse(status=204)
        resp["HX-Refresh"] = "true"
        return resp

    return redirect(reverse("settings"))
