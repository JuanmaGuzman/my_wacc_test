from django.urls import path, include
from . import views

webhooks = [
    path(
        "typeform/submission",
        views.TypeformSubmission.as_view(),
        name="TypeformSubmission"
    )
]

urlpatterns = [
    path("", views.index, name="index"),
    path("webhooks/", include((webhooks, "webhooks"))),
]