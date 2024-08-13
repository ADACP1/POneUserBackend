from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from companies.api.serializers import CompanyCreateSerializer,CompanyListSerializer,CompanyUpdateSerializer
from companies.models import Company
from drf_yasg.utils import swagger_auto_schema

class CompanyListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CompanyListSerializer(many=True)},operation_summary="GET all Companies",operation_description="List all Companies (IsAuthenticated)",)
    def get(self, request):        
        print(request.user) 
        if request.user.tenant == 'sincro@adachr.com':
            print('daniela')
            print(request.user)
            gettenant = request.query_params.get('tenant') 
            company = Company.objects.filter(deleted=False, tenant=gettenant)
            serializer = CompanyListSerializer(company, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(request_body=CompanyCreateSerializer,responses={201: CompanyCreateSerializer(),400: 'Bad request'},operation_summary="CREATE a Company",operation_description="Create a Company (IsAuthenticated)",)        
    def post(self, request):
        if request.user.tenant == 'sincro@adachr.com':
            gettenant = request.query_params.get('tenant')
            serializer = CompanyCreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(tenant=gettenant)
                return Response(serializer.data, status=status.HTTP_201_CREATED)        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)    
    
class CompanyView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CompanyListSerializer(),404: 'Company does not exist',500: 'General Error'},operation_summary="GET a Company by id ",operation_description="List one Company by id (IsAuthenticated)",)
    def get(self, request, pk):
        if request.user.tenant == 'sincro@adachr.com':
            gettenant = request.query_params.get('tenant')
            try:            
                company = Company.objects.get(id=pk, deleted=False, tenant=gettenant)
            except Company.DoesNotExist:
                return Response({"message": "Company does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except Company.MultipleObjectsReturned:
                return Response({"message": "Multiple Companies with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = CompanyListSerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)    
        else:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)        

    @swagger_auto_schema(request_body=CompanyUpdateSerializer,responses={200: CompanyUpdateSerializer(),404: 'Company does not exist' ,400: 'Bad Request'},operation_summary="UPDATE a Company by id",operation_description="Update one Company by id (IsAuthenticated)",)    
    def put(self, request, pk):
        if request.user.tenant == 'sincro@adachr.com':        
            gettenant = request.query_params.get('tenant')
            try:
                company = Company.objects.get(id=pk, deleted=False, tenant=gettenant)
            except Company.DoesNotExist:
                return Response({"message": "Company does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CompanyUpdateSerializer(company, request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)      
     
    
    @swagger_auto_schema(responses={200: 'The Company has been deleted', 404:'Company does not exist'},operation_summary="DELETE a Company by id ",operation_description="Delete one Company by id (IsAuthenticated)",)    
    def delete(self, request, pk):
        if request.user.tenant == 'sincro@adachr.com':                    
            gettenant = request.query_params.get('tenant')
            try:
                company = Company.objects.get(id=pk, deleted=False, tenant=gettenant)
            except Company.DoesNotExist:
                return Response({"message": "Company does not exist"}, status=status.HTTP_404_NOT_FOUND)

            company.deleted = True
            company.save()

            return Response({"message": "The Company has been deleted"},status=status.HTTP_200_OK)    
        else:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)          