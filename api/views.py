import socket
import datetime
import requests
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import CityInputSerializer

@api_view(['GET'])
def hello_view(request):
    hostname = socket.gethostname()
    now = datetime.datetime.now().strftime("%y%m%d%H%M")

    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=23.8103&longitude=90.4125&current_weather=true")
        data = response.json()
        temperature = data['current_weather']['temperature']
    except:
        temperature = "N/A"

    result = {
        "hostname": hostname,
        "datetime": now,
        "version": os.getenv("APP_VERSION", "unknown"),
        "weather": {
            "dhaka": {
                "temperature": str(temperature),
                "temp_unit": "c"
            }
        }
    }
    return Response(result)

@api_view(['GET'])
def health_check(request):
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=23.8103&longitude=90.4125&current_weather=true")
        if response.status_code == 200:
            return Response({"status": "healthy", "third_party_api": "reachable"})
    except:
        return Response({"status": "unhealthy", "third_party_api": "unreachable"}, status=503)

    return Response({"status": "unhealthy"}, status=503)

@swagger_auto_schema(
    method='post',
    request_body=CityInputSerializer,
    responses={200: openapi.Response(description="Weather info for the given city, It will correct city name automaticly with matched chracter")},
)

#Adding other cities as well, it will correct city name if spealing is wrong.
@api_view(['POST'])
def get_city_weather(request):
    serializer = CityInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    city = serializer.validated_data["city"].strip()

    # Step 1: Geocode
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geo_response = requests.get(geocode_url)
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return Response({"error": "Wrong city name."}, status=400)

    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]

    # Step 2: Weather
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    current_weather = weather_data.get("current_weather")
    if not current_weather:
        return Response({"error": "Weather data not found."}, status=500)

    result = {
        "city": location["name"],
        "latitude": lat,
        "longitude": lon,
        "temperature": current_weather["temperature"],
        "temp_unit": "°C",
        "weather_code": current_weather["weathercode"],
        "wind_speed": current_weather["windspeed"],
    }

    return Response(result, status=200)