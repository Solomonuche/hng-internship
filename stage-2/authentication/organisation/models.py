from django.db import models
from users.models import User
from uuid import uuid4

# Create your models here.
class Organisation(models.Model):
    """
    Organisation model
    """

    orgId = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True, default='')
    users = models.ManyToManyField(User, related_name='organisations')
