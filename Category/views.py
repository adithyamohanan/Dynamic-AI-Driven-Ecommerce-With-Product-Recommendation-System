from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from .models import ReviewRating
from django.db.models import Avg
import csv 
import os
from django.conf import settings
from django.contrib.auth.models import User
from cart.models import CartItem
from .models import Category
import datetime  # Import datetime module


# other imports...

def category_products(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'shop-product-list.html', {'products': products, 'category': category})



        





def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    
    p_image = product.p_images.all()
    
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Round the average_rating to one decimal place
    average_rating = round(average_rating, 1)
    
    
    
    
    
    
    
    context = {
        
        "product": product,
        "p_image": p_image,
        "reviews" : reviews, 
        "average_rating": average_rating,
    }
    return render(request, 'shop-item.html', context)

def product_lines_view(request):
    context = {
        'product_list': Product.objects.all(),
    }
    return render(request, 'product_lines/product_list.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
    
                return redirect(url)
            
            
            
def averageReview(self):
    reviews = ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
    avg = 0
    if reviews['average'] is not None:
        avg = float(reviews['average'])
        
    return avg

        
            
def generate_product_csv():
    products_with_details = Product.objects.all()
    data = []
    for product in products_with_details:
        additional_images = ', '.join([str(image.images) for image in product.additional_images.all()])
        custom_fields = ', '.join([f"{field.heading}: {field.key_values}" for field in product.productcustomfield_set.all()])
        data.append({
            'Product Name': product.name,
            'Category': product.get_category_display(),
            'Description': product.description,
            'Price': product.price,
            'Stock': product.stock,
            'Image': product.image.url if product.image else '',
            'Additional Images': additional_images,
            'Custom Fields': custom_fields,
            'Created At': product.created_at,
            'Updated At': product.updated_at,
        })

    file_path = os.path.join(settings.MEDIA_ROOT, 'products_with_details.csv')
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product Name', 'Category', 'Description', 'Price', 'Stock', 'Image', 'Additional Images', 'Custom Fields', 'Created At', 'Updated At']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return file_path
                
                




def generate_recommendation_csv():
    products_with_details = Product.objects.all()
    data = []
    
    for product in products_with_details:
        
        reviews = ReviewRating.objects.filter(product=product, status=True)
        
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
       
        if average_rating > 3:
        
            for review in reviews:
                # Retrieve the user associated with the review
                user_id = review.user.id
                data.append({
                    'Review ID': review.id,
                    'Product ID': product.id,
                    'User ID': user_id,
                    'Review Text': review.review,
                    'Sentiment': '',  # Placeholder for sentiment analysis
                    'Timestamp': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                })

    file_path = os.path.join(settings.MEDIA_ROOT, 'sentiment_analysis.csv')
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Review ID', 'Product ID', 'User ID', 'Review Text', 'Sentiment', 'Timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return file_path



def generate_recommendation_csv_full():
    products_with_details = Product.objects.all()
    data = []
    
    for product in products_with_details:
        
        reviews = ReviewRating.objects.filter(product=product, status=True)
        
        
        for review in reviews:
                # Retrieve the user associated with the review
            user_id = review.user.id
            data.append({
                'Review ID': review.id,
                'Product ID': product.id,
                'User ID': user_id,
                'Review Text': review.review,
                'Sentiment': '',  # Placeholder for sentiment analysis
                'Timestamp': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

    file_path = os.path.join(settings.MEDIA_ROOT, 'sentiment_analysis_full.csv')
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Review ID', 'Product ID', 'User ID', 'Review Text', 'Sentiment', 'Timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return file_path
    








