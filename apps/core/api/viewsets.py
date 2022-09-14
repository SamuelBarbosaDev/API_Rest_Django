from rest_framework import viewsets
from core.api.serializers import ClienteSerializer
from core import models

# Serializers define the API representation.
class ClienteSerializer(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    queryset = models.Cliente.objects.all()
