from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login', view=views.login_user, name='login'),
    path('logout', view=views.logout_request, name='logout'),
    path('register', view=views.registration, name='register'),  # 👈 wichtig!
    path('get_cars', views.get_cars, name='getcars'),
    path('get_dealers/', view=views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>/', view=views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/reviews/. ', views.get_dealer_reviews, name='dealer_reviews'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
