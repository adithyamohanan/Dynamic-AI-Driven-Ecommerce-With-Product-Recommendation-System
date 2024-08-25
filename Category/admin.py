from django.contrib import admin
from .models import Category, Product, ProductImage, ProductCustomField, ReviewRating

class ProductCustomFieldInline(admin.TabularInline):
    model = ProductCustomField
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductCustomFieldInline, ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)

