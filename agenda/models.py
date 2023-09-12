from django.db import models


class Agendamento(models.Model):
    prestador = models.ForeignKey(
        'auth.user',
        related_name='agendamentos',
        on_delete=models.CASCADE
    )
    data_horario = models.DateTimeField()
    nome_cliente = models.CharField(max_length=43)
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=13)
    cancelamento_cliente = models.BooleanField(default=False)
