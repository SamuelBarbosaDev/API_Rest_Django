from typing import Iterable
from agenda.models import Agendamento
from agenda.libs import brasil_api
from datetime import (
    date,
    datetime,
    timedelta,
    timezone
)


def get_horario_disponiveis(data: date) -> Iterable[datetime]:
    """
    Retorna uma lista com objetos do tipo datetime cujas datas são o mesmo dia
    passado (data) e os horários são os horário disponíveis para aquele dia,
    conforme outros agendamentos existem.
    """
    try:
        if brasil_api.is_feriado(data):
            return []
    except ValueError:
        pass

    start = datetime(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=9,
        minute=0,
        tzinfo=timezone.utc
    )
    end = datetime(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=18,
        minute=0,
        tzinfo=timezone.utc
    )
    delta = timedelta(minutes=30)
    horario_disponiveis = set()

    while start < end:
        if not Agendamento.objects.filter(data_horario=start).exists():
            horario_disponiveis.add(start)
        start = start + delta

    return horario_disponiveis
