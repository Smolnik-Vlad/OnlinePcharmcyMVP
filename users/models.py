from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from cart.models import Cart


class CommonUser(AbstractUser):
    username = models.CharField(_("username"), max_length=30, null=True, blank=True, default=None, unique=False)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')


class Customer(models.Model):
    user = models.OneToOneField(CommonUser, related_name="customer", on_delete=models.CASCADE, null=True)

    telephone_number = models.CharField(max_length=20)
    cart = models.OneToOneField(Cart, related_name="customer", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"
