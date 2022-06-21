from django.urls import include, path
from rest_framework import routers
from .views import DoctorsViewSet


accounts_router = routers.DefaultRouter()
accounts_router.register(
    "doctors", DoctorsViewSet, basename="doctors"
)
