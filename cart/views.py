from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CartItem
from Category.models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from checkout.models import Order, Order_Successful
from django.conf import settings









def view_cart(request):
    
    if request.user.is_authenticated:
        
        cart_items = CartItem.objects.filter(user=request.user)
        total_no_of_item = CartItem.objects.filter(user=request.user).count()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        
        return render(request, 'cart.html', {'cart_items':cart_items,'total_price':total_price,'total_no_of_item':total_no_of_item})
    
    else:
        
        cart_message = messages.warning(request, 'Please login to access the cart!')
        
        return redirect('login')
    
        
    return render(request, 'login.html')


def cart_totals(request):
    total_price = 0
    total_no_of_item = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_no_of_item = cart_items.count()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return {'total_price': total_price, 'total_no_of_item': total_no_of_item}
    
    
    

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        # Get the Razorpay order ID from the session
        razorpay_order_id = request.session.get('razorpay_order')
        if not razorpay_order_id:
            # Redirect or handle error if razorpay_order_id is not found
            pass
        
        product = Product.objects.get(id=product_id)
        
        # Add or update the cart item
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        
        # Create or update the order item
        
        
        # Create or update the successful order item
        
        
        return redirect('view_cart')
    else:
        cart_message = messages.warning(request, 'Please login to access the cart!')
        return redirect('login')


def remove_from_cart(request, order_id):
    if request.user.is_authenticated:
        order_item = get_object_or_404(CartItem, id=order_id, user=request.user)
        order_item.delete()
    return redirect('view_cart')


@require_POST
def increment_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@require_POST
def decrement_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, product=product, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        
        cart_item.delete()
    return redirect('view_cart')



def checkout(request):
    if request.user.is_authenticated:
            
        shipping_form = ShippingAddressForm(request.POST or None)

        if request.method == 'POST':
            if shipping_form.is_valid():
                address = shipping_form.save(commit=False)
                address.user = request.user
                address.save()
    
        all_order = CartItem.objects.filter(user=request.user)
        total_no_of_item = CartItem.objects.filter(user=request.user).count()
        total_price = sum(item.product.price * item.quantity for item in all_order)

        context = {
            'all_order': all_order,
            'total_price': total_price,
            'total_no_of_item': total_no_of_item,
            'shipping_form': shipping_form,
        }

        return render(request, 'checkout.html', context)
    else:
        return redirect('login')
    return render(request, 'login.html')


        
        
    

