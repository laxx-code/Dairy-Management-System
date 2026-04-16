from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    BakeryProductViewSet,
    DailySupplyViewSet,
    VendorViewSet,
    MilkRecordViewSet,
    BillingViewSet,
    CustomerPaymentViewSet
)

router = DefaultRouter()
router.register(r"customers", CustomerViewSet)
router.register(r"bakery-products", BakeryProductViewSet)
router.register(r"daily-supply", DailySupplyViewSet, basename="daily-supply")
router.register(r"vendors", VendorViewSet)
router.register(r"milk-records", MilkRecordViewSet)
router.register(r"billing", BillingViewSet, basename="billing")
router.register(r'payments', CustomerPaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


