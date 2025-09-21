from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=215, null=False)
    last_name = models.CharField(max_length=215, null=False)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=215, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('guest','Guest'),
            ('host','Host'),
            ('admin','Admin')
        ],
        null= False
    )
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
