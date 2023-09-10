from rest_framework import status
from django.http import JsonResponse
from agenda.models import Agendamento
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from agenda.serializers import AgendamentoSerializer


class AgendamentoDetail(APIView):
    def get(self, request, id):
        obj = get_object_or_404(klass=Agendamento, id=id)
        serializer = AgendamentoSerializer(instance=obj)

        return JsonResponse(data=serializer.data)

    def patch(self, request, id):
        obj = get_object_or_404(klass=Agendamento, id=id)

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

    def delete(self, request, id):
        obj = get_object_or_404(klass=Agendamento, id=id)
        obj.cancelamento_cliente = True
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgendamentoList(APIView):
    def get(self, request):
        qs = Agendamento.objects.filter(cancelamento_cliente=False)
        serializer = AgendamentoSerializer(qs, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.data
        serializer = AgendamentoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED
            )

        return JsonResponse(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
