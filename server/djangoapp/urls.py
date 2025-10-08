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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
