from rest_framework import serializers
from employees.models import Employee,Department,Position
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
            'date_of_birth', 'hire_date', 'company', 'position', 'department',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country','tenant'
        )

class ManagersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 'company',
            'position', 'department', 'is_manager', 'created_at', 'updated_at',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country'
        )





class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 
            'date_of_birth', 'hire_date', 'company', 'position', 'department',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country'
        )

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 'company',
            'position', 'department', 'is_manager', 'created_at', 'updated_at',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country'
        )


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'name', 'last_name', 'email', 'phone_number', 
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country',
            'position', 'department', 'is_active'
        )

class EmployeeEmail_VerifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee      
        fields = (
            'email_verified',
        )

class EmployeeUpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    #verification_code = serializers.CharField(max_length=6)
    confirm_password = serializers.CharField(write_only=True)    
    current_password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ('current_password','password','confirm_password')#,'verification_code')

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        current_password = data.get('current_password')
        #verification_code = data.get('verification_code')       
        
        # Verificar que el password actual es correcto
        if not check_password(current_password, self.instance.password):
            raise serializers.ValidationError("Current password is incorrect.")        

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")     

        #if verification_code != 'codigo':
            #raise serializers.ValidationError("Verification Code do not match.")   
        

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

        return data
    

    #encriptar el password
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    

class EmployeeTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, tenant):
        # Obtén el token estándar
        token = super().get_token(tenant)

        # Añade información adicional al token
        token['tenant_id'] = tenant.id 
        token['tenant_email'] = tenant.email 
        token['role'] = 'user'          

        return token