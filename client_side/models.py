from django.db import models
from django.contrib.auth import get_user_model
from airhouse.models import CustomUser

class CustomerProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='customer_profile')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    # Credit card information
    credit_card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)
    

    def __str__(self):
        return f"{self.user.email}'s Customer Profile"
