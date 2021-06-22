from django.db import models
from django.contrib.auth.models import User
# Create your models here.

TYPE_CHOICES = [
    (1, 'Buyer'),
    (2, 'Vendor'),
    (3, 'Runner'),
    (4, 'Hub')
]


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=150)
    is_primary = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.user.user.username


class Runner(models.Model):
    user = models.OneToOneField(
        CustomUser, primary_key=True, on_delete=models.CASCADE)
    max_orders = models.IntegerField(default=10)
    running_dia = models.IntegerField(default=5)
