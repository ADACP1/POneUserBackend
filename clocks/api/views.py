# clocks/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clocks.models import Clock, AbsenceType
from clocks.api.serializers import ClockListSerializer, ClockCreateSerializer, AbsenceTypeCreateSerializer, AbsenceTypeUpdateSerializer, AbsenceTypeListSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from drf_yasg.utils import swagger_auto_schema


class ClockListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ClockListSerializer(many=True)},operation_summary="GET all Clocks (the last 1000)",operation_description="List all Clocks  (the last 1000) (IsAuthenticated)",)    
    def get(self, request):
        clocks = Clock.objects.filter(tenant = request.user.tenant,employee= request.user).order_by('-date')[:1000]
        serializer = ClockListSerializer(clocks, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LastClockView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ClockListSerializer()},operation_summary="GET last Clocks",operation_description="Get the last Clock (IsAuthenticated)",)    
    def get(self, request):
        clock = Clock.objects.filter(employee=request.user, tenant=request.user.tenant).order_by('-date').first()
        if clock:
            serializer = ClockListSerializer(clock) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No clocks found."}, status=status.HTTP_404_NOT_FOUND)


class ClockCreateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]      
    @swagger_auto_schema(request_body=ClockCreateSerializer,responses={201: ClockCreateSerializer(),400: 'Bad request'},operation_summary="CREATE a Clock",operation_description="Create a Clock (IsAuthenticated)",)            
    def post(self, request):        
        # Inicializa el serializer con los datos de entrada
        #serializer = ClockCreateSerializer(data=request.data)
        serializer = ClockCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Guarda el nuevo registro
            clock_instance = serializer.save(tenant=request.user.tenant, employee=request.user)
            response_serializer = ClockListSerializer(clock_instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    

class AbsenceTypeByCompanyListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]        
    @swagger_auto_schema(responses={200: AbsenceTypeListSerializer()},operation_summary="GET AbsenceType by company ",operation_description="List AbsenceType by company  (IsAuthenticated)",)
    def get(self, request, company_id):
        absencetype = AbsenceType.objects.filter(tenant = request.user.tenant, deleted=False, companies =company_id).order_by('name')
        serializer = AbsenceTypeListSerializer(absencetype, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AbsenceTypeListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: AbsenceTypeListSerializer(many=True)},operation_summary="GET all AbsenceType",operation_description="List all AbsenceType (IsAuthenticated)",)
    def get(self, request):
        absencetype = AbsenceType.objects.filter(tenant = request.user.tenant, deleted=False).order_by('name')
        serializer = AbsenceTypeListSerializer(absencetype, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    
    @swagger_auto_schema(request_body=AbsenceTypeCreateSerializer,responses={201: AbsenceTypeCreateSerializer(),400: 'Bad request'},operation_summary="CREATE a AbsenceType",operation_description="Create a AbsenceType (IsAuthenticated)",)        
    def post(self, request):
        serializer = AbsenceTypeCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            tenant = request.user.tenant
            print(tenant)
            companies = serializer.validated_data.get('companies', [])
            for company in companies:
                print(company.tenant)
                if company.tenant!= tenant or company.deleted == True:
                    return Response(
                        {"message": f"Company {company.id} does not belong to your tenant."},
                        status=status.HTTP_400_BAD_REQUEST
                        )            
            serializer.save(tenant=request.user.tenant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


class AbsenceTypeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: AbsenceTypeListSerializer()},operation_summary="GET a AbsenceType by id ",operation_description="List one AbsenceType by id  (IsAuthenticated)",)
    def get(self, request, pk):
        try:
            absencetype = AbsenceType.objects.get(id=pk, tenant = request.user.tenant, deleted=False)
        except AbsenceType.DoesNotExist:
            return Response({"message": "AbsenceType does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except AbsenceType.MultipleObjectsReturned:
            return Response({"message": "Multiple AbsenceType with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

        serializer = AbsenceTypeListSerializer(absencetype)
        return Response(serializer.data, status=status.HTTP_200_OK)
     

    @swagger_auto_schema(request_body=AbsenceTypeUpdateSerializer,responses={200: AbsenceTypeUpdateSerializer(),404: 'AbsenceType does not exist' ,400: 'Bad Request'},operation_summary="UPDATE a AbsenceType by id",operation_description="Update one AbsenceType by id (IsAuthenticated)",)    
    def put(self, request, pk):
        try:
            absencetype = AbsenceType.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except AbsenceType.DoesNotExist:
            return Response({"message": "AbsenceType does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AbsenceTypeUpdateSerializer(absencetype, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
    
    @swagger_auto_schema(responses={200: 'The AbsenceType has been deleted', 404:'AbsenceType does not exist'},operation_summary="DELETE a AbsenceType by id ",operation_description="Delete one AbsenceType by id (IsAuthenticated)",)    
    def delete(self, request, pk):
        try:
            absencetype = AbsenceType.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except AbsenceType.DoesNotExist:
            return Response({"message": "AbsenceType does not exist"}, status=status.HTTP_404_NOT_FOUND)

        absencetype.deleted = True
        absencetype.save()

        return Response({"message": "The AbsenceType has been deleted"},status=status.HTTP_200_OK)     