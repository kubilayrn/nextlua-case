from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet,VehicleModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'vehiclemodels', VehicleModelViewSet)

urlpatterns = router.urls