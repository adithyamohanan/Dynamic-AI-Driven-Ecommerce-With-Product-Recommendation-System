from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment, Order_Successful
from .forms import ShippingAddressForm
from cart.models import CartItem
from Category.models import Product
from django.contrib.auth.models import User
from .constants import PaymentStatus
import razorpay
import json

# Instantiate Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required
def checkout(request):
    shipping_form = ShippingAddressForm(request.POST or None)
    if request.method == 'POST':
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.user = request.user
            address.save()

    all_order = CartItem.objects.filter(user=request.user)
    total_no_of_item = all_order.count()
    total_price = sum(item.product.price * item.quantity for item in all_order)

    context = {
        'all_order': all_order,
        'total_price': total_price,
        'total_no_of_item': total_no_of_item,
        'shipping_form': shipping_form,
        'razorpay_key_id': settings.RAZOR_KEY_ID,
    }

    return render(request, 'checkout.html', context)

def success(request):
    
    if request.user.is_authenticated:
        
        cart_item, created = Order_Successful.objects.create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
    
    
        

    
    return render(request, 'order_success.html')

def payment_cancelled(request):
    return render(request, 'order_failed.html')

@login_required
def order_payment(request):
    if request.method == "POST":
        amount = request.POST.get("total_price")
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        
        razorpay_order = client.order.create(
            {"amount": float(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        
        try:
            order = Order.objects.create(razorpay_order=razorpay_order["id"])
            
        
            request.session['razorpay_order'] = razorpay_order["id"]
            
           
            
            
            
            
            
            
              
            

            return render(
                request,
                "checkout.html",
                {
                    "razorpay_key": settings.RAZOR_KEY_ID,
                    "order": order,
                    "amount": amount,
                },
            )
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(f"Error processing order: {str(e)}")
    
    return render(request, "checkout.html")



        
        
       




@csrf_exempt
def razorpay_callback(request):
    
    
    return render(request, 'order_success.html')
    
    
    
    
    

            
            
        
       
      
    


    
    