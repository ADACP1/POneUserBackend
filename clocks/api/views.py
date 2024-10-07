# clocks/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clocks.models import Clock
from clocks.api.serializers import ClockListSerializer, ClockCreateSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from drf_yasg.utils import swagger_auto_schema


class ClockListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ClockListSerializer(many=True)},operation_summary="GET all Clocks",operation_description="List all Clocks (IsAuthenticated)",)    
    def get(self, request):
        clocks = Clock.objects.filter(tenant = request.user.tenant,employee= request.user).order_by('date')
        serializer = ClockListSerializer(clocks, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClockCreateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]      
    @swagger_auto_schema(request_body=ClockCreateSerializer,responses={201: ClockCreateSerializer(),400: 'Bad request'},operation_summary="CREATE a Clock",operation_description="Create a Clock (IsAuthenticated)",)            
    def post(self, request):
        # Obtener el último registro de fichaje para el empleado
        last_clock = Clock.objects.filter(employee=request.user, tenant=request.user.tenant).order_by('-date').first()
        
        # Determinar el tipo de fichaje basado en el último
        if last_clock:
            last_type = last_clock.type
            new_type = 'out' if last_type == 'in' else 'in'  # Cambia el tipo
        else:
            new_type = 'in'  # Si no hay registros previos, es check in
        
        # Inicializa el serializer con los datos de entrada
        serializer = ClockCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Guarda el nuevo registro con el tipo determinado            

            clock_instance = serializer.save(tenant=request.user.tenant, employee=request.user, type=new_type)
            response_serializer = ClockListSerializer(clock_instance)            
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)  # Devuelve los datos y el código de estado 201
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 