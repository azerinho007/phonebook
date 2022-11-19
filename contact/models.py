from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PhoneNumber(models.Model):
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number


class Contact(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phones = models.ManyToManyField(PhoneNumber)
    email = models.CharField(max_length=150, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
