from agenda.serializers import AgendamentoSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from agenda.models import Agendamento
from django.http import JsonResponse

def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializer(obj)

    return JsonResponse(serializer.data)
