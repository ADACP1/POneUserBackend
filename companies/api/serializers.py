from rest_framework import serializers
from companies.models import Company


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyListLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')     

class CompanyUpdateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Company
        fields = [campo.name for campo in Company._meta.fields if campo.name not in ['registration_date', 'updated_at', 'created_at','tenant']]   

class CompanyCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Company        
        fields = [campo.name for campo in Company._meta.fields if campo.name not in ['registration_date', 'updated_at', 'created_at','tenant','deleted']]