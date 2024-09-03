from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
#from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.parsers import MultiPartParser, FormParser
from employees.api.serializers import ManagersListSerializer,ManagerCreateSerializer,DepartmentListSerializer,DepartmentUpdateSerializer,DepartmentCreateSerializer,EmployeeUpdatePasswordSerializer,EmployeeListLiteSerializer
from employees.api.serializers import PositionListSerializer,PositionUpdateSerializer,PositionCreateSerializer, EmployeeCreateSerializer,EmployeeListSerializer,EmployeeUpdateSerializer,EmployeeEmail_VerifiedSerializer,EmployeeTokenObtainPairSerializer
from employees.models import Employee,Department,Position
from companies.models import Company
#from core.models import City,Country
from companies.api.serializers import CompanyListSerializer,CompanyListLiteSerializer
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import csv
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password



class DepartmentByCompanyListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]        
    @swagger_auto_schema(responses={200: DepartmentListSerializer()},operation_summary="GET Departments by company ",operation_description="List departments by company  (IsAuthenticated)",)
    def get(self, request, company_id):
        department = Department.objects.filter(tenant = request.user.tenant, deleted=False, company =company_id).order_by('name')
        serializer = DepartmentListSerializer(department, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: DepartmentListSerializer(many=True)},operation_summary="GET all Departments",operation_description="List all departments (IsAuthenticated)",)
    def get(self, request):
        department = Department.objects.filter(tenant = request.user.tenant, deleted=False).order_by('name')
        serializer = DepartmentListSerializer(department, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    
    @swagger_auto_schema(request_body=DepartmentCreateSerializer,responses={201: DepartmentCreateSerializer(),400: 'Bad request'},operation_summary="CREATE a Department",operation_description="Create a Department (IsAuthenticated)",)        
    def post(self, request):
        serializer = DepartmentCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            tenant = request.user.tenant
            companies = serializer.validated_data.get('companies', [])
            for company in companies:
                if company.tenant!= tenant or company.deleted == True:
                    return Response(
                        {"message": f"Company {company.id} does not belong to your tenant."},
                        status=status.HTTP_400_BAD_REQUEST
                        )            
            serializer.save(tenant=request.user.tenant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


class DepartmentView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: DepartmentListSerializer()},operation_summary="GET a Department by id ",operation_description="List one department by id  (IsAuthenticated)",)
    def get(self, request, pk):
        try:
            department = Department.objects.get(id=pk, tenant = request.user.tenant, deleted=False)
        except Department.DoesNotExist:
            return Response({"message": "Department does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Department.MultipleObjectsReturned:
            return Response({"message": "Multiple Departments with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

        serializer = DepartmentListSerializer(department)
        return Response(serializer.data, status=status.HTTP_200_OK)
     

    @swagger_auto_schema(request_body=DepartmentUpdateSerializer,responses={200: DepartmentUpdateSerializer(),404: 'Department does not exist' ,400: 'Bad Request'},operation_summary="UPDATE a Department by id",operation_description="Update one Department by id (IsAuthenticated)",)    
    def put(self, request, pk):
        try:
            department = Department.objects.get(id=pk, deleted=False, tenant=request.user)
        except Department.DoesNotExist:
            return Response({"message": "Department does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentUpdateSerializer(department, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
    
    @swagger_auto_schema(responses={200: 'The Department has been deleted', 404:'Department does not exist'},operation_summary="DELETE a Department by id ",operation_description="Delete one Department by id (IsAuthenticated)",)    
    def delete(self, request, pk):
        try:
            department = Department.objects.get(id=pk, deleted=False, tenant=request.user)
        except Department.DoesNotExist:
            return Response({"message": "Department does not exist"}, status=status.HTTP_404_NOT_FOUND)

        department.deleted = True
        department.save()

        return Response({"message": "The Department has been deleted"},status=status.HTTP_200_OK)        
    
class PositionByCompanyListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]        
    @swagger_auto_schema(responses={200: PositionListSerializer()},operation_summary="GET Positions by company ",operation_description="List Positions by company  (IsAuthenticated)",)
    def get(self, request, company_id):
        position = Position.objects.filter(tenant = request.user.tenant, deleted=False, company =company_id).order_by('name')
        serializer = PositionListSerializer(position, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PositionListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: PositionListSerializer(many=True)},operation_summary="GET all Positions",operation_description="List all positions (IsAuthenticated)",)
    def get(self, request):
        position = Position.objects.filter(tenant = request.user.tenant, deleted=False).order_by('name')
        serializer = PositionListSerializer(position, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=PositionCreateSerializer,responses={201: PositionCreateSerializer(),400: 'Bad request'},operation_summary="CREATE a Position",operation_description="Create a Position (IsAuthenticated)",)        
    def post(self, request):
        serializer = PositionCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            tenant = request.user.tenant
            companies = serializer.validated_data.get('companies', [])
            for company in companies:
                if company.tenant!= tenant or company.deleted == True:
                    return Response(
                        {"message": f"Company {company.id} does not belong to your tenant."},
                        status=status.HTTP_400_BAD_REQUEST
                        )            
            serializer.save(tenant=request.user.tenant)            
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
            
    

class PositionView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: PositionListSerializer()},operation_summary="GET a Position by id ",operation_description="List one position by id  (IsAuthenticated)",)
    def get(self, request, pk):
        try:
            position = Position.objects.get(id=pk, tenant = request.user.tenant, deleted=False)
        except Position.DoesNotExist:
            return Response({"message": "Position does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Position.MultipleObjectsReturned:
            return Response({"message": "Multiple Positions with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = PositionListSerializer(position)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    @swagger_auto_schema(request_body=PositionUpdateSerializer,responses={200: PositionUpdateSerializer(),404: 'Position does not exist' ,400: 'Bad Request'},operation_summary="UPDATE a Position by id",operation_description="Update one Position by id (IsAuthenticated)",)    
    def put(self, request, pk):
        try:
            position = Position.objects.get(id=pk, deleted=False, tenant=request.user)
        except Position.DoesNotExist:
            return Response({"message": "Position does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PositionUpdateSerializer(position, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
    
    @swagger_auto_schema(responses={200: 'The Position has been deleted', 404:'Position does not exist'},operation_summary="DELETE a Position by id ",operation_description="Delete one Position by id (IsAuthenticated)",)    
    def delete(self, request, pk):
        try:
            position = Position.objects.get(id=pk, deleted=False, tenant=request.user)
        except Position.DoesNotExist:
            return Response({"message": "Position does not exist"}, status=status.HTTP_404_NOT_FOUND)

        position.deleted = True
        position.save()

        return Response({"message": "The Position has been deleted"},status=status.HTTP_200_OK)            
    



class ManagerListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: ManagersListSerializer(many=True)},operation_summary="GET all Managers",operation_description="List all Managers (IsAuthenticated)",)
    def get(self, request):
        #companies = Company.objects.filter(tenant = request.user, deleted=False)
        if request.user.tenant == 'sincro@adachr.com':
            gettenant = request.query_params.get('tenant')        
            manager = Employee.objects.filter(tenant = gettenant, deleted=False, is_manager=True, email_verified=True).order_by('name')
            serializer = ManagersListSerializer(manager, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)             
    

    @swagger_auto_schema(request_body=ManagerCreateSerializer,responses={201: ManagerCreateSerializer(),400: 'Bad Request'},operation_summary="CREATE a Manager",operation_description="Create a manager (IsAuthenticated)",)        
    def post(self, request):
        if request.user.tenant == 'sincro@adachr.com':    
            gettenant = request.query_params.get('tenant')      
            serializer = ManagerCreateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):                
                companies = serializer.validated_data.get('companies', [])
                for company in companies:
                    if company.tenant != gettenant:
                        return Response(
                            {"message": f"This Company {company.id} in companies does not belong to your tenant."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
             
                company = serializer.validated_data.get('company')                
                if company.tenant != gettenant:
                    return Response(
                        {"message": f"This Company {company.id} does not belong to your tenant."},
                        status=status.HTTP_400_BAD_REQUEST
                    )                       
                    
                try:
                    serializer.save(is_manager=True, tenant=gettenant, origin='admin')
                except Exception as e:
                    print(e)
                    return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(serializer.data, status=status.HTTP_201_CREATED)        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)             
        else:
            return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)             
                     
"""                
            # Generar una contraseña aleatoria
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            encrypted_password = make_password(password)
            
            manager = serializer.save(is_manager=True, origin='admin', password=encrypted_password)


            # Enviar la contraseña por correo
            send_mail(
                'Your Manager Account needs to be verified',
                #f'Hello {manager.name},\n\nYour account Manager has been created. Here are your login details:\n\nUsername: {manager.email}\nPassword: {password}\n\nPlease change your password after logging in for the first time.',
                f'Hello {manager.name},\n\nYour account Manager has been created. Please click in this link to verify your email: http://localhost:8080/verify/{manager.email_verification_token}',
                'notificacionesinternas@eninter.com',
                [manager.email]
            )
 """

class EmployeeListLiteView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: EmployeeListLiteSerializer(many=True)},operation_summary="GET all Employees Lite Version",operation_description="List all Employees Lite Version (IsAuthenticated)",)
    def get(self, request):
        employee = Employee.objects.filter(tenant = request.user.tenant, deleted=False).order_by('name')
        serializer = EmployeeListLiteSerializer(employee, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EmployeeListView(APIView):    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: EmployeeListSerializer(many=True)},operation_summary="GET all Employees",operation_description="List all Employees (IsAuthenticated)",)
    def get(self, request):
        employee = Employee.objects.filter(tenant = request.user.tenant, deleted=False).order_by('name')
        serializer = EmployeeListSerializer(employee, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(request_body=EmployeeCreateSerializer,responses={201: EmployeeCreateSerializer(),400: 'Bad Request'},operation_summary="CREATE a Employee",operation_description="Create a employee (IsAuthenticated)",)        
    def post(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            tenant = request.user.tenant
            companies = serializer.validated_data.get('companies', [])
            for company in companies:
                if company.tenant != tenant:
                    return Response(
                        {"message": f"This Company {company.id} in companies does not belong to your tenant."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            company = serializer.validated_data.get('company')                
            if company.tenant != tenant:
                return Response(
                    {"message": f"This Company {company.id} does not belong to your tenant."},
                    status=status.HTTP_400_BAD_REQUEST
                )                
            serializer.save(is_manager=False, tenant=request.user.tenant, origin='user')
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  



    
class EmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: EmployeeListSerializer(),404: 'Employee does not exist',500: 'General Error'},operation_summary="GET Employee Data ",operation_description="List Employee Data logged in the system. (IsAuthenticated)",)    
    def get(self, request):
        try:
            
            employee = Employee.objects.get(email=request.user)

        except Employee.DoesNotExist:
            return Response({"message": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Employee.MultipleObjectsReturned:
            return Response({"message": "Multiple Employees with the same id found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = EmployeeListSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    

    @swagger_auto_schema(request_body=EmployeeUpdateSerializer,responses={200: EmployeeUpdateSerializer(),404: 'Employee does not exist' ,400: 'Bad Request'},operation_summary="UPDATE Employee Data",operation_description="Update Employee Data logged in the system. (IsAuthenticated)",)    
    def put(self, request, pk):
        try:
            employee = Employee.objects.get(email=request.user)
        except Employee.DoesNotExist:
            return Response({"message": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeUpdateSerializer(employee, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
    """
    @swagger_auto_schema(responses={200: 'The Employee has been deleted', 404:'Employee does not exist'},operation_summary="DELETE a Employee by id ",operation_description="Delete one Employee by id (IsAuthenticated)",)           
    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(id=pk, deleted=False, tenant=request.user.tenant)
        except Employee.DoesNotExist:
            return Response({"message": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)

        employee.deleted = True
        employee.save()

        return Response({"message": "The Employee has been deleted"},status=status.HTTP_200_OK)    
"""        
        

class EmployeeCompaniesListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CompanyListSerializer(many=True), 404: 'Employee not found'},operation_summary="GET all Companies from Employee",operation_description="List all Companies from a Employee (IsAuthenticated)",)    
    def get(self, request):
        try:
           employee = Employee.objects.get(email=request.user)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
    
        companies =  employee.companies.all()
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EmployeeCompaniesListLiteView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CompanyListLiteSerializer(many=True), 404: 'Employee not found'},operation_summary="GET all Companies from Employee Lite Version",operation_description="List all Companies from a Employee Lite Version(IsAuthenticated)",)    
    def get(self, request):
        try:
            employee = Employee.objects.get(email=request.user)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        

        companies =  employee.companies.all()
        serializer = CompanyListLiteSerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EmployeeCompanyListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CompanyListSerializer(many=True), 404: 'Employee not found'},operation_summary="GET Company from Employee",operation_description="Get Company from a Employee (IsAuthenticated)",)    
    def get(self, request):
        try:
            employee = Employee.objects.get(email=request.user)
            print(employee)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CompanyListSerializer(employee.company)
        return Response(serializer.data, status=status.HTTP_200_OK)    

class EmployeeCompanyListLiteView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: CompanyListLiteSerializer(many=True), 404: 'Employee not found'},operation_summary="GET Company from Employee Lite Version",operation_description="Get Company from a Employee Lite Version(IsAuthenticated)",)    
    def get(self, request):
        try:
            employee = Employee.objects.get(email=request.user)
            print(employee)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CompanyListLiteSerializer(employee.company)
        return Response(serializer.data, status=status.HTTP_200_OK)   
        
    

    
    
class RemoveCompanyFromEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200:'Company removed from Employee successfully'},operation_summary="REMOVE Company from a Employee",operation_description="Remove one company from one Employee by id (IsAuthenticated)",)       
    def post(self, request, pk, company_id):
        try:
            employee = Employee.objects.get(id=pk, tenant=request.user.tenant, deleted=False)
            company = Company.objects.get(id=company_id, tenant=request.user.tenant, deleted=False)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Company.DoesNotExist:
            return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        if company in employee.companies.all():
            employee.companies.remove(company)
            return Response({"message": "Company removed from employee successfully"}, status=status.HTTP_200_OK)    
        else:
            return Response({"message": "Company not found in employee"}, status=status.HTTP_404_NOT_FOUND)
    
class AddCompanyToEmployeeView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200:'Company added to Employee successfully'},operation_summary="ADD Company to a Employee",operation_description="Add one company to one Employee by id (IsAuthenticated)",)           
    def post(self, request, pk, company_id):
        try:
            employee = Employee.objects.get(id=pk, tenant=request.user.tenant, deleted=False)
            company = Company.objects.get(id=company_id, tenant=request.user.tenant, deleted=False)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Company.DoesNotExist:
            return Response({"message": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        if company in employee.companies.all():
            return Response({"message": "Company already added to employee"}, status=status.HTTP_404_NOT_FOUND)
        else:
            employee.companies.add(company)
            return Response({"message": "Company added to employee successfully"}, status=status.HTTP_200_OK)




class DownloadEmployeeTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: 'File',400: 'Bad Request',500: 'General Error'},operation_summary="DOWNLOAD Employee Template",operation_description="Download Employee Template (IsAuthenticated)",)    
    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employee_template.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'name', 'last_name', 'email', 'phone_number', 'date_of_birth', 
            'hire_date', 'company', 'position', 'department',
            'address_line1', 'address_line2', 'state', 'zip_code', 'supervisor'
            'country', 'city'
        ])
        writer.writerow([
            'required', 'required', 'required', 'optional', 'optional', 
            'optional', 'required', 'optional', 'optional',
            'required', 'optional', 'optional', 'optional', 'optional', 'optional', 
            'required', 'required'
        ])        
        return response
    
class DownloadDepartmentTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: 'File',400: 'Bad Request',500: 'General Error'},operation_summary="DOWNLOAD Department Template",operation_description="Download Department Template (IsAuthenticated)",)     
    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="department_template.csv"'
        writer = csv.writer(response)
        writer.writerow(['name','companies'])
        writer.writerow(['required', 'required (company separated by |)'])
        return response

class DownloadPositionTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: 'File',400: 'Bad Request',500: 'General Error'},operation_summary="DOWNLOAD Position Template",operation_description="Download Position Template (IsAuthenticated)",)     
    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="position_template.csv"'
        writer = csv.writer(response)
        writer.writerow(['name','companies'])
        writer.writerow(['required', 'required (company separated by |)'])
        return response    
    

class UploadEmployeeFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
   
    @swagger_auto_schema(
        operation_description="Upload a CSV or Excel file with employee data",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="CSV or Excel file with employee data"
            )
        ],
        responses={201: "Data imported successfully", 400: "Unsupported file"}
    )
    def post(self, request, format=None):
        file_obj = request.data['file']

        if file_obj.name.endswith('.csv'):
            data = pd.read_csv(file_obj)
        elif file_obj.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file_obj)
        else:
            return Response({"message": "Unsupported file"}, status=status.HTTP_400_BAD_REQUEST)

        for index, row in data.iterrows():
            employee = Employee.objects.create(
                name=row['name'],
                last_name=row['last_name'],
                email=row['email'],
                phone_number=row.get('phone_number'),
                date_of_birth=row.get('date_of_birth'),
                hire_date=row.get('hire_date'),
                position=Position.objects.get(id=row['position']),
                department=Department.objects.get(id=row['department']),                                
                address_line1=row.get('address_line1'),
                address_line2=row.get('address_line2'),
                state=row.get('state'),
                zip_code=row.get('zip_code'),
                country=row.get('country'),
                city=row.get('city'),
                tenant=request.user.tenant,
                is_manager=False,
                is_active=True,
                origin='import'

            )

            companies = row['company'].split(',')
            for company_id in companies:
                employee.company.add(Company.objects.get(id=company_id))


        return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)

class UploadDepartmentFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @swagger_auto_schema(
        operation_description="Upload a CSV or Excel file with department data",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="CSV or Excel file with department data"
            )
        ],
        responses={201: "Data imported successfully", 400: "Unsupported file"}
    )
    def post(self, request, format=None):
        file_obj = request.data['file']

        if file_obj.name.endswith('.csv'):
            data = pd.read_csv(file_obj)
        elif file_obj.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file_obj)
        else:
            return Response({"message": "Unsupported file"}, status=status.HTTP_400_BAD_REQUEST)

        tenant = request.user.tenant
        try:
            # Validar todas las compañías primero
            for index, row in data.iterrows():
                companies = str(row['companies']).split('|')  # Asumiendo que las compañías están separadas por comas en el archivo
                print(companies)
                for company_id in companies:
                    company = Company.objects.filter(id=company_id.strip(), tenant=tenant,deleted=False).first()
                    print(company)
                    if not company:
                        return Response(
                            {"message": f"The company '{company_id.strip()}' in row {index + 1} does not belong to your tenant."},
                            status=status.HTTP_400_BAD_REQUEST
                    )

        # Si todas las validaciones son correctas, crear los departamentos

            for index, row in data.iterrows():
                department = Department.objects.create(
                    name=row['name'],
                    tenant=tenant
                )

                companies = str(row['companies']).split('|')
                valid_companies = [
                    Company.objects.get(id=company_id.strip(), tenant=tenant,deleted=False)
                    for company_id in companies
                ]

                department.company.set(valid_companies)
                department.save()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)



class UploadPositionFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @swagger_auto_schema(
        operation_description="Upload a CSV or Excel file with position data",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="CSV or Excel file with position data"
            )
        ],
        responses={201: "Data imported successfully", 400: "Unsupported file"}
    )
    def post(self, request, format=None):
        file_obj = request.data['file']

        if file_obj.name.endswith('.csv'):
            data = pd.read_csv(file_obj)
        elif file_obj.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file_obj)
        else:
            return Response({"message": "Unsupported file"}, status=status.HTTP_400_BAD_REQUEST)

        tenant = request.user.tenant
        try:
            # Validar todas las compañías primero
            for index, row in data.iterrows():
                companies = str(row['companies']).split('|')  # Asumiendo que las compañías están separadas por comas en el archivo
                print(companies)
                for company_id in companies:
                    company = Company.objects.filter(id=company_id.strip(), tenant=tenant,deleted=False).first()
                    if not company:
                        return Response(
                            {"message": f"The company '{company_id.strip()}' in row {index + 1} does not belong to your tenant."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

        # Si todas las validaciones son correctas, crear los departamentos

            for index, row in data.iterrows():
                position = Position.objects.create(
                    name=row['name'],
                    tenant=tenant
                )

                companies = str(row['companies']).split('|')
                valid_companies = [
                    Company.objects.get(id=company_id.strip(), tenant=tenant,deleted=False)
                    for company_id in companies
                ]

                position.company.set(valid_companies)
                position.save()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)





class EmployeeEmailVerificationView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]  
    @swagger_auto_schema(responses={200: 'Employee Email verified successfully.',400: 'Bad Request'},operation_summary="VERIFY Employee",operation_description="Update Employee Verified field",)            
    def get(self, request, token):
        try:
            profile = Employee.objects.get(email_verification_token=token)

            if profile.email_verification_token_expires is not None and profile.email_verification_token_expires < timezone.now():
                return Response({'message': 'The token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if profile.email_verified:
                return Response({'message': 'The email has already been verified previously.'}, status=status.HTTP_400_BAD_REQUEST)            



            profile.email_verified = True
            profile.save()
            return Response({'message': 'Employee Email verified successfully.'}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)   
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmployeeTokenObtainPairSerializer    
    throttle_classes = [UserRateThrottle, AnonRateThrottle]  
    @swagger_auto_schema(responses={200: 'Ok',400: 'Email verification required'},operation_summary="LOGIN Employee with check email verified",operation_description="Login Employee with check email verified",)      
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        emailverify = Employee.objects.get(email=request.data['email']).email_verified

        if emailverify==True: 
            token = serializer.validated_data
            return Response(token, status=status.HTTP_200_OK)      
           
        else:
            return Response({"message": "Email verification required."}, status=status.HTTP_400_BAD_REQUEST)     
           
        

class EmployeeUpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(request_body=EmployeeUpdatePasswordSerializer,responses={200:  'Password changed successfully.',400: 'Bad Request'},operation_summary="UPDATE Password Employee",operation_description="Update password Employee logged in the system. (IsAuthenticated)",)    
    def patch(self, request):
        employee = Employee.objects.get(id=request.user.id)
        serializer = EmployeeUpdatePasswordSerializer(employee, request.data.tenant)
        if serializer.is_valid(raise_exception=True):
            serializer.save()            
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       


    
class EmployeeEmail_VerifiedView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    @swagger_auto_schema(responses={200: EmployeeEmail_VerifiedSerializer()},operation_summary="GET Employee Data email verified",operation_description="Show Employee Data email verified. (IsAuthenticated)",)
    def get(self, request):
        serializer = EmployeeEmail_VerifiedSerializer(request.user.tenant)
        return Response(serializer.data, status=status.HTTP_200_OK)         
    
