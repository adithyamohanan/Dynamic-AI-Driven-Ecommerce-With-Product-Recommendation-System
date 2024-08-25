from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from cart.models import CartItem
from Category.models import ReviewRating  # Corrected import statement
from .views import generate_product_csv, generate_recommendation_csv, generate_recommendation_csv_full

# Signal handlers for product CSV file
@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def update_csv_on_product_change(sender, instance, **kwargs):
    if kwargs.get('created') or kwargs.get('updated') or kwargs.get('delete'):
        generate_product_csv()

# Signal handlers for recommendation CSV file
@receiver(post_save, sender=ReviewRating)
def update_recommendation_csv_on_product_change(sender, instance, created, **kwargs):
    if created:  # Only update recommendation CSV on product creation
        generate_recommendation_csv()


@receiver(post_save, sender=ReviewRating)
def update_recommendation_csv_full_on_product_change(sender, instance, created, **kwargs):
    if created:  # Only update recommendation CSV on product creation
        generate_recommendation_csv_full()