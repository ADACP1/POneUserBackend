
from rest_framework import serializers
from clocks.models import Clock , AbsenceType, AbsenceEmployee
    

class AbsenceTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceType
        fields = ('id', 'name', 'companies','tenant','require_validation','require_addittional_info','created_at', 'updated_at','deleted')

class AbsenceTypeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceType
        fields = ('name','require_validation','require_addittional_info')

class AbsenceTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceType
        fields = ('id', 'name','companies','require_validation','require_addittional_info')          



class AbsenceEmployeeListSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    absence_type_name = serializers.SerializerMethodField()  # Campo para el nombre del tipo de ausencia
    created_at = serializers.SerializerMethodField()  #    

    class Meta:
        model = AbsenceEmployee
        fields = '__all__' 


    def get_employee_name(self, obj):
        return obj.employee.name +' '+ obj.employee.last_name        
    
    def get_absence_type_name(self, obj):
        # Devuelve el nombre del tipo de ausencia
        return obj.absence_type.name

    def get_created_at(self, obj):
        # Devuelve solo la fecha de created_at en formato 'YYYY-MM-DD'
        return obj.created_at.strftime('%Y-%m-%d')    

class AbsenceEmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceEmployee
        fields = ['absence_type','text']  # Solo incluye longitud y latitud

    def validate(self, data):
        # Obtén el tipo de ausencia
        absence_type = data.get('absence_type')

        # Verifica si el tipo de ausencia requiere validación y si el texto es suficiente
        if absence_type and absence_type.require_addittional_info:
            text = data.get('text', '')

            # Verifica que el campo text tenga al menos 5 caracteres
            if len(text) < 5:
                raise serializers.ValidationError({"message": "This absence type requires additional information"})

        return data        


class AbsenceEmployeeValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceEmployee
        fields = ['validate']        



class ClockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = '__all__'  # Incluye todos los campos del modelo

class ClockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = ['longitude', 'latitude','type']  # Solo incluye longitud y latitud

    def validate_type(self, value):
        # Asegurarse de que el tipo sea 'in' o 'out'
        if value not in ['in', 'out']:
            raise serializers.ValidationError("The type must be either 'in' or 'out'.")
        return value        

    def validate(self, data):
        request = self.context['request']
        # Obtener el último fichaje del usuario
        last_clock = Clock.objects.filter(employee=request.user, tenant=request.user.tenant).order_by('-date').first()

        # Verificar el tipo del último fichaje y compararlo con el nuevo tipo
        if last_clock:
            last_type = last_clock.type
            new_type = data.get('type')

            # Verificar que el nuevo tipo sea el opuesto del último tipo
            if last_type == 'in' and new_type != 'out':
                raise serializers.ValidationError({"message": "The next clock must be 'out'."})
            elif last_type == 'out' and new_type != 'in':
                raise serializers.ValidationError({"message": "The next clock must be 'in'."})
        else:
            # Si no hay registros previos, solo puede ser 'in'
            if data.get('type') != 'in':
                raise serializers.ValidationError({"message": "The first clock must be 'in'."})

        return data        