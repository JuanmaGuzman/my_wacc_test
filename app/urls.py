from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # ... your other patterns ...
    path("", views.index, name="index"),
]
