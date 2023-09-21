import csv
from io import StringIO
from core.celery import app
from django.conf import settings
from django.core.mail import EmailMessage
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
    return output.getvalue()


@app.task
def envia_email(to: str | None):
    email = EmailMessage(
        subject='Agendamento - Agendando horário',
        body='Relatório com agendamentos',
        from_email=settings.EMAIL_FROM,
        to=[to],
    )
    email.attach('Relatório.csv', gera_relatorio(), 'text/csv')
    email.send()
