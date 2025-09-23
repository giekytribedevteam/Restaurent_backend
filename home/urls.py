from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import FloorViewset  , FloorListAPIView , MenucategroyViewSet , MenuItemView

router = DefaultRouter()
router.register(r'floor',FloorViewset , basename='floor')
router.register(r'category', MenucategroyViewSet, basename='categroy')
router.register(r'items',MenuItemView , basename='items')

   

urlpatterns = [
    path('',include(router.urls)),
    path("table/",FloorListAPIView.as_view() , name="tables")
    
 
]   
