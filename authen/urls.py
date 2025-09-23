from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import Userviewset , Loginviewset , ChanagePasswordviewset , ForgetPasswordViewset, ResetPasswordView ,  GetMeviewset , UserPhotoView


router = DefaultRouter()
router.register(r'user',Userviewset)
router.register(r'photo',UserPhotoView)


urlpatterns = [
    path('',include(router.urls)),
    path("login/",Loginviewset.as_view(), name="login"),
    path("chanagepassword/",ChanagePasswordviewset.as_view(),name="chanagepassword"),
    path("forgot-password/", ForgetPasswordViewset.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("getme/" , GetMeviewset.as_view(),name="Getme"),
   

]   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
