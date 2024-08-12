from rest_framework import serializers
from employees.models import Employee,Department,Position
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



class ManagersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 'company',
            'position', 'department', 'is_manager', 'created_at', 'updated_at',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country'
        )


class ManagerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'name', 'last_name', 'email', 'phone_number', 
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country',
            'position', 'department', 'is_active'
        )


class ManagerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'last_name', 'email', 'phone_number', 
            'date_of_birth', 'hire_date', 'company', 'position', 'department',
            'address_line1', 'address_line2', 'state', 'zip_code', 'city', 'country'
        )