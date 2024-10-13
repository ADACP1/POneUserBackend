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