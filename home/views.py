from django.shortcuts import render
from rest_framework import viewsets , status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Floorname , Table , Menucategroy , MenuItem
from .serializers import FloorSerializer , TableSerializer , MenucategroySerializer , MenuItemSerializer

# Create your views here.


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



class MenucategroyViewSet(viewsets.ModelViewSet):
    queryset = Menucategroy.objects.all()
    serializer_class = MenucategroySerializer

    
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