from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from core.api.serializers import CountryListSerializer, LanguageListSerializer, CityListSerializer
from core.models import Country, Language, City
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count



class CountryListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]  
    @swagger_auto_schema(responses={200: CountryListSerializer(many=True)},operation_summary="GET all Countries",operation_description="List all Countries  (IsAuthenticated)",)
    def get(self, request):
        #countries = Country.objects.all()
        countries = Country.objects.annotate(num_cities=Count('city')).filter(num_cities__gt=0).order_by('id')
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CountryView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CountryListSerializer(),404: 'Country does not exist',500: 'General Error'},operation_summary="GET a Country by id ",operation_description="List one Country by id (IsAuthenticated)",)
    def get(self, request, pk):
        try:
            country = Country.objects.get(id=pk)
        except Country.DoesNotExist:
            return Response({"message": "Country does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Country.MultipleObjectsReturned:
            return Response({"message": "Multiple Countries with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        serializer = CountryListSerializer(country)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
class CityListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]  
    @swagger_auto_schema(responses={200: CityListSerializer(many=True)},operation_summary="GET all Cities",operation_description="List all Cities  (IsAuthenticated)",)
    def get(self, request, country=None):
        city = City.objects.filter(country=country)
        serializer = CityListSerializer(city, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CityView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CityListSerializer(),404: 'City does not exist',500: 'General Error'},operation_summary="GET a Cities by id ",operation_description="List one Cities by id (IsAuthenticated)",)    
    def get(self, request, pk):
        try:
            city = City.objects.get(id=pk)
        except City.DoesNotExist:
            return Response({"message": "City does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except City.MultipleObjectsReturned:
            return Response({"message": "Multiple Cities with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        serializer = CityListSerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    
class LanguageListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]  
    @swagger_auto_schema(responses={200: LanguageListSerializer(many=True)},operation_summary="GET all Languages",operation_description="List all Languages  (IsAuthenticated)",)
    def get(self, request):
        lang = Language.objects.all()
        serializer = LanguageListSerializer(lang, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class LanguageView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: LanguageListSerializer(),404: 'Language does not exist',500: 'General Error'},operation_summary="GET a Languages by id ",operation_description="List one Languages by id (IsAuthenticated)",)        
    def get(self, request, pk):
        try:
            lang = Language.objects.get(id=pk)
        except Language.DoesNotExist:
            return Response({"message": "Language does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Language.MultipleObjectsReturned:
            return Response({"message": "Multiple Languages with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                  
        serializer = LanguageListSerializer(lang)
        return Response(serializer.data, status=status.HTTP_200_OK)    