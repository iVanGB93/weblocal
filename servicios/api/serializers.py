from rest_framework import serializers
from servicios.models import Oper, Recarga, EstadoServicio

class ServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoServicio
        fields = ('__all__')

class OperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oper
        fields = ('__all__')

class RecargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recarga
        fields = ('id', 'code')