import csv
from io import StringIO
from core.celery import app
from django.contrib.auth.models import User
from agenda.serializers import PrestadorSerializer
from django.core.mail import send_mail, EmailMessage


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
    return output.getvalue()


@app.task
def envia_email():
    email = EmailMessage(
        subject='Agendamento - Agendando horário',
        body='Relatório com agendamentos',
        from_email='from@exemple.com',
        to=['to@example.com'],
    )
    email.attach('Relatório.csv', gera_relatorio(), 'text/csv')
    email.send()
