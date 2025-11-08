from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, backend_url
import logging
import json
import requests  # ✅ Jetzt korrekt importiert

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
            username = data.get("userName")
            password = data.get("password")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(
                {"userName": username, "status": "Authenticated"}
            )
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse(
        {"info": "Please send a POST request with JSON {userName, password}."}
    )


# -------------------------------
# LOGOUT VIEW
# -------------------------------
@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


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

            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {"userName": username, "error": "Already Registered"}
                )

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            login(request, user)
            return JsonResponse(
                {"userName": username, "status": "Authenticated"}
            )
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return JsonResponse({"error": "Invalid data or request"})

    return JsonResponse({"status": "Only POST method allowed"})


# -------------------------------
# GET CARS
# -------------------------------
def get_cars(request):
    count = CarMake.objects.count()
    print(f"CarMake count: {count}")

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("make")
    cars = [
        {"CarModel": model.name, "CarMake": model.make.name}
        for model in car_models
    ]
    return JsonResponse({"CarModels": cars})


# -------------------------------
# GET DEALERSHIPS
# -------------------------------
def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    print("DEBUG: get_dealerships calling endpoint:", endpoint)
    dealerships = get_request(endpoint)
    print("DEBUG: get_dealerships received:", dealerships)
    return JsonResponse({"status": 200, "dealers": dealerships})


# -------------------------------
# GET DEALER REVIEWS
# -------------------------------
def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    review_details = []
    for review in reviews:
        sentiment_result = analyze_review_sentiments(
            review.get("review", "")
        )
        sentiment = (
            sentiment_result.get("label", "neutral")
            if sentiment_result
            else "neutral"
        )
        review_details.append(
            {
                "id": review.get("id"),
                "name": review.get("name"),
                "dealership": review.get("dealership"),
                "review": review.get("review"),
                "purchase": review.get("purchase"),
                "car_make": review.get("car_make"),
                "car_model": review.get("car_model"),
                "car_year": review.get("car_year"),
                "sentiment": sentiment,
            }
        )

    return JsonResponse({"status": 200, "reviews": review_details})


# -------------------------------
# GET DEALER DETAILS
# -------------------------------
def get_dealer_details(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse(
        {
            "status": 200,
            "dealer": {
                "id": dealership.get("id"),
                "name": dealership.get("full_name"),
                "address": dealership.get("address"),
                "city": dealership.get("city"),
                "state": dealership.get("state"),
            },
        }
    )


# -------------------------------
# ADD REVIEW
# -------------------------------
@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": 400, "message": "POST request required"}
        )

    try:
        data = json.loads(request.body)
        endpoint = f"{backend_url}/insert_review"
        response = requests.post(endpoint, json=data)
        response.raise_for_status()
        return JsonResponse({"status": 200, "review": response.json()})
    except Exception as e:
        print("Error in add_review:", e)
        return JsonResponse({"status": 500, "message": str(e)})
