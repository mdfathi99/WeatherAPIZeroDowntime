from rest_framework import serializers

class CityInputSerializer(serializers.Serializer):
    city = serializers.CharField(help_text="Name of the city to fetch weather for")
