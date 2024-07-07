from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """
    App user model
    """

    userId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    firstName = models.CharField(max_length=500)
    lastName = models.CharField(max_length=500)
    email = models.CharField(max_length=500, unique=True)
    phone = models.CharField(max_length=500, blank=True, default='')

     # Remove the username field and set email as the username field
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email