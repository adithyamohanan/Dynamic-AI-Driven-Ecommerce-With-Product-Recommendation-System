from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Category.models import Product
from django.urls import reverse
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus


# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.user.username}'s Shipping Address"
    
    @property
    def product_name(self):
        return self.product.name if self.product else ''



class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    razorpay_order = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)

    def __str__(self):
        product_name = self.product.name if self.product else "Unknown Product"
        return f"{self.quantity} x {product_name}"
      
    

   
   

class Order_Successful(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    razorpay_order = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    
    ORDER_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        # Add more status options as needed
    )
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Pending')
    is_paid = models.BooleanField(default=False)
    
    
    PAYMENT_METHOD_CHOICES = (
        ('Pending', 'Pending'),
        ('cod', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        # Add more payment methods as needed
    )
   
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Pending')
    
    
   

    def __str__(self):
        return f'{self.user} --- {self.product}'
    
    
    
class Payment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    

    def __str__(self):
        return f"Payment for {self.product.name} by {self.user.username}"
    
    
    
    
    

    
    
    





    
    
    







