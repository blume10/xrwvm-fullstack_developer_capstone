# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from datetime import datetime
# Get an instance of a logger
logger = logging.getLogger(__name__)

# -------------------------------
# LOGIN VIEW
# -------------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    else:
        return JsonResponse({"info": "Please send a POST request with JSON {userName, password}."})


# -------------------------------
# LOGOUT VIEW
# -------------------------------
@csrf_exempt
def logout_request(request):
    # Benutzer-Session beenden
    logout(request)
    # Antwort zurückgeben – leerer Benutzername
    data = {"userName": ""}
    return JsonResponse(data)

# -------------------------------
# REGISTRATION VIEW
# -------------------------------
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            first_name = data.get("firstName", "")
            last_name = data.get("lastName", "")
            email = data.get("email", "")

            # Prüfen, ob der Benutzername bereits existiert
            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"})

            # Benutzer erstellen
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Benutzer automatisch einloggen
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return JsonResponse({"error": "Invalid data or request"})
    else:
        return JsonResponse({"status": "Only POST method allowed"})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
