# HelloWorldProject/HelloWorldApp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from Category import urls

urlpatterns = [
    path('',views.home_page, name='homeapp'),
    path('login/',views.loginn, name='login'),
    path('regiser/',views.register, name='register'),
    path('logout/', views.logout_view, name="logout"),
    path('search/',views.search_page, name='search'),
    path('account/',views.account,name='account'),
    
    
    
    
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

