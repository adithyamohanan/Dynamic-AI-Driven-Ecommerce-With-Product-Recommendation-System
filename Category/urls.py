from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from home_app import urls

app_name = 'category'


urlpatterns = [
    path('category_products/<str:category>/', views.category_products, name='category_products'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    

    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)