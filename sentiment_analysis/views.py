from django.shortcuts import render
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import os
from django.conf import settings
from django.http import HttpResponse
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from Category.models import Product

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    
    # Convert to lowercase
    tokens = [word.lower() for word in tokens]
    
    # Remove punctuation
    tokens = [word for word in tokens if word not in string.punctuation]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

def get_sentiment_scores(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores

def recommend_products(cluster_id, df):
    cluster_df = df[df['Cluster'] == cluster_id]
    product_counts = cluster_df['Product ID'].value_counts()
    top_product_id = product_counts.idxmax()
    top_product_df = cluster_df[cluster_df['Product ID'] == top_product_id]
    unique_user_ids = top_product_df['User ID'].unique()
    recommended_products = df[df['User ID'].isin(unique_user_ids)]['Product ID'].unique()
    return recommended_products

def cluster_and_recommend(request):
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'sentiment_analysis.csv')
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
    else:
        return HttpResponse("CSV file not found", status=404)
    
    df['Review Text'] = df['Review Text'].apply(preprocess_text)
    df['Sentiment Scores'] = df['Review Text'].apply(get_sentiment_scores)
    df['Sentiment Compound Score'] = df['Sentiment Scores'].apply(lambda x: x['compound'])
    
    X = df[['Sentiment Compound Score']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X_scaled)
    
    df['Cluster'] = kmeans.labels_
    
    silhouette_avg = silhouette_score(X_scaled, kmeans.labels_)
    print("Silhouette Score:", silhouette_avg)
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='Sentiment Compound Score', y='Review ID', hue='Cluster', palette='viridis')
    plt.title('K-means Clustering of Reviews')
    plt.xlabel('Sentiment Compound Score')
    plt.ylabel('Review ID')
    plt.legend(title='Cluster')
    plt.close()
    
    # Determine the cluster ID with the most recommended products
    cluster_with_most_products = df['Cluster'].value_counts().idxmax()
    
    # Get recommended products for the cluster with the most products
    recommended_products = recommend_products(cluster_with_most_products, df)
    
    recommended_product_details = ("{}".format(recommended_products))
    
    
    # Fetch product details for recommended products
    recommended_product_details = Product.objects.filter(id__in=recommended_products)
    
    
    # Construct a message with recommended product details
    message = "Recommended Products for Cluster {}: {}".format(cluster_with_most_products, recommended_product_details)
    
    context = {
        'message': message,
        'recommended_product_details' : recommended_product_details, 
        
    }
    
    return render(request, 'shop-index.html', context)

