import csv
from rest_framework import status
from rest_framework import generics
from datetime import datetime, date
from agenda.models import Agendamento
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from agenda.utils import get_horario_disponiveis
from django.http.response import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
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


@api_view(http_method_names=['GET'])
def get_horarios(request):
    data = request.query_params.get('data')
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
    horarios_disponiveis = sorted(list(get_horario_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)


@api_view(http_method_names=['GET'])
def healthcheck(request):
    return Response(data={"status": "OK"}, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@permission_classes([permissions.IsAdminUser])
def prestador_list(request):
    formato = request.query_params.get('formato')
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)

    if formato == 'csv':
        data_hoje = date.today()
        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename="Relatório{data_hoje}.csv"'
            }
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                'datetime',
                'name',
                'email',
                'phone_number',
                'prestador'
            ]
        )
        for prestador in serializer.data:
            agendamentos = prestador['agendamentos']

            for agendamento in agendamentos:
                writer.writerow(
                    [
                        agendamento['data_horario'],
                        agendamento['nome_cliente'],
                        agendamento['email_cliente'],
                        agendamento['telefone_cliente'],
                        agendamento['prestador'],
                    ]
                )
        return response

    else:
        return Response(serializer.data, status=status.HTTP_200_OK)
