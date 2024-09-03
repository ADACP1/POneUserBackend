from rest_framework import serializers
from core.models import Country, Language, City


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name','created_at', 'updated_at')

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name','created_at', 'updated_at','country')                

class LanguageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name','created_at', 'updated_at')        