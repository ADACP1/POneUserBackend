
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
        fields = ['longitude', 'latitude', 'type']

    def validate_type(self, value):
        # Asegurarse de que el tipo sea 'in', 'out', o 'abs'
        if value not in ['in', 'out', 'abs']:
            raise serializers.ValidationError("The type must be 'in', 'out', or 'abs'.")
        return value

    def validate(self, data):
        request = self.context['request']
        # Obtener el último fichaje del usuario
        last_clock = Clock.objects.filter(employee=request.user, tenant=request.user.tenant).order_by('-date').first()

        if last_clock:
            last_type = last_clock.type
            new_type = data.get('type')

            # Definir las transiciones válidas
            valid_transitions = {
                'in': ['out'],       # De 'in' solo puede pasar a 'out'
                'out': ['in', 'abs'] # De 'out' puede pasar a 'in' o 'abs'
            }

            if new_type not in valid_transitions.get(last_type, []):
                raise serializers.ValidationError({
                    "message": f"The transition from '{last_type}' to '{new_type}' is not allowed."
                })
        else:
            # Si no hay registros previos, solo puede ser 'in'
            if data.get('type') != 'in':
                raise serializers.ValidationError({"message": "The first clock must be 'in'."})

        return data
