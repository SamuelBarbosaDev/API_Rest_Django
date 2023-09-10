from django.utils import timezone
from rest_framework import serializers
from agenda.models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = [
            'data_horario',
            'nome_cliente',
            'email_cliente',
            'telefone_cliente',
        ]

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                detail='O agendamento não pode ser feito no passado.',
                code=400
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
