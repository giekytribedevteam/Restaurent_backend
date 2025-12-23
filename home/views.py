import stripe
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets , status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Floorname , Table , Menucategroy , MenuItem , Order , OrderItem , KOT  , KOTItem , Payment 
from .serializers import FloorSerializer , TableSerializer , MenucategroySerializer , MenuItemSerializer , OrderSerializer ,   OrderItemSerializer,     KOTSerializer , KOTItemSerializer , PaymentSerializer 
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
#  Create your views here.


# stripe.api_key = settings.STRIPE_SECRET_KEY 

class FloorViewset(viewsets.ModelViewSet): 
    queryset = Floorname.objects.all()
    serializer_class = FloorSerializer 

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Floor list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "Floor details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": True,
            "message": "Floor created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": True,
            "message": "Floor updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "Floor deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)

class FloorListAPIView(APIView):
    def get(self, request):
        try:
         floors = Floorname.objects.all()
         serializer = FloorSerializer(floors, many=True)
         return Response({"data":serializer.data,"status": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e),
                 "status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR 
            )

class TableViewset(viewsets.ModelViewSet):
    queryset = Table.objects.all()    
    serializer_class = TableSerializer 

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Tables  list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "Menucategory deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)

class MenucategroyViewSet(viewsets.ModelViewSet):
    queryset = Menucategroy.objects.all()
    serializer_class = MenucategroySerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Menucategory  list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "Menucategory details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print("data : ==>>" , request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": True,
            "message": "Menucategory created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": True,
            "message": "Menucategory updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "Menucategory deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)

class MenuItemView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend , filters.SearchFilter]
    filterset_fields = ['menucategory', 'item_name', 'is_avaiable']
    search_fields = ['item_name']
    

    def list(self, request, *args, **kwargs):
        category_name = request.query_params.get('category', None)
        search_name = request.query_params.get('search' , None)
        if category_name:
            category = Menucategroy.objects.filter(name=category_name).first()
            if category:
                queryset = MenuItem.objects.filter(menucategory=category)   
            else:
                queryset = MenuItem.objects.none()  

        elif search_name:
           queryset  = MenuItem.objects.filter(item_name=search_name)      

        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "MenuItems list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "MenuItem details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": True,
            "message": "MenuItem created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": True,
            "message": "MenuItem updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "MenuItem deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)
    
class OrderViewset(viewsets.ModelViewSet):   
    queryset =  Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['orderType']


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Order list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "Order details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": True,
            "message": "Order created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": True,
            "message": "Order updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "Order deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)

 
class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


    def get_serializer(self, *args, **kwargs):
    
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "OrderItem list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "OrderItem details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        message = "Order items created successfully" if isinstance(request.data, list) else "Order item created successfully"

        return Response({
            "status": True,
            "message": message,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "status": True,
            "message": "OrderItem updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "OrderItem deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)

class KOTListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        kots = KOT.objects.exclude(status="READY").order_by("created_at")
        serializer = KOTSerializer(kots, many=True)

        return Response({
            "status": True,
            "message": "KOTListView list fetched successfully",
            "count": kots.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class KOTStautsListView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self , request , pk):
        try:
            kot = KOT.objects.get(pk=pk)
        except KOT.DoesNotExist:
            return Response({"status": False, "message": "KOT not found"}, status=404)
        
        status_value = request.data.get("status")
        if status_value not in ["PENDING" , "COOKING" , "READY"]:
           return Response({"status":False , "message":"Invalid status"} , status=404)
        
        kot.status = status_value
        kot.save()

        return Response({
            "status": True,
            "message": f"KOT marked {status_value}"
        },status=status.HTTP_200_OK)

# class PaymentViewset(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer 


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload,
#             sig_header,
#             settings.STRIPE_WEBHOOK_SECRET
#         )
#     except stripe.error.SignatureVerificationError:
#         return JsonResponse({"error": "Invalid signature"}, status=400)

#     if event["type"] == "payment_intent.succeeded":
#         intent = event["data"]["object"]
#         order_id = intent["metadata"]["order_id"]

#         payment = Payment.objects.get(order_id=order_id)
#         payment.payment_status = "PAID"
#         payment.save(update_fields=["payment_status"])

#         # OPTIONAL: mark order completed
#         payment.order.status = "COMPLETED"
#         payment.order.save(update_fields=["status"])

#     return JsonResponse({"status": "success"})


# class CreateStripePaymentIntent(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         order_id = request.data.get("order_id")

#         try:
#             order = Order.objects.get(id=order_id)
#         except Order.DoesNotExist:
#             return Response({"status": False, "message": "Order not found"}, status=404)


#         amount = int(order.grandTotal * 100)

#         intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency="inr",
#             metadata={"order_id": order.id}
#         )

#         payment, _ = Payment.objects.get_or_create(
#             order=order,
#             defaults={
#                 "payment_method": "STRIPE",
#                 "transaction_id": intent.id
#             }
#         )

#         return Response({
#             "status": True,
#             "client_secret": intent.client_secret,
#             "payment_id": payment.id
#         }, status=status.HTTP_200_OK)
