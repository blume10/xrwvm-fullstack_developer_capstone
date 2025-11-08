from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "djangoapp"

urlpatterns = [
    path("login", view=views.login_user, name="login"),
    path("logout", view=views.logout_request, name="logout"),
    path("register", view=views.registration, name="register"),
    path("get_cars", views.get_cars, name="getcars"),
    path("get_dealers/", views.get_dealerships, name="get_dealers"),
    path(
        "get_dealers/<str:state>/",
        view=views.get_dealerships,
        name="get_dealers_by_state",
    ),
    # Dealer Details
    path(
        "get_dealer/<int:dealer_id>/",
        views.get_dealer_details,
        name="get_dealer_details",
    ),
    path(
        "get_dealer/<int:dealer_id>",
        views.get_dealer_details,
        name="get_dealer_details_no_slash",
    ),
    # Dealer Reviews
    path(
        "get_dealer_reviews/<int:dealer_id>/",
        views.get_dealer_reviews,
        name="get_dealer_reviews",
    ),
    path("add_review", views.add_review, name="add_review"),
    # Optionaler API-Alias
    path(
        "api/dealer/<int:dealer_id>/",
        views.get_dealer_details,
        name="api_get_dealer",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
