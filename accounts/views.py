from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render

from .models import User
from store.models import Cart


def register(request):

    if request.user.is_authenticated:
        return redirect("product_list")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone_number = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        # Validate required fields
        if not username or not email or not phone_number or not password:
            messages.error(
                request,
                "Please fill in all required fields."
            )
            return render(
                request,
                "accounts/register.html"
            )

        # Password confirmation
        if password != password_confirm:
            messages.error(
                request,
                "Passwords do not match."
            )
            return render(
                request,
                "accounts/register.html"
            )

        # Check username
        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "That username is already taken."
            )
            return render(
                request,
                "accounts/register.html"
            )

        # Check email
        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "An account with that email already exists."
            )
            return render(
                request,
                "accounts/register.html"
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
        )
        Cart.objects.create(user=user)
        # Automatically log user in
        login(request, user)

        messages.success(
            request,
            "Your M-Cart account has been created successfully."
        )

        return redirect("product_list")

    return render(
        request,
        "accounts/register.html"
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("product_list")

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            email=email,
            password=password,
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}."
            )

            return redirect("product_list")

        messages.error(
            request,
            "Invalid email or password."
        )

    return render(
        request,
        "accounts/login.html"
    )

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")