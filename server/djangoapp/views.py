# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime
from .models import CarMake, CarModel
from .populate import initiate
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .restapis import get_request, analyze_review_sentiments
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


def get_cars(request):
    count = CarMake.objects.count()
    print(f"CarMake count: {count}")

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.make.name
        })
    return JsonResponse({"CarModels": cars})

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...
#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    print("DEBUG: get_dealerships calling endpoint:", endpoint)
    dealerships = get_request(endpoint)
    print("DEBUG: get_dealerships received:", dealerships)
    return JsonResponse({"status":200,"dealers":dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        review_details = []
        for review in reviews:
            # Sentimentanalyse mit Microservice aufrufen
            sentiment_result = analyze_review_sentiments(review.get("review", ""))
            sentiment = sentiment_result.get("label", "neutral") if sentiment_result else "neutral"
            
            # Review-Daten + Sentiment speichern
            review_detail = {
                "id": review.get("id"),
                "name": review.get("name"),
                "dealership": review.get("dealership"),
                "review": review.get("review"),
                "purchase": review.get("purchase"),
                "car_make": review.get("car_make"),
                "car_model": review.get("car_model"),
                "car_year": review.get("car_year"),
                "sentiment": sentiment
            }
            review_details.append(review_detail)

        return JsonResponse({"status": 200, "reviews": review_details})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
