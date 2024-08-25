from django.contrib import admin
from .models import ShippingAddress,Order,Payment,Order_Successful


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
    
    def product_name(self, obj):
        return obj.product.name if obj.product else ''
    
    product_name.short_description = 'Product Name'

admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Order_Successful)







    
    
    

