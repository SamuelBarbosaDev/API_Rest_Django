import csv
from core.celery import app
from io import StringIO
from django.contrib.auth.models import User
from agenda.serializers import PrestadorSerializer


@app.task
def gera_relatorio():
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(instance=prestadores, many=True)
    output = StringIO()
    writer = csv.writer(output)
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
    return output
