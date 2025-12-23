from rest_framework import serializers
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
import random
import string
from .models import User , PasswordResetToken ,UserPhoto

class UserCreateSerializers(serializers.ModelSerializer):
     
    class Meta:
        model = User
        fields = [ 'id','profile_picture' , 'first_name' , 'last_name' , 'email' , 'date_joined' ,'role' , 'phone_number' ,'address' , 'adhar_proof' , 'gender' , 'account_number' ,'ifsc_code' , 'username' , 'pan_number' , 'nationality']

    def create(self , validated_data): 
        dummy_password = "".join(random.choices(string.ascii_letters + string.digits, k=10))

        user = User.objects.create_user(**validated_data)
        user.set_password(dummy_password)
        user.save()

        subject = "You are New Credentials"
        massage = (
                f"Hello {user.first_name},\n\n"
                f"You account has been created,\n\n"
                f"Role : {user.role},\n"
                f" Temporary Password :{dummy_password},\n\n"
        )

        try:
                
            send_mail( 
                   subject,
                   massage,
                   from_email='websolutions.ajay@gmail.com',  
                   recipient_list=[user.email],
                   fail_silently=False,
            )
        except Exception as e:
            print("does not send email:",{e})
     
        return user


class UserSerializers(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True ,required=False)

    class Meta:
        model = User
        fields = [ 'id' , 'profile_picture'  , 'first_name' , 'last_name' , 'email' , 'date_joined', 'created_at' ,'role' , 'phone_number' ,'address' , 'adhar_proof' , 'gender' , 'account_number' ,'ifsc_code' , 'username' , 'pan_number' , 'nationality' , 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError("Both email and password are required !")
        print(User.objects.all())
        user = authenticate(email=email , password=password)
        if not user:
            raise  serializers.ValidationError("invaild email and password !")
        if not user:
            raise serializers.ValidationError("user Invaild !")       
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


    def validate_old_password(self, value):
        user = self.context["request"].user
        print("=-=-=-=" ,  user)
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        
   
        reset_token = PasswordResetToken.create_token(user)

    
        FRONTEND_URL = "http://localhost:3000"
        reset_url = f"{FRONTEND_URL}/reset-password?token={reset_token.token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_url}",
            from_email='websolutions.ajay@gmail.com' ,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return value
    

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            reset_token = PasswordResetToken.objects.get(token=data["token"])
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired token.")

        if reset_token.is_expired():
            reset_token.delete()  
            raise serializers.ValidationError("Token has expired.")

        data["user"] = reset_token.user  
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()

    
        PasswordResetToken.objects.filter(user=user).delete()    



class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = ['id', 'user' , 'image']
        extra_kwargs = {
            'user': {'read_only': True}
        }
class GetMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [ 'id','first_name' , 'last_name' , 'email' , 'date_joined' ,'role' , 'phone_number' ,'address' , 'adhar_proof' , 'gender' , 'account_number' ,'ifsc_code' , 'username' , 'pan_number' , 'nationality']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_photo = UserPhoto.objects.filter(user=instance).values('image').first()
        print(user_photo,"=-=-==-=-")
        if user_photo:
           representation['profile_picture'] = user_photo['image']
        else:
            representation['profile_picture'] = None 

        return representation

   