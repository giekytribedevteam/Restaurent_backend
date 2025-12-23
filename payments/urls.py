from django.urls import path
from .views import stripe_webhook
from rest_framework.routers import DefaultRouter
from .views import PaymentViewset

router = DefaultRouter()
router.register("payments", PaymentViewset)

urlpatterns =  [
    path("stripe/webhook/", stripe_webhook),
]

