from rest_framework import mixins
from rest_framework import generics
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer


class AgendamentoDetail(
    mixins.RetrieveModelMixin,  # GET
    mixins.UpdateModelMixin,  # PATCH e PUT
    mixins.DestroyModelMixin,  # DELETE
    generics.GenericAPIView,  # API genérica
):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(
            request=request,
            args=args,
            kwargs=kwargs,
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(
            request=request,
            args=args,
            kwargs=kwargs,
        )

    def put(self, request, *args, **kwargs):
        return self.update(
            request=request,
            args=args,
            kwargs=kwargs,
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(
            request=request,
            args=args,
            kwargs=kwargs,
        )


class AgendamentoList(
    mixins.ListModelMixin,  # Adicionando mixin de listagem
    mixins.CreateModelMixin,  # Adicionando mixin de Criação
    generics.GenericAPIView,  # Class genérica
):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(
            request=request,
            args=args,
            kwargs=kwargs
        )

    def post(self, request, *args, **kwargs):
        return self.create(
            request=request,
            args=args,
            kwargs=kwargs
        )
