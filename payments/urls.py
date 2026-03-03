from django.urls import path , include
from .views import stripe_webhook
from rest_framework.routers import DefaultRouter
from .views import PaymentViewset

router = DefaultRouter()
router.register(r'payments',PaymentViewset,basename="payments")

urlpatterns = [
    path("stripe/webhook/", stripe_webhook),
    path("", include(router.urls)),  
]
