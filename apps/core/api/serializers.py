from core.models import Cliente
from rest_framework import serializers

# Serializers define the API representation.
class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        lookup_field = 'nome'
        extra_kwargs = {
            'url': {'lookup_field': 'nome'}
        }
