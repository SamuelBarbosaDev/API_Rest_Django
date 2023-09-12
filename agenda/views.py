from rest_framework import generics
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer


# /api/agendamento_list/?username=admin
class AgendamentoList(generics.ListCreateAPIView):
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Agendamento.objects.filter(prestador__username=username)
        return queryset


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
