import requests
from datetime import date
from django.conf import settings


def is_feriado(data: date) -> bool:
    """
    - Chama a APi Com o ano da data.
    - Verificar se os feriados retornados possuem a data igual a data
    solicitada pelo nosso usuário.
    - Caso afirmativo: retorna uma lista vazia.
    """

    if settings.TESTING == 1:
        return False

    r = requests.get(
        url=f'https://brasilapi.com.br/api/feriados/v1/{data.year}'
    )

    if r.status_code != 200:
        raise ValueError('Não foi possível consultar os feriados!')

    feriados = r.json()

    for feriado in feriados:
        data_feriado_as_str = feriado['date']
        data_feriado = date.fromisoformat(data_feriado_as_str)
        if data == data_feriado:
            return True

    return False
