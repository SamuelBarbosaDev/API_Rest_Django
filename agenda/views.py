from agenda.serializers import AgendamentoSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from agenda.models import Agendamento
from django.http import JsonResponse


@api_view(http_method_names=['GET'])
def agendamento_detail(request, id):
    # Como ver um agendamento em específico?
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializer(obj)

    return JsonResponse(serializer.data)


@api_view(http_method_names=['GET', 'POST'])
def agendamento_list(request):
    if request.method == 'GET':
        # Como listar todos os agendamentos?
        qs = Agendamento.objects.all()
        serializer = AgendamentoSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = request.data
        serializer = AgendamentoSerializer(data=data)

        if serializer.is_valid():
            # Como criar um novo agendamentos se os dados forem válidos?
            validated_data = serializer.validated_data

            Agendamento.objects.create(
                data_horario=validated_data['data_horario'],
                nome_cliente=validated_data['nome_cliente'],
                email_cliente=validated_data['email_cliente'],
                telefone_cliente=validated_data['telefone_cliente'],
            )
            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED
            )

        return JsonResponse(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
