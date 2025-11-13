# todoapp/auth_views.py
from typing import Any, Dict
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .mongo_user_service import create_user, verify_user_credentials, find_user_by_email
import logging

logger = logging.getLogger(__name__)

def signup_view(request: HttpRequest) -> HttpResponse:
    """GET -> signup form. POST -> create user and log in."""
    if request.method == "GET":
        return render(request, "signup.html", {"error": None})
    # POST
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "")
    password2 = request.POST.get("password2", "")
    full_name = request.POST.get("full_name", "").strip()
    if not email or not password:
        return render(request, "signup.html", {"error": "Email and password required"})
    if password != password2:
        return render(request, "signup.html", {"error": "Passwords do not match"})
    try:
        user = create_user(email, password, full_name)
        request.session["user_id"] = user["id"]
        logger.info("New user created: %s", email)
        return redirect("/")
    except ValueError as exc:
        return render(request, "signup.html", {"error": str(exc)})
    except Exception:
        logger.exception("Error creating user")
        return render(request, "signup.html", {"error": "Unexpected error"})

def login_view(request: HttpRequest) -> HttpResponse:
    """GET -> login form. POST -> verify credentials and set session."""
    if request.method == "GET":
        return render(request, "login.html", {"error": None})
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "")
    user = verify_user_credentials(email, password)
    if not user:
        return render(request, "login.html", {"error": "Invalid credentials"})
    request.session["user_id"] = user["id"]
    return redirect("/")

def logout_view(request: HttpRequest) -> HttpResponse:
    request.session.flush()
    return redirect("/auth/login/")
