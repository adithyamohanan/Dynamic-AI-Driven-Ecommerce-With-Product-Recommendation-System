from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('checkout/', views.checkout, name='check_out'),  # Updated URL pattern
    path('success/', views.success, name='success'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path("payment/", views.order_payment, name="payment"),
    path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
