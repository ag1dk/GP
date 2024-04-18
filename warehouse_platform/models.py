from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta

# Custom User Model
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'customer'),
        (2, 'warehouse_owner'),
        (3, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

# Ensure we're using the custom user model
User = get_user_model()

class Item(models.Model):
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    owner = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    warehouse_type = models.CharField(max_length=50, default='Industrial', choices=(
        ('industrial', 'Industrial'),
        ('personal', 'Personal'),
        ('food_products', 'Food Products'),
        ('online_sellers', 'Online Sellers Storage'),
        ('archiving', 'Archiving Storage')
    ))
    area = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    camera_monitoring = models.BooleanField(default=False)
    contract_type = models.CharField(max_length=20, default='monthly', choices=(
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ))
    # Rental fields
    is_rented = models.BooleanField(default=False)
    rented_by = models.ForeignKey(User, related_name='rentals', on_delete=models.SET_NULL, null=True, blank=True)
    rental_end_date = models.DateTimeField(null=True, blank=True)

    def check_rental_status(self):
        """ Checks if the rental period has ended and updates the item status accordingly. """
        if self.is_rented and self.rental_end_date <= timezone.now():
            self.is_rented = False
            self.rented_by = None
            self.save()

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/')
