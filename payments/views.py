import stripe
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from home.models import Payment , Order
from home.serializers import PaymentSerializer
from .services import create_payment_intent

# @csrf_exempt
# def stripe_webhook(request):
    
#     print("WEBHOOK HIT")

#     payload = request.body
#     sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except Exception:
#         return JsonResponse({"error": "Invalid webhook"}, status=400)
    
    
#     print("EVENT TRIGGER" ,event)

#     #  Payment succeeded
#     if event["type"] == "payment_intent.succeeded":
#         intent = event["data"]["object"]
#         order_id = intent["metadata"]["order_id"]

#         order = Order.objects.get(id=order_id)

#         Payment.objects.update_or_create(
#             order=order,
#             defaults={
#                 "payment_status": "SUCCESS",
#                 "transaction_id": intent.id,
#                 "payment_method": intent.payment_method_types[0]
#             }
#         )

#         order.status = "COMPLETED"
#         order.save()
    
#     print("EVENT TRIGGER" , event["type"])

#     # Payment failed
#     if event["type"] == "payment_intent.payment_failed":
#         intent = event["data"]["object"]
#         Payment.objects.filter(
#             transaction_id=intent.id
#         ).update(payment_status="FAILED")

#     return JsonResponse({"status": "ok"})

@csrf_exempt
def stripe_webhook(request):
    print("WEBHOOK HIT")

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print("SIGNATURE ERROR", e)
        return JsonResponse({"error": "invalid signature"}, status=400)

    print("EVENT:", event["type"])
    print("EVENT DATA" ,event)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent["metadata"].get("order_id")

        if not order_id:
            print(" NO ORDER ID")
            return JsonResponse({"ignored": True})

        order = Order.objects.get(id=order_id)

        Payment.objects.update_or_create(
            order=order,
            defaults={
                "payment_status": "SUCCESS",
                "transaction_id": intent.id,
                "payment_method": intent.payment_method_types[0],
            }
        )

        order.status = "COMPLETED"
        order.save()

        print("PAYMENT SUCCESS UPDATED")

    return JsonResponse({"status": "ok"})



class PaymentViewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.validated_data["order"]

        # Create or update payment
        payment, _ = Payment.objects.get_or_create(
            order=order,
            defaults={
                "payment_method": serializer.validated_data["payment_method"]
            }
        )

        # Create Stripe PaymentIntent
        intent = create_payment_intent(order)

        payment.transaction_id = intent.id
        payment.save()

        return Response({
            "status": True,
            "message": "Payment initiated",
            "client_secret": intent.client_secret,
            "payment_id": payment.id
        }, status=status.HTTP_201_CREATED)
