from datetime import datetime
from rest_framework import generics
from agenda.models import Agendamento
from rest_framework import permissions
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from agenda.utils import get_horario_disponiveis
from rest_framework.decorators import api_view
from agenda.serializers import (
    AgendamentoSerializer,
    PrestadorSerializer
)


class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        username = request.query_params.get('username', None)

        if request.user.username == username:
            return True

        else:
            return False


class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True

        else:
            return False


# /api/agendamento_list/?username=admin
class AgendamentoList(generics.ListCreateAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Agendamento.objects.filter(prestador__username=username)
        return queryset


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsPrestador]


class PrestadorList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = PrestadorSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(http_method_names=['GET'])
def get_horarios(request):
    data = request.query_params.get('data')
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
    horarios_disponiveis = sorted(list(get_horario_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)
