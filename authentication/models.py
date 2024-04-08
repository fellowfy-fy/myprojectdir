from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField("Phone number", unique=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)