from django.db import models
from django.contrib.auth import get_user_model
from airhouse.models import CustomUser, InventoryItem

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
    
class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(InventoryItem, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.email}"
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.inventory_item.name} in cart for {self.cart.user.email}"

