# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    last_profile_update = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.id:  
            self.date_joined = timezone.now()
        self.last_active = timezone.now()  
        super().save(*args, **kwargs)

