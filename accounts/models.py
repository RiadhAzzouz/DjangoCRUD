from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)



class UserManager(BaseUserManager):
    def create_user(self, address, phone, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not address:
            raise ValueError("Users must have an address")
        if not phone:
            raise ValueError("Users must have a phone number")
        if not email:
            raise ValueError("Users must have an email")
        if not password:
            raise ValueError("Users must have a password")


        user_obj = self.model(
            address=address,
            phone=phone,
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, address, phone, email, password=None):
        user = self.create_user(
            address=address,
            phone=phone,
            email=email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, address, phone, email, password=None):
        user = self.create_user(
            address=address,
            phone=phone,
            email=email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user




class User(AbstractBaseUser):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['address', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



class Trainee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True)
    cv = models.FileField(null=True)

    def __str__(self):
        return self.first_name+' '+self.last_name



class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    rc = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.company_name

class Education(models.Model):
    trainee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=255)
    diploma = models.CharField(max_length=255)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.school_name
