from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    # Define your category choices here
    MOBILES = 'Mobiles'
    LAPTOPS_DESKTOPS = 'Laptop and Desktop'
    STORAGE = 'Storage'
    CAMERA_ACCESSORIES = 'Camera and Accessories'
    GAMING = 'Gaming'
    SMART_WEARABLES = 'Smart Wearables'
    TELEVISION = 'Television'

    CATEGORY_CHOICES = [
        (MOBILES, 'Mobiles'),
        (LAPTOPS_DESKTOPS, 'Laptop and Desktop'),
        (STORAGE, 'Storage'),
        (CAMERA_ACCESSORIES, 'Camera and Accessories'),
        (GAMING, 'Gaming'),
        (SMART_WEARABLES, 'Smart Wearables'),
        (TELEVISION, 'Television'),
    ]

    # Use a string reference to the Product model for choices
    product_categories = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.product_categories

    class Meta:
        verbose_name_plural = 'categories'

class Product(models.Model):
    MOBILES = 'Mobiles'
    LAPTOPS_DESKTOPS = 'Laptop and Desktop'
    STORAGE = 'Storage'
    CAMERA_ACCESSORIES = 'Camera and Accessories'
    GAMING = 'Gaming'
    SMART_WEARABLES = 'Smart Wearables'
    TELEVISION = 'Television'
    HEATERS = 'Heaters'
    STEAMER = 'Steamer'
    HUMIDIFIERS = 'Humidifiers'
    KETTLES = 'Kettles'
    AIR_CONDITIONERS = 'Air Conditioners'
    AIR_COOLERS = 'Air Coolers'
    MINI_FRIDGE = 'MINI FRIDGE'
    HAND_HELD_FANS = 'Hand Held Fans'
    DE_HUMIDIFIERS = 'De Humidifiers'
    FANS = 'Fans'
    AIR_PURIFIERS = 'Air Purifiers'
    PORTABLE_FANS = 'Portable fans'

    CATEGORY_CHOICES = [
        (MOBILES, 'Mobiles'),
        (LAPTOPS_DESKTOPS, 'Laptop and Desktop'),
        (STORAGE, 'Storage'),
        (CAMERA_ACCESSORIES, 'Camera and Accessories'),
        (GAMING, 'Gaming'),
        (SMART_WEARABLES, 'Smart Wearables'),
        (TELEVISION, 'Television'),
        (HEATERS, 'Heaters'),
        (STEAMER, 'Steamer'),
        (HUMIDIFIERS, 'Humidifiers'),
        (KETTLES, 'Kettles'),
        (AIR_CONDITIONERS, 'Air Conditioners'),
        (AIR_COOLERS, 'Air Coolers'),
        (MINI_FRIDGE, 'MINI FRIDGE'),
        (HAND_HELD_FANS, 'Hand Held Fans'),
        (DE_HUMIDIFIERS, 'De Humidifiers'),
        (FANS, 'Fans'),
        (AIR_PURIFIERS, 'Air Purifiers'),
        (PORTABLE_FANS, 'Portable fans'),
        
        
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(null=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    additional_images = models.ManyToManyField('ProductImage', blank=True, related_name='product_additional_images')
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
   
    
    

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return f'Image for {self.product.name}'


class ProductCustomField(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    key_values = models.JSONField()

    def __str__(self):
        return self.heading

    def add_key_value(self, key, value):
        # Add a new key-value pair to the existing dictionary
        self.key_values[key] = value
        self.save()

    def get_key_values(self):
        # Return the dictionary of key-value pairs
        return self.key_values
    
    
class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

def _str_(self):
	return self.subject


User.add_to_class('num_reviews', lambda self: ReviewRating.objects.filter(user=self).count())


