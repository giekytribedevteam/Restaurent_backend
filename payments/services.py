import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(order):
    """
    Create Stripe PaymentIntent for an Order
    """
    intent = stripe.PaymentIntent.create(
        amount=int(order.grandTotal * 100),  # INR → paise
        currency="inr",
        metadata={
            "order_id": order.id
        },
        automatic_payment_methods={"enabled": True},
    )
    return intent
