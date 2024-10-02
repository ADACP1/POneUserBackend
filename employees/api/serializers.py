from rest_framework import serializers
from employees.models import Employee,Department,Position,EmployeeVerificationCode
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
#from companies.models import Company

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'company', 'created_at', 'updated_at')

class DepartmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name',)

class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name','company')          




class PositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name', 'company','created_at', 'updated_at')


class PositionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('name',)

class PositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name','company')        



class ManagerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 
            'company', 'position', 'department',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country','companies','ubication'
        )

class ManagersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 'company','ubication',
            'position', 'department', 'is_manager','date_of_birth', 'hire_date', 
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country','companies','ubication','supervisor','tenant'
        )





class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 
            'company', 'ubication','position', 'department',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country','schedule'
        )

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 'company','ubication',
            'position', 'department', 'is_manager','date_of_birth', 'hire_date',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country','supervisor','tenant','preferred_language','schedule','email_verified'
        )

class EmployeeLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'name', 'last_name', 'email', 'phone_number','address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country',
        )        

class EmployeeListLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name')    

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'name', 'last_name', 'email', 'phone_number', 
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country','supervisor','company','ubication',
            'position', 'department', 'is_active','schedule'
        )

class EmployeeChangePreferedLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee      
        fields = (
            'preferred_language',
        )        

class EmployeeEmail_VerifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee      
        fields = (
            'email_verified',
        )

class EmployeeSendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class EmployeeUpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    confirm_password = serializers.CharField(write_only=True)    
    current_password = serializers.CharField(write_only=True)
    verification_code = serializers.CharField(max_length=6, write_only=True)

    class Meta:
        model = Employee
        fields = ('current_password', 'password', 'confirm_password', 'verification_code')

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        current_password = data.get('current_password')
        verification_code = data.get('verification_code')     



        # Verificar que las contraseñas coincidan
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        # Validar el código de verificación
        try:
            verification = EmployeeVerificationCode.objects.get(employee=self.instance, code=verification_code)
            print(verification)
            
            # Verificar si el código ha expirado
            if verification.is_expired():
                verification.delete()  # Eliminar el código si ha expirado
                raise serializers.ValidationError("Verification code has expired.")

        except EmployeeVerificationCode.DoesNotExist:
            raise serializers.ValidationError("Verification code is incorrect or expired.")


        # Verificar que la contraseña actual sea correcta
        if not check_password(current_password, self.instance.password):
            raise serializers.ValidationError("Current password is incorrect.")
        

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char in '@!$&#%?¿*+-' for char in password):
            raise serializers.ValidationError("Password must contain at least one special character (@!$&#%?¿*+-).") 
        
        verification.delete()
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
        

     
class EmployeeUpdateForgetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    verification_code = serializers.CharField(max_length=6)
    confirm_password = serializers.CharField(write_only=True)    

    class Meta:
        model = Employee
        fields = ('password','confirm_password','verification_code')

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        verification_code = data.get('verification_code')       
        
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")     
       
       
        # Validar el código de verificación
        try:
            verification = EmployeeVerificationCode.objects.get(code=verification_code)
            
            # Verificar si el código ha expirado
            if verification.is_expired():
                verification.delete()  # Eliminar el código si ha expirado
                raise serializers.ValidationError("Verification code has expired.")

        except EmployeeVerificationCode.DoesNotExist:
            raise serializers.ValidationError("Verification code is incorrect or expired.")

        # Eliminar el código de verificación después de su uso
   
        

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char in '@!$&#%?¿*+-' for char in password):
            raise serializers.ValidationError("Password must contain at least one special character (@!$&#%?¿*+-).") 

        #verification.delete()
        return data
    

    def save(self):
        validated_data = self.validated_data
        password = validated_data.pop('password')
        verification_code = validated_data.pop('verification_code')

        try:
            verification = EmployeeVerificationCode.objects.get(code=verification_code)
            employee = verification.employee
            
            # Actualizar la contraseña del Tenant
            employee.password = make_password(password)
            employee.save()
            verification.delete()
            
        except EmployeeVerificationCode.DoesNotExist:
            raise serializers.ValidationError("Verification code is incorrect or expired.")

            

    

class EmployeeTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, tenant):
        # Obtén el token estándar
        token = super().get_token(tenant)

        # Añade información adicional al token
        token['user_id'] = tenant.id 
        token['user'] = tenant.email 
        token['tenant'] = tenant.tenant 
        token['role'] = 'manager' if tenant.is_manager else 'user'

        return token