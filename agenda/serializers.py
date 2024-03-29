from django.utils import timezone
from agenda.models import Agendamento
from rest_framework import serializers
from django.contrib.auth.models import User
from agenda.utils import get_horario_disponiveis

"""
Regras de negócio:

- Qualquer cliente (auteicado ou não) seja capaz de criar um agendamento.
- Apenas o prestador de serviço pode visualizar todos os agendamentos em sua
agenda.
- Apenas o prestador de serviço pode manipular os seus agendamentos.
"""


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = [
            'id',
            'data_horario',
            'nome_cliente',
            'email_cliente',
            'telefone_cliente',
            'prestador'
        ]

    prestador = serializers.CharField()

    def validate_prestador(self, value):
        try:
            prestador_obj = User.objects.get(username=value)

        except User.DoesNotExist:
            raise serializers.ValidationError('Usuário não encontrado!')

        return prestador_obj

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                detail='O agendamento não pode ser feito no passado.',
                code=400
            )

        if value not in get_horario_disponiveis(value.date()):
            raise serializers.ValidationError(
                'Esse horário não está disponível, pois, é feriado.'
            )

        return value

    def validate(self, attrs):
        telefone_cliente = attrs.get('telefone_cliente', '')
        email_cliente = attrs.get('email_cliente', '')

        if (
            email_cliente.endswith('.br') and
            telefone_cliente.startswith('+') and not
            telefone_cliente.startswith('+55')
        ):
            raise serializers.ValidationError(
                'E-mail (.br) brasileiro deve estar associado a um número do brasil (+55)'
            )

        return attrs


class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'agendamentos',
        ]

    agendamentos = AgendamentoSerializer(many=True, read_only=True)
