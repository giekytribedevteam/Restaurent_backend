from django.shortcuts import render
from rest_framework import viewsets ,status ,parsers
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User , UserPhoto
from rest_framework_simplejwt.tokens import RefreshToken
from .permission import IsAdmin
from  .serializers import UserSerializers , UserCreateSerializers , LoginSerializer , ChangePasswordSerializer , ForgotPasswordSerializer,  ResetPasswordSerializer,GetMeSerializer , UserPhotoSerializer
# Create your views here.


class Userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializers
        return UserSerializers

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsAdmin()]  
        return [IsAuthenticated()]
    

    def get_permissions(self):
        if self.action == "DELETE":
            return [IsAuthenticated(), IsAdmin()]  
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            "status": True,
            "message": "User created successfully",
            "data": UserSerializers(user).data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "status": True,
            "message": "Users fetched successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response_data = {
            "status": True,
            "message": "User details fetched successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"detail": "User deleted successfully.",
                             "status": True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found.",
                             "status": False}, status=status.HTTP_404_NOT_FOUND)
        

    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({
                "status": False,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "status": True,
            "message": "User updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # def destroy(self, request, *args, **kwargs):
    #     try:
    #      user = self.get_object()
    #      user.delete()
    #      return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)
    #     except User.DoesNotExist:
    #      return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class Loginviewset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "data": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": UserCreateSerializers(user).data
                    },
                    "status": True
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    "status": False
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    

class ChanagePasswordviewset(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)

            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response(
                {      
                    "message": "Password changed successfully",
                    "status": True
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    "status": False
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ForgetPasswordViewset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            return Response(
                { 
                    "message": "Password reset token sent to your email.",
                    "status": True
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    "status": False
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):  
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {  
                    "message": "Password reset successful.",                   
                    "status": True
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    "status": False
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class GetMeviewset(APIView):
     permission_classes = [AllowAny]
     def get(self, request):
        try:
            user = request.user
            serializer = GetMeSerializer(user)
            return Response({"data":serializer.data,"status": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e),
                 "status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserPhotoView(viewsets.ModelViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = UserPhotoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser] 

    def get_queryset(self):
        return UserPhoto.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





