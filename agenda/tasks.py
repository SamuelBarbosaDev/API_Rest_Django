import csv
from io import StringIO
from core.celery import app
from django.core.mail import send_mail
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
    print(output.getvalue())


@app.task
def envia_email():
    send_mail(
        subject='Subject here',
        message='here is the message.',
        from_email='from@exemple.com',
        recipient_list=['to@example.com'],
        fail_silently=False
    )
