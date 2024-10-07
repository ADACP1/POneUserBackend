
from rest_framework import serializers
from clocks.models import Clock  


class ClockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = '__all__'  # Incluye todos los campos del modelo

class ClockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = ['longitude', 'latitude']  # Solo incluye longitud y latitud