from django.shortcuts import render
import requests
import datetime
from django.templatetags.static import static
# Create your views here.

API_KEY = "AIzaSyCdL5g_nnCpzEE-YuaH0eiU7FMSahlgCgw"
SEARCH_ENGINE_ID = "f4a482b78a89045ef"

def get_city_image(city):
    query = f"{city} 1920x1080"
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&num=1"
    response = requests.get(url).json()
    items = response.get("items")

    if items:
        return items[0]["link"]   # ✅ first image link
    
    return None

def home(request):
    api_key = 'f34a90cd9737fc019de6f906ac5caff6'
    city = request.POST.get('city', 'mumbai')  # default city
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()
    success = data.get("cod") == 200

    city_image = get_city_image(city)

    context = {
        "success": success,
        "city": city.upper(),
        "datetime": datetime.datetime.now(),
        "city_image": city_image
    }

    if success:
        context.update({
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "desc": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "weather_main": data["weather"][0]["main"],
        })

    return render(request, "home.html", context)