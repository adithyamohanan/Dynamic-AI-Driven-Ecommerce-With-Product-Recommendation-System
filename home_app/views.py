from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from Category.models import Product
from django.db.models import Q


# Create your views here.
def home_page(request):
    return render(request,'shop-index.html')


def login1(request):
    return render(request, 'login_register.html')

def sample(request):
    return render(request, 'sample.html')

def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'shop-index.html')
        else:
            messages.error(request, "Invalid login")
            return redirect('login')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect("register")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.info(request, "Successfully Registered")
            login(request, user)
            return redirect('/')
            return redirect('homeapp')
    else:
        return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('/')


def search_page(request):
    
    
    context = {}
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword) | Q(category__icontains=keyword))
            context = {
                'products': products
            }
   
    return render(request, 'search.html', context)



    
    

def account(request):
    
    
    
    return render(request, 'order_dashboard.html')



    
    
    