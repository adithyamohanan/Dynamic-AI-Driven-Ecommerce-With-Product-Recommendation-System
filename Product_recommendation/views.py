import json  
from django.shortcuts import render  
import urllib.request  
import json  
from Category.models import Product


  
# Create your views here.  
  
def weather_recommendations(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?lat=' + latitude + '&lon=' + longitude + '&units=imperial&appid=164fec96a27b97680ee442e489ce3f06').read()
        else:
            city = request.POST.get('city')
            if city:
                source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=imperial&appid=164fec96a27b97680ee442e489ce3f06').read()
            else:
                context = {}
                context['need_geolocation'] = True
                return render(request, 'shop-index.html', context)
    else:
        context = {}
        context['need_geolocation'] = True
        return render(request, 'shop-index.html', context)

    list_of_data = json.loads(source)
    temp_celsius = (list_of_data['main']['temp'] - 32) * 5/9

    context = {
        'city': list_of_data['name'],
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp": round(temp_celsius, 2),  
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
    }

    return render(request, 'shop-index.html', context)



            
            
        
