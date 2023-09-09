from agenda.serializers import AgendamentoSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from agenda.models import Agendamento
from django.http import JsonResponse


@api_view(http_method_names=['GET', 'PATCH', 'DELETE'])
def agendamento_detail(request, id):
    obj = get_object_or_404(klass=Agendamento, id=id)

    if request.method == 'GET':
        # Como ver um agendamento em específico?
        serializer = AgendamentoSerializer(instance=obj)
        return JsonResponse(data=serializer.data)

    if request.method == 'PATCH':
        serializer = AgendamentoSerializer(
            instance=obj,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return JsonResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'DELETE':
        # Como deletar um agendamento em específico?
        # obj.delete()
        obj.cancelamento_cliente = True
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def agendamento_list(request):
    if request.method == 'GET':
        # Como listar todos os agendamentos?
        qs = Agendamento.objects.filter(cancelamento_cliente=False)
        # qs = Agendamento.objects.all()
        serializer = AgendamentoSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = request.data
        serializer = AgendamentoSerializer(data=data)

        if serializer.is_valid():
            # Como criar um novo agendamentos se os dados forem válidos?
            serializer.save()
            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED
            )

        return JsonResponse(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
