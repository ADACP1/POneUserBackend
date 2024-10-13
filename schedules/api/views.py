from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employees.models import Employee
from schedules.models import ScheduleNotification, ScheduleDetail, Schedule
from schedules.api.serializers import ScheduleNotificationSerializer,ScheduleDetailSerializer,ScheduleSerializer,ScheduleCreateUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle



class ScheduleNotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ScheduleNotificationSerializer(many=True)},operation_summary="GET all Schedules Notification",operation_description="List all Schedules Notification (IsAuthenticated)",)
    def get(self, request):
        schedulenotification = ScheduleNotification.objects.filter()
        serializer = ScheduleNotificationSerializer(schedulenotification, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ScheduleNotificationView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ScheduleNotificationSerializer(),404: 'Schedule Notification does not exist',500: 'General Error'},operation_summary="GET a Schedule Notification by id ",operation_description="List one Schedule Notification by id (IsAuthenticated)",)
    def get(self, request, pk):
        try:            
            schedulenotification = ScheduleNotification.objects.get(id=pk)
        except ScheduleNotification.DoesNotExist:
            return Response({"message": "Schedule Notification does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ScheduleNotification.MultipleObjectsReturned:
            return Response({"message": "Multiple Schedule Notification with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ScheduleNotificationSerializer(schedulenotification)
        return Response(serializer.data, status=status.HTTP_200_OK)        







class ScheduleDetailListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ScheduleDetailSerializer(many=True)},operation_summary="GET all Schedule Details",operation_description="List all Schedule Details (IsAuthenticated)",)
    def get(self, request):
        scheduledetail = ScheduleDetail.objects.filter(deleted=False, tenant=request.user.tenant)
        serializer = ScheduleDetailSerializer(scheduledetail, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(request_body=ScheduleDetailSerializer,responses={201: ScheduleDetailSerializer(),400: 'Bad request'},operation_summary="CREATE a Schedule Detail",operation_description="Create a Schedule Detail (IsAuthenticated)",)        
    def post(self, request):
        serializer = ScheduleDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(tenant=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ScheduleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ScheduleDetailSerializer(),404: 'Schedule Detail does not exist',500: 'General Error'},operation_summary="GET a Schedule Detail by id ",operation_description="List one Schedule Detail by id (IsAuthenticated)",)
    def get(self, request, pk):
        try:            
            scheduledetail = ScheduleDetail.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except ScheduleDetail.DoesNotExist:
            return Response({"message": "Schedule Detail does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ScheduleDetail.MultipleObjectsReturned:
            return Response({"message": "Multiple Schedule Details with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ScheduleDetailSerializer(scheduledetail)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    

    @swagger_auto_schema(request_body=ScheduleDetailSerializer,responses={200: ScheduleDetailSerializer(),404: 'Schedule Detail does not exist' ,400: 'Bad Request'},operation_summary="UPDATE a Schedule Detail by id",operation_description="Update one Schedule Detail by id (IsAuthenticated)",)    
    def put(self, request, pk):
        try:
            scheduledetail = ScheduleDetail.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except ScheduleDetail.DoesNotExist:
            return Response({"message": "Schedule Detail does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduleDetailSerializer(scheduledetail, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
    
    @swagger_auto_schema(responses={200: 'The Schedule Detail has been deleted', 404:'Schedule Detail does not exist'},operation_summary="DELETE a Schedule Detail by id ",operation_description="Delete one Schedule Detail by id (IsAuthenticated)",)    
    def delete(self, request, pk):
        try:
            scheduledetail = ScheduleDetail.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except scheduledetail.DoesNotExist:
            return Response({"message": "Schedule Detail does not exist"}, status=status.HTTP_404_NOT_FOUND)

        scheduledetail.deleted = True
        scheduledetail.save()

        return Response({"message": "The Schedule Detail has been deleted"},status=status.HTTP_200_OK)        
    
    

class ScheduleListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ScheduleSerializer(many=True)},operation_summary="GET all Schedules",operation_description="List all Schedules (IsAuthenticated)",)
    def get(self, request):
        schedule = Schedule.objects.filter(deleted=False, tenant=request.user.tenant)
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ScheduleCreateView(APIView):
    @swagger_auto_schema(request_body=ScheduleCreateUpdateSerializer,responses={201: ScheduleCreateUpdateSerializer(),400: 'Bad request'},operation_summary="CREATE a Schedule",operation_description="Create a Schedule (IsAuthenticated)",)        
    def post(self, request, *args, **kwargs):
        serializer = ScheduleCreateUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Obtener el tenant del usuario autenticado
            tenant = request.user.tenant  # Ajusta esto si `tenant` es diferente en tu modelo
            # Crear el Schedule con el tenant
            serializer.save(tenant=tenant)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
"""    
class ScheduleCreateView(APIView):
    @swagger_auto_schema(request_body=ScheduleCreateUpdateSerializer,responses={201: ScheduleCreateUpdateSerializer(),400: 'Bad request'},operation_summary="CREATE a Schedule",operation_description="Create a Schedule (IsAuthenticated)",)        
    def post(self, request):
        serializer = ScheduleCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Verificar que todos los ScheduleDetails pertenezcan al mismo tenant
            schedule_details_ids = [detail.id for detail in serializer.validated_data['scheduledetails']]
            schedule_details = ScheduleDetail.objects.filter(id__in=schedule_details_ids, tenant=request.user, deleted=False)

            if schedule_details.count() != len(schedule_details_ids):
                return Response({"message": "All ScheduleDetails must belong to the same tenant as the Schedule."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(tenant=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
"""    
class ScheduleUpdateView(APIView):
    @swagger_auto_schema(request_body=ScheduleCreateUpdateSerializer, responses={200: ScheduleCreateUpdateSerializer(), 404: 'Schedule does not exist', 400: 'Bad Request'},operation_summary="UPDATE a Schedule by id", operation_description="Update a Schedule by id (IsAuthenticated)",)
    def put(self, request, pk):
        try:
            schedule = Schedule.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except Schedule.DoesNotExist:
            return Response({"message": "Schedule does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScheduleCreateUpdateSerializer(schedule, data=request.data)
        if serializer.is_valid():
            
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ScheduleView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ScheduleSerializer(),404: 'Schedule does not exist',500: 'General Error'},operation_summary="GET a Schedule by id ",operation_description="List one Schedule by id (IsAuthenticated)",)
    def get(self, request, pk):
        try:            
            schedule = Schedule.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except Schedule.DoesNotExist:
            return Response({"message": "Schedule does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Schedule.MultipleObjectsReturned:
            return Response({"message": "Multiple Schedules with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)    

    
    
    @swagger_auto_schema(responses={200: 'The Schedule has been deleted', 404:'Schedule does not exist'},operation_summary="DELETE a Schedule by id ",operation_description="Delete one Schedule by id (IsAuthenticated)",)    
    def delete(self, request, pk):
        try:
            schedule = Schedule.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except schedule.DoesNotExist:
            return Response({"message": "Schedule does not exist"}, status=status.HTTP_404_NOT_FOUND)

        schedule.deleted = True
        schedule.save()

        return Response({"message": "The Schedule has been deleted"},status=status.HTTP_200_OK)        
    
class ScheduleMeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ScheduleSerializer(),404: 'Schedule does not exist',500: 'General Error'},operation_summary="GET My Schedule ",operation_description="List My Schedule (IsAuthenticated)",)
    def get(self, request):
        try:            
            employee = Employee.objects.get(email=request.user)
            schedule = Schedule.objects.get(name=employee.schedule,  tenant=request.user.tenant)
        except Schedule.DoesNotExist:
            return Response({"message": "Schedule does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Schedule.MultipleObjectsReturned:
            return Response({"message": "Multiple Schedules with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)        