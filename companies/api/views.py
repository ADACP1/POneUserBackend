from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from companies.api.serializers import CompanyCreateSerializer,CompanyListSerializer,CompanyUpdateSerializer,UbicationListSerializer,UbicationCreateUpdateSerializer
from companies.models import Company, Ubication
from drf_yasg.utils import swagger_auto_schema

class CompanyListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CompanyListSerializer(many=True)},operation_summary="GET all Companies",operation_description="List all Companies (IsAuthenticated)",)
    def get(self, request):        
        if request.user.tenant == 'sincro@adachr.com':            
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
        



    

class UbicationListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: UbicationListSerializer(many=True)},operation_summary="GET all Ubications",operation_description="List all Ubications (IsAuthenticated)",)
    def get(self, request):                    
        ubications = Ubication.objects.filter(deleted=False, tenant=request.user.tenant)
        serializer = UbicationListSerializer(ubications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    

class UbicationByCompanyListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: UbicationListSerializer(many=True)},operation_summary="GET all Ubications of company",operation_description="List all Ubications of company (IsAuthenticated)",)
    def get(self, request, company_id):     
        try:
            company = Company.objects.get(id=company_id, deleted=False, tenant = request.user.tenant)
        except Company.DoesNotExist:
            return Response({"message": "Company not found."}, status=status.HTTP_404_NOT_FOUND)                    
        ubications = Ubication.objects.filter(deleted=False, company=company,tenant=request.user.tenant)
        serializer = UbicationListSerializer(ubications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=UbicationCreateUpdateSerializer,responses={201: UbicationCreateUpdateSerializer(),400: 'Bad request'},operation_summary="CREATE a Ubications",operation_description="Create a Ubications (IsAuthenticated)",)        
    def post(self, request, company_id):        
        try:
            company = Company.objects.get(id=company_id, deleted=False, tenant = request.user.tenant)
        except Company.DoesNotExist:
            return Response({"message": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UbicationCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(company=company,tenant=request.user.tenant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UbicationView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @swagger_auto_schema(request_body=UbicationCreateUpdateSerializer, responses={200: UbicationCreateUpdateSerializer(), 400: 'Bad request'}, operation_summary="UPDATE a Ubication",  operation_description="Update a specific Ubication by ID (IsAuthenticated)")
    def put(self, request, company_id, ubication_id):
        try:
            company = Company.objects.get(id=company_id,tenant = request.user.tenant)
        except Company.DoesNotExist:
            return Response({"message": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            ubication = Ubication.objects.get(id=ubication_id, company=company,tenant=request.user.tenant)
        except Ubication.DoesNotExist:
            return Response({"message": "Ubication not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UbicationCreateUpdateSerializer(ubication, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content', 404: 'Not Found'},operation_summary="DELETE a Ubication",operation_description="Mark a specific Ubication as deleted (IsAuthenticated)")
    def delete(self, request, company_id, ubication_id):
        try:
            company = Company.objects.get(id=company_id,tenant = request.user.tenant,deleted=False)
        except Company.DoesNotExist:
            return Response({"message": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            ubication = Ubication.objects.get(id=ubication_id, company=company, deleted = False,tenant=request.user.tenant)
        except Ubication.DoesNotExist:
            return Response({"message": "Ubication not found."}, status=status.HTTP_404_NOT_FOUND)

        # Marcamos la ubicación como eliminada (borrado lógico)
        ubication.deleted = True
        ubication.save()
        return Response({"message": "The Ubication has been deleted"},status=status.HTTP_200_OK)        