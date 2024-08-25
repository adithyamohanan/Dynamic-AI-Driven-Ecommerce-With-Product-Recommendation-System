from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from Category import urls

urlpatterns = [
    # URL pattern for the root URL ('/')
    path('', views.weather_recommendations, name='weather_recommendations'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
