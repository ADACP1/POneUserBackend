
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




class ClockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = '__all__'  # Incluye todos los campos del modelo

class ClockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = ['longitude', 'latitude','type']  # Solo incluye longitud y latitud

    class Meta:
        model = Clock
        fields = ['longitude', 'latitude', 'type']  # Incluye 'type' para que se valide correctamente

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