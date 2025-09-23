from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager , AbstractUser
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from datetime import timedelta
# Create your models here.

class UserRoles(models.TextChoices):
    SUPER_ADMIN = "super_admin", "Super Admin"
    CASHIER = "cashier", "Cashier"
    CHEF = "chef", "Chef"
    WAITER = "waiter", "Waiter"


GENDER_CHOICES = [
 ("MALE", 'Male'),
 ("FEMALE", 'Female'),
 ("OTHER", 'Other'),
 ]


class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None, role=UserRoles.WAITER , **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)

        

        user = self.model(email=email, role=role ,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
   
        extra_fields["role"] = UserRoles.SUPER_ADMIN

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser , PermissionsMixin):
  profile_picture = models.CharField(max_length=100 , blank=True , null=True)
  email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
  )
  username = models.CharField(max_length=100 , blank=True)
  first_name = models.CharField(max_length=100 , blank=True)
  last_name = models.CharField(max_length=100 , blank=True)
  date_joined = models.DateTimeField(blank=True, null=True)
  role = models.CharField(max_length=100,choices=UserRoles.choices,default=UserRoles.WAITER)
  phone_number = models.CharField(max_length=50,blank=True)
  address = models.CharField(max_length=255,blank=True)
  adhar_proof = models.CharField(max_length=150,blank=True)
  pan_number = models.CharField(max_length=150,blank=True)
  nationality = models.CharField(max_length=150,blank=True)
  gender = models.CharField(max_length=50,choices=GENDER_CHOICES,default='MALE')
  account_number = models.CharField(max_length=255,blank=True)
  ifsc_code = models.CharField(max_length=150,blank=True)
  
  is_superuser = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  objects = MyUserManager()
 

  def has_perm(self, perm, obj=None):
      return self.is_active and self.is_superuser

  def has_module_perms(self, app_label):
      return self.is_active and self.is_superuser


  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.first_name
  

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < now() - timedelta(hours=1)  

    @staticmethod
    def create_token(user):
        token = get_random_string(length=64)
        return PasswordResetToken.objects.create(user=user, token=token)


 
class UserPhoto(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True ,  related_name="photo")
    image = models.ImageField(upload_to="user_photos/") 
 
    def __str__(self):
        return f"Photo of {self.user.username}"